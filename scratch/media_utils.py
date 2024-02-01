#!/usr/bin/env python
import argparse
from utils import media

def main():
    parser = argparse.ArgumentParser(description="Command line utility for basic media file operations.")
    subparser = parser.add_subparsers(dest='command')

    add_subtitles = subparser.add_parser('add_subtitles')
    trim_media = subparser.add_parser('cutvideo')
    audio_to_video = subparser.add_parser('audiotovideo')
    video_to_audio = subparser.add_parser('videotoaudio')

    add_subtitles.add_argument("-i", "--input", type=str, required=True)
    add_subtitles.add_argument("-s", "--subtitles", type=str, required=True)
    add_subtitles.add_argument("-o", "--output", type=str, required=True)
    add_subtitles.add_argument("-t", "--title", type=str, default=None, required=False)

    trim_media.add_argument("-f", "--file", required=True, type=str)
    trim_media.add_argument("-s", "--start", required=False, default=None, type=str)
    trim_media.add_argument("-e", "--end", required=False, default=None, type=str)

    audio_to_video.add_argument("-a", "--audio", required=True, type=str)
    audio_to_video.add_argument("-i", "--image", required=True, type=str)
    audio_to_video.add_argument("-o", "--output", required=True, type=str)
    audio_to_video.add_argument("-f", "--force", required=False, type=bool, default=True)

    video_to_audio.add_argument("-i", "--input", required=True, type=str)
    video_to_audio.add_argument("-o", "--output", required=True, type=str)
    video_to_audio.add_argument("-f", "--force", required=False, type=bool, default=True)

    args = parser.parse_args()

    if args.command == "add_subtitles":
        print("Adding subtitles file %s for %s with output file %s" % (
            args.subtitles_file, args.input_video, args.output_file
        ))
        """
        media.add_subtitles(input_video=args.input,
                            subtitles_file=args.subtitles,
                            video_final=args.output,
                            title=args.title)
        """

    elif args.command == "cutvideo":
        print("Trimming the file %s")
        media.trim_media(args.file, args.start, args.end)

    elif args.command == "audiotovideo":
        media.audio_to_video(args.audio, args.image, args.output, replace=args.force)

    elif args.command == "videotoaudio":
        media.video_to_audio(args.input, args.output, replace=args.force)

if __name__ == '__main__':
    main()