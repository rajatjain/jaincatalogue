#!/usr/bin/env py

import os
from utils import media

HOME = os.getenv("HOME")
base_folder = "%s/Adhyatm Work/Samaysar Kalash Tika/" % HOME
html_file = "%s/kalash_tika.txt" % base_folder


class AudioFile:
    def __init__(self, sr, gatha, kalash, notes, lang):
        self.serial_no = sr
        self.gatha = gatha
        self.kalash = kalash
        self.notes = notes
        self.language = lang

    def __str__(self):
        return "[Serial: %s]  [Gatha: %s] [Kalash: %s] [Notes: %s] [Lang: %s]" % (
            self.serial_no_str, self.gatha, self.kalash, self.notes, self.language
        )

    def file_name(self):
        str = "%s_%s" % (self.serial_no, self.language)
        if self.gatha:
            if len(self.gatha) == 1:
                g_str = "G-%d" % self.gatha[0]
            elif len(self.gatha) == 2:
                g_str = "G-%d-%d" % (self.gatha[0], self.gatha[1])
            str = "%s_%s" % (str, g_str)
        if self.kalash:
            if len(self.kalash) == 1:
                k_str = "K-%d" % self.kalash[0]
            elif len(self.kalash) == 2:
                k_str = "K-%d-%d" % (self.kalash[0], self.kalash[1])
            str = "%s_%s" % (str, k_str)
        if self.notes:
            str = "%s_%s" % (str, self.notes)
        str = "%s.mp3" % str
        return str

    def get_title(self):
        str = "%s Samaysaar Kalash Tika" % self.serial_no
        if self.gatha:
            if len(self.gatha) == 1:
                g_str = "Gatha %d" % self.gatha[0]
            elif len(self.gatha) == 2:
                g_str = "Gatha %d-%d" % (self.gatha[0], self.gatha[1])
            str = "%s %s" % (str, g_str)
        if self.kalash:
            if len(self.kalash) == 1:
                k_str = "Kalash %d" % self.kalash[0]
            elif len(self.kalash) == 2:
                k_str = "Kalash %d-%d" % (self.kalash[0], self.kalash[1])
            str = "%s %s" % (str, k_str)
        if self.notes:
            str = "%s %s" % (str, self.notes)
        return str


class Meta:
    artist = "Gurudev Kanji Swami"
    album = "Samaysaar Kalash"
    album_artist = "Acharya Amrutchandra"
    album_art_file = "%s/%s" % (HOME, "Personal Drive/My Drive/Jainism/images/upscale/Amrutchandra Acharya.jpeg")
    genre = "Pravachan"

    def __init__(self, title, name, track_num):
        self.title = title
        self.name = name
        self.track_num = track_num
        self.artist = Meta.artist
        self.album = Meta.album
        self.album_art_file = Meta.album_art_file
        self.genre = Meta.genre


indices = dict()


def get_indices():
    fh = open(html_file, 'r')

    # Sample Index
    # ['Pravachan 483   58m:24s', 'Samaysar', '411, 412', '239', '', '1968-02-10', 'Mahaa Sud 11, Sat', 'Guj\n']
    for line in fh.readlines():
        if line.startswith('Pravachan'):
            splt = line.split("\t")
            sno = splt[0].split("Pravachan")[1].split()[0].strip()
            try:
                sr = int(sno)
                sr = "%03d" % sr
            except:
                sr = sno
            gatha = splt[2].strip()
            if gatha:
                first = int(gatha.split(',')[0].strip())
                last = int(gatha.split(',')[-1].strip())
                gatha = [first]
                if last != first:
                    gatha = gatha + [last]
            else:
                gatha = None
            kalash = splt[3].strip()
            if kalash:
                fk = int(kalash.split(',')[0].strip())
                lk = int(kalash.split(',')[-1].strip())
                kalash = [fk]
                if fk != lk:
                    kalash = kalash + [lk]
            else:
                kalash = None
            notes = splt[4].strip()
            if notes:
                if notes.startswith("Syaadvad") or notes.startswith("Shakti"):
                    notes = notes
                else:
                    notes = None
            else:
                notes = None
            language = splt[7].strip()
            audio = AudioFile(sr, gatha, kalash, notes, language)
            indices[sr] = audio


def rename():
    lst = os.listdir(base_folder)
    for file in lst:
        if not file.endswith('.mp3'):
            continue
        id = file.split("skt")[1].split("_")[0]
        try:
            idx = int(id)
            idx = "%03d" % idx
        except:
            idx = id
        new_name = "%s/%s" % (base_folder, indices[idx].file_name())
        old_name = "%s/%s" % (base_folder, file)
        print("Rename %s to %s" % (file, indices[idx].file_name()))
        os.rename(old_name, new_name)


def add_meta():
    lst = os.listdir(base_folder)
    for file in lst:
        if not file.endswith('.mp3'):
            continue
        idx = file.split("_")[0]
        audio_file = indices[idx]
        meta = Meta(audio_file.get_title(), audio_file.file_name(), idx)
        media.add_metadata("%s/%s" % (base_folder, file), meta.album, meta.artist, meta.album_artist,
                           meta.album_art_file, meta.track_num, meta.title, meta.genre)


def main():
    get_indices()
    rename()
    add_meta()


if __name__ == "__main__":
    main()