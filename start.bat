@echo off
setlocal

echo Verificando pacotes Python...

:: Cria um ambiente virtual local (opcional, remova se não quiser)
:: python -m venv venv
:: call venv\Scripts\activate

:: Verifica se o yt-dlp está instalado
pip show yt-dlp >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Requisitos nao encontrados. Instalando do requirements.txt...
    pip install -r requirements.txt
) ELSE (
    echo Requisitos ja instalados.
)

:: Executa o bot
echo Iniciando o bot...
python ytdownloader.py

endlocal
pause
