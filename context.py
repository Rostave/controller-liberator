"""
Group: Keyboard Liberators
"""
from utils import check_os
if check_os() != "Darwin":
    from tkparam import TKParamWindow


class Context:
    """
    Application context storing component references.
    """
    def __init__(self, config):
        self.cfg = config  # configuration object reference
        self.detector = None  # pose detector instance
        self.gui = None  # GUI window reference
        self.preset_mgr = None  # GUI settings reference
        self.mapper = None  # pose-control mapper instance
        self.gamepad = None  # virtual gamepad reference
        if check_os() != "Darwin":
            self.tkparam = TKParamWindow(title="Keyboard Liberators Calibration")  # tkparam window reference
        else:
            self.tkparam = None

    @property
    def active_preset(self):
        return self.preset_mgr.active_preset

    def close(self):
        if self.tkparam:
            self.tkparam.quit()
