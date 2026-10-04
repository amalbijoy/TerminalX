"""
TerminalX - Enhanced Terminal Emulator
Version: X.1
"""

import os
import platform
import socket
import random
import string
import time
import subprocess
import json
import hashlib
from datetime import datetime
import sys
import shutil
import glob
import re
import threading
import getpass
import zipfile
import tarfile

# Constants and Configuration
DRIVE_PATHS = {
    'A': 'A:/',
    'B': 'B:/',
    'C': 'C:/',
    'D': 'D:/',
    'E': 'E:/',
    'F': 'F:/',
    'G': 'G:/',
    'H': 'H:/',
    'I': 'I:/',
    'J': 'J:/',
    'K': 'K:/',
    'L': 'L:/',
    'M': 'M:/',
    'N': 'N:/',
    'O': 'O:/',
    'P': 'P:/',
    'Q': 'Q:/',
    'R': 'R:/',
    'S': 'S:/',
    'T': 'T:/',
    'U': 'U:/',
    'V': 'V:/',
    'W': 'W:/',
    'X': 'X:/',
    'Y': 'Y:/',
    'Z': 'Z:/'
}

HOST_NAME = socket.gethostname()
HOST_IP = socket.gethostbyname(HOST_NAME)
# Fixed the CHARS string - removed the problematic quote
CHARS = string.ascii_letters + string.digits + '!@#$%^&*().,?~[]{}+=_-|:;"<>/'

COLOR_CODES = {
    'default': '\033[0m',
    'black': '\033[90m',
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'bright_red': '\033[1;31m',
    'bright_green': '\033[1;32m',
    'bright_blue': '\033[1;34m',
    'bright_yellow': '\033[1;33m',
    'bright_cyan': '\033[1;36m',
    'bright_magenta': '\033[1;35m'
}

# Comprehensive CMD-equivalent aliases
ALIASES = {
    'ls': 'dir',
    'cls': 'clear',
    'pwd': 'cd',
    'cat': 'type',
    'cp': 'copy',
    'mv': 'move',
    'rm': 'del',
    'rmdir': 'rd',
    'mkdir': 'md',
    'ps': 'tasklist',
    'kill': 'taskkill',
    'which': 'where',
    'find': 'findstr',
    'grep': 'findstr',
    'head': 'more',
    'tail': 'more',
    'touch': 'echo.',
    'exit': 'quit',
    'logout': 'quit',
    'shutdown': 'poweroff',
    'reboot': 'restart'
}

# Global variables
CURRENT_COLOR = COLOR_CODES['default']
CURRENT_DIR = os.getcwd()
COMMAND_HISTORY = []
ENVIRONMENT_VARS = dict(os.environ)

def show_banner():
    """Display TerminalX banner"""
    banner = f"""
{COLOR_CODES['bright_red']}
████████╗███████╗██████╗░███╗░░░███╗██╗███╗░░██╗░█████╗░██╗░░░░░██╗░░██╗
╚══██╔══╝██╔════╝██╔══██╗████╗░████║██║████╗░██║██╔══██╗██║░░░░░╚██╗██╔╝
░░░██║░░░█████╗░░██████╔╝██╔████╔██║██║██╔██╗██║███████║██║░░░░░░╚███╔╝░
░░░██║░░░██╔══╝░░██╔══██╗██║╚██╔╝██║██║██║╚████║██╔══██║██║░░░░░░██╔██╗░
░░░██║░░░███████╗██║░░██║██║░╚═╝░██║██║██║░╚███║██║░░██║███████╗██╔╝╚██╗
░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝╚═╝░░╚══╝╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝
{COLOR_CODES['default']}

{COLOR_CODES['bright_green']}TerminalX [Version X.1] - Terminal Environment{COLOR_CODES['default']}
{COLOR_CODES['yellow']}Type 'help' for commands.{COLOR_CODES['default']}
{COLOR_CODES['cyan']}Enhanced with 100+ commands for professional use.{COLOR_CODES['default']}
"""
    print(banner)

# ========== FILE AND DIRECTORY OPERATIONS ==========

def cmd_dir(args=""):
    """List directory contents (equivalent to Windows DIR command)"""
    if not args:
        path = CURRENT_DIR
    else:
        path = args.strip()
        if not os.path.exists(path):
            print(f"{COLOR_CODES['red']}The system cannot find the path specified.{COLOR_CODES['default']}")
            return

    try:
        print(f"{COLOR_CODES['cyan']} Directory of {path}{COLOR_CODES['default']}")
        print()

        items = os.listdir(path)
        total_files = 0
        total_dirs = 0
        total_size = 0

        for item in sorted(items):
            item_path = os.path.join(path, item)
            try:
                stat = os.stat(item_path)
                mod_time = datetime.fromtimestamp(stat.st_mtime).strftime("%m/%d/%Y  %I:%M %p")

                if os.path.isdir(item_path):
                    print(f"{mod_time}    {COLOR_CODES['blue']}<DIR>{COLOR_CODES['default']}          {item}")
                    total_dirs += 1
                else:
                    size = stat.st_size
                    print(f"{mod_time}        {size:>12,} {item}")
                    total_files += 1
                    total_size += size
            except:
                print(f"{'?' * 20}    {COLOR_CODES['red']}ERROR{COLOR_CODES['default']}         {item}")

        print(f"{COLOR_CODES['green']}{total_files:>15} File(s) {total_size:>15,} bytes{COLOR_CODES['default']}")
        print(f"{COLOR_CODES['green']}{total_dirs:>15} Dir(s){COLOR_CODES['default']}")

    except Exception as e:
        print(f"{COLOR_CODES['red']}Error: {e}{COLOR_CODES['default']}")

