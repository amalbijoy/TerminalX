# `TerminalX` 

**`TerminalX`** is an enhanced, cross-platform terminal emulator that brings Windows CMD functionality to any operating system while providing 100+ additional commands for professional system administration, development, and network operations.

## Features

### **100+ Commands Available**
- **File & Directory Operations**: `DIR`, `CD`, `COPY`, `MOVE`, `DEL`, `MD`, `RD`, `TYPE`, `MORE`, `TREE`, `ATTRIB`.
- **System Information**: `VER`, `SYSTEMINFO`, `HOSTNAME`, `WHOAMI`, `DATE`, `TIME`.
- **Network Tools**: `PING`, `IPCONFIG`, `NETSTAT`, `NSLOOKUP`, `PORTSCAN`.
- **Process Management**: `TASKLIST`, `TASKKILL` with full PID and image name support.
- **Text Processing**: `FINDSTR`, `SORT`, `FC` (file comparison).
- **Environment**: `SET`, `PATH`, `ECHO` with full variable management.
- **Utilities**: `WHERE`, `TIMEOUT`, `TITLE`, `COLOR`, `CALC`, `ENCODE`.

### **Enhanced User Experience**
- **Colorful Interface**: Beautiful ASCII banner and color-coded output.
- **Windows-Style Prompts**: Authentic `C:\>` style prompts with drive letters.
- **Cross-Platform Aliases**: Unix/Linux command support (`ls`, `cat`, `grep`, etc.).
- **Command History**: Track and recall previous commands.
- **Comprehensive Help**: Built-in help system with `HELP [command]`.

### **Professional Tools**
- **Network Diagnostics**: Built-in port scanner and network analysis.
- **Security Features**: Text encoding/decoding, password generation.
- **File Management**: Advanced file operations with error handling.
- **System Monitoring**: Process monitoring and system information gathering.

## Installation:

### Prerequisites:
- Python 3.6 or higher.
- Optional: `psutil` for advanced process management.

### Quick Install:
```bash
# Clone the repository.
git clone https://github.com/amalbijoy/TerminalX.git
cd TerminalX

# Install optional dependencies (recommended).
pip install psutil

# Run TerminalX
python TerminalX.py
```

### One-File Installation:
Simply download `TerminalX.py` and run:
```bash
python TerminalX.py
```

## Quick Start:

```bash
# Launch TerminalX
python TerminalX.py

# Basic commands:
C:\> dir                    # List directory contents.
C:\> cd Documents           # Change directory.
C:\> ping google.com        # Network connectivity test.
C:\> tasklist              # Show running processes.
C:\> help                  # Show all available commands.
```

## Command Reference:

### File Operations:
| Command            | Description             | Example                     |
| ------------------ | ----------------------- | --------------------------- |
| `DIR [path]`       | List directory contents | `dir C:\Users`              |
| `CD [path]`        | Change directory        | `cd Documents`              |
| `COPY source dest` | Copy files              | `copy file1.txt backup.txt` |
| `MOVE source dest` | Move/rename files       | `move old.txt new.txt`      |
| `DEL filename`     | Delete files            | `del unwanted.txt`          |
| `MD dirname`       | Create directory        | `md NewFolder`              |
| `RD dirname`       | Remove directory        | `rd OldFolder`              |
| `TYPE filename`    | Display file contents   | `type readme.txt`           |

### System Information:
| Command      | Description               | Example      |
| ------------ | ------------------------- | ------------ |
| `SYSTEMINFO` | Comprehensive system info | `systeminfo` |
| `HOSTNAME`   | Display computer name     | `hostname`   |
| `WHOAMI`     | Current user information  | `whoami`     |
| `DATE`       | Display current date      | `date`       |
| `TIME`       | Display current time      | `time`       |
| `VER`        | TerminalX version         | `ver`        |

### Network Tools:
| Command         | Description               | Example               |
| --------------- | ------------------------- | --------------------- |
| `PING host`     | Test network connectivity | `ping google.com`     |
| `IPCONFIG`      | Network configuration     | `ipconfig`            |
| `NETSTAT`       | Network statistics        | `netstat -a`          |
| `NSLOOKUP host` | DNS lookup                | `nslookup github.com` |
| `PORTSCAN`      | Port scanning utility     | `portscan`            |

