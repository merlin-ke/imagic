import pathlib
import csv
from bs4 import *
import requests
import os
import subprocess
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime
import time
import requests
import hashlib


# Create folder to store images
def folder_create(url, images):
    try:
        # get domain name from entered url
        domain_name = urlparse(url).netloc

        # get current date and time
        now = str(datetime.now())

        # format date to suit folder name parameters
        date_time = now.replace('-', '').replace(' ', '_').replace(':', '').split('.')

        # generate save location folder name
        folder_name = f"{domain_name}_{date_time[0]}"

        # create the save location folder
        os.mkdir(folder_name)

    # if folder exists with that name, ask another name
    except:
        print("Folder with that name already exists! Enter a different name.")
        folder_create()

    # image download start
    download_images(images, folder_name)

    # read exif for all downloaded images
    time.sleep(1)
    getExifData(folder_name)


#Function do get exif for all images downloaded.
def download_images(images, folder_name):
    # initial count is zero
    count = 0

    # print total images found in URL
    print(f"\nAttempting to download and save {len(images)} image(s) to '{folder_name}'\n")

    # checking if images is not zero
    if len(images) != 0:
        for i, image in enumerate(images):
            # From image tag ,Fetch image Source URL

            # 1. data-srcset
            # 2. data-src
            # 3. data-fallback-src
            # 4. src

            # Here we will use exception handling

            # first, search for "data-srcset" in img tag
            try:
                # search for "data-srcset" in img tag
                image_link = image["data-srcset"]

            # then we will search for "data-src" in img tag and so on.
            except:
                try:
                    # search for "data-src" in img tag
                    image_link = image["data-src"]
                except:
                    try:
                        # search for "data-fallback-src" in img tag
                        image_link = image["data-fallback-src"]
                    except:
                        try:
                            # search for "src" in img tag
                            image_link = image["src"]

                        # if no source URL found
                        except:
                            pass

            # After getting Image Source URL
            # We will try to get the content of image
            try:
                # Handle images with relative source paths
                if 'http' not in image_link.lower():
                    image_link = url.rstrip('/') + image_link

                    # Parse image link to allow removal of query strings
                    scheme = urlparse(image_link).scheme
                    host = urlparse(image_link).netloc
                    path = urlparse(image_link).path

                    formatted_link = f"{scheme}://{host}{path}"

                    r = requests.get(formatted_link).content

                # Default for images with full paths
                else:
                    # Parse image link to allow removal of query strings
                    scheme = urlparse(image_link).scheme
                    host = urlparse(image_link).netloc
                    path = urlparse(image_link).path

                    formatted_link = f"{scheme}://{host}{path}"

                    r = requests.get(formatted_link).content

                # Get image name and extension from the link
                basename = os.path.basename(formatted_link)

                # extract image name and extension from basename
                img_name, img_ext = os.path.splitext(basename)

                try:

                    # possibility of decode
                    r = str(r, 'utf-8')

                except UnicodeDecodeError:

                    # Calculate md5 hash of downloaded image
                    img_hash = hashlib.md5(r).hexdigest()

                    # After checking above condition, download image with original filename
                    # Append hash to filename for unique names to prevent overwriting
                    image_path = f"{folder_name}/image{count + 1}{img_ext}"

                    with open(f"{image_path}", "wb+") as f:
                        f.write(r)

                    # Rudimentary image download progress
                    count += 1
                    print(f"{count} of {len(images)} image(s) downloaded")
            except:
                pass

        # There might be a possibility not all images will download
        # if all images were downloaded
        if count == len(images):
            print(f"\nAll images downloaded!\n")

        # if not all images were downloaded
        else:
            not_downloaded = len(images) - count
            print(f"\n{count} image(s) downloaded. Failed to download {not_downloaded} image(s)\n")


def getExifData(folder_name):
    # Reuse the same folder created to store images
	files= Path(folder_name)

    # Count number of files whose exif was a success, failed	
	fileCount=0
	failedscannedCount=0
	fileswithnoexif=0  
	fileswithexif=0
    
    # Give filename same name as folder name    
	formatted_name=folder_name.strip()
	csv_file =  open(f"{formatted_name}.csv", 'w')
	writer = csv.writer(csv_file, delimiter=",")

    # CSV Columns    
	header =['Image Name', "Exif Data", "Size", "MD5 Sum Hash", "SHA 1 Hash"]
	writer.writerow(header)

    # Loop through all files to get Exif and hashes.    
	for file in files.iterdir():
		if file.is_file():
            # Get Directory path            
			imgFilepath=Path(file).resolve()
            # Start Count
			fileCount +=1
            # Get File name
			imgFilename=Path(file).name
			##print(f"File name and path is {imgFilepath}")

			try:
				##print(f"exiv2 for {imgFilepath} done...can we print output? ")

                # run Exiv2 command and spefic Exif options                
				exfildata_command=subprocess.run(["exiv2", "-p", "e", imgFilepath],capture_output=True,text=True)
				exfildata=str.strip(exfildata_command.stdout)
                #fileCount =1
                # Check if Image has Exif Data and print size. Images without data will have same size
				if(len(exfildata) == 0):
					exfildata="No Exif Data Detected."
					##print(f"Size is {len(exfildata)}")
					writer.writerow([imgFilename,exfildata,len(exfildata),imgMD5(imgFilepath),imgSHA1(imgFilepath)])
					fileswithnoexif +=1                    
                # Image has Exif, 
				else:
					print(f"Size is {len(exfildata)}")
					writer.writerow([imgFilename,exfildata,len(exfildata),imgMD5(imgFilepath),imgSHA1(imgFilepath)])
					fileswithexif +=1
			except:
				print(f"Error encountred with {imgFilepath}, proceeding on")
				failedscannedCount +=1
				pass
        # House cleaning
		else:
			##print(f"{pathlib.Path(file).resolve} is not a file")
			fileCount -=1
	print(f"Total Files scanned are {fileCount}, Files with ExifData are {fileswithexif}, Files without ExifData are {fileswithnoexif},Files whose ExifData Scan failed are {failedscannedCount}")
	csv_file.close()

# Get MD5 sum
def imgMD5(imgPath):
    md5_hash = hashlib.md5()
    with open(imgPath,"rb") as f:
        for byte_block in iter(lambda: f.read(4096),b""):
            md5_hash.update(byte_block)
        return md5_hash.hexdigest()

# Get SHA 1
def imgSHA1(imgPath):
    # make a hash object
   h = hashlib.sha1()

   # open file for reading in binary mode
   with open(imgPath,'rb') as file:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)
   # return the hex representation of digest
   return h.hexdigest()

# Main Function
def main(url):
    # content of URL
    r = requests.get(url)

    # Parse HTML Code
    soup = BeautifulSoup(r.text, 'html.parser')

    # Find all images in URL
    images = soup.findAll('img')

    # Call folder create function
    folder_create(url, images)

# take url
url = input("Enter URL:- ")

# CALL MAIN FUNCTION
main(url)