def cmd_cd(args=""):
    """Change directory (equivalent to Windows CD command)"""
    global CURRENT_DIR

    if not args:
        print(CURRENT_DIR)
        return

    path = args.strip()

    # Handle special cases
    if path == "..":
        path = os.path.dirname(CURRENT_DIR)
    elif path == "\\":
        path = "\\"
    elif path == "~":
        path = os.path.expanduser("~")
    elif len(path) == 2 and path[1] == ':':
        path += '\\'

    try:
        os.chdir(path)
        CURRENT_DIR = os.getcwd()
    except Exception as e:
        print(f"{COLOR_CODES['red']}The system cannot find the path specified.{COLOR_CODES['default']}")

def cmd_md(args=""):
    """Create directory (equivalent to Windows MD/MKDIR command)"""
    if not args:
        print(f"{COLOR_CODES['red']}The syntax of the command is incorrect.{COLOR_CODES['default']}")
        return

    try:
        os.makedirs(args.strip(), exist_ok=True)
        print(f"{COLOR_CODES['green']}Directory created successfully.{COLOR_CODES['default']}")
    except Exception as e:
        print(f"{COLOR_CODES['red']}Error: {e}{COLOR_CODES['default']}")

def cmd_rd(args=""):
    """Remove directory (equivalent to Windows RD/RMDIR command)"""
    if not args:
        print(f"{COLOR_CODES['red']}The syntax of the command is incorrect.{COLOR_CODES['default']}")
        return

    path = args.strip()
    if not os.path.exists(path):
        print(f"{COLOR_CODES['red']}The system cannot find the file specified.{COLOR_CODES['default']}")
        return

    try:
        if "/s" in args.lower():
            shutil.rmtree(path)
        else:
            os.rmdir(path)
        print(f"{COLOR_CODES['green']}Directory removed successfully.{COLOR_CODES['default']}")
    except Exception as e:
        print(f"{COLOR_CODES['red']}Error: {e}{COLOR_CODES['default']}")

def cmd_copy(args=""):
    """Copy files (equivalent to Windows COPY command)"""
    if not args:
        print(f"{COLOR_CODES['red']}The syntax of the command is incorrect.{COLOR_CODES['default']}")
        return

    parts = args.strip().split()
    if len(parts) < 2:
        print(f"{COLOR_CODES['red']}The syntax of the command is incorrect.{COLOR_CODES['default']}")
        return

    source, dest = parts[0], parts[1]

    try:
        if os.path.isfile(source):
            shutil.copy2(source, dest)
            print(f"{COLOR_CODES['green']}        1 file(s) copied.{COLOR_CODES['default']}")
        else:
            print(f"{COLOR_CODES['red']}The system cannot find the file specified.{COLOR_CODES['default']}")
    except Exception as e:
        print(f"{COLOR_CODES['red']}Error: {e}{COLOR_CODES['default']}")

def cmd_move(args=""):
    """Move files (equivalent to Windows MOVE command)"""
    if not args:
        print(f"{COLOR_CODES['red']}The syntax of the command is incorrect.{COLOR_CODES['default']}")
        return

    parts = args.strip().split()
    if len(parts) < 2:
        print(f"{COLOR_CODES['red']}The syntax of the command is incorrect.{COLOR_CODES['default']}")
        return

    source, dest = parts[0], parts[1]

    try:
        shutil.move(source, dest)
        print(f"{COLOR_CODES['green']}        1 file(s) moved.{COLOR_CODES['default']}")
    except Exception as e:
        print(f"{COLOR_CODES['red']}Error: {e}{COLOR_CODES['default']}")

def cmd_del(args=""):
    """Delete files (equivalent to Windows DEL command)"""
    if not args:
        print(f"{COLOR_CODES['red']}The syntax of the command is incorrect.{COLOR_CODES['default']}")
        return

    filename = args.strip()

    try:
        if '*' in filename or '?' in filename:
            files = glob.glob(filename)
            if not files:
                print(f"{COLOR_CODES['red']}Could Not Find {filename}{COLOR_CODES['default']}")
                return
            for file in files:
                os.remove(file)
            print(f"{COLOR_CODES['green']}{len(files)} file(s) deleted.{COLOR_CODES['default']}")
        else:
            if os.path.exists(filename):
                os.remove(filename)
                print(f"{COLOR_CODES['green']}1 file deleted.{COLOR_CODES['default']}")
            else:
                print(f"{COLOR_CODES['red']}Could Not Find: {filename}{COLOR_CODES['default']}")
    except Exception as e:
        print(f"{COLOR_CODES['red']}Error: {e}{COLOR_CODES['default']}")

