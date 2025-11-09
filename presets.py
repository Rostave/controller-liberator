"""
Group: Keyboard Liberators
This module provides a minimal PresetManager class for storing and applying button/controls presets """

from typing import Dict, Any, Optional, List, Callable
from context import Context
import json
import os


class Preset:
    """
    Preference preset data class.
    """

    def __init__(self):
        self.name: str = "default"
        """Preset name"""

        self.visual = {
            "show_fps": True,  # Show in-screen real-time FPS text
            "show_cam_capture": True,  # Show camera capture window
            "show_pose_estimation": True,  # Visualize pose estimation landmarks
            "fist_center_circle_radius": -1,
            "fist_center_circle_color": "#ffffff",
        }

        self.mapping = {
            "max_pitch": 0.4,
            "fist_thresh": 0.06,
            "behind_thresh": 0.08,
            "joystick_deadzone": 0.02,
            "steering_scale": 1.0,
        }
        """Mapping settings"""


class PresetManager:
    """
    PresetManager class for storing and applying button/controls presets
    """
    presets_path = "Presets"

    def __init__(self, ctx: Context):
        self.ctx = ctx
        ctx.preset_mgr = self
        self._presets: Dict[str, Preset] = {}  # name -> Preset

        self.active_preset_name: str = "default"
        self.active_preset: Optional[Preset, None] = Preset()

        self.register_preset("default", Preset())  # add default preset
        self.__on_update_preset: List[Callable] = list()  # delegates on applying a new preset

    def register_preset(self, name: str, data: Preset) -> None:
        """Register a new preset.
        :param name: Preset name
        :param data: Preset data
        """
        self._presets[name] = data

    def unregister_preset(self, name: str) -> None:
        """Remove a registered preset (if it exists)."""
        if name in self._presets:
            del self._presets[name]
            if self.active_preset == self._presets.get(name):
                self.active_preset = None

    def register_preset_update_callback(self, callback: Callable) -> None:
        """Register a callback to be called when a new preset is applied."""
        self.__on_update_preset.append(callback)

    def unregister_preset_update_callback(self, callback: Callable) -> None:
        """Unregister a callback."""
        if callback in self.__on_update_preset:
            self.__on_update_preset.remove(callback)

    def list_presets(self):
        """Return a list of registered preset names."""
        return list(self._presets.keys())

    def get_preset(self, name: str) -> Preset:
        """Return preset data for the specified name or None."""
        return self._presets.get(name)

    def apply_preset(self, name: str) -> bool:
        """Apply the preset with the specified name (if it exists), return whether successful."""
        if name in self._presets:
            self.active_preset_name = name
            self.active_preset = self._presets[name]
            print(f"Applied preset: {name}")
            for callback in self.__on_update_preset:
                callback(self.active_preset)
            return True

        print(f"Not found preset named {name}")
        return False

    def load_presets(self) -> None:
        """Load presets from local file."""
        presets = os.listdir(self.presets_path)
        preset_count: int = 0
        for preset_file in presets:
            if not preset_file.endswith(".json"):
                continue
            self.__load_from_file(os.path.join(self.presets_path, preset_file))
            preset_count += 1
        print(f"Loaded {preset_count} presets")

        default_preset_name = self.ctx.cfg.get("Preferences", "default_preset", fallback="default")
        if not self.get_preset(default_preset_name):
            print(f"Invalid preset, using default")
            default_preset_name = "default"
        self.apply_preset(default_preset_name)

    def __load_from_file(self, path: str) -> None:
        """Load preset from file."""
        with open(path, 'r') as f:
            file = f.read()
            f.close()

        raw = json.loads(file)
        preset = Preset()
        preset.visual = raw.get("visual", preset.visual)
        preset.mapping = raw.get("mapping", preset.mapping)

        preset.name = os.path.splitext(os.path.basename(path))[0]
        self.register_preset(preset.name, preset)

    def save_active_to_file(self) -> None:
        if self.active_preset_name == "default":
            return
        self.save_active_to_new_file(self.active_preset_name)

    def save_active_to_new_file(self, name: str) -> None:
        """Save current preset to file."""
        preset: Preset = self.active_preset
        if preset is None:
            return

        # Adding settings
        config = dict()
        config['visual'] = preset.visual
        config['mapping'] = preset.mapping
        path = os.path.join(self.presets_path, f"{name}.json")

        with open(path, 'w') as configfile:
            json.dump(config, configfile, indent=2)

        print(f"Saved preset: {name}")


if __name__ == "__main__":
    from context import Context
    import configparser
    config = configparser.ConfigParser()
    config.read("sysconfig.ini")
    ctx = Context(config)
    mgr = PresetManager(ctx)
    mgr.load_presets()
    print(mgr.list_presets())
    mgr.active_preset.visual["show_fps"] = False
    mgr.save_active_to_new_file("test")
    del config, ctx, mgr


