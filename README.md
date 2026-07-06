# ImageViewerPlusPlus
Advanced image viewer I made awhile back that supports [27 image formats across 30 file extensions](#supported-formats), the app is built using CustomTKinter for the UI 
The program is quite simple in structure its 1 source code file 
keep in mind its not a fully complete app I made it for fun and I probably won't update it 

if you don't want to install Python (and the Pip Packages) you can head over the [Releases](https://github.com/TeeDot69/ImageViewerPlusPlus/releases) page and download the precompiled Windows Executable I made, if you're on Linux or macOS you're out of luck because I don't regularly use Linux nor do I own a mac and I can't be arsed to load up a Linux VM or WSL and set it up to compile it once when that only takes maybe 2½ Minutes 
<p>
<img width="1034" height="762" alt="Screenshot 2026-07-06 095312" src="https://github.com/user-attachments/assets/ffe41501-c851-4c9f-9aa8-84052ebaf496" />
</p>
<p>
 <img width="1036" height="762" alt="Screenshot 2026-07-06 095337" src="https://github.com/user-attachments/assets/b942f075-2396-4e26-9d6f-fa7a0aeb1d2a" />
 A screenshot of a png loaded into the program
</p>
<p>
 <img width="1036" height="773" alt="Screenshot 2026-07-06 095530" src="https://github.com/user-attachments/assets/c54e7d74-1d01-49b3-89e8-3ddbe58681b5" />
A screenshot of a jpg of a png loaded into the program
</p>

## Prerequisites
If you don't run it via the Windows Executable (or are on Linux/Mac) this it what you'll need Installed
 - Python
 - Custom Tkinter (aka CustomTk or CTK)
 - Pillow
 - Pillow-Heif
 - TKinter (this may already be included if not install this)

For Linux you may want to install python3-pip and python3-venv because last time I coded Python on Linux I felt like I was losing iq points


## Compiling (Optional)
You can also compile it using PyInstaller (or another tool like Auto Py to Exe), you do NOT have to compile it as Python is interpeted.
To compile with PyInstaller or Auto Py to Exe, First clone the repo to a local location on your device Extract the ZIP Archive 
run the following command (or paste into auto py to exe)
```pyinstaller --noconfirm --onefile --windowed  "path\to\script\imgview.py"```
it will then output to the `/output` folder in your operating system's executable format (Windows; .exe, Linux; ELF Executable, macOS; mac executable or .app)

## Supported formats
 - `.png`
 - `.jpg`
 - `.jpeg`
 - `.gif`
 - `.bmp`
 - `.tiff`
 - `.tif`
 - `.webp`
 - `.ico`
 - `.heic`
 - `.heif`
 - `.avif`
 - `.jp2`
 - `.jpx`
 - `.psd`
 - `.pcx`
 - `.tga`
 - `.exif`
 - `.wmf`
 - `.emf`
 - `.dib`
 - `.pbm`
 - `.pgm`
 - `.ppm`
 - `.pnm`
 - `.sgi`
 - `.im`
 - `.cur`
 - `.xbm`
 - `.xpm`