def cmd_ren(args=""):
    """Rename files (equivalent to Windows REN command)"""
    if not args:
        print(f"{COLOR_CODES['red']}The syntax of the command is incorrect.{COLOR_CODES['default']}")
        return

    parts = args.strip().split()
    if len(parts) < 2:
        print(f"{COLOR_CODES['red']}The syntax of the command is incorrect.{COLOR_CODES['default']}")
        return

    old_name, new_name = parts[0], parts[1]

    try:
        os.rename(old_name, new_name)
        print(f"{COLOR_CODES['green']}File renamed successfully.{COLOR_CODES['default']}")
    except Exception as e:
        print(f"{COLOR_CODES['red']}Error: {e}{COLOR_CODES['default']}")

def cmd_type(args=""):
    """Display file contents (equivalent to Windows TYPE command)"""
    if not args:
        print(f"{COLOR_CODES['red']}The syntax of the command is incorrect.{COLOR_CODES['default']}")
        return

    filename = args.strip()

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            print(f.read())
    except FileNotFoundError:
        print(f"{COLOR_CODES['red']}The system cannot find the file specified.{COLOR_CODES['default']}")
    except Exception as e:
        print(f"{COLOR_CODES['red']}Error: {e}{COLOR_CODES['default']}")

def cmd_more(args=""):
    """Display file contents page by page (equivalent to Windows MORE command)"""
    if not args:
        print(f"{COLOR_CODES['red']}The syntax of the command is incorrect.{COLOR_CODES['default']}")
        return

    filename = args.strip()

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        lines_per_page = 20
        for i in range(0, len(lines), lines_per_page):
            for line in lines[i:i+lines_per_page]:
                print(line, end='')

            if i + lines_per_page < len(lines):
                input(f"{COLOR_CODES['yellow']}-- More --{COLOR_CODES['default']}")

    except FileNotFoundError:
        print(f"{COLOR_CODES['red']}The system cannot find the file specified.{COLOR_CODES['default']}")
    except Exception as e:
        print(f"{COLOR_CODES['red']}Error: {e}{COLOR_CODES['default']}")

# ========== SYSTEM INFORMATION COMMANDS ==========

def cmd_ver(args=""):
    """Display version information (equivalent to Windows VER command)"""
    print(f"{COLOR_CODES['green']}TerminalX [Version X.1.0]{COLOR_CODES['default']}")
    print(f"{COLOR_CODES['cyan']}Based on: {platform.system()} {platform.release()}{COLOR_CODES['default']}")

def cmd_systeminfo(args=""):
    """Display comprehensive system information"""
    print(f"{COLOR_CODES['cyan']}System Information{COLOR_CODES['default']}")
    print("=" * 50)
    print(f"Host Name:                 {HOST_NAME}")
    print(f"OS Name:                   {platform.system()}")
    print(f"OS Version:                {platform.release()}")
    print(f"OS Manufacturer:           {platform.version()}")
    print(f"System Manufacturer:       {platform.machine()}")
    print(f"System Type:               {platform.architecture()[0]}")
    print(f"Processor:                 {platform.processor()}")
    print(f"Python Version:            {platform.python_version()}")
    print(f"Current User:              {getpass.getuser()}")

    # Memory information (if psutil is available)
    try:
        import psutil
        memory = psutil.virtual_memory()
        print(f"Total Physical Memory:     {memory.total // (1024**3):,} GB")
        print(f"Available Physical Memory: {memory.available // (1024**3):,} GB")
    except ImportError:
        print("Total Physical Memory:     N/A (psutil not installed.)")

def cmd_hostname(args=""):
    """Display computer name"""
    print(HOST_NAME)

def cmd_ipconfig(args=""):
    """Display network configuration"""
    print(f"{COLOR_CODES['cyan']}Windows IP Configuration{COLOR_CODES['default']}")
    print()
    print(f"Host Name . . . . . . . . . . . . : {HOST_NAME}")
    print(f"Primary Dns Suffix  . . . . . . . :")
    print(f"Node Type . . . . . . . . . . . . : Hybrid")
    print(f"IP Routing Enabled. . . . . . . . : No")
    print(f"WINS Proxy Enabled. . . . . . . . : No")
    print()
    print(f"Ethernet adapter Local Area Connection:")
    print()
    print(f"   Connection-specific DNS Suffix  . :")
    print(f"   Description . . . . . . . . . . . : Network Adapter")
    print(f"   Physical Address. . . . . . . . . : XX-XX-XX-XX-XX-XX")
    print(f"   DHCP Enabled. . . . . . . . . . . : Yes")
    print(f"   IP Address. . . . . . . . . . . . : {HOST_IP}")

def cmd_whoami(args=""):
    """Display current username"""
    try:
        username = getpass.getuser()
        domain = os.environ.get('USERDOMAIN', HOST_NAME)
        print(f"{domain}\\{username}")
    except:
        print("Unknown User")

def cmd_date(args=""):
    """Display or set system date"""
    if args:
        print(f"{COLOR_CODES['red']}Setting date is not supported in TerminalX.{COLOR_CODES['default']}")
        return

    current_date = datetime.now()
    print(f"The current date is: {current_date.strftime('%a %m/%d/%Y')}")

def cmd_time(args=""):
    """Display or set system time"""
    if args:
        print(f"{COLOR_CODES['red']}Setting time is not supported in TerminalX.{COLOR_CODES['default']}")
        return

    current_time = datetime.now()
    print(f"The current time is: {current_time.strftime('%I:%M:%S.%f')[:-4]} {current_time.strftime('%p')}")

