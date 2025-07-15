@ECHO OFF
@SET PYTHONIOENCODING=utf-8
@SET PYTHONUTF8=1
@FOR /F "tokens=2 delims=:." %%A in ('chcp') do for %%B in (%%A) do set "_CONDA_OLD_CHCP=%%B"
@chcp 65001 > NUL
@CALL "C:\Users\16262\miniconda3\condabin\conda.bat" activate "c:\Users\16262\Documents\GitHub\russell2000-data-pipeline\.conda"
@IF %ERRORLEVEL% NEQ 0 EXIT /b %ERRORLEVEL%
@c:\Users\16262\Documents\GitHub\russell2000-data-pipeline\.conda\python.exe -Wi -m compileall -q -l -i C:\Users\16262\AppData\Local\Temp\tmp727ygnxe -j 0
@IF %ERRORLEVEL% NEQ 0 EXIT /b %ERRORLEVEL%
@chcp %_CONDA_OLD_CHCP%>NUL