### Process Management:
| Command             | Description            | Example                    |
| ------------------- | ---------------------- | -------------------------- |
| `TASKLIST`          | Show running processes | `tasklist`                 |
| `TASKKILL /PID id`  | Kill process by PID    | `taskkill /PID 1234`       |
| `TASKKILL /IM name` | Kill process by name   | `taskkill /IM notepad.exe` |

### Advanced Features:
| Command             | Description            | Example                   |
| ------------------- | ---------------------- | ------------------------- |
| `FINDSTR text file` | Search text in files   | `findstr "error" log.txt` |
| `TREE [path]`       | Display directory tree | `tree C:\Projects`        |
| `CALC`              | Built-in calculator    | `calc`                    |
| `ENCODE`            | Text encoding/decoding | `encode`                  |
| `COLOR attr`        | Change terminal colors | `color 0A`                |

## Cross-Platform Compatibility:

### Windows Users:
- **Native CMD replacement** with enhanced features.
- All standard Windows commands work as expected.
- Additional tools not available in standard CMD.

### Linux/Unix Users:
- **Familiar aliases**: Use `ls`, `cat`, `grep`, `ps` commands.
- Windows command learning environment.
- Cross-platform script compatibility.

### macOS Users:
- **Best of both worlds**: Unix familiarity with Windows compatibility.
- Perfect for mixed-environment development.
- Consistent command experience.

## System Requirements:

- **Operating System**: Windows, Linux, macOS.
- **Python**: 3.6 or higher.
- **Memory**: 50MB RAM minimum.
- **Storage**: 1MB disk space.
- **Optional**: `psutil` library for enhanced process management.

## Configuration

### Environment Variables:
TerminalX respects system environment variables and allows modification:
```bash
C:\> set PATH=C:\NewPath;%PATH%    # Modify PATH.
C:\> set MYVAR=MyValue             # Set custom variable.
C:\> set                           # View all variables.
```

### Color Customization:
```bash
C:\> color 0A        # Black background, light green text.
C:\> color 1F        # Blue background, white text.
C:\> color           # View color help.
```

## Troubleshooting:

### Common Issues:

**1. Process commands not working**
```bash
# Install psutil for full functionality.
pip install psutil
```

**2. Colors not displaying**
- Ensure your terminal supports ANSI color codes.
- Try different terminal emulators (Windows Terminal, iTerm2, etc.).

**3. Permission errors**
- Run with appropriate privileges for system operations.
- Some commands require administrator/root access.

### Getting Help:
```bash
C:\> help              # General help.
C:\> help dir          # Specific command help.
C:\> taskkill /?       # Windows-style help.
```

## Contributing:
1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/AmazingFeature`
3. **Commit changes**: `git commit -m 'Add AmazingFeature'`
4. **Push to branch**: `git push origin feature/AmazingFeature`
5. **Open a Pull Request**

## License:

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Use Cases

### System Administration:
- **Server Management**: Monitor processes, check system info, manage files.
- **Network Troubleshooting**: Ping hosts, check connections, scan ports.
- **Automated Scripts**: Consistent commands across platforms.

### Development:
- **Cross-Platform Development**: Same commands on Windows, Linux, Mac.
- **Build Scripts**: Reliable file operations and system interactions.
- **Environment Setup**: Manage paths and environment variables.

### Education:
- **Command Line Learning**: Safe environment to learn terminal commands.
- **Windows/Unix Bridge**: Learn both command paradigms.
- **System Administration Training**: Professional-grade tools.

## Why `TerminalX`?

### For Windows Users:
- **Enhanced CMD**: All CMD functionality plus 50+ additional commands.
- **Better Interface**: Colors, better error messages, comprehensive help.
- **Professional Tools**: Network scanning, advanced file operations.

### For Unix/Linux Users:
- **Windows Compatibility**: Learn Windows commands without switching OS.
- **Development Tool**: Test Windows-specific scripts and commands.
- **Educational**: Understand Windows system administration.

### For Everyone:
- **Cross-Platform**: One terminal that works everywhere.
- **Professional**: Real tools for real work.
- **Open Source**: Free, customizable, community-driven.

## Statistics:

- **100+** Commands available.
- **Cross-Platform** compatibility.
- **Professional-grade** system tools.
- **Active development** and community support.
---
