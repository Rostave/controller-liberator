"""keyboard_liberator package

This package exposes utility helpers from the project so they can be
imported as `import keyboard_liberator` or `from keyboard_liberator import utils`.
"""
from .utils import (
    L,
    avg,
    clamp01,
    dist_pow,
    set_window_topmost,
    set_window_transparency,
    key2pygame_mapping,
    fold_tkparam_win_on_close,
    save_preset_on_close,
    select_preset_json,
    check_os,
)
from .main import run

__all__ = [
    "L",
    "avg",
    "clamp01",
    "dist_pow",
    "set_window_topmost",
    "set_window_transparency",
    "key2pygame_mapping",
    "fold_tkparam_win_on_close",
    "save_preset_on_close",
    "select_preset_json",
    "check_os",
    "run",
]
