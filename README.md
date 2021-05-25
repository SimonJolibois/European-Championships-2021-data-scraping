# European-Championships-2021-data-scraping
## Description
.py script to scrap results of the European Championships 2021 at Budapest 

## How to use
In the .py choose the path of the directory you want to stock the output files at (path variable)

You need to download the webpage from which you want to collect data:
Look here for the races: http://budapest2020.microplustiming.com/indexBudapest2021_web.php
Right click -> Save as

After that, point where the html file is in the .py (adress of page variable)
Let the code do the rest.
The output is a collection of different folders containing a .json with the metadata of the race and a .csv with the actual data (swimmers, times)
