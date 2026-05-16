@echo off
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$p='data\dashboard-v2\launcher\last-launch.json'; $u='http://127.0.0.1:8503/'; if(Test-Path $p){try{$j=Get-Content $p -Raw | ConvertFrom-Json; if($j.url){$u=$j.url}}catch{}}; Start-Process $u"
