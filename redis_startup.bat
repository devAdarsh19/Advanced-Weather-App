@echo off
start "" wsl.exe
timeout /t 10 /nobreak >nul
wsl redis-cli