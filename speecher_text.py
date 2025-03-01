from gtts import gTTS
import simpleaudio as sa
import pygame
import os

tts = gTTS('глупая задница ниггер', lang='ru')
audio_file = 'hello.mp3'
tts.save(audio_file)



pygame.mixer.init()
pygame.mixer.music.load(audio_file)
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
    

os.remove(audio_file)