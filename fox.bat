@echo off
title FoxCod 2.6c Comfort
chcp 65001 >nul

if "%~1"=="" goto interaction

:run_file
cls
python "%~dp0engine.py" "%~1"
echo.
echo ------------------------------------------
echo √ Скрипт выполнен. Консоль активна.

:interaction
echo Введите f для запуска, q для выхода (автозакрытие через 5 минут)
:: Команда choice с таймаутом 300 секунд
choice /c fq /t 300 /d q /n /m "Ожидание выбора (f/q): "

if errorlevel 2 exit
if errorlevel 1 goto run_file

goto interaction
