set CUR_DATE=
set CUR_DIR=

for %%d in ("%cd%") do set CUR_DIR=%%~nxd

del *.zip

@for /f "skip=1" %%x in ('wmic os get localdatetime') do if not defined CUR_DATE set CUR_DATE=%%x
echo Current date is %CUR_DATE%

set ZIP="D:\Program Files\7-Zip\7z"
set FILE=%CUR_DIR%_%CUR_DATE%.zip

REM Backup de la base de datos..
REM set DB=db_trading.bak
REM pg_dump -U postgres -d trading -h localhost -F c -f .\%DB%

%ZIP% a %FILE% . -xr!node_modules -xr!env*

set DEST="D:\Onedrive\Backups"

REM psql -U postgres -d trading
REM CREATE DATABASE nombre_base;
REM pg_restore 
REM -U username -h hostname -d database_name /path/to/backup_file.backup

MOVE *.zip %DEST%

pause