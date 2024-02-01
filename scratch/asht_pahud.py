import os
import pathlib
import shutil

from utils import media

DIR = "/Users/rajatj/jain9.rajat@gmail.com - Google Drive/My Drive/Jainism/Gurudev Pravachan/Asht Pahud"

ALBUM = "Asht Pahud"
ARTIST = "Acharya Kund Kund"
ALBUM_ARTIST = "Gurudev Kanji Swami"
ALBUM_ART = "/Users/rajatj/Personal Drive/My Drive/Jainism/images/upscale/kundkund acharya.jpg"

def scan():
    fh = open("%s/fh.csv" % DIR, "w")
    loc = pathlib.Path(DIR)
    for file in loc.rglob("*.mp3"):
        fname = os.path.basename(file)
        pahud = str(file).split("/")[-2]
        if fname.startswith("apt"):
            index = fname.split("_")[0][3:]
        elif fname.startswith("ap"):
            index = fname.split("_")[0][2:]

        if "1970" in fname:
            series = 1970
        elif "1973" in fname:
            series = 1973
        fh.write("%s,%s,%s\n" % (pahud, index, series))

map = dict()

def build_map():
    global map
    fh = open("%s/fh.csv" % DIR, "r")
    for line in fh.readlines():
        line = line.replace('\ufeff', '')
        line = line.strip()
        splt = line.split(",")
        num = str(splt[0].strip())
        try:
            n = int(num)
            num = "%03d" % n
        except:
            num = num
        p1 = splt[1].strip()[3:]
        index = splt[2].strip()
        try:
            i1 = int(index)
            index = "%03d" % i1
        except:
            index = index
        series = str(splt[3].strip())
        gatha = str(splt[4].strip())
        lang = splt[5].strip()
        p2 = None
        g2 = None
        if splt[6]:
            p2 = splt[6].strip()[3:]
            g2 = str(splt[7].strip())
        if series not in map:
            map[series] = dict()

        map[series][index] = [num, p1, gatha, lang, p2, g2]

def rename():
    global map
    loc = pathlib.Path(DIR)
    files = []
    for file in loc.rglob("*.mp3"):
        files.append(file)
    files.sort()

    for file in files:
        fname = os.path.basename(file)
        pahud = str(file).split("/")[-2]
        if fname.startswith("apt"):
            index = fname.split("_")[0][3:]
        elif fname.startswith("ap"):
            index = fname.split("_")[0][2:]

        if "1970" in fname:
            series = "1970"
        elif "1973" in fname:
            series = "1973"

        meta = map[series][index]
        # print("%s - %s" % (fname, meta))

        # format: num_series-num_lang_pahud-G<>_pahud-G<>
        # print(meta)
        p1 = meta[1].replace(' ', '')
        new_fname = "%s_%s.%s_%s_%s-G%s" % (
            meta[0], series[2:], index, meta[3], p1, meta[2])
        if meta[4] is not None and meta[5] is not None:
            p2 = meta[4].replace(' ', '')
            new_fname = "%s_%s-G%s" % (new_fname, p2, meta[5])
        new_fname = "%s.mp3" % new_fname

        if "163" in fname:
            print("%s -> %s" % (fname, new_fname))
        if "107" in fname:
            print("%s -> %s" % (fname, new_fname))
        new_file = str(file)
        new_file = new_file.replace(fname, new_fname)

        shutil.move(file, new_file)

        # add metadata
        track_num = meta[0]
        title = "Asht Pahud %s : %s Gatha %s" % (
            meta[0], meta[1], meta[2]
        )
        if meta[4] is not None and meta[5] is not None:
            title = "%s : %s Gatha %s" % (title, meta[4], meta[5])

        media.remove_metadata(new_file)
        media.add_metadata(
            new_file, "Asht Pahud", "Gurudev Kanji Swami", "Acharya Kund Kund",
            ALBUM_ART, track_num=track_num, title=title)

def change_meta():
    loc = pathlib.Path(DIR)
    for file in loc.rglob("*.mp3"):
        file_name = str(file)
        print(file_name)
        fname = os.path.basename(file)
        splt = fname.split("_")
        pahud = file_name.split("/")[-2][2:]
        index = splt[0]
        gatha = splt[3].split(".")[0].split("-G")[1]
        new_title = "%s %s - Gatha %s (Asht Pahud)" % (
            pahud, index, gatha)

        media.remove_metadata(file_name)
        media.add_metadata(
            file_name, "Asht Pahud", "Gurudev Kanji Swami", "Acharya Kund Kund",
            ALBUM_ART, track_num=index, title=new_title)


# build_map()
# rename()
change_meta()