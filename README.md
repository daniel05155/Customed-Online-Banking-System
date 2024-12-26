# Customed Online Banking System
## Overview

This project is a customized online banking system built with Django. 
It includes essential banking features such as account management, deposit, withdrawal, balance inquiry, and fund transfer. The system is designed to ensure secure, efficient, and user-friendly banking operations.

Currently, this is an ongoing project. Future enhancements will include integration with web scraping tools to retrieve customized stock prices, economics indicator, expanding the system into investment and financial analytics.

## Technologies Used 
* Python 3.10.14
* Web Framework: Django==5.1
* Data Storage: db.sqlite3
* Front End:  HTML, CSS, JavaScript

## Current Features
* User Authentication
* Deposit, withdraw, and transfer funds 
* Check the account balance in real-time.
* Investment tracking (Not Yet)

## Setup and Installation
1. Clone this repository:
   ```
   git clone [repository URL]
   ```
2. Navigate to the project directory:
   ```
   cd Customed-Online-Banking-System
   ```
3. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
## Usage
1. Create migrations:
   ```
   python manage.py makemigrations
   ```
2. Migrate them:
   ```
   python manage.py migrate
   ```
3. Start the application: 
   ```
   python manage.py runserver
   ```

