import speech_recognition as sr
from gtts import gTTS
import os
import threading
import pygame
import time
import glob

# Индексы для микрофона HyperX и вывода VB-Audio
MIC_DEVICE_INDEX = 2  # Индекс вашего микрофона (HyperX QuadCast S)
OUTPUT_DEVICE_INDEX = 28  # Индекс VB-Audio (CABLE Input)


# Функция для удаления старых записей
def delete_old_records():
    files = glob.glob("speech_*.mp3")
    for f in files:
        try:
            os.remove(f)
        except Exception as e:
            print(f"Не удалось удалить {f}: {e}")


# Функция для воспроизведения текста
def play_audio(filename):
    # Инициализация pygame для воспроизведения на устройстве по умолчанию
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue  # Ожидание завершения воспроизведения

    pygame.mixer.quit()  # Явное завершение работы микшера перед удалением файла
    os.remove(filename)  # Удаляем файл после завершения использования


def speak_text(text):
    # Удаление старых записей перед созданием новой
    delete_old_records()

    # Создаем уникальное имя файла на основе времени
    filename = f"speech_{int(time.time())}.mp3"

    # Переводим текст и озвучиваем на русском
    tts = gTTS(text=text, lang="ru")
    tts.save(filename)  # Сохраняем файл в текущей директории

    # Запуск воспроизведения в отдельном потоке
    thread = threading.Thread(target=play_audio, args=(filename,))
    thread.start()


def continuous_listen_and_talk():
    recognizer = sr.Recognizer()
    with sr.Microphone(device_index=MIC_DEVICE_INDEX) as source:
        print("Настройка шумоподавления...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Увеличено время для шумоподавления
        print("Начинаю слушать...")

        while True:
            try:
                print("Слушаю...")
                # Распознаем речь на русском языке
                audio = recognizer.listen(source, timeout=0, phrase_time_limit=3)
                print("Обрабатываю...")
                text = recognizer.recognize_google(audio, language="ru-RU")  # Русский язык для распознавания
                print(f"Вы сказали: {text}")

                # Запуск озвучивания на русском языке в отдельном потоке
                thread = threading.Thread(target=speak_text, args=(text,))
                thread.start()

            except sr.UnknownValueError:
                print("Не удалось распознать речь, повторите...")
            except sr.RequestError as e:
                print(f"Ошибка сервиса распознавания речи; {e}")
            except sr.WaitTimeoutError:
                print("Микрофон молчит, продолжаю слушать...")


if __name__ == "__main__":
    continuous_listen_and_talk()