# ========== PROCESS MANAGEMENT COMMANDS ==========

def _run_external_command(command_line):
    """Run an external executable without invoking a shell."""
    try:
        parts = shlex.split(command_line, posix=(os.name != "nt"))
    except ValueError as exc:
        print(f"{COLOR_CODES['red']}Invalid command syntax: {exc}{COLOR_CODES['default']}")
        return
    if not parts:
        return
    try:
        subprocess.run(parts, shell=False, check=False)
    except FileNotFoundError:
        print(f"{COLOR_CODES['red']}'{parts[0]}' is not recognized as an executable command.{COLOR_CODES['default']}")
    except OSError as exc:
        print(f"{COLOR_CODES['red']}Command failed: {exc}{COLOR_CODES['default']}")

def cmd_tasklist(args=""):
    """Display running processes (equivalent to Windows TASKLIST command)"""
    try:
        import psutil
        print(f"{COLOR_CODES['cyan']}{'Image Name':<25} {'PID':<8} {'Memory Usage':<15}{COLOR_CODES['default']}")
        print("=" * 50)
        
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                name = proc.info['name']
                pid = proc.info['pid']
                memory = proc.info['memory_info'].rss // (1024 * 1024)  # Convert to MB
                print(f"{name:<25} {pid:<8} {memory:>10} MB")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
    except ImportError:
        print(f"{COLOR_CODES['yellow']}Process listing requires psutil module.{COLOR_CODES['default']}")
        print("Alternative: Using basic process listing...")
        if platform.system().lower() == 'windows':
            subprocess.run(['tasklist'], shell=False, check=False)
        else:
            subprocess.run(['ps', 'aux'], shell=False, check=False)

def cmd_taskkill(args=""):
    """Terminate processes (equivalent to Windows TASKKILL command)"""
    if not args:
        print(f"{COLOR_CODES['red']}ERROR: Invalid argument/option - ''.{COLOR_CODES['default']}")
        print('Type "TASKKILL /?" for usage.')
        return
    
    if "/?" in args:
        print("TASKKILL [/F] [/PID processid | /IM imagename]")
        print("")
        print("Description:")
        print("    This tool is used to terminate tasks by process id (PID) or image name.")
        print("")
        print("Parameter List:")
        print("    /PID    processid   Specifies the PID of the process to be terminated.")
        print("    /IM     imagename   Specifies the image name of the process to be terminated.")
        print("    /F                  Specifies to forcefully terminate the process(es).")
        return
    
    try:
        import psutil
        
        if "/PID" in args:
            parts = args.split()
            pid_index = parts.index("/PID") + 1
            if pid_index < len(parts):
                pid = int(parts[pid_index])
                process = psutil.Process(pid)
                process.terminate()
                print(f"{COLOR_CODES['green']}SUCCESS: Sent termination signal to the process with PID. {pid}.{COLOR_CODES['default']}")
            else:
                print(f"{COLOR_CODES['red']}ERROR: Invalid argument/option - '/PID'.{COLOR_CODES['default']}")
        
        elif "/IM" in args:
            parts = args.split()
            im_index = parts.index("/IM") + 1
            if im_index < len(parts):
                image_name = parts[im_index]
                killed = False
                for proc in psutil.process_iter(['pid', 'name']):
                    if proc.info['name'].lower() == image_name.lower():
                        proc.terminate()
                        killed = True
                        print(f"{COLOR_CODES['green']}SUCCESS: Sent termination signal to the process \"{image_name}\" with PID. {proc.pid}.{COLOR_CODES['default']}")
                
                if not killed:
                    print(f"{COLOR_CODES['red']}ERROR: The process \"{image_name}\" not found.{COLOR_CODES['default']}")
            else:
                print(f"{COLOR_CODES['red']}ERROR: Invalid argument/option - '/IM'.{COLOR_CODES['default']}")
                
    except ImportError:
        print(f"{COLOR_CODES['yellow']}Process management requires psutil module.{COLOR_CODES['default']}")
    except Exception as e:
        print(f"{COLOR_CODES['red']}ERROR: {e}{COLOR_CODES['default']}")

# ========== NETWORK COMMANDS ==========

def cmd_ping(args=""):
    """Ping a host (equivalent to Windows PING command)"""
    if not args:
        print(f"{COLOR_CODES['red']}Bad parameter: {args}{COLOR_CODES['default']}")
        return

    host = args.strip().split()[0]  # Get first argument as host
    
    # Validate host to prevent command injection
    # Allow only alphanumeric, dots, hyphens, and colons (for IPv6)
    if not re.match(r'^[a-zA-Z0-9.\-:]+$', host):
        print(f"{COLOR_CODES['red']}Invalid host format.{COLOR_CODES['default']}")
        return

    # Default ping behavior
    count = 4
    if "-t" in args:
        count = 999999  # Continuous ping
    elif "-n" in args:
        parts = args.split()
        try:
            n_index = parts.index("-n") + 1
            if n_index < len(parts):
                count = int(parts[n_index])
        except (ValueError, IndexError):
            pass

    print(f"Pinging {host} with 32 bytes of data:")
    print()

    param = '-n' if platform.system().lower() == 'windows' else '-c'
    cmd = ['ping', param, str(count), host]

    try:
        subprocess.run(cmd, shell=False, check=False)
    except Exception as e:
        print(f"{COLOR_CODES['red']}Ping request could not find host. {host}.{COLOR_CODES['default']}")

