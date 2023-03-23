import os.path
import time

from numpy import arange
from colorama import Fore
from colorama import init
from moviepy.editor import *

init()


def merge_video_clip(path_directory, res_name):
    if os.path.exists(path_directory):
        print(Fore.CYAN + "[+] Сканирование директории")
        clip_in_dir = os.listdir(path_directory)
        clip_to_merge = []
        for clip in clip_in_dir:
            if clip.endswith(".mp4") or clip.endswith(".avi"):
                VideoFileClip(os.path.join(path_directory, clip))
                clip_to_merge.append(VideoFileClip(os.path.join(path_directory, clip)))

        if len(clip_to_merge) <= 1:
            print(Fore.RED + "[-] В указанной директории нечего объединять")
            main()
            return
        else:
            print(Fore.YELLOW + f"[+] Найдено фалов: {len(clip_to_merge)}")
            merge_final = concatenate_videoclips(clip_to_merge)
            print(Fore.YELLOW + f"[+] Длительность объединяемого видео: "
                                f"{time.strftime('%H:%M:%S', time.gmtime(merge_final.duration))}\n[+] Начинаю "
                                f"объединение файлов...\n")
            merge_final.write_videofile(os.path.join(os.getcwd(), f"{res_name}.mp4"))
            print(Fore.GREEN + "\n[+] Объединение файлов завершено")
            print(Fore.GREEN + f'[+] Видео сохранено в папку: "{os.path.join(os.getcwd(), f"{res_name}.mp4")}"')
            main()
            return
    else:
        print(Fore.RED + "[-] Указанного пути не существует")
        main()
        return


def clip_video(path_file, start_time, end_time):
    if os.path.isfile(path_file):
        if os.path.split(path_file)[-1].endswith(".mp4") or os.path.split(path_file)[-1].endswith(".avi"):
            dir_vid = os.path.split(path_file)[0]
            suff = f".{os.path.split(path_file)[-1].split('.')[-1]}"
            vid_clip_name = f"{os.path.split(path_file)[-1].removesuffix(suff)}_clip{suff}"

            try:
                start = int(start_time.split(":")[0]) * 60 + int(start_time.split(":")[1])
            except IndexError:
                start = int(start_time)
            except ValueError:
                print(Fore.RED + "[-] Вы ввели не число")
                main()
                return
            try:
                end = int(end_time.split(":")[0]) * 60 + int(end_time.split(":")[1])
            except IndexError:
                end = int(end_time)
            except ValueError:
                print(Fore.RED + "[-] Вы ввели не число")
                main()
                return

            print(Fore.CYAN + "[+] Начинаю вырезку фрагмента видео")
            print(Fore.YELLOW + f"   - Длительность фрагмента: {end - start} секунд")

            clip = VideoFileClip(path_file)
            print(Fore.YELLOW + f"   - Общая продолжительность видео: {clip.duration} секунд\n")

            clip_clip = clip.subclip(start, end)
            print(Fore.CYAN + "[+] Записываю фрагмент видео...\n")
            clip_clip.write_videofile(os.path.join(dir_vid, f"{vid_clip_name}"))
            clip.reader.close()
            clip.audio.reader.close_proc()
            print(Fore.GREEN + f'\n[+] Видео сохранено в папку: "{os.path.join(dir_vid, f"{vid_clip_name}")}"')
            main()
            return
        else:
            print(Fore.RED + "[-] Формат файла не поддерживается")
            main()
            return
    else:
        print(Fore.RED + "[-] Не указан файл")
        main()
        return


def remove_audio_from_video(path_file):
    suff = f".{os.path.split(path_file)[-1].split('.')[-1]}"
    vid_name = f"{os.path.split(path_file)[-1].removesuffix(suff)}_witout_audio{suff}"
    if os.path.isfile(path_file):
        if os.path.split(path_file)[-1].endswith(".mp4") or os.path.split(path_file)[-1].endswith(".avi"):
            print(Fore.CYAN + "[+] Удаление аудио")
            video = VideoFileClip(path_file)
            video.without_audio().write_videofile(os.path.join(os.path.split(path_file)[0], vid_name))
            print(Fore.GREEN + f"[+] Удаление аудио завершено. \n   - Файл сохранен: "
                               f'"{os.path.join(os.path.split(path_file)[0], vid_name)}"')
            main()
            return
        else:
            print(Fore.RED + "[-] Формат файла не поддерживается")
            main()
            return
    else:
        print(Fore.RED + "[-] Файл не обнаружен")
        main()
        return


