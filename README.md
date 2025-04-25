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

## 🔐 Secutiry Notes
This honeypot must be run in a test environment for research or monitoring alone. Never deploy it on production systems or without authorization.

## 🧪 Requirements

- Python 3.6+
- Flask
- Paramiko

## Install dependencies with:

```bash
pip install flask paramiko
```

## ⚙️ User Manual
- Clone the repository:
```bash
git clone https://github.com/esha3027/Honeypot1.git
```
- Activate virtual environment:
```bash
python3 -m venv I-venv
source I-venv/bin/activate
```
- Run the files:
  i) Run via command line:
  ```bash
  python argparse_file.py -a <IP_ADDRESS> -p <PORT> --ssh OR --http [-u USERNAME] [-pw PASSWORD]
  ```
  ii) Run SSH Honeypot:
  ```bash
  python argparse_file.py -a 0.0.0.0 -p 2222 --ssh -u [username] -pw [password]
  ```
  iii) Run HTTP Honeypot:
  ```bash
  python argparse_file.py -a 0.0.0.0 -p 8080 --http -u admin -pw password
  ```

## 📓 Log Files
- audits.log: SSH Login Attempts
- cmdaudits.log: Commands execute within the simulated SSH shell.
- http_audits.log: HTTP login attempts.

## 🧰 Future Work
- Implement support for concurrent multi-protocol monitoring using threading or multiprocessing.
- Implement geo-IP lookup for advanced logging.
- Implement alert system (email/Slack/webhook) upon suspicious access.

## 🧑‍💻 Authors
- Esha Halder
- Trambak Konar
