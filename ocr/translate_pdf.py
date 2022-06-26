#!/usr/bin/env python

import io
import os
import subprocess
import shutil
import time

from concurrent.futures import ThreadPoolExecutor

from docx import Document
from docx.shared import Pt

from google.cloud import vision

"""
Requirements:
  - Google Cloud Account
  - Linux/MacOS
  - Python

Setup:
  - Create a Google Cloud Account
  - Create a new project from https://console.cloud.google.com
  - Setup credentials and download the credentials JSON file
    https://cloud.google.com/docs/authentication/getting-started
  - Enable vision API: https://cloud.google.com/vision/docs/setup
  - gcloud auth login

  - Install requisite libraries
    * ghostscript
    * imagemagick
  - Using 'pip' download the following libraries
    * python-docx
    * google-cloud-vision

  - Run the script by changing the required parameters

For M1 macos users: 
    For M1 mac, the regular 'pip install' commands would not work
    as the default pip binaries are compiled with x86 architecture.

    Use the following command to install the requisite libraries.

    pip install --no-binary :all: python-docx --no-cache-dir --ignore-installed
    pip install --no-binary :all: google-cloud-vision --no-cache-dir --ignore-installed
"""

"""
The tool accepts a .pdf file location and then converts it into a fully translated
.docx file. Here's how it happens:

  - The .pdf file is converted into a list of .jpg files
  - Google vision APIs are used to convert each .jpg
    file into a .txt file
  - All the .txt files are stored locally
  - All the .txt files are combined into the final .docx file
  
Notes:
This script uses google vision APIs which is chargeable by Google.
Please be aware of this before using this. Check the prices here to estimate your cost:
https://cloud.google.com/vision/pricing#prices
"""


# The base folder where the original PDF file is kept.
BASE_FOLDER = "/Users/rajatj/pdfs"

# The folder where the JPG files from the PDF files will be stored.
JPG_FOLDER = "%s/jpg" % BASE_FOLDER

# The folders where text files are stored.
TXT_FOLDER = "%s/txt" % BASE_FOLDER

BASE_FILE = "%s/%s" % (BASE_FOLDER, "Bund bund Ma Amrut.pdf")

vision_client = vision.ImageAnnotatorClient()

def init():
    # Create all the base folders
    for folder in [JPG_FOLDER, TXT_FOLDER]:
        if os.path.isdir(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)

def convert_pdf_to_images():
    os.chdir(JPG_FOLDER)
    cmd = [ "convert", "-density", "200", BASE_FILE, "page_%03d.jpg" ]
    print("Calling cmd: %s ..." % (' '.join(cmd)))
    print("This may take some time.")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate()
    print("PDF to images done!")


def detect_text(filename):
    file_name = os.path.abspath(filename)
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    text_detection_response = vision_client.text_detection(image=image)
    annotations = text_detection_response.text_annotations
    if len(annotations) > 0:
        text = annotations[0].description
    else:
        text = ''
    print('Extracted text from image %s (%s chars)' % (filename, len(text)))

    output_name = filename.split(".")[0].split("/")[-1] + ".txt"
    fh = open(os.path.join(TXT_FOLDER, output_name), 'w')
    fh.write(text)
    fh.close()
    print("Text detection done for file %s" % filename)

def txt2doc():
    base_fname = os.path.basename(BASE_FILE)
    final_fname = os.path.join(BASE_FOLDER, base_fname.split('.')[0] + ".docx")
    if os.path.isfile(final_fname):
        os.remove(final_fname)
    files = []
    for file in os.listdir(TXT_FOLDER):
        files.append(file)
    files.sort()
    print(files)
    document = Document()
    style = document.styles['Normal']
    style.font.name = 'Helvetica'
    style.font.size = Pt(10)

    for file in files:
        contents = open(os.path.join(TXT_FOLDER, file)).read()
        document.add_paragraph(contents, style=style)
        document.add_page_break()
    document.save(final_fname)

def main():
    start = time.time()
    init()

    convert_pdf_to_images()
    files = []
    for file in os.listdir(JPG_FOLDER):
        files.append(os.path.join(JPG_FOLDER, file))
    files.sort()
    print(files)

    futures = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        for file in files:
            futures.append(executor.submit(detect_text, file))

        for future in futures:
            print(future.result())

    txt2doc()
    end = time.time()
    print("Total time: %.2f secs" % (end - start))

if __name__ == '__main__':
    main()
