import os
import sys
import shutil
import pathlib

from utils import media

HOME = os.getenv("HOME")
BASE_DIR = "%s/Adhyatm Work/Tattvarta Sutra/" % (HOME)
DIR = "%s/Adhyaya 08" % (BASE_DIR)
CSV_FILE = "%s/list.txt" % BASE_DIR
files = dict()

# index -> (start, end)
# both start & end can be null
cut_index = dict()

def build_index():
    loc = pathlib.Path(DIR)
    for file in loc.rglob("*.mp4"):
        print(str(file))
        fname = os.path.basename(file)
        index = fname.split("_")[0]
        files[index] = str(file)

def build_cut_index():
    fh = open(CSV_FILE, 'r')
    for line in fh.readlines():
        line = line.strip()
        if line.startswith('num'):
            continue
        splt = line.split(",")
        index = splt[0]
        start = splt[1]
        end = splt[2]

        if not start:
            start = None

        if not end:
            end = None
        cut_index[index] = [start, end]

def cut_files():
    for key in files.keys():
        loc = files[key]
        start_end = cut_index[key]
        start = start_end[0]
        end = start_end[1]
        media.trim_media(loc, start, end, dry=False)

def main():
    build_index()
    build_cut_index()
    cut_files()

if __name__ == '__main__':
    main()