def cmd_netstat(args=""):
    """Display network statistics (equivalent to Windows NETSTAT command)"""
    try:
        if platform.system().lower() == 'windows':
            subprocess.run(['netstat', *shlex.split(args, posix=(os.name != 'nt'))], shell=False, check=False)
        else:
            # Linux/Mac equivalent
            if args:
                subprocess.run(['netstat', *shlex.split(args, posix=(os.name != 'nt'))], shell=False, check=False)
            else:
                subprocess.run(['netstat', '-tuln'], shell=False, check=False)
    except Exception as e:
        print(f"{COLOR_CODES['red']}Error: {e}{COLOR_CODES['default']}")

def cmd_nslookup(args=""):
    """DNS lookup utility (equivalent to Windows NSLOOKUP command)"""
    if not args:
        print("Default Server:  dns.google")
        print("Address:  8.8.8.8")
        print()
        print("> ", end="")
        host = input().strip()
        if not host:
            return
    else:
        host = args.strip()

    try:
        import socket
        ip_address = socket.gethostbyname(host)
        print(f"Server:  dns.google")
        print(f"Address:  8.8.8.8")
        print()
        print(f"Non-authoritative answer:")
        print(f"Name:    {host}")
        print(f"Address:  {ip_address}")
    except Exception as e:
        print(f"{COLOR_CODES['red']}DNS request timed out.{COLOR_CODES['default']}")

# ========== TEXT PROCESSING COMMANDS ==========

def cmd_findstr(args=""):
    """Search for strings in files (equivalent to Windows FINDSTR command)"""
    if not args:
        print("FINDSTR: Bad command line.")
        return

    parts = args.strip().split('"')
    if len(parts) >= 3:  # "search string" filename format
        search_string = parts[1]
        filename = parts[2].strip()
    else:
        # Space-separated format
        parts = args.strip().split()
        if len(parts) < 2:
            print("FINDSTR: Bad command line.")
            return
        search_string = parts[0]
        filename = parts[1]

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            line_number = 0
            found = False
            for line in f:
                line_number += 1
                if search_string.lower() in line.lower():
                    print(f"{filename}:{line_number}:{line.rstrip()}")
                    found = True

            if not found:
                print("FINDSTR: No matches found.")

    except FileNotFoundError:
        print(f"FINDSTR: Cannot open: {filename}")
    except Exception as e:
        print(f"FINDSTR: Error - {e}")

def cmd_sort(args=""):
    """Sort text file contents (equivalent to Windows SORT command)"""
    if not args:
        print("The syntax of the command is incorrect.")
        return

    filename = args.strip()

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        sorted_lines = sorted(lines)
        for line in sorted_lines:
            print(line, end='')

    except FileNotFoundError:
        print("The system cannot find the file specified.")
    except Exception as e:
        print(f"Error: {e}")

def cmd_fc(args=""):
    """Compare files (equivalent to Windows FC command)"""
    parts = args.strip().split()
    if len(parts) < 2:
        print("The syntax of the command is incorrect.")
        return

    file1, file2 = parts[0], parts[1]

    try:
        with open(file1, 'r', encoding='utf-8') as f1:
            lines1 = f1.readlines()
        with open(file2, 'r', encoding='utf-8') as f2:
            lines2 = f2.readlines()

        print(f"Comparing files {file1} and {file2}")

        if lines1 == lines2:
            print("FC: no differences encountered.")
        else:
            max_lines = max(len(lines1), len(lines2))
            for i in range(max_lines):
                line1 = lines1[i] if i < len(lines1) else ""
                line2 = lines2[i] if i < len(lines2) else ""

                if line1 != line2:
                    print(f"***** {file1}")
                    print(f"{i+1:5}: {line1.rstrip()}")
                    print(f"***** {file2}")
                    print(f"{i+1:5}: {line2.rstrip()}")
                    print("*****")

    except FileNotFoundError as e:
        print("The system cannot find the file specified.")
    except Exception as e:
        print(f"Error: {e}")

# ========== SYSTEM UTILITIES ==========

def cmd_tree(args=""):
    """Display directory tree structure (equivalent to Windows TREE command)"""
    path = args.strip() if args else CURRENT_DIR

    if not os.path.exists(path):
        print("Invalid path - No such file or directory.")
        return

    print(f"Folder PATH listing for volume.")
    print(f"Volume serial number is XXXX-XXXX.")
    print(path)

    def print_tree(directory, prefix=""):
        try:
            items = sorted(os.listdir(directory))
            dirs = [item for item in items if os.path.isdir(os.path.join(directory, item))]
            files = [item for item in items if os.path.isfile(os.path.join(directory, item))]

            # Print directories first
            for i, dirname in enumerate(dirs):
                is_last_dir = (i == len(dirs) - 1) and len(files) == 0
                current_prefix = "└───" if is_last_dir else "├───"
                print(f"{prefix}{current_prefix}{dirname}")

                next_prefix = prefix + ("    " if is_last_dir else "│   ")
                print_tree(os.path.join(directory, dirname), next_prefix)

            # Then print files
            for i, filename in enumerate(files):
                is_last = i == len(files) - 1
                current_prefix = "└───" if is_last else "├───"
                print(f"{prefix}{current_prefix}{filename}")

        except PermissionError:
            print(f"{prefix}[Access Denied]")

    print_tree(path)

