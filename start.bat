taskkill /F /IM python.exe>nul 2>&1
if errorlevel 1 (echo Python not found.) else (echo Python is killed.)
taskkill /F /IM pythonw.exe>nul 2>&1
if errorlevel 1 (echo Python not found.) else (echo Python is killed.)

python run.py