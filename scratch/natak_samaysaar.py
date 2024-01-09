import os
import pathlib
import shutil

from utils import media

DIR = "/Users/rajatj/Adhyatm Work/Pravachans/Natak Samaysaar"

ALBUM = "Natak Samaysaar"
ARTIST = "Pandit Banarasidas"
ALBUM_ARTIST = "Gurudev Kanji Swami"
ALBUM_ART = "/Users/rajatj/Personal Drive/My Drive/Jainism/images/pandit-banarasidasji-5-1.jpg"

map = dict()

def build_map():
    global map
    fh = open("%s/list.csv" % DIR, "r")
    for line in fh.readlines():
        line = line.replace('\ufeff', '')
        line = line.strip()
        splt = line.split("#")
        num = str(splt[0].strip())
        try:
            n = int(num)
            num = "%03d" % n
        except:
            num = num
        s = splt[1].strip()
        # modify it so that 2,3,4,5 becomes
        s1 = s.replace("-", ",")
        s2 = s1.split(",")
        if len(s2) > 1:
            shlok = "%s-%s" % (s2[0].strip(), s2[-1].strip())
        else:
            shlok = s2[0]
        language = splt[2].strip()
        adhikar = splt[3].strip()
        map[int(num)] = [int(num), shlok, language, adhikar]

def rename():
    global map
    loc = pathlib.Path(DIR)
    files = []
    for file in loc.rglob("*.mp3"):
        files.append(file)
    files.sort()

    for file in files:
        fname = os.path.basename(file)
        num = int(fname.split("_")[0][3:])
        meta = map[num]
        shlok = meta[1]
        lang = meta[2]
        adhikar = meta[3]

        new_fname = "%03d_%s_%s_S-%s.mp3" % (num, lang, adhikar, shlok)
        new_fname = new_fname.replace(" ", "-")
        new_fname = "%s/%s" % (DIR, new_fname)
        print("Move: %s - %s" % (file, new_fname))
        shutil.move(file, new_fname)

        shlok_string = shlok
        if shlok == "Summary":
            shlok_string = "Summary"
        else:
            shlok_string = "Shlok %s" % shlok
        # add metadata
        track_num = num
        title = "Natak Samaysaar %03d - %s - %s" % (
            num, adhikar, shlok_string
        )
        print(title)

        media.remove_metadata(new_fname)
        media.add_metadata(
            new_fname, ALBUM, ALBUM_ARTIST, ARTIST,
            ALBUM_ART, track_num=track_num, title=title)

build_map()
rename()