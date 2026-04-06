@echo off
:: Запускаем движок и передаем ему первый аргумент (имя .foxcod файла)
python "%~dp0engine.py" "%~dp0%1"
pause