def cmd_attrib(args=""):
    """Display or change file attributes (equivalent to Windows ATTRIB command)"""
    if not args:
        # Display all files in current directory with attributes
        try:
            for item in os.listdir(CURRENT_DIR):
                item_path = os.path.join(CURRENT_DIR, item)
                attrs = ""

                if os.path.isdir(item_path):
                    attrs += "D"
                if os.access(item_path, os.R_OK):
                    attrs += "R" if not os.access(item_path, os.W_OK) else ""
                if item.startswith('.'):
                    attrs += "H"

                attrs = attrs.ljust(10)
                print(f"{attrs} {item_path}")

        except Exception as e:
            print(f"Error: {e}")
    else:
        filename = args.strip()
        if os.path.exists(filename):
            print(f"     {filename}")
        else:
            print("File not Found")

def cmd_diskpart():
    """Disk partitioning utility simulation"""
    print(f"{COLOR_CODES['yellow']}Microsoft DiskPart version X.1{COLOR_CODES['default']}")
    print()
    print("Copyright (C) Microsoft Corporation.")
    print("On computer: " + HOST_NAME)
    print()
    print(f"{COLOR_CODES['red']}WARNING: DiskPart functionality is limited in TerminalX.{COLOR_CODES['default']}")
    print("Type 'help' for DiskPart commands or 'exit' to return to TerminalX.")

    while True:
        command = input("DISKPART> ").strip().lower()

        if command == 'exit':
            break
        elif command == 'help':
            print("Available commands: list disk, list volume, exit")
        elif command == 'list disk':
            print("  Disk ###  Status         Size     Free     Dyn  Gpt")
            print("  --------  -------------  -------  -------  ---  ---")
            print("  Disk 0    Online          500 GB      0 B        *")
        elif command == 'list volume':
            print("  Volume ###  Ltr  Label        Fs     Type        Size     Status     Info")
            print("  ----------  ---  -----------  -----  ----------  -------  ---------  --------")
            print("  Volume 0     C   System       NTFS   Partition    500 GB  Healthy    Boot")
        else:
            print(f"Unknown command: {command}")

# ========== ENVIRONMENT AND REGISTRY ==========

def cmd_set(args=""):
    """Display or set environment variables (equivalent to Windows SET command)"""
    if not args:
        # Display all environment variables
        for key, value in sorted(ENVIRONMENT_VARS.items()):
            print(f"{key}={value}")
    else:
        if "=" in args:
            # Set variable
            key, value = args.split("=", 1)
            ENVIRONMENT_VARS[key.strip()] = value.strip()
            print(f"{COLOR_CODES['green']}Variable set: {key}={value}{COLOR_CODES['default']}")
        else:
            # Display specific variable
            key = args.strip()
            if key in ENVIRONMENT_VARS:
                print(f"{key}={ENVIRONMENT_VARS[key]}")
            else:
                print(f"Environment variable {key} not defined.")

def cmd_path(args=""):
    """Display or set the PATH variable"""
    if args:
        ENVIRONMENT_VARS['PATH'] = args.strip()
        print(f"{COLOR_CODES['green']}PATH updated{COLOR_CODES['default']}")
    else:
        print(f"PATH={ENVIRONMENT_VARS.get('PATH', '')}")

def cmd_echo(args=""):
    """Display message (equivalent to Windows ECHO command)"""
    if not args:
        echo_state = ENVIRONMENT_VARS.get('ECHO', 'ON')
        print(f"ECHO is {echo_state}.")
    elif args.strip().upper() in ['ON', 'OFF']:
        ENVIRONMENT_VARS['ECHO'] = args.strip().upper()
    else:
        print(args)

# ========== ARCHIVE AND COMPRESSION ==========

def cmd_compact(args=""):
    """Display or alter file compression (simulation)"""
    if not args:
        print(f"Compression is not supported for: {CURRENT_DIR}")
    else:
        filename = args.strip()
        if os.path.exists(filename):
            print(f"Compressing: {filename}...")
            print(f"1 files within 1 directories were processed.")
        else:
            print("File not found.")

# ========== SECURITY COMMANDS ==========

def cmd_cipher(args=""):
    """Encryption tool simulation"""
    print("Cipher command simulation.")
    if "/w" in args:
        print("Writing random data to unused disk space...")
        time.sleep(2)
        print("Data overwrite is complete.")
    else:
        print("Use cipher /w to securely delete unused disk space")

# ========== ADDITIONAL UTILITY COMMANDS ==========

def cmd_where(args=""):
    """Locate executable files (equivalent to Windows WHERE command)"""
    if not args:
        print("WHERE: Missing operand.")
        return

    command = args.strip()

    # Check current directory first
    if os.path.isfile(os.path.join(CURRENT_DIR, command)):
        print(os.path.join(CURRENT_DIR, command))
        return

    # Check PATH directories
    path_dirs = ENVIRONMENT_VARS.get('PATH', '').split(os.pathsep)
    found = False

    for directory in path_dirs:
        if directory:
            for ext in ['', '.exe', '.com', '.bat', '.cmd']:
                full_path = os.path.join(directory, command + ext)
                if os.path.isfile(full_path):
                    print(full_path)
                    found = True

    if not found:
        print(f"INFO: Could not find: '{command}'.")

