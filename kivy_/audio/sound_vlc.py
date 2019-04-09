from kivy.core.audio import Sound, SoundLoader
import vlc
import time
from datetime import datetime, timedelta
# from kivy.core import core_register_libs

# MediaPlayer = vlc.MediaPlayer()


class SoundVlc(Sound):
    @staticmethod
    def extensions():
        return ("mp3", "mp4", "aac", "3gp", "flac", "mkv", "wav", "ogg")

    def __init__(self, **kwargs):
        self._media_player = None
        self._length = 0  # in seconds
        self._position = 0
        super().__init__(**kwargs)

    def load(self):
        self.unload()
        self._media_player = vlc.MediaPlayer(self.filename)

    def unload(self):
        self.stop()
        self._media_player = None

    def play(self):
        if not self._media_player:
            return
        _is_playing = self._media_player.is_playing()
        _waiting_0 = datetime.utcnow()

        if _is_playing == 0:
            self._media_player.play()
        print('sound_vlc.play()')
        while (_is_playing == 0) and ((datetime.utcnow() - _waiting_0).total_seconds() < 4):
            _is_playing = self._media_player.is_playing()
            print(' sound.play, is playing: ', _is_playing, ' delay: ', datetime.utcnow() - _waiting_0)
            time.sleep(0.5)

        # now seek to saved progress (written by _read_progress),
        # because vlc can seek only when is_playing == 1
        self.length
        print('sound_vlc.play() ... seeking to: ', self._saved_progress)
        self.seek(self._saved_progress)

    def stop(self):
        print('sound_vlc.stop()')
        if not self._media_player:
            return
        self._media_player.stop()

    def seek(self, position):
        """
        seek to position
        :param position: in seconds
        :return:
        """
        print('sound_vlc.seek')
        try:
            self._media_player.set_position(position / self._length)
        except ZeroDivisionError:
            print('   _length == 0, skipping')

    def get_pos(self):
        if self.length == 0:
            self._get_length()
        self._position = self._media_player.get_position() * self._length
        print('sound_vlc position: ', self._position)
        return self._position

    def _get_length(self):
        if self._media_player:
            self._length = self._media_player.get_length() / 1000
            print('vlc media length: ', int(self._length))
            return self._length
        return super()._get_length()

    def pause(self):
        if not self._media_player:
            return
        self._media_player.pause()
        print('sound_vlc.pause()')


SoundLoader.register(SoundVlc)


if __name__ == '__main__':
    sound = SoundVlc()
    sound.load()
