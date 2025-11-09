"""
Group: Keyboard Liberators
Main entrance of the program. The code initializes components and maintain the main loop.
The loop handles the process flow from image capturing to landmark detection to pose-control mapping.
"""

import pygame
import cv2
import configparser

from context import Context
from presets import PresetManager
from detector import Detector
from gamepad import VGamepad
from mapping import PoseControlMapper
from gui import GUI

# Load configuration
config = configparser.ConfigParser()
config.read('sysconfig.ini')

# Initialize components
ctx = Context(config)
preset_mgr = PresetManager(ctx)
camera = cv2.VideoCapture(0)
FPS = camera.get(cv2.CAP_PROP_FPS)
RESO = camera.get(cv2.CAP_PROP_FRAME_WIDTH), camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
gui = GUI(ctx, RESO, FPS)
detector = Detector(ctx)
mapper = PoseControlMapper(ctx)
gamepad = VGamepad(True)
ctx.gamepad = gamepad
preset_mgr.load_presets()

# Main loop
while True:
    if not gui.handle_events():
        print("Quit application")
        break

    gui.clock_tick()
    gui.clear_color()

    ret, frame = camera.read()
    if not ret:
        print("Cannot capture frame")
        break

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Turn BGR image format to RGB
    landmarks, visual_pose = detector.get_landmarks(frame)  # Detect pose landmarks

    if landmarks:
        gui.render_np_frame(visual_pose)  # Draw webcam capture
        feats = mapper.extract_features(landmarks)  # Extract pose features
        gui.render_pose_features(feats)  # Draw pose features on GUI
        # gui.render_game_controls(feats)  # Draw game controls based on extracted features
        # mapper.trigger_control()  # Map pose features to gamepad controls
    else:
        gui.render_np_frame(frame)

    gui.update_display()  # Update GUI display

# Release resources
camera.release()
gamepad.release()
detector.close()
gui.quit()
ctx.close()
