import os
import sys
import shutil
import pathlib

from utils import media

FILES_LOC = "/Users/rajatj/jain9.rajat@gmail.com - Google Drive/My Drive/Jainism/Gurudev Pravachan/Ishtopadesh"
ALBUM_ART = "/Users/rajatj/jain9.rajat@gmail.com - Google Drive/My Drive/Jainism/images/upscale/Acharya_Dharsen_upscaled.jpeg"

# This is for regular Gurudev's Pravachans formats of the type:
# 010_Guj_G-10-12_K-15-18.mp3
def scan_folder():
    # fname = "014_70.014_Guj_DarshanPahud-G16-17.mp3"
    loc = pathlib.Path(FILES_LOC)
    for file in loc.rglob("*.mp3"):
        fname = os.path.basename(file)
        lst = fname.split("_")
        index = int(lst[0])
        language = lst[1]
        gatha = lst[2].split(".")[0][1:]

        title = "Ishtopadesh %02d - Gatha %s" % (index, gatha)
        print(title)
        media.remove_metadata(file)
        media.add_metadata(
            file, "Ishtopadesh", "Gurudev Kanji Swami",
            "Acharya Pujyapad Swami", ALBUM_ART,
            track_num=index, title=title, genre="Pravachan")

def scan_folder1():
    loc = pathlib.Path(FILES_LOC)
    for file in loc.rglob("*.mp3"):
        fname = os.path.basename(file)
        index = fname.split("_")[0]
        title = "Panchastikaya %03d" % int(index)
        gatha = fname.split("_")[3].split(".")[0]
        gatha = gatha[len("G-"):]
        title = "%s - Gatha %s" % (title, gatha)
        print(title)
        media.remove_metadata(file)
        media.add_metadata(
            file, "Panchastikaya", "Gurudev Kanji Swami",
            "Acharya Kund Kund", ALBUM_ART, track_num=index,
            genre="Pravachan", title=title)

scan_folder()
