# Flask Boilerplate
### _Flask boilerplate inspired by The Flask Mega-Tutorial by Miguel Grinberg_

### July 17, 2019 Release Notes

* **V0.1**  
This first version is the simplest Flask web server including the organization of the files and folders for bigger projects.

| Files | Description |
| - | - |
| config.py | This file contains most of the configuration variables that your app needs. |
| run.py | This is the file that is invoked to start up a development server. It gets a copy of the app from your package and runs it. This won’t be used in production, but it will see a lot of mileage in development. |
| requirements.txt | This file lists all of the Python packages that your app depends on. You may have separate files for production and development dependencies. |
| /app/	| This is the package that contains your application. |
| /app/\_\_init__.py	| This file initializes your application and brings together all of the various components. |
| /app/main/\_\_init__.py	| Set the forlder using Blueprint |
| /app/main/views.py |	This is where the routes are defined. |
| /app/static/	|This directory contains the public CSS, JavaScript, images and other files that you want to make public via your app. It is accessible from app.com/static/ by default. |
| app/static/styles.css | Main custom CSS file. |
| /app/templates/ |	This is where you’ll put the Jinja2 templates for your app. |
| /app/templates/index.htm | File used by the app as an index |
