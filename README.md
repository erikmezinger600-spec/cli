# PCSploit — Post-Exploitation C2 Framework

**PCSploit** is a modular, cross-platform post-exploitation and remote access 
framework built in Python for authorized penetration testing. It provides a 
command & control (C2) server with encrypted communications, dynamic module 
loading, and a lightweight client that runs in-memory.

> **⚠️ AUTHORIZED USE ONLY**  
> This tool is for authorized security assessments and educational purposes.  
> The user confirms they have explicit written permission to test the target systems.

## Features

- **AES-256 encrypted C2 channel** — Diffie-Hellman key exchange + AES-GCM encryption
- **Modular architecture** — drop Python modules into `modules/` and clients load them remotely
- **Persistent SQLite database** — sessions survive disconnects
- **Interactive reverse shell** — full terminal access on the target
- **Post-exploitation modules** — keylogger, screenshot, packet sniffer, port scanner, privilege escalation, persistence, file grabber, webcam, process control
- **Multi-platform** — Windows, Linux, macOS
- **Payload stagers** — minimal staged payloads that download the full client in memory
- **In-memory execution** — no disk writes on the target

## Installation

```bash
git clone https://github.com/yourusername/PCSploit.git
cd PCSploit
pip install -r requirements.txt
