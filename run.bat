@echo off
echo Select the environment to run:
echo [1] Production
echo [2] Non_Prod
echo [3] Unit Test

:: 设置默认选项为2 (Non_Prod)，超时时间为5秒
choice /C 123 /N /T 5 /D 2 /M "Select your option (default Non_Prod in 5 seconds):"

:: 检查是否因为超时而使用默认值
if "%ERRORLEVEL%"=="255" echo You did not provide your choice, using default value of Non_Prod.

:: 根据用户的选择设置环境变量
if "%ERRORLEVEL%"=="1" set APP_ENV=Prod
if "%ERRORLEVEL%"=="2" set APP_ENV=Non_Prod
if "%ERRORLEVEL%"=="3" set APP_ENV=Unit_Test

streamlit run app.py


