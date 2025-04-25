# 🛡️ Multi-Mode Honeypot System

This is a modular, Python honeypot system that emulates HTTP and SSH servers to capture and record unauthorized access attempts. It supports flexible configuration through command-line arguments and can be utilized to observe attacker activity for cybersecurity research or defense.

## 📁 Project Structure

- `argparse_file.py`: Primary entry script that parses command-line arguments and initiates either the HTTP or SSH honeypot.
- `http_honeypot.py`: A Flask web honeypot that mimics a login page and records credential attempts.
- `SSH_honeypot.py`: An emulated SSH server with Paramiko that records login attempts and user command history.

## 🚀 Features

- ✅ Dual-mode: Select running an SSH or HTTP honeypot.
- ✅ Logging with rotation: Maintains logs in check with rotating file handlers.
- ✅ Emulated SSH shell: Reacts to simple commands such as `pwd`, `whoami`, `ls`, etc.
- ✅ Web login trap: Captures any entered credentials on a spoofed web page.
- ✅ Adjustable credentials through command line arguments.

## 🧪 Requirements

- Python 3.6+
- Flask
- Paramiko
