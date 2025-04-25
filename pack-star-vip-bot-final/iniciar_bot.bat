@echo off
cd /d "%~dp0"
echo Ativando ambiente virtual...
python -m venv venv
call venv\Scripts\activate
echo Instalando dependências...
pip install -r requirements.txt
echo Iniciando o bot...
python bot.py
pause
