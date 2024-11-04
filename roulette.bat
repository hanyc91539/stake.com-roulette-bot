@echo off
if not exist "C:\chrome\betplay" mkdir "C:\chrome\roulette"
echo.
set /p input=Do you have a browser open for Stake Roulette?(y/n):
if /I "%input%"=="n" (
    start chrome.exe -remote-debugging-port=9025 --user-data-dir="C:\chrome\roulette"
)
echo.
set /p input=Make sure you are logged in to the Stake.(y/n):
echo.
if /I "%input%"=="y" (
    python roulette.py
)
pause