def extract_mp3(path_file):
    file_in_dir = []
    if os.path.isdir(path_file):
        print(Fore.CYAN + "[+] Сканирование директории")
        file_in_dir = os.listdir(path_file)
    elif os.path.isfile(path_file):
        file_in_dir = os.listdir(os.getcwd())

    video_to_extract = []
    mp3_list = []

    for file in file_in_dir:
        print(Fore.CYAN + f'\r[+] Добавляю файлы для извлечения: "{file}"', end="")
        if file.endswith(".mp4") or file.endswith(".avi"):
            mp3_suff = f".{file.replace('.', '_').split('_')[-1]}"
            mp3_list.append(f"{file.removesuffix(mp3_suff)}.mp3")
            video_to_extract.append(VideoFileClip(os.path.join(os.getcwd(), file)))

    if len(video_to_extract) > 0:
        print(Fore.CYAN + "\n[+] Запуск извлечения аудио\n")
        for num, video in enumerate(video_to_extract):
            if os.path.exists(os.path.join(os.getcwd(), mp3_list[num])):
                mp3_name = f"{mp3_list[num].removesuffix('.mp3')}_{num + 1}.mp3"
                video.audio.write_audiofile(os.path.join(os.getcwd(), mp3_name))
                print(Fore.YELLOW + f'[+] Аудио из файла: "{mp3_name}" извлечено\n')
            else:
                video.audio.write_audiofile(os.path.join(os.getcwd(), mp3_list[num]))
                print(Fore.YELLOW + f'[+] Аудио из файла: "{mp3_list[num]}" извлечено\n')
        print(Fore.GREEN + "[+] Все видео файлы в директории обработаны. Аудио извлечено")
    else:
        print(Fore.RED + "\n[-] Файлов в директории не обнаружено")
        return


def zoom_in_out(path_file, value):
    try:
        float(value)
    except ValueError:
        print(Fore.RED + "[-] Введено неверное значение коэффициента")
        main()
        return

    suff = f".{os.path.split(path_file)[-1].split('.')[-1]}"
    vid_name = f"{os.path.split(path_file)[-1].removesuffix(suff)}_zoom{suff}"
    if os.path.isfile(path_file):
        if os.path.split(path_file)[-1].endswith(".mp4") or os.path.split(path_file)[-1].endswith(".avi"):
            print(Fore.CYAN + f"[+] Изменение громкости звука видео на: {value}")
            video = VideoFileClip(path_file)
            video.volumex(float(value)).write_videofile(os.path.join(os.path.split(path_file)[0], vid_name))
            print(Fore.GREEN + f"[+] Громкость изменена. Видео сохранено в папку: "
                               f'"{os.path.join(os.path.split(path_file)[0], vid_name)}"')
            main()
            return
        else:
            print(Fore.RED + "[-] Формат файла не поддерживается")
            main()
            return
    else:
        print(Fore.RED + "[-] Указанного файла не существует")
        main()
        return


def merge_video_audio(path_file_v, path_file_a):
    if not os.path.exists(path_file_v):
        print(Fore.RED + "[-] С видеофайлом непорядок")
        main()
        return

    if not os.path.exists(path_file_a):
        print(Fore.RED + "[-] С аудиофайлом непорядок")
        main()
        return

    suff = f".{os.path.split(path_file_v)[-1].split('.')[-1]}"
    vid_name = f"{os.path.split(path_file_v)[-1].removesuffix(suff)}_aud{suff}"
    if path_file_v.endswith(".mp4") or path_file_v.endswith(".avi") and path_file_a.endswith(".mp3"):
        print(Fore.CYAN + "[+] Добавляю аудио к видео")
        videoclip = VideoFileClip(path_file_v)
        audioclip = AudioFileClip(path_file_a)

        videoclip.audio = audioclip
        videoclip.write_videofile(os.path.join(os.path.split(path_file_v)[0], vid_name))
        print(Fore.GREEN + f'[+] Аудио добавлено. Файл сохранен:'
                           f' "{os.path.join(os.path.split(path_file_v)[0], vid_name)}"')
        main()
        return
    else:
        print(Fore.RED + "[-] Неверный формат файлов")
        main()
        return


