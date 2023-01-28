# Googlelogin

This is a practice app that allows login via Google

# Working
The app has 3 routes only, /, /dashboard and /logout. The /dashboard is a protected area that needs login to access. When you access /, you will be redirected immediately to Google to select your login email. If the email does not exist in our database, it will be registered and you will be asked to login afresh. If it exists, you will be logged in successfully and redirected to dashboard, where a list of registered users are visible. 

To logout, access the /logout path.

# Requirements
See requirements.txt