from os import path, environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from PIL import Image

class GifPlayer:
    def __init__(self, win: pygame.Surface, pos: tuple, fp: str, resize: tuple = (0, 0)):
        """This loads in a Gif. if resize!=(0, 0) then this method also resizes the gif to the given coordinates"""
        self.win = win
        self.resize = resize
        self.pos = pos
        self.file_path = fp if fp != '' and path.isfile(fp) and fp.endswith('.gif') else None
        if self.file_path is None:
            raise FileNotFoundError

        self.frames = self.get_frames()
        self.num_frames = len(self.frames)
        self.frame_index = 0

    def get_frames(self):
        frames = []
        with Image.open(self.file_path) as curr_gif:
            for i in range(curr_gif.n_frames):
                curr_gif.seek(i)
                self.size = curr_gif.size
                if self.resize != (0, 0) and self.resize[0] >= 0 and self.resize[1] >= 0:
                    curr_gif.resize(self.resize)
                frames.append(pygame.image.fromstring(curr_gif.tobytes(), curr_gif.size, curr_gif.mode).convert())
        return frames

    def play(self, dt: float, playback_speed: float = 1):
        if int(self.frame_index) < self.num_frames:
            self.win.blit(self.frames[int(self.frame_index)], self.pos)
        else:
            self.frame_index = 0

        self.frame_index += 1 * (playback_speed * dt)
