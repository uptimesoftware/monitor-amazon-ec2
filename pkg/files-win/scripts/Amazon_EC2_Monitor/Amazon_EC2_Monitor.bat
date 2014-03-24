@ECHO OFF
set PHPDIR=..\..\apache\php\
set INSTANCES="%CD%\instances.txt"
python ..\..\plugins\scripts\monitor-amazon-ec2\monitor-amazon-ec2.py
if errorlevel 0 ..\addsystem.exe %INSTANCES% >> addsystem.log
if errorlevel 0	"%PHPDIR%\php.exe" ..\..\plugins\scripts\monitor-amazon-ec2\monitor-amazon-ec2-update-host-check.php >> updatehostcheck.log
exit /b %errorlevel%