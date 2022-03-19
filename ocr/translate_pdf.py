#!/usr/bin/env python

import os
import subprocess
import shutil
import time

from concurrent.futures import ThreadPoolExecutor

from docx import Document
from docx.shared import Pt

from google.cloud import storage
from google.cloud import translate_v2 as translate
from google.cloud import vision

"""
Requirements:
 - Need to download GOOGLE_APPLICATION_CREDENTIALS in a JSON file and set it as an environment variable.
 - imagemagick (for 'convert' application)
 - python-docx (creating .docx file)
 - google cloud storage, translate, vision packages etc.
"""

"""
The tool accepts a .pdf file location and then converts it into a fully translated
.docx file. Here's how it happens:

  - The .pdf file is converted into a list of .jpg files
  - All the .jpg files are uploaded to google cloud storage
  - Google translate/vision APIs are used to convert each .jpg
    file into a .txt file
  - All the .txt files are stored locally
  - All the .txt files are combined into the final .docx file
  
Notes:
  - 'convert' by imagemagick is the library used to convert .pdf to .jpg files
     A better tool (native python sdk) will be helpful
  - Each jpg file needs to be present in google cloud storage (requirement)
  - User needs to have a google cloud account, download the credentials file
  - Environment variable GOOGLE_APPLICATION_CREDENTIALS needs to be set pointing
    to the json file containing the credentials
  - Need to enable the google cloud vision, translate APIs on google cloud console
    (https://cloud.google.com/functions/docs/tutorials/ocr)
    
This is tested on macOS. However, it should work equally well on any linux environment.
"""


BASE_FOLDER = "/Users/rjain/pdfs"
JPG_FOLDER = "%s/jpg" % BASE_FOLDER
TXT_FOLDER = "%s/txt" % BASE_FOLDER

BASE_FILE = "%s/%s" % (BASE_FOLDER, "Dhyeya_Purvak_Gyeya_H.pdf")

vision_client = vision.ImageAnnotatorClient()
translate_client = translate.Client()
storage_client = storage.Client()

INPUT_BUCKET = "jaincatalogue-images"
INPUT_BUCKET_PREFIX = "jpgs"

files_text = dict()


def init():
    # Create all the base folders
    for folder in [JPG_FOLDER, TXT_FOLDER]:
        if os.path.isdir(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)
    clear_gcp_bucket()


def convert_pdf_to_images():
    os.chdir(JPG_FOLDER)
    cmd = [ "convert", "-density", "200", BASE_FILE, "page_%03d.jpg" ]
    print("Calling cmd: %s ..." % (' '.join(cmd)))
    print("This may take some time.")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate()
    print("PDF to images done!")


def clear_gcp_bucket():
    bucket = storage_client.bucket(INPUT_BUCKET)
    for blob in bucket.list_blobs(prefix=INPUT_BUCKET_PREFIX):
        blob.delete()
    print("GCS bucket cleared")


def upload_images_to_gcs():
    bucket = storage_client.bucket(INPUT_BUCKET)
    total_files = 0
    for file in os.listdir(JPG_FOLDER):
        total_files += 1
    uploaded_files = 0
    for file in os.listdir(JPG_FOLDER):
        if os.path.isfile(os.path.join(JPG_FOLDER, file)):
            blob = bucket.blob(INPUT_BUCKET_PREFIX + "/" + file)
            blob.upload_from_filename(os.path.join(JPG_FOLDER, file))
            uploaded_files += 1
            print("Uploaded %s: %d of %d" % (file, uploaded_files, total_files))
    print("Uploaded all images to gcs")

def detect_text(filename):
    text_detection_response = vision_client.text_detection({
        'source': {'image_uri': 'gs://{}/{}'.format(INPUT_BUCKET, filename)}
    })
    annotations = text_detection_response.text_annotations
    if len(annotations) > 0:
        text = annotations[0].description
    else:
        text = ''
    print('Extracted text from image %s (%s chars)' % (filename, len(text)))

    output_name = filename.split(".")[0].split("/")[1] + ".txt"
    files_text[output_name] = text
    print("Text detection done")

def save_results():
    print('Total files collected: %d' % len(files_text.keys()))
    total_chars = 0
    for file, text in files_text.items():
        fh = open(os.path.join(TXT_FOLDER, file), "w")
        fh.write(text)
        fh.close()
        total_chars += len(text)
        print('Saved file %s' % file)
    print("Total chars extracted: %d" % total_chars)


def translate():
    bucket = storage_client.bucket(INPUT_BUCKET)
    blobs = bucket.list_blobs(prefix=INPUT_BUCKET_PREFIX)
    files = list()
    for blob in blobs:
        files.append(blob.name)
    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(detect_text, files)


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


if __name__ == '__main__':
    start = time.time()
    init()

    convert_pdf_to_images()
    upload_images_to_gcs()
    translate()
    save_results()
    txt2doc()
    clear_gcp_bucket()
    end = time.time()
    print("Total time: %.2f secs" % (end - start))
