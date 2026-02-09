# 1. 定义你刚才找到的那个真实物理路径
mv C:\\Users\\1\\Desktop\\脚本\\py_excel\\dist\\main.exe C:\\Users\\1\\Desktop\\脚本\\py_excel\\dist\\main2.exe
$SourceDir = "C:\Users\1\AppData\Roaming\uv\python\cpython-3.13.11-windows-x86_64-none"

# 2. 执行打包指令
# 我们把那个目录下所有的 .dll 全部塞进去，确保万无一失
uv run pyinstaller --noconsole --clean --onefile `
    --icon="ico.ico" `
    --add-binary "$SourceDir\*.dll;." `
    --add-data "assets/*.ttf;assets" `
    main.py