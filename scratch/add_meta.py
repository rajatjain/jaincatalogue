import os
import sys
import shutil
import pathlib

from utils import media

FILES_LOC = "/Users/rajatj/Personal Drive/My Drive/Jainism/Gurudev Pravachan/Chhah Dhala"
ALBUM_ART = "/Users/rajatj/Personal Drive/My Drive/Jainism/images/Pandit Daulat Ram Ji.jpg"
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

scan_folder()