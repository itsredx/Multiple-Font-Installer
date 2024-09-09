import os
import platform
import shutil
import subprocess
import ctypes

# Define font directory for Ubuntu (Linux)
UBUNTU_FONT_DIR = os.path.expanduser('~/.local/share/fonts')

def is_admin():
    """Check if the script is running with admin privileges (Windows)"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def install_fonts_in_ubuntu(font_dir):
    """Install fonts in Ubuntu"""
    if not os.path.exists(UBUNTU_FONT_DIR):
        os.makedirs(UBUNTU_FONT_DIR)

    for font_file in os.listdir(font_dir):
        if font_file.endswith(('.ttf', '.otf')):
            full_font_path = os.path.join(font_dir, font_file)
            print(f'Installing {font_file} in Ubuntu...')
            shutil.copy(full_font_path, UBUNTU_FONT_DIR)

    # Update the font cache
    subprocess.run(['fc-cache', '-f', '-v'], check=True)
    print('Fonts successfully installed and cache updated in Ubuntu!')

def install_fonts_in_windows(font_dir):
    """Install fonts in Windows"""
    # Define Windows font directory dynamically
    WINDOWS_FONT_DIR = os.path.join(os.environ['WINDIR'], 'Fonts')

    if not is_admin():
        print("This script needs to be run as administrator on Windows.")
        return

    for font_file in os.listdir(font_dir):
        if font_file.endswith(('.ttf', '.otf')):
            full_font_path = os.path.join(font_dir, font_file)
            print(f'Installing {font_file} in Windows...')
            shutil.copy(full_font_path, WINDOWS_FONT_DIR)

            # Register font in Windows Registry
            font_name = os.path.basename(full_font_path)
            reg_key = f"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Fonts"
            subprocess.run([
                'reg', 'add', reg_key, '/v', font_name, '/t', 'REG_SZ', '/d', font_name, '/f'
            ], check=True)

    print('Fonts successfully installed in Windows!')

def install_fonts(font_dir):
    """Detect OS and install fonts accordingly"""
    current_os = platform.system()

    if current_os == 'Linux':
        install_fonts_in_ubuntu(font_dir)
    elif current_os == 'Windows':
        install_fonts_in_windows(font_dir)
    else:
        print(f'Unsupported OS: {current_os}')

if __name__ == '__main__':
    # Define your font directory here
    font_dir = '/home/red-x/Downloads/FONTS/Fonts'

    if not os.path.exists(font_dir):
        print(f"The directory {font_dir} does not exist.")
    else:
        install_fonts(font_dir)

