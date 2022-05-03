# imagic
Image forensic python script that uses Exiv2 to get Exif Data

### Background and Motivation
This project builds on the contributions of [@abhigoya](https://auth.geeksforgeeks.org/user/abhigoya), [@ruhelaa48](https://auth.geeksforgeeks.org/user/ruhelaa48) on [GeeksforGeeks](https://www.geeksforgeeks.org/how-to-download-all-images-from-a-web-page-in-python/), which served as the starting point. [Exvi2](https://www.kali.org/tools/exiv2/), a C++ library and a command line utility to manage image metadata. It provides fast and easy read and write access to the EXIF, IPTC and XMP metadata of images in various formats. Special acknowledgement to [@Ray M](https://github.com/crim3hound) for answering my problem broadcast and working on a solution.

I was working on a case where a threat actor had leaked some images online. My objective was to do recon on the images and check whether that had an EXIF Data that could help me identify the TA. Downloading the images manually and running EXIF wasn't feasible. I needed a tool that if given the link to the images, it could download all the images, get EXIF Data, calculate forensic hashes and then create a  report. []

I couldn't find any similar project or tools and decided to work on a similar tool since the required individual tools were available. My focus was to automate the process by utilizing existing tools. [@Ray M](https://github.com/crim3hound) reached out, and I shared part of my research with him which enabled him to create [DownloadedImagesExifReader](https://github.com/crim3hound/DownloadedImagesExifReader) and based on some of his work, I was able to add more improvement to my script.

### Requirements
1. Python v3.7.x and newer. Download [here](https://www.python.org/downloads/).
2. [Exvi2](https://www.kali.org/tools/exiv2/). Kali comes with Exvi2 preinstalled, which worked for me.

### Example

````
imagic.py 
Enter URL:- https://<someurl>
Attempting to download and save 48 image(s) to 'someurl_20220503_024658'
1 of 48 image(s) downloaded
2 of 48 image(s) downloaded
3 of 48 image(s) downloaded
4 of 48 image(s) downloaded
.
.
.
All images downloaded!
Total Files scanned are 48, Files with ExifData are 0, Files without ExifData are 48,Files whose Exif Data Scan failed are 0
````
### Result
![imagic  2022-05-03 122537](https://user-images.githubusercontent.com/55712262/166431108-00348836-8e49-43e5-9a75-85169bc16dc2.png)

                                                                                                                               
