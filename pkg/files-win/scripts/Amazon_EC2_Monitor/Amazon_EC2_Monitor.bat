@ECHO OFF
set PHPDIR=..\..\apache\php
set INSTPATH="%MIBDIRS%\..\plugins\scripts\monitor-amazon-ec2\instances.txt"
set ADDPATH="%MIBDIRS%\..\plugins\scripts\monitor-amazon-ec2\addsystems.log"
set UPDATEPATH="%MIBDIRS%\..\plugins\scripts\monitor-amazon-ec2\updatehostcheck.log"
python ..\..\plugins\scripts\monitor-amazon-ec2\monitor-amazon-ec2.py
if errorlevel 0 ..\addsystem.exe %INSTPATH% >> %ADDPATH%
if errorlevel 0	"%PHPDIR%\php.exe" ..\..\plugins\scripts\monitor-amazon-ec2\monitor-amazon-ec2-update-host-check.php >> %UPDATEPATH%
exit /b %errorlevel%