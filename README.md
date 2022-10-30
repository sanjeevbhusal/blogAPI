# **_Note for Self_**

- The application is not complete. The purpose to make this application was to build an API using all the best practises used by industry.
- For the same reason, i have tried my best to use practises such as
  - descriptive commit messages
    - I had used git previouly but always used with bad and generic commit messgaes like "fixed", "done", etc.
    - So, I wanted to use git like I am working in a company professionally.
  - use of pull requests
    - I hadn't sent a pull request till date. I always used to merge branches and push the main branch.
    - So, Although I was the only deveoper, I still wanted to go through the flow of creating and merging pull request.
- - Use of Canvan Board to track progress
    - I made this application using trello as the project management tool. I still have a lot of functionality listed in my backlog/todo which I aim to complete gradually.
  - Abstraction
    - I have tried my best to reduce the code through abstraction while still making it very readable.
    - I still feel the serialization and deserialization can be improved greatly and will implement it in future.
  - Testing
    - I tried testing a API first time. So, tests are in bad quality and quantity of tests are also low.
    - There are a lot of places where I can improve. I aim to take a API testing course and further improve the tests in future.

---

<br/>
<br/>
<br/>

# Installation Prerequiste

- Python (version >= 3.10 )
- Pip (Generally comes with Python itself)

<br/>
<br/>

# Running project locally

1. Clone the repository

2. In the root directory of the project create a virtual environment by following below steps:

   - To create a virtual environment run the following command in the terminal from your **project's root directory**.

     ```python
     python -m venv venv
     ```

   - A **venv** folder has been created in your root directory.
   - To **activate the virtual environment** in the terminal, run following command in your terminal depending upon your **Operating System** . Make sure to run the command from your **project's root directory**.

   - On Unix or MacOS using bash shell:
     ```python
     source venv/bin/activate
     ```
   - On Unix or MacOS, using the csh shell:
     ```python
     source venv/bin/activate.csh
     ```
   - On Unix or MacOS, using the fish shell:
     ```python
     source venv/bin/activate.fish
     ```
   - On Windows using the Command Prompt:
     ```python
     venv\Scripts\activate.bat
     ```
   - On Windows using the Powershell:
     ```python
     venv\Scripts\Activate.ps1
     ```

3. There is a **requirements.txt** file in the root directory of the project.

   - It consists of all the project dependencies with their appropriate versions.

   - Run folllowing command in terminal from your **project's root directory** to install all of them.
     ```python
     pip install -r requirements.txt
     ```

4. The aplication requires a secret key to perform functionality such as creating token

   - by default, a secret is provided in the application.
   - However, it is recommended you have your own secret key. The application throws an warning(**not error**) if you donot set a secret key.
   - To set a secret key, create a **.env** file in the **project's root directory** and add a variable
     ```python
     # .env file
     SECRET_KEY="YOUR SECRET KEY GOES HERE"
     ```

5. Now, its time to create the database and all associated tables .

   - There is a file called **seed_database.py** in the root directory of the project.
   - To create database and all the tables run following command from your **project's root directory** in terminal.
     ```python
     python seed_database.py
     ```
   - You can also **Optionally** seed the tables with preexisting data.
   - To create database, tables and also to seed tables, run following command from your **project's root directory** in terminal.
     ```python
     python seed_database.py seed
     ```
   - You should see a database called **"dev_database.db"** or another folder called **instance** in your root directory.

   - **Warning**:

     - Both the above commands will drop all tables and data in the existing database(if any) and create new tables.

     - So, my recommendation is **not to use this command** once you start interacting with API, else your data will be lost.

6. Now the project is ready to be used.

   - **wsgi.py** file is the entry point of the application.

   - Run following command in the terminal from your **project's root directory** to start flask web server.
     ```python
     python wsgi.py
     ```
   - The web server should be up and running.

7. You shouldnot get any error if you followed the steps properly. If you get any error, review the steps again.

<br/>
<br/>

# Explaining Project Files

1. wsgi.py
   - This is the entry point of the application. You should run this file to start the webserver.
2. seed_database.db
   - This file creates the database, tables and **Optionally** seed the tables with preexisting data.
3. requirements.txt
   - This file consists of project's dependencies and should be installed before running the wsgi.py file.
4. blog_api

   - This is the package consisting of all the functionalities of the API

   - blog_api/init.py

     - this is the file where all the blueprints is imported and initialized to create the flask application instance. This file contains a function called create_app

       - create_app function
         - this function receives a configuation class to use as the configuration. by default, it uses Development Configuration.
         - this function creates the flask app, registers all the extensions, configurations, blueprints and finally returns the app instance.
         - this function also has some import statements inside it instead of blog_api/init.py file to avoid circular import errors.

     - wsgi.py file runs this file and imports create_app function to initalize the application.

   - blog_api/config.py
     - this is the file where all the configuration(Development, Testing, Production) are stored.
   - blog_api/extensions.py

     - this file registers all the third party extensions like flask-sqlalchemy, bcrypt etc with the flask app instance.
     - this file contains 3 functions.

       - register_error_handler
         - this function registers all the predefined errors with application's error handler
       - enable_foreign_key
         - this function enables sqlite to enable use of foreign key. this is only called if user uses sqllite as their database.
       - register extensions
         - this function registers all extensions with application instance following application factory design pattern.

     - all 3 functions are called inside **create_app method** of **blog_api/**init**.py file.**

   - blog_api/exceptions.py

     - this file contains all generic exceptions not related to any specific blueprint. t
     - there are 3 exceptions defined here.
       - ApiError
         - This exception serves as a **parent exception** in the project. This exception is extended by other exception.
       - TokenDoesnotExistError
         - This exception is used when user doesnot supply a **token** in the request, while accessing an endpoint which **requries authorization**.
       - InvalidTokenError
         - This exception is used when a token is **present** in the request but is **invalid or have expired**.

   - blog_api/utils.py

     - this file contains all the **utility function**used throughout the project.

   - blog_api/tests

     - this is the directory containing all the **tests** defined for the project.

   - blog_api/blueprints

     - this is the directory containing all the **blueprints** of our project.
     - This directory contains a file **init.py** and some **other directories(user, post etc)**.

       - blog_api/blueprints/init.py

         - init.py imports all the blueprints objects.
         - All these imported blueprint objects are then imported by **create_app** function from blog_api/init.py.

       - blog_api/blueprints/**other directories**(user, post etc)

         - each directory represent individual blueprint. Each blueprint has few files like init, models, schema, views etc.

         - blog_api/blueprints/init.py

           - This file just expose the blueprint object which gets imported by blueprints/init.py file.

         - blog_api/blueprints/models.py

         - This file contains the **Database model** for the blueprint and all methods operating on the model.

         - blog_api/blueprints/views.py
         - This file invokes the specfic **blueprint object**.
         - The blueprint gets **registered** to the application in **create_app** function from blog_api/init.py file.
         - It also contains all the **routes and associated view function**
         - blog_api/blueprints/schema.py

         - This file contains schema's for all the routes(end point) of the same blueprint

         - blog_api/blueprints/exceptions.py
         - this file contains blueprint specific exceptions.