def cmd_timeout(args=""):
    """Timeout utility (equivalent to Windows TIMEOUT command)"""
    if not args:
        print("The syntax of the command is incorrect.")
        return

    try:
        timeout_value = int(args.strip())
        print(f"Waiting for {timeout_value} seconds, press a key to continue ...")
        time.sleep(timeout_value)
        print()
    except ValueError:
        print("The syntax of the command is incorrect.")

def cmd_title(args=""):
    """Set window title (equivalent to Windows TITLE command)"""
    if args:
        print(f"{COLOR_CODES['cyan']}Window title set to: {args.strip()}{COLOR_CODES['default']}")
        # Note: Actual window title change would require additional terminal escape sequences
    else:
        print("Sets the window title for a command prompt window.")

def cmd_color(args=""):
    """Change terminal colors (equivalent to Windows COLOR command)"""
    if not args:
        print("Sets the default console foreground and background colors.")
        print("COLOR [attr]")
        print("  attr        Specifies color attribute of console output.")
        print()
        print("Color attributes are specified by TWO hex digits -- the first")
        print("corresponds to the background; the second the foreground.")
        return

    color_map = {
        '0': 'black', '1': 'blue', '2': 'green', '3': 'cyan',
        '4': 'red', '5': 'magenta', '6': 'yellow', '7': 'white',
        '8': 'bright_black', '9': 'bright_blue', 'A': 'bright_green',
        'B': 'bright_cyan', 'C': 'bright_red', 'D': 'bright_magenta',
        'E': 'bright_yellow', 'F': 'bright_white'
    }

    color_code = args.strip().upper()
    if len(color_code) == 2:
        bg_color = color_map.get(color_code[0], 'default')
        fg_color = color_map.get(color_code[1], 'default')
        print(f"{COLOR_CODES['green']}Color changed to background: {bg_color}, foreground: {fg_color}{COLOR_CODES['default']}")
    else:
        print("Invalid color specification.")

# ========== HELP SYSTEM ==========

def cmd_help(args=""):
    """Display help information (equivalent to Windows HELP command)"""
    if args:
        command = args.strip().lower()
        # Show help for specific command
        help_texts = {
            'dir': 'Displays a list of files and subdirectories in a directory.',
            'cd': 'Displays the name of or changes the current directory.',
            'copy': 'Copies one or more files to another location.',
            'del': 'Deletes one or more files.',
            'md': 'Creates a directory.',
            'rd': 'Removes a directory.',
            'type': 'Displays the contents of a text file.',
            'ping': 'Sends ICMP echo requests to network hosts.',
            'ipconfig': 'Displays network interface configuration.',
            'netstat': 'Displays network connections and statistics.',
            'tasklist': 'Displays currently running processes.',
            'taskkill': 'Terminates running processes.',
            'set': 'Displays, sets, or removes environment variables.',
            'echo': 'Displays messages or toggles command echoing.',
            'findstr': 'Searches for strings in files.',
            'sort': 'Sorts input and writes results to output.',
            'tree': 'Displays directory structure graphically.',
            'attrib': 'Displays or changes file attributes.',
            'where': 'Displays the location of executable files.',
            'timeout': 'Pauses the command processor for specified seconds.',
            'title': 'Sets the window title.',
            'color': 'Sets default console foreground and background colors.',
            'ver': 'Displays the version number.',
            'date': 'Displays or sets the date.',
            'time': 'Displays or sets the system time.',
            'hostname': 'Displays the computer name.',
            'whoami': 'Displays the current username.'
        }

        help_text = help_texts.get(command, f"No help available for: '{command}'")
        print(help_text)
        return

    # Main help menu
    help_text = f"""
{COLOR_CODES['bright_cyan']}=== TerminalX Help ==={COLOR_CODES['default']}

{COLOR_CODES['yellow']}File & Directory Commands:{COLOR_CODES['default']}
  DIR [drive:][path][filename] - List directory contents
  CD [/D] [drive:][path]       - Change directory
  MD [drive:]path              - Create directory
  RD [/S] [drive:]path         - Remove directory
  COPY source destination      - Copy files
  MOVE source destination      - Move/rename files
  DEL [/P] [/S] filename       - Delete files
  REN oldname newname          - Rename files
  TYPE filename                - Display file contents
  MORE filename                - Display file contents page by page
  TREE [drive:][path] [/F]     - Display directory tree
  ATTRIB [filename]            - Display/change file attributes

{COLOR_CODES['yellow']}System Information:{COLOR_CODES['default']}
  VER                          - Display version information
  SYSTEMINFO                   - Display comprehensive system info
  HOSTNAME                     - Display computer name
  WHOAMI                       - Display current username
  DATE                         - Display current date
  TIME                         - Display current time

{COLOR_CODES['yellow']}Network Commands:{COLOR_CODES['default']}
  PING [-t] [-n count] host    - Send ICMP echo requests
  IPCONFIG [/all]              - Display network configuration
  NETSTAT [-a] [-n] [-r]       - Display network statistics
  NSLOOKUP [hostname]          - DNS lookup utility

{COLOR_CODES['yellow']}Process Management:{COLOR_CODES['default']}
  TASKLIST [/FI filter]        - Display running processes
  TASKKILL /PID pid | /IM name - Terminate processes

{COLOR_CODES['yellow']}Text Processing:{COLOR_CODES['default']}
  FINDSTR [/I] string filename - Search for strings in files
  SORT filename                - Sort file contents
  FC file1 file2               - Compare files

{COLOR_CODES['yellow']}Environment:{COLOR_CODES['default']}
  SET [variable=[string]]      - Display/set environment variables
  PATH [drive:]path            - Display/set search path
  ECHO [message]               - Display message or toggle echo

{COLOR_CODES['yellow']}System Utilities:{COLOR_CODES['default']}
  WHERE filename               - Locate executable files
  TIMEOUT /T seconds           - Pause for specified time
  TITLE [string]               - Set window title
  COLOR [attr]                 - Set console colors
  CLS                          - Clear screen

{COLOR_CODES['yellow']}Archives & Security:{COLOR_CODES['default']}
  COMPACT [filename]           - Display/alter file compression
  CIPHER [/w]                  - Encryption utility

{COLOR_CODES['yellow']}Additional Commands:{COLOR_CODES['default']}
  HELP [command]               - Display help information
  EXIT                         - Exit TerminalX
  QUIT                         - Exit TerminalX

{COLOR_CODES['green']}Note: Most standard CMD commands are supported. For detailed help on any command,
type: HELP [command name]{COLOR_CODES['default']}
"""
    print(help_text)

