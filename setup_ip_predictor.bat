@echo off
echo ===== INICIANDO INSTALACIÓN DEL ENTORNO =====

:: 1. Crear entorno virtual (opcional)
python -m venv venv
if %errorlevel% neq 0 (
    echo Error creando el entorno virtual.
    pause
    exit /b
)

:: 2. Activar entorno virtual
call venv\Scripts\activate

:: 3. Instalar librerías necesarias
echo Instalando dependencias...
pip install --upgrade pip
pip install streamlit pandas scikit-learn matplotlib seaborn

:: 4. Confirmación
echo Todas las dependencias fueron instaladas correctamente.

:: 5. Ejecutar la aplicación
echo Iniciando la aplicación...
streamlit run app.py

pause
