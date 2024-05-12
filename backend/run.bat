@echo off

REM 啟動虛擬環境
call myenv\Scripts\activate

REM 切換到 app 目錄
cd app

REM 使用 start 命令在背景中運行 Flask 應用程式
start python app.py

REM 打開網頁
start http://127.0.0.1:5000/