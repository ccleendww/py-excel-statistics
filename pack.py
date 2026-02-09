import os
import sys
import subprocess
from pathlib import Path

# 1. 自动定位真实的 Python DLL 路径
# 这里直接问 UV 真正的 Python 在哪
try:
    python_exe = subprocess.check_output(["uv", "python", "find", "3.13"], text=True).strip()
    python_bin_dir = str(Path(python_exe).parent)
    print(f"找到真实的 Python 目录: {python_bin_dir}")
except:
    print("错误：无法通过 UV 找到 Python 3.13，请确保已安装。")
    sys.exit(1)

# 2. 构造 PyInstaller 命令
# 我们手动把真实的 DLL 路径塞进去
cmd = [
    "uv", "run", "pyinstaller",
    "--noconsole",
    "--clean",
    "--onefile", # 或者 --onedir
    "--icon=ico.ico",
    f"--add-binary={python_bin_dir}/*.dll;.",  # 这里的路径现在是绝对路径，不会弄错
    "--add-data=assets/*.ttf;assets",
    "main.py"
]

print("正在执行打包命令...")
subprocess.run(cmd)