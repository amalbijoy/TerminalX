# TerminalX

> A Python terminal environment inspired by Windows CMD, with cross-platform aliases, built-in system tools, and a fallback path for external commands.

## What it is

TerminalX is a single-file terminal application that provides a collection of Windows-style commands and familiar Unix aliases from one prompt.

It is **not** a drop-in replacement for Windows CMD, Bash, or PowerShell. Some commands depend on the host operating system, installed utilities, and available permissions.

## Features

### Built-in command groups

- File and directory operations: `DIR`, `CD`, `MD`, `RD`, `COPY`, `MOVE`, `DEL`, `REN`, `TYPE`, `MORE`
- System information: `VER`, `SYSTEMINFO`, `HOSTNAME`, `WHOAMI`, `DATE`, `TIME`
- Network tools: `PING`, `IPCONFIG`, `NETSTAT`, `NSLOOKUP`
- Process management: `TASKLIST`, `TASKKILL`
- Text and comparison tools: `FINDSTR`, `SORT`, `FC`, `TREE`, `ATTRIB`
- Environment and shell utilities: `SET`, `PATH`, `ECHO`, `WHERE`, `TIMEOUT`, `TITLE`, `COLOR`, `CLS`
- Additional utilities: `COMPACT`, `CIPHER`, `HELP`, `EXIT`

### Unix-style aliases

Examples include:

```text
ls    → dir
cat   → type
cp    → copy
mv    → move
rm    → del
grep  → findstr
ps    → tasklist
kill  → taskkill
which → where
```

### External command fallback

Commands that are not built in are passed to the operating system through Python's subprocess API rather than a shell. This still means external programs execute with the privileges of the current user.

### Interface

- CMD-style prompt
- Colored terminal output
- Command history during the current process
- Built-in `HELP` system
- Cross-platform path and command handling where supported by the host OS

## Installation

### Requirements

- Python **3.8+**
- `psutil` for the packaged installation

Install the project in editable mode:

```bash
git clone https://github.com/amalbijoy/TerminalX.git
cd TerminalX
python -m pip install -e .
```

Then launch:

```bash
terminalx
```

### Run without installation

```bash
python TerminalX.py
```

A direct script launch can still work with reduced functionality when optional system information/process features are unavailable.

## Examples

```text
C:\> dir
C:\> cd Documents
C:\> ping example.com
C:\> tasklist
C:\> help tasklist
C:\> ls
C:\> grep "error" log.txt
```

## Testing

Basic automated tests are included for aliases, version output, directory listing, and help output.

```bash
python -m unittest discover -s tests
```

The repository also contains a GitHub Actions workflow for the Python checks.

## Platform notes

TerminalX contains platform-specific behavior for commands such as process inspection, network configuration, console colors, and screen clearing. Results therefore vary between Windows, Linux, and macOS.

Argument parsing is intentionally lightweight and is not a full shell parser, so advanced quoting, pipelines, redirection, and shell scripting are outside the current scope.

## Safety

TerminalX includes commands that can modify files, terminate processes, and execute external programs. Use it with the same care you would use with the underlying operating system tools. It is not a sandbox.

## License

GPL-3.0-only. See [LICENSE](LICENSE).
