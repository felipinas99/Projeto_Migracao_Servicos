# Projeto_Migracao_Servicos
Migracao de dados utilizando API e banco de dados


# Driver ODBC para bancos de dados
Postgresql: https://www.postgresql.org/ftp/odbc/releases/
SQL SERVER: https://learn.microsoft.com/pt-br/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16#download-for-windows
ORACLE: https://www.oracle.com/database/technologies/instant-client/winx64-64-downloads.html
Mysql: https://dev.mysql.com/downloads/connector/odbc/




https://turbodbc.readthedocs.io/en/latest/pages/getting_started.html
https://www.boost.org/releases/latest/


The Boost libraries must be compiled, hence if you don’t have a suitable C++ compiler installed already, download the “Build Tools for Visual Studio 2019” from Microsoft Visual Studio, and install the “C++ build tools” Workload.
Download Boost from https://www.boost.org/ (click on the “Current Release” version link, e.g. “Version 1.72.0”, then download the Windows zip file).
Unzip the zipfile somewhere on your PC, e.g. the Downloads folder.
in command prompt 
Run .\bootstrap.bat (this generates the b2 executable).
Run .\b2 (this generates the stage directory and contents, takes a few minutes to run).