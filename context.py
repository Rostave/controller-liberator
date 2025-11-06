"""
Group: Keyboard Liberators
"""


class Context:
    """
    Application context storing component references.
    """
    def __init__(self):
        self.cfg = None  # configuration object reference
        self.gui = None  # GUI window reference
        self.tkparam = None  # tkparam window reference
        self.gamepad = None  # virtual gamepad reference
