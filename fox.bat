@echo off
title FoxCod Interpreter
chcp 65001 >nul

:: Проверяем, перетащили ли файл на батник
if "%~1"=="" goto interaction

:run_file
cls
echo [Запуск %~nx1...]
python "%~dp0engine.py" "%~1"
echo.
echo ------------------------------------------
echo √ Скрипт выполнен. Консоль активна.
echo.

:interaction
echo Введите f для запуска %~nx1 или q для выхода
set /p choice=Выбор: 

if /i "%choice%"=="f" goto run_file
if /i "%choice%"=="q" exit
if /i "%choice%"=="й" goto run_file
if /i "%choice%"=="й" exit

:: Если ввели что-то другое, просто возвращаемся к выбору
goto interaction
