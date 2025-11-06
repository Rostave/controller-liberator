"""
Group: Keyboard Liberators
"""

from context import Context
from time import time as tm
import pygame


class GUI:
    """
    Graphical user interface built using Pygame.
    """
    def __init__(self, ctx: Context):
        self.ctx: Context = ctx

        win_reso_x = int(ctx.cfg.get('window', "win_reso_x"))
        win_reso_y = int(ctx.cfg.get('window', "win_reso_y"))

        pygame.init()
        self.caption = ctx.cfg.get("window", "caption")
        pygame.display.set_caption(self.caption)
        self.fps = int(ctx.cfg.get('window', "win_fps"))
        self.win_resolution = (win_reso_x, win_reso_y)
        self.screen = pygame.display.set_mode(self.win_resolution)
        self.clock = pygame.time.Clock()

        self.show_caption_fps = ctx.cfg.getboolean('window', "show_caption_fps")
        self.delta_time: float = 0.0
        self.running_time: float = 0.0
        self._running_start_time: float = tm()
        self._fps_accum_target: int = ctx.cfg.getint('window', "smooth_fps_accum_frames")
        self._fps_accum_time: int = 0
        self._fps_accum_count: int = 0
        self._smoothed_fps: int = 0

    def clock_tick(self):
        """
        Update the clock and return the elapsed time in seconds.
        """
        self.running_time = tm() - self._running_start_time
        self.delta_time = self.clock.tick(self.fps) / 1000.0
        if self.show_caption_fps:
            self.__calc_smooth_fps()
            self.caption = f"{self.caption}  FPS: {self._smoothed_fps}"
            pygame.display.set_caption(self.caption)
        return self.delta_time

    def __calc_smooth_fps(self):
        """
        Calculate the smoothed FPS based on the accumulated FPS values.
        """
        print(1)
        self._fps_accum_count += 1
        self._fps_accum_time += self.delta_time
        if self._fps_accum_count >= self._fps_accum_target:
            self._smoothed_fps = round(self._fps_accum_count / self._fps_accum_time)
            pygame.display.set_caption(f"{self.caption}  FPS: {self._smoothed_fps}")
            self._fps_accum_count = 0
            self._fps_accum_time = 0.0

    def render_webcam_capture(self, frame):
        """
        Visualize the webcam capture to the screen.
        TODO: Visualize the webcam capture to the screen.
        """

    def render_pose_landmarks(self, landmarks):
        """
        Visualize the pose landmarks (links) to the screen.
        TODO: Given Mediapipe upper body pose landmarks, visualize the pose landmarks (links) to the screen.
        """
