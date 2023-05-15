#!/usr/bin/env python

import os
import sys
import shutil

from utils import media

CSV_FILE = "/Users/rajatj/Adhyatm Work/Panchastikay/list.csv"
FILES_LOC = "/Users/rajatj/Adhyatm Work/Panchastikay"

pravachan_index = dict()
pravachan_index[69] = dict()
pravachan_index[64] = dict()

def scan_files():
    DIR = "%s/%s" % (FILES_LOC, "Combined")
    for file in os.listdir(DIR):
        if file.startswith('.DS'):
            continue
        year = 0
        if file.startswith("64"):
            year = 64
        elif file.startswith("69"):
            year = 69
        else:
            print("Year %s not found" % file)
            sys.exit(1)

        index = int(file.split("_")[1])
        meta = pravachan_index[year][index]
        new_fname = "%03d_%02d_%s_G-%s.mp3" % (meta[0], index, meta[2], meta[1])
        print("Renaming %s to %s" % (file, new_fname))
        shutil.copy("%s/%s" % (DIR, file), "%s/Final/%s" % (FILES_LOC, new_fname))

def create_index():
    global pravachan_index
    fh = open(CSV_FILE, "r")
    for line in fh.readlines():
        line = line.strip()
        if line.startswith("#"):
            continue
        vals = line.split(",")
        global_index = int(vals[0])
        series_index = int(vals[1])
        gatha = vals[2]
        date = vals[3]
        language = vals[4]

        if "69" in date or "70" in date:
            pravachan_index[69][series_index] = [global_index, gatha, language]
        elif "64" in date:
            pravachan_index[64][series_index] = [global_index, gatha, language]

def add_meta():
    DIR = "%s/%s" % (FILES_LOC, "Final")
    for file in os.listdir(DIR):
        if file.startswith(".DS"):
            continue
        print(file)
        splt = file.split("_")
        index = file.split("_")[0]
        title = "Panchastikaya %s - Gatha %s" % (splt[0], splt[3][2:])
        media.add_metadata("%s/%s" % (DIR, file),
                           "Panchastikaya", "Gurudev Kanji Swami", "Acharya Kund Kund",
                           "/Users/rajatj/jain9.rajat@gmail.com - Google Drive/My Drive/Jainism/images/upscale/kundkund acharya 2.jpeg",
                           track_num=index, title=title)


if __name__ == '__main__':
    # create_index()
    # scan_files()
    add_meta()