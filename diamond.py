#!/usr/bin/env python

from datetime import date, timedelta
from time import sleep
import re
import os

from ChangeUA import MyOpener, MyReader

# Getting next week's Wed. date
d_next = ((date.today() + timedelta(-(date.weekday(date.today()) - 2))) +
          timedelta(days=7))
NEXT_WEEK = '{0.month}.{0.day}.{0.year}'.format(d_next)
NEXT_WEEK_SLASH = '{0.month}/{0.day}/{0.year}'.format(d_next)
NEXT_WEEK_VAR = d_next.strftime('%m/%d/%y')

# names of the temp files
DIAMOND = './diamond.txt'
DIAMOND2 = './diamond2.txt'

regex_block = lambda regex, content: ''.join(re.findall(regex, content))


def get_links():
    """Get a list of all of the comic book links on the main page."""
    myreader = MyReader()
    diamond = myreader.read_it('http://www.previewsworld.com/Home/1/1/71/954')

    if not diamond:
        print "ERROR WITH THE MAIN PAGE! SHUTTING DOWN..."
        exit(1)

    # trim the page's content and save it as diamond2.txt
    open(DIAMOND, 'w').write(diamond)
    trim_diamond = open(DIAMOND2, 'w')
    mag = 2
    htmlc = 0

    # We don't mechandise, magazines, etc.
    with open(DIAMOND) as f:
        for line in f:
            if '<h2 align="center">PREMIER PUBLISHERS</h2>' in line:
                htmlc = htmlc + 1
            if '<h2 align="center">MAGAZINES</h2>' in line:
                mag = mag - 1
            if "Magazines" in line:
                mag = mag - 1
                if not mag:
                    exit(1)
            if htmlc == 1 and mag:
                trim_diamond.write(line)
    trim_diamond.close()

    content = open(DIAMOND2, 'r').read()
    regex = '<td><a href="(\w\S+)"'
    links = re.findall(regex, content)
    return links


def get_detail_page(link):
    """Fetch the detail page and remove some of the tags."""
    myreader = MyReader()
    detail_page = myreader.read_it(link)
    if not detail_page:
        return detail_page
    else:
        tags = [
            "<br>", "</br>", "<i>", "</i>",
            "<b>", "</b>", "<strong>", "</strong>",
            "\r\n", "\t\t"
        ]
        for tag in tags:
            detail_page = detail_page.replace(tag, "")
        return detail_page


def get_image(detail_file, detail_page, _id):
    """Fetch the image and save it locally."""
    outpath = os.path.join('./covers/', NEXT_WEEK, _id + '.jpg')
    path = regex_block('"FancyPopupImage" href="(/\w\S+)"', detail_page)
    image_url = 'http://www.previewsworld.com' + path
    myopener = MyOpener()
    successful = myopener.grab_it(image_url, outpath)
    if not successful:
        print "WARNING: NO IMAGE FOR THIS COMIC!!!"
        detail_file.write("<IMAGE>no")
    else:
        detail_file.write("<IMAGE>yes")


def get_details(detail_file, detail_page, count):
    """
    Use regular expressions to grab the data we want out of the
    detail_page and save it to detail_file. Then return _id, which
    will be used to save the cover image associated with this comic.
    """
    regex_dict = {
        '<TITLE>': '<meta property="og:title" content="([^<]+)"',
        '<PUBLISHER>': 'Publisher:&nbsp;([^<]+)<',
        '<CREATORS>': '"StockCodeCreators">([^<]+)<',
        '<DESCRIPTION>': '"PreviewsHtml">([^<]+)<',
        '<SRP>': 'SRP: ([^<]+)<',
    }

    for k, v in regex_dict.items():
        attr = regex_block(v, detail_page)
        detail_file.write(k + attr)
        if not attr:
            print "WARNING: EMPTY ATTRIBUTE FOR THIS ITEM!"

    _id = str(count - 1)
    detail_file.write(
        "<RELEASE>" + NEXT_WEEK_SLASH + "<ID>" + _id + "<VARIANT>no"
    )
    return _id


def clean_up():
    """Delete the temp files."""
    try:
        os.remove(DIAMOND)
        os.remove(DIAMOND2)
    except OSError as e:
        if e.errno == 2:
            print "Nothing to clean up!"
        else:
            print e


def makepath():
    """Create the path where the comic covers will be stored."""
    path = os.path.join('./covers/', NEXT_WEEK)
    try:
        os.makedirs(path)
        print "Creating the path", path, "..."
    except OSError as e:
        if e.errno == 17:
            print "The path", path, "already exists..."
        else:
            print e


def main():
    makepath()
    mylinks = get_links()
    detail_file = open('./detail_file.txt', 'w')
    count = 1
    total = len(mylinks)
    for link in mylinks:
        print "---------------------------------------------"
        print "%d of %d \nOpening link at \n%s \nand grabbing data..." % (
            count, total, link)
        count += 1

        detail_page = get_detail_page(link)
        if not detail_page:
            print "ERROR: PROBLEM WITH LINK:", link
            print "MOVING TO THE NEXT COMIC..."
            continue

        _id = get_details(detail_file, detail_page, count)
        get_image(detail_file, detail_page, _id)
        print "Done!"
        sleep(1)
    detail_file.close()
    clean_up()
    print "...finished!"


if __name__ == "__main__":
    main()
