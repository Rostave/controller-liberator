from tkparam import TKParamWindow
import time


if __name__ == '__main__':
    # 创建个tk窗口，窗口在线程中运行
    # create a tkinter window running in a thread
    window = TKParamWindow(title="example window")

    # 定义窗口中需要调整的参数
    # define parameters to be adjusted in the window
    float_param = window.scalar("float", default_value=1.0, range_min=-1.5, range_max=2.3)
    float_param2 = window.scalar("float2", default_value=2.2, range_min=-1.5, range_max=2.3)
    try:
        float_param_dup = window.scalar("float", default_value=2.0, range_min=-1.5, range_max=2.3)
    except ValueError as e:
        print(f"Got Duplicated name error: {e}")
    int_param = window.scalar("int", default_value=3.3, range_min=-10, range_max=10, is_int=True)
    bool_button = window.button_bool("btn", default_value=False, on_change=lambda status: print(f"Button clicked: status: {status}"))

    print(f"get parameter: {window.get_param_by_name('float')}")
    print(f"get parameter: {window.get_param_by_name('float1')}")
    print(f"get parameter: {window.get_param_by_name('float2')}")
    print(f"get parameter: {window.get_param_by_name('int')}")
    print(f"get parameter: {window.get_param_by_name('btn')}")

    print(f"All parameters: {window.dump_param_to_dict()}")
    input("Press Enter to load new value...")
    window.load_param_from_dict({"float": 1.2, "float1": 2, "float2": "0.1", "int": 3, "btn": True})
    print(f"All parameters: {window.dump_param_to_dict()}")

    input("Enter to quit")
    window.quit()
    print("Quit")
