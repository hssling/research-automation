@echo off
REM ===============================================
REM RESEARCH AUTOMATION PLATFORM
REM Database Setup Script for Windows
REM ===============================================

echo ===========================================
echo Research Automation Platform
echo Database Setup Script
echo ===========================================

REM Check if MySQL is installed
where mysql >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: MySQL is not installed or not in PATH
    echo Please download and install MySQL from:
    echo https://dev.mysql.com/downloads/mysql/
    echo or install via: winget install Oracle.MySQL
    pause
    exit /b 1
)

echo MySQL found. Setting up research automation database...

REM Connect to MySQL and create database
echo Creating research_automation_production database...
mysql -u root -p < database_schema.sql 2>nul
if %errorlevel% neq 0 (
    echo ERROR: MySQL connection failed
    echo Please ensure MySQL service is running and you have the correct root password
    echo You may need to run this as administrator
    pause
    exit /b 1
)

echo ===========================================
echo SUCCESS: Database setup completed!
echo ===========================================

echo Database: research_automation_production
echo Tables created: 12 tables ready for enterprise research workflow

echo Next Steps:
echo 1. Install PHP and Composer (if not already installed)
echo 2. Run: composer create-project laravel/laravel research-automation-api
echo 3. Configure Laravel .env file with database connection
echo 4. Generate Eloquent models: php artisan make:model User -m (for all models)

echo ===========================================
pause
