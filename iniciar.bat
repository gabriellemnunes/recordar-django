@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe py -m venv .venv || goto erro
call .venv\Scripts\activate.bat
python -m pip install -r requirements.txt || goto erro
python manage.py makemigrations recordar || goto erro
python manage.py migrate || goto erro
python manage.py demo || goto erro
python manage.py test || goto erro
echo Abra http://127.0.0.1:8001/ quando o servidor iniciar.
python manage.py runserver 127.0.0.1:8001
pause
exit /b
:erro
echo Falha na configuracao. Confira a mensagem acima.
pause
exit /b 1
