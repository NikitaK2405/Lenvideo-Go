import os.path
import sys
import time

from colorama import Fore
from colorama import init
from moviepy.editor import *

init()


def get_video_len(path_directory):
    if os.path.exists(path_directory):
        print(Fore.CYAN + "[+] Directory scanning")
        clip_in_dir = os.listdir(path_directory)
        clip_to_merge = []
        for clip in clip_in_dir:
            if clip.endswith(".mp4") or clip.endswith(".avi"):
                VideoFileClip(os.path.join(path_directory, clip))
                clip_to_merge.append(VideoFileClip(os.path.join(path_directory, clip)))

        if len(clip_to_merge) <= 1:
            print(Fore.RED + "[-] There are no video files in directory")
            main()
            return
        else:
            print(Fore.YELLOW + f"[+] Files found: {len(clip_to_merge)}")
            merge_final = concatenate_videoclips(clip_to_merge)
            print(Fore.YELLOW + f"[+] Total duration of found video files: "
                                f"{time.strftime('%H:%M:%S', time.gmtime(merge_final.duration))}")
            main()
            return
    else:
        print(Fore.RED + "[-] The specified path does not exist")
        main()
        return


def main():
    user_change = input(Fore.LIGHTWHITE_EX + "\nSelect action:\n"
                                             "   [0] Exit\n"
                                             "   [1] Find total duration of video files in a folder\n"
                                             "   >>> ")
    if user_change == "0":
        sys.exit()
    elif user_change == "1":
        get_video_len(input(Fore.LIGHTWHITE_EX + "\n[+] Enter path to the file folder: "))
    else:
        print(Fore.RED + "\n[-] Unidentified action: please try again")
        main()


if __name__ == "__main__":
    main()