def cmd_clear():
    """Clear the screen (equivalent to Windows CLS command)"""
    os.system('cls' if os.name == 'nt' else 'clear')

def cmd_quit(args=""):
    """Exit TerminalX"""
    print(f"{COLOR_CODES['green']}Thank you for using TerminalX!{COLOR_CODES['default']}")
    time.sleep(0.5)
    return True

# ========== MAIN TERMINAL LOOP ==========

def main():
    """Main terminal loop"""
    global COMMAND_HISTORY, CURRENT_DIR
    cmd_clear()
    show_banner()

    # Command dictionary for faster lookup
    commands = {
        'dir': cmd_dir,
        'cd': cmd_cd,
        'md': cmd_md,
        'mkdir': cmd_md,
        'rd': cmd_rd,
        'rmdir': cmd_rd,
        'copy': cmd_copy,
        'move': cmd_move,
        'del': cmd_del,
        'delete': cmd_del,
        'ren': cmd_ren,
        'rename': cmd_ren,
        'type': cmd_type,
        'more': cmd_more,
        'ver': cmd_ver,
        'version': cmd_ver,
        'systeminfo': cmd_systeminfo,
        'hostname': cmd_hostname,
        'ipconfig': cmd_ipconfig,
        'whoami': cmd_whoami,
        'date': cmd_date,
        'time': cmd_time,
        'tasklist': cmd_tasklist,
        'taskkill': cmd_taskkill,
        'ping': cmd_ping,
        'netstat': cmd_netstat,
        'nslookup': cmd_nslookup,
        'findstr': cmd_findstr,
        'find': cmd_findstr,
        'sort': cmd_sort,
        'fc': cmd_fc,
        'tree': cmd_tree,
        'attrib': cmd_attrib,
        'compact': cmd_compact,
        'cipher': cmd_cipher,
        'set': cmd_set,
        'path': cmd_path,
        'echo': cmd_echo,
        'where': cmd_where,
        'timeout': cmd_timeout,
        'title': cmd_title,
        'color': cmd_color,
        'help': cmd_help,
        'cls': cmd_clear,
        'clear': cmd_clear,
        'exit': cmd_quit,
        'quit': cmd_quit,
        'diskpart': cmd_diskpart
    }

    while True:
        try:
            # Update current directory in case it changed
            CURRENT_DIR = os.getcwd()

            # Create CMD-style prompt
            drive = os.path.splitdrive(CURRENT_DIR)[0]
            if not drive:
                drive = "~"

            prompt = f"{CURRENT_COLOR}{drive}{CURRENT_DIR[len(drive):]}>{COLOR_CODES['default']}"

            user_input = input(prompt).strip()

            if not user_input:
                continue

            # Add to history
            COMMAND_HISTORY.append(user_input)

            # Parse command and arguments
            parts = user_input.split(' ', 1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""

            # Handle aliases
            command = ALIASES.get(command, command)

            # Execute command
            if command in commands:
                result = commands[command](args)
                if result is True:  # Exit command
                    break
            else:
                # Try to execute as system command
                try:
                    _run_external_command(user_input)
                except Exception as e:
                    print(f"{COLOR_CODES['red']}'{command}' is not recognized as an internal or external command,")
                    print(f"operable program or batch file.{COLOR_CODES['default']}")

        except KeyboardInterrupt:
            print(f"^C")
            continue
        except EOFError:
            print(f"\n{COLOR_CODES['green']}Thank you for using TerminalX!{COLOR_CODES['default']}")
            break
        except Exception as e:
            print(f"{COLOR_CODES['red']}Error: {e}{COLOR_CODES['default']}")

if __name__ == '__main__':
    main()

