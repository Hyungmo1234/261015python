@echo off
setlocal EnableExtensions
REM Daily study note publisher — Agent 불필요. Windows 작업 스케줄러에서 호출.

set "REPO=C:\Users\LT-013\261015python"
set "LOGDIR=%REPO%\logs"
if not exist "%LOGDIR%" mkdir "%LOGDIR%"

for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set "TS=%%I"
set "LOG=%LOGDIR%\daily_study_%TS%.log"

set "GIT_AUTHOR_NAME=형모 양"
set "GIT_AUTHOR_EMAIL=tytyrrr13@gmail.com"
set "GIT_COMMITTER_NAME=%GIT_AUTHOR_NAME%"
set "GIT_COMMITTER_EMAIL=%GIT_AUTHOR_EMAIL%"
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"

set "PY=%REPO%\.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=py"
if not exist "%REPO%\.venv\Scripts\python.exe" (
  where py >nul 2>&1 || where python >nul 2>&1
)

echo === daily study publish %DATE% %TIME% ===>> "%LOG%"
echo REPO=%REPO%>> "%LOG%"
echo PY=%PY%>> "%LOG%"

"%PY%" "%REPO%\scripts\daily_study_publish.py" %* >> "%LOG%" 2>&1
set "RC=%ERRORLEVEL%"
echo === exit %RC% ===>> "%LOG%"
exit /b %RC%
