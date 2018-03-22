# :sunrise: Google Images Download
Python Script for 'searching' and 'downloading' hundreds of Google images to the local hard disk!

## Summary
This is a command line python program to search keywords/key-phrases on Google Images and then also optionally download one or more images to your computer. This is a small program which is ready-to-run, but still under development. Many more features will be added to it going forward.

## Compatability
This program is compatible with both the versions of python (2.x and 3.x). It is a download-and-run program with no changes to the file. You will just have to specify parameters through the command line.
___

## How to run the script?
1. Download this repository on your local hard drive
2. Open the terminal (for mac/linux OS) or command prompt (for windows OS) and browse to the location of downloaded file 'google-images-download.py'
3. Type in one of the following command mentioned below

## Usage
**Python3:** `python3 google-images-download.py [Arguments...]`

**Python2:** `python google-images-download.py [Arguments...]`

### Arguments 

| Argument  | Short hand | Explanation |
| --- | :---: | --- |
|**keywords**| k | Denotes the keywords/key phrases you want to search for and the directory file name. <br> Tips: <br> * If you simply type the keyword, Google will best try to match it <br> * If you want to search for exact phrase, you can wrap the keywords in double quotes ("") <br> * If you want to search to contain either of the words provided, use **OR** between the words. <br> * If you want to explicitly not want a specific word use a minus sign before the word (-)|
|**suffix_keywords**| sk | Denotes additional words added after main keyword while making the search query. Useful when you have multiple suffix keywords for one keyword <br> The final search query would be: <keyword> <suffix keyword>|
|**limit** | l |Denotes number of images that you want to download.  |
|**format** | f |Denotes the format/extension that you want to download. <br> `Possible values: jpg, gif, png, bmp, svg, webp, ico`|
|**color** | c |Denotes the color filter that you want to apply to the images. <br> `Possible values: red, orange, yellow, green, teal, blue, purple, pink, white, gray, black, brown`|
|**color_type** | ct |Denotes the color type you want to apply to the images. <br> `Possible values: full-color, black-and-white, transparent`|
|**usage_rights** | r |Denotes the usage rights/licence under which the image is classified. <br> `Possible values: labled-for-reuse-with-modifications, labled-for-reuse, labled-for-noncommercial-reuse-with-modification, labled-for-nocommercial-reuse`|
|**size** | s |Denotes the relative size of the image to be downloaded. <br> `Possible values: large, medium, icon`|
|**aspect_ratio** | a |Denotes the aspect ration of images to download. <br> `Possible values: tall, square, wide, panoramic`|
|**type** | t |Denotes the type of image to be downloaded. <br> `Possible values: face,photo,clip-art,line-drawing,animated`|
|**time** | w |Denotes the time the image was uploaded/indexed. <br> `Possible values: past-24-hours, past-7-days`|
|**delay** | d |Time to wait between downloading two images|
|**url** | u |Allows you search by image. It downloads images from the google images link provided|
|**single_image** | x |Allows you to download one image if the complete URL of the image is provided|
|**output_directory** | o |Allows you specify the main directory name. If not specified, it will default to 'downloads'|
|**similar_images** | si |Reverse Image Search. Searches and downloads images that are similar to the image link/url you provide.|
|**specific_site** | ss |Allows you to download images with keywords only from a specific website/domain name you mention as indexed in Google Images.|


**Note:** If `single_image` or `url` parameter is not present, then keywords is a mandatory parameter. No other parameters are mandatory.

## Examples
* If you have python 2.x version installed

`python google-images-download.py --keywords "Polar bears, baloons, Beaches" --limit 20`

* If you have python 3.x version installed

`python3 google-images-download.py --keywords "Polar bears, baloons, Beaches" --limit 20`

* Using Suffix Keywords allows you to specify words after the main keywords. For example if the `keyword = car` and `suffix keyword = 'red,blue'` then it will first search for `car red` and then `car blue`

`python3 google-images-download.py --k "car" -sk 'red,blue,white' -l 10`

* To use the short hand command

`python google-images-download.py -k "Polar bears, baloons, Beaches" -l 20`

* To download images with specific image extension/format

`python google-images-download.py --keywords "logo" --format svg`

* To use color filters for the images

`python google-images-download.py -k "playground" -l 20 -c red`

* To use non-English keywords for image search

`python google-images-download.py -k "北极熊" -l 5`

* To download images from the google images link

`python google-images-download.py -k "sample" -u <google images page URL>`

* To save images in specific main directory (instead of in 'downloads')

`python google-images-download.py -k "boat" -o "boat_new"`

* To download one single image with the image URL

`python google-images-download.py --keywords "baloons" --single_image <URL of the images>`

* To download images with size and type constrains

`python google-images-download.py --keywords "baloons" --size medium --type animated`

* To download images with specific usage rights

`python google-images-download.py --keywords "universe" --usage_rights labled-for-reuse`

* To download images with specific color type

`python google-images-download.py --keywords "flowers" --color_type black-and-white`

* To download images with specific aspect ratio

`python google-images-download.py --keywords "universe" --aspect_ratio panoramic`

* To download images which are similar to the image in the image URL that you provided (Reverse Image search).

`python3 pr.py -si <image url> -l 10`

* To download images from specific website or domain name for a given keyword

`python google-images-download.py --keywords "universe" --specific_site example.com`

===> The images would be downloaded in their own sub-directories inside the main directory (either the one you provided or in 'downloads') in the same folder as the python file that you run.


___

## SSL Errors
If you do see SSL errors on Mac for Python 3 please go to Finder —> Applications —> Python 3 —> Click on the ‘Install Certificates.command’ and run the file.

## Contribute
Anyone is welcomed to contribute to this script. If you would like to make a change, open a pull request. For issues and discussion visit the [Issue Tracker](https://github.com/hardikvasa/google-images-download/issues)

## :exclamation::exclamation: Disclaimer
This program lets you download tons of images from Google. Please do not download any image without violating its copyright terms. Google Images is a search engine that merely indexes images and allows you to find them.  It does NOT produce its own images and, as such, it doesn't own copyright on any of them.  The original creators of the images own the copyrights.  

Images published in the United States are automatically copyrighted by their owners, even if they do not explicitly carry a copyright warning.  You may not reproduce copyright images without their owner's permission, except in "fair use" cases, or you could risk running into lawyer's warnings, cease-and-desist letters, and copyright suits. Please be very careful before its usage!
