from kivy.core.audio import SoundLoader
import time
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.clock import Clock
#from kivy.garden import iconfonts
import kivy.garden.iconfonts
from datetime import datetime
from os import path, mkdir
from kivy.utils import platform
from kivy.core import core_register_libs
from m_file import Ini2
# using ffpyplayer

kv_files = ['player.kv', 'file_selector.kv']
for each in kv_files:
    kv = path.join(path.dirname(path.realpath(__file__)), each)
    with open(kv, encoding='utf-8') as f:
        Builder.load_string(f.read())

kivy.garden.iconfonts.register('default_font', 'fa-solid-900.ttf', 'all_fontawesome.fontd')


class PlayerLayout(BoxLayout):
    # TODO: save progress
    pos_str = StringProperty()
    file_name = StringProperty()
    track_len = StringProperty()

    def __init__(self):
        super().__init__()
        self.file_name = ''
        self.sound = None
        self.scheduled_job1 = None
        self.scheduled_job2 = None

    def rev(self, step):
        print('rev, step :', -step)
        self.sound.seek(int(self.pos_int) - step)

    def ff(self, step):
        print('ff, step :', step)
        self.sound.seek(int(self.pos_int) + step)

    def _get_position(self, *args):
        self.pos_int = self.sound.get_pos()
        # time = datetime.utcfromtimestamp(self.pos_int)
        # print(time)
        # self.pos_str = f'{str(time.hour).zfill(2)}:{str(time.minute).zfill(2)}:{str(time.second).zfill(2)}'
        self.pos_str = self._time_int_to_str(self.pos_int)
        # print(self.pos_str)

    def _time_int_to_str(self, time_int):
        time = datetime.utcfromtimestamp(time_int)
        str_ = f'{str(time.hour).zfill(2)}:{str(time.minute).zfill(2)}:{str(time.second).zfill(2)}'
        return str_

    def play(self):
        # app1.sound.play()
        if self.sound is not None:
            self.sound.play()
            self.scheduled_job1 = Clock.schedule_interval(self._get_position, 1)
            self.scheduled_job2 = Clock.schedule_interval(self._save_progress, 10)
            self.track_len = self._time_int_to_str(self.sound.length)
            print(' track length: ', self.track_len)
        else:
            print('self sound is None')

    def pause(self):
        if self.sound is not None:
            if platform == 'android':
                # app1.sound.pause()
                self.sound.pause()
            else:
                # app1.sound.stop()
                self.sound.stop()

    def stop(self):
        # app1.sound.stop()
        # app1.sound.seek(0)
        self.sound.stop()
        self.sound.seek(0)
        Clock.unschedule(self.scheduled_job1)

    def _save_progress(self, *args):
        """
        saves last position to json file
        :return: True on success
        TODO
        """
        print('saving progress', self.pos_int)


class FileChooserPopup(BoxLayout):
    path_ = StringProperty('C:\\Users\\pkrssak\\AppData\\Roaming\\podcast_downloader')

    def select(self):
        print('selected: ', self.ids.filechooser.selection)
        self.parent.return_to_player(self.ids.filechooser.selection[0])


class MainLayout(FloatLayout):
    def __init__(self, config_dir):
        # TODO: send step config to PlayerLayout
        self.player_layout = PlayerLayout()
        self.file_select_layout = FileChooserPopup()
        super().__init__()

        self.config_dir = config_dir
        self.ini = Ini2()

        default_config = {
            'start_path': self.config_dir,
            'last_file': '',
            'small_step': 20,
            'big_step': 150,
        }

        loaded_config = self.ini.read(path.join(path.dirname(path.realpath(__name__)), 'config.json'))

        if not loaded_config:
            self.ini.write(path.join(self.config_dir, 'config.json'), default_config)
            print('writing default config into config.json')

        self.configuration = {**default_config, **loaded_config}

        if self.configuration['last_file'] != '':
            self.add_widget(self.player_layout)
        else:
            self.add_widget(self.file_select_layout)

    def open_file(self):
        print('MainLayout open_file called')
        self.remove_widget(self.player_layout)
        self.add_widget(self.file_select_layout)

    def return_to_player(self, file_name):
        print('Returning to player')
        self.player_layout.file_name = file_name
        self.player_layout.sound = SoundLoader.load(file_name)
        self.remove_widget(self.file_select_layout)
        self.add_widget(self.player_layout)


class AudioPlayer(App):
    def __init__(self):
        super().__init__()
        print('--------------')
        # overrides default kivy 1.10.1 user_data_dir creation strategy
        # which creates data_dir in /data folder
        if platform == 'android':
            data_dir = path.join('/sdcard', self.name)
        else:
            data_dir = self.user_data_dir
        if not path.exists(data_dir):
            print('creating dir: ', data_dir)
            mkdir(data_dir)
        print('using data_dir: ', data_dir)
        self.data_dir = data_dir
        self.main_layout = MainLayout(self.data_dir)

        # hack for ffpyplayer audio provider - does not work well
        # audio_libs = [('ffpyplayer', 'audio_ffpyplayer')]
        # libs_loaded = core_register_libs('audio', audio_libs)
        # print('audio libs loaded: ', libs_loaded)

    def build(self):
        # file_name = 'Siddharta - Na soncu.mp3'
        # path_to_file = path.join(self.data_dir, file_name)
        # print('loading file: ', path_to_file)
        # self.sound = SoundLoader.load(path_to_file)
        # self.sound.play()
        # # self.main_layout = MainLayout(file_name)
        # Clock.schedule_interval(self.main_layout._get_position, 1)
        return self.main_layout


if __name__ == '__main__':
    app1 = AudioPlayer()
    app1.run()
