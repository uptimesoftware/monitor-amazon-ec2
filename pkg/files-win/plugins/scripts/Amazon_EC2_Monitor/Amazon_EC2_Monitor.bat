@ECHO OFF
set PHPDIR=..\..\..\apache\php\
set INSTANCES="%CD%\instances.txt"
python Amazon_EC2_Monitor.py
if errorlevel 0 ..\..\..\scripts\addsystem.exe %INSTANCES% >> addsystem.log
if errorlevel 0	"%PHPDIR%\php.exe" Amazon_EC2_Monitor_Update_Host_Check.php >> updatehostcheck.log
exit /b %errorlevel%