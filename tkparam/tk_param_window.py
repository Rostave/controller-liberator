from threading import Thread
from .tk_param import *
import time
from typing import Callable, List
import warnings


class TKParamWindow:
    def __init__(self, title="tkparam window"):
        self._root = None
        self.title = title
        self._mainloop_thread = None
        self._is_running: bool = False

        self.params: dict = {}
        """Search by name"""

        self._start_thread_loop()
        time.sleep(0.1)  # leave time for tk to initialize

    @property
    def root(self):
        return self._root

    def _start_thread_loop(self):
        if self._is_running:
            return
        self._is_running = True
        self._mainloop_thread = Thread(target=self._creat_tk_thread)
        self._mainloop_thread.start()

    def _join_loop_thread(self):
        if self._mainloop_thread:
            return
        self._mainloop_thread.join()
        self._is_running = False

    def _creat_tk_thread(self):
        self._root = ttk.Window()
        self._root.title(self.title)
        self._root.mainloop()

    def _check_name_duplication(self, name):
        if self.params.get(name) is not None:
            raise ValueError(f"Already created parameter named: '{name}', name duplication not allowed")

    def quit(self):
        """
        quit the window and join the thread
        """
        self._root.quit()
        self._join_loop_thread()

    def scalar(self,
               param_name: str,
               default_value: float = None,
               range_min: float = None,
               range_max: float = None,
               is_int: bool = False,
               group: str = "") \
            -> TkScalar:
        """
        get a scalar parameter from the window
        :param param_name: parameter name
        :param default_value: default value
        :param range_min: minimum value
        :param range_max: maximum value
        :param is_int: is integer or float
        :param group: grouping hierarchy, leave empty for default; use '/' to separate hierarchy
        :return: the scalar parameter, using TkScalar.get() to get the value
        """
        self._check_name_duplication(param_name)
        data_type = TKDataType.INT if is_int else TKDataType.FLOAT
        param = TK_PARAM_SCALAR_MAP[data_type](self.root, param_name, data_type, default_value, range_min, range_max)
        self.params[param_name] = param
        return param

    def button_bool(self,
                    param_name: str,
                    default_value: bool = True,
                    on_change: Callable[[bool], None] = None,
                    group: str = "") \
            -> TkBoolBtn:
        """
        get a button parameter from the window
        :param param_name: parameter name
        :param default_value: default value
        :param on_change: callback function when the button is clicked
        :param group: grouping hierarchy, leave empty for default; use '/' to separate hierarchy
        :return: the button parameter, using TkBoolBtn.get() to get the value
        """
        self._check_name_duplication(param_name)
        data_type = TKDataType.BOOL
        param = TK_PARAM_SCALAR_MAP[data_type](self.root, param_name, default_value, on_change)
        self.params[param_name] = param
        return param

    def get_param_by_name(self, param_name: str, fallback=None):
        """
        get a created parameter by name
        :param param_name: parameter name given when created
        :param fallback: fallback value if not required name is not found
        :return: the created parameter instance
        """
        if param_name not in self.params:
            warnings.warn(f"parameter named '{param_name}' not found", stacklevel=2)
            return fallback
        return self.params.get(param_name)

    def dump_param_to_dict(self) -> dict:
        """
        dump all parameters
        :return: a dictionary containing all parameters and their values
        """
        ret = {}
        for param in self.params.values():
            ret[param.name] = param.get()
        return ret

    def load_param_from_dict(self, param_dict: dict):
        """
        load parameters from a dictionary, will create new parameters if not exist
        :param param_dict: dictionary containing parameters and their values
        """

        def check_type(value):
            return isinstance(value, (int, float, bool))

        for k, v in param_dict.items():
            if not check_type(v):
                warnings.warn(f"type '{type(v)}' of parameter '{k}' is not acceptable, skipped", stacklevel=2)
                continue

            if param := self.params.get(k):
                param.set(v)
            else:
                warnings.warn(f"parameter named '{k}' not found, skipped", stacklevel=2)
                continue