def extract_image_from_video(path_file):
    if os.path.exists(path_file):
        suff = f".{os.path.split(path_file)[-1].split('.')[-1]}"
        vid_name = f"{os.path.split(path_file)[-1].removesuffix(suff)}"
        if path_file.endswith(".mp4") or path_file.endswith(".avi"):
            print(Fore.CYAN + "[+] Сохранение кадров из видео")
            if not os.path.isdir(os.path.join(os.path.split(path_file)[0], vid_name)):
                os.mkdir(os.path.join(os.path.split(path_file)[0], vid_name))

            video = VideoFileClip(path_file)
            s_fps = (1 / video.fps) * 10
            for clip in arange(0, video.duration, s_fps):
                print(Fore.YELLOW + f"\r[+] Сохраняю: {clip}/{video.duration}", end="")
                video.save_frame(os.path.join(os.path.split(path_file)[0], vid_name, f"{vid_name}_{clip}.jpg"), clip)
            print(Fore.GREEN + f"\n[+] Кадры из видео сохранены в папку: "
                               f'"{os.path.join(os.path.split(path_file)[0], vid_name)}"')
            main()
            return
        else:
            print(Fore.RED + "[-] Неверное расширение файла")
            main()
            return
    else:
        print(Fore.RED + "[-] Указанного видео не существует")
        main()
        return


def clip_from_image(path_dir, name_clip, s_duration):
    try:
        dur = float(s_duration)
    except ValueError:
        print(Fore.RED + "[-] Неверное значение длительности кадра")
        main()
        return

    if os.path.exists(path_dir):
        print(Fore.CYAN + "[+] Создание видео из картинок")
        os.chdir(path_dir)
        images = list(filter(lambda img: img.endswith(".jpg"), os.listdir(path_dir)))
        clips = [ImageClip(im).set_duration(dur) for im in images]
        video_merge = concatenate_videoclips(clips, method="compose")
        video_merge.write_videofile(f"{name_clip}.mp4", fps=25)
        print(Fore.GREEN + f"[+] Видео создано и сохранено в папку: {path_dir}")
        main()
        return
    else:
        print(Fore.RED + "[-] Указанной директории не существует")
        main()
        return


def main():
    user_change = input(Fore.RESET + "\n[+] Выберите действие:\n   [1] Объединить видео\n   [2] Вырезать фрагмент\n   "
                                     "[3] Удалить аудиодорожку из видео\n   [4] Извлечь аудио\n   [5] Изменить "
                                     "громкость видео\n"
                                     "   [6] Добавить аудио к видео\n   [7] Извлечь кадры из видео\n   "
                                     "[8] Создать клип из картинок\n   [9] Выход\n   >>> ")
    if user_change == "1":
        merge_video_clip(input("\n[+] Введите путь к папке с файлами: "),
                         input("[+] Введите название для объединенного видео: "))
    elif user_change == "2":
        clip_video(input("\n[+] Введите путь к файлу видео: "), input("[+] Введите время начала фрагмента\n"
                                                                      "   - пример: 02:25\n   >>> "),
                   input("[+] Введите время окончания фрагмента\n"
                         "   - пример: 03:50\n   >>> "))
    elif user_change == "3":
        remove_audio_from_video(input("\n[+] Введите путь к файлу видео: "))
    elif user_change == "4":
        extract_mp3(input("\n[+] Введите путь к видео или, к папке с видео: "))
    elif user_change == "5":
        zoom_in_out(input("\n[+] Введите путь к файлу видео: "),
                    input("[+] Введите коэффициент для изменения громкости\n   "
                          "- Нормальная громкость: 1 (пример коэффициента: 0.5, 1.2)\n   >>> "))
    elif user_change == "6":
        merge_video_audio(input("\n[+] Введите путь к файлу видео: "), input("[+] Введите путь к файлу аудио: "))
    elif user_change == "7":
        extract_image_from_video(input("\n[+] Введите путь к файлу видео: "))
    elif user_change == "8":
        clip_from_image(input("\n[+] Введите путь к папке с картинками: "), input("[+] Введите название клипа: "),
                        input("[+] Введите продолжительность показа кадра (прим.: 0.1 или 1): "))
    elif user_change == "9":
        exit(0)
    else:
        print(Fore.RED + "\n[-] Неопознанный выбор. Повторите снова")
        main()


if __name__ == "__main__":
    main()
