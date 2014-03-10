diamond
========

This is a script I'd made a while back to scrape next week's comic book releases from Diamond Comic Book Distributor's website.
I created this script before I knew about software like Beautiful Soup and Scrapy... 

When you run the script, it'll create a folder in the current directory called 'covers', then inside of that it'll create
another folder using next week's Wednesday's date (comics are released every Wednesday), which will store the comic book
cover images. It'll also create a file called 'detail_file.txt', which will contain the details of the comics (things like
title, description, etc.). detail_file.txt is written to in a way that makes it easy to parse with regular expressions.
Also created are 2 temp files that are deleted when the script finishes grabbing all of the comics.

Included is ChangeUA, a script for changing the user-agent and reading/grabbing resources.

Run it like so:

    $ python diamond.py

    Creating the path ./covers/3.12.2014 ...
    ---------------------------------------------
    1 of 132 
    Opening link at 
    http://www.previewsworld.com/Home/1/1/71/914?stockItemID=NOV130069 
    and grabbing data...
    Done!
    ---------------------------------------------
    2 of 132 
    Opening link at 
    http://www.previewsworld.com/Home/1/1/71/914?stockItemID=SEP130086 
    and grabbing data...
    WARNING: EMPTY ATTRIBUTE FOR THIS ITEM!
    Done!
    ---------------------------------------------
    ...
