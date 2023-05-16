import os
import sys
import shutil
import pathlib

from utils import media

FILES_LOC = "/Users/rajatj/Personal Drive/My Drive/Jainism/Pravachan/Yugal Ji/Bhaag - 1/19 Tattva Charcha Mumbai"
ALBUM_ART = "/Users/rajatj/Personal Drive/My Drive/Jainism/images/Yugal Ji.jpg"

# This is for regular Gurudev's Pravachans formats of the type:
# 010_Guj_G-10-12_K-15-18.mp3
def scan_folder():
    loc = pathlib.Path(FILES_LOC)
    for file in loc.rglob("*.mp3"):
        fname = os.path.basename(file)
        index = fname.split("_")[0]
        dhal = fname.split("_")[2]
        gatha = fname.split("_")[3].split(".")[0][1:]
        title = "Chhah Dhala %s - %s - Gatha %s" % (index, dhal, gatha)
        print(title)
        media.remove_metadata(file)
        media.add_metadata(
            file, "Chhah Dhala", "Gurudev Kanji Swami",
            "Pandit Daulat Ram", ALBUM_ART,
            track_num=index, title=title)

def scan_folder1():
    loc = pathlib.Path(FILES_LOC)
    for file in loc.rglob("*.mp3"):
        fname = os.path.basename(file)
        index = fname.split("_")[1].split(".")[0]
        title = "Babuji Yugalji Neelambar Tatva Charcha - %s" % index
        media.remove_metadata(file)
        media.add_metadata(
            file, "Neelambar Tatva Charcha", "Babu Jugal Kishore Jain Yugal",
            "Babu Jugal Kishore Jain Yugal", ALBUM_ART,
            track_num=index, title=title)

scan_folder1()
