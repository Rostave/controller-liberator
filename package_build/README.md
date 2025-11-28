# Controller Liberator Package

This directory contains the packaged version of the Controller Liberator project.
It allows you to install the project as a Python library and use it in your own code or run it directly.

## 1. Installation (安装)

First, navigate to this directory in your terminal:
首先，在终端中进入此目录：

```bash
cd package_build
```

Then install the package using pip:
然后使用 pip 安装此包：

```bash
pip install .
```

*(If you are developing, you can use `pip install -e .` for editable mode)*
*(如果你是开发者，可以使用 `pip install -e .` 进行可编辑安装)*

## 2. Usage (使用方法)

Once installed, you have two ways to use the controller:
安装完成后，你有两种方式使用控制器：

### Method A: Command Line (命令行方式)

You can run the controller directly from anywhere in your terminal:
你可以在终端的任何位置直接运行控制器：

```bash
keyboard-liberator
```

### Method B: Python Import (Python 导入方式)

You can import the package in your own Python script. This is useful if you want to integrate it into another application or just launch it programmatically.
你可以在自己的 Python 脚本中导入此包。如果你想将其集成到其他应用程序中，或者只是通过代码启动它，这非常有用。

Create a file named `start_game.py`:
创建一个名为 `start_game.py` 的文件：

```python
import keyboard_liberator

# Start the controller application
# 启动控制器应用程序
keyboard_liberator.run()
```

Then run your script:
然后运行你的脚本：

```bash
python start_game.py
```

## 3. Uninstall (卸载)

If you want to remove the package:
如果你想移除此包：

```bash
pip uninstall keyboard-liberator
```

## 4. Q&A: Can I use "pip install keyboard-liberator"? (常见问题)

**Q: Can I just type `pip install keyboard-liberator` instead of `pip install .`?**
**问：我能直接输 `pip install keyboard-liberator` 而不是 `pip install .` 吗？**

**A:**
- **Locally (本地)**: No. `pip install .` tells pip "install the package in the **current folder**".
  (不行。`.` 代表“当前文件夹”，这是告诉 pip 安装你电脑上这个位置的代码。)

- **Remotely (远程)**: Yes, BUT only if you publish it to PyPI.
  (可以，但前提是你必须把它发布到 Python 官方仓库 PyPI。)
  
  If you upload your package to [pypi.org](https://pypi.org/), then anyone in the world can type `pip install keyboard-liberator` to download and install it, just like `pip install numpy`.
  (如果你把它上传到 PyPI，全世界的人都可以通过这个命令安装它，就像安装 numpy 一样。)

## 5. License & Contributing (开源协议与贡献)

This project is open source and available under the MIT License.
本项目开源并遵循 MIT 协议。

Feel free to fork, modify, and distribute!
欢迎 Fork、修改和分发！

### Cross-Platform Support (跨平台支持)

- **Windows**: Uses `vgamepad` to emulate a virtual Xbox 360 controller.
- **macOS / Linux**: Uses `pynput` to map gestures to keyboard keys (WASD).
  *(Note: Virtual gamepad emulation is not natively supported on macOS/Linux in this version, so it falls back to keyboard mapping.)*

- **Windows**: 使用 `vgamepad` 模拟虚拟 Xbox 360 手柄。
- **macOS / Linux**: 使用 `pynput` 将手势映射为键盘按键 (WASD)。
  *(注：此版本在 macOS/Linux 上暂不支持原生虚拟手柄模拟，因此回退到键盘映射模式。)*


### How to share via GitHub (Private/Team) (如何通过 GitHub 分享给组员)

If your code is on GitHub (even in a private repository), your team members can install it directly from there without you sending files.
如果你的代码在 GitHub 上（即使是私有仓库），你的组员可以直接从那里安装，而不需要你发送文件。

**Requirement (前提):**
They must have access to the repository (e.g., they are added as collaborators).
他们必须有访问该仓库的权限（例如，他们已被添加为协作者）。

**Command (命令):**
Tell them to run this command (replace `YourUsername` and `YourRepo` with actual values):
告诉他们运行以下命令（请将 `YourUsername` 和 `YourRepo` 替换为实际值）：

```bash
pip install "git+https://github.com/YourUsername/YourRepo.git#subdirectory=package_build"
```

*Note: The `#subdirectory=package_build` part is important because your package is inside that folder, not at the root of the repository.*
*注意：`#subdirectory=package_build` 这部分很重要，因为你的包在这个子文件夹里，而不是在仓库的根目录。*

### How to share as a single file (如何像发安装包一样分享)

If you don't want to publish to the internet but want a file to send to friends:
如果你不想发布到网上，但想发一个文件给朋友安装：

1.  **Build the package (打包)**:
    ```bash
    pip install build
    python -m build
    ```
    This will create a `dist/` folder with a `.whl` file inside.
    (这会生成一个 `dist/` 文件夹，里面有一个 `.whl` 文件。)

2.  **Install the file (安装文件)**:
    Your friends can install that specific file:
    (你的朋友可以安装那个文件：)
    ```bash
    pip install keyboard_liberator-0.1.0-py3-none-any.whl
    ```
