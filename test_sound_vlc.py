import kivy
from kivy.core import core_register_libs
from kivy.core.audio import SoundLoader
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy_.audio import sound_vlc
import time

print('initializing sound libs')
kivy_options_mod = list(kivy.kivy_options['audio'])
kivy_options_mod.append('vlc')
kivy.kivy_options['audio'] = tuple(kivy_options_mod)
audio_libs = [('vlc', 'sound_vlc')]
libs_loaded = core_register_libs('audio', audio_libs, base='kivy_')
print('audio libs loaded: ', libs_loaded)

path_ = 'mp3\\Episode 1242.mp3'

# sound = sound_vlc.SoundVlc(source=path_)
sound = SoundLoader.load(path_)
sound.load()
# sound.play()

"""
for i in range(10):
    # print(sound.length, sound.get_pos())
    print(' is playing: ', sound._media_player.is_playing())
    sound.length
    sound.get_pos()
    time.sleep(1)

sound.stop()
sound.unload()
"""