import os.path
import sys
import time

from colorama import Fore
from colorama import init
from moviepy.editor import *

init()


def get_video_len(path_directory):
    if os.path.exists(path_directory):
        print(Fore.CYAN + "[+] Сканирование директории")
        clip_in_dir = os.listdir(path_directory)
        clip_to_merge = []
        for clip in clip_in_dir:
            if clip.endswith(".mp4") or clip.endswith(".avi"):
                VideoFileClip(os.path.join(path_directory, clip))
                clip_to_merge.append(VideoFileClip(os.path.join(path_directory, clip)))

        if len(clip_to_merge) <= 1:
            print(Fore.RED + "[-] В указанной директории нет видеофайлов")
            main()
            return
        else:
            print(Fore.YELLOW + f"[+] Найдено фалов: {len(clip_to_merge)}")
            merge_final = concatenate_videoclips(clip_to_merge)
            print(Fore.YELLOW + f"[+] Общая длительность найденных видеофайлов: "
                                f"{time.strftime('%H:%M:%S', time.gmtime(merge_final.duration))}")
            main()
            return
    else:
        print(Fore.RED + "[-] Указанного пути не существует")
        main()
        return


def main():
    user_change = input(Fore.LIGHTWHITE_EX + "\nВыберите действие:\n"
                                             "   [0] Выход\n"
                                             "   [1] Найти общую продолжительность видеофайлов в папке\n"
                                             "   >>> ")
    if user_change == "0":
        sys.exit()
    if user_change == "1":
        get_video_len(input(Fore.LIGHTWHITE_EX + "\n[+] Введите путь к папке с файлами: "))


if __name__ == "__main__":
    main()
