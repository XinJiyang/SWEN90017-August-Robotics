# This branch is used for back-end development


<!-- <img src="https://images.unsplash.com/photo-1501776192086-602832fae6e6?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"> -->

# <img src="https://cdn.freebiesupply.com/logos/large/2x/the-university-of-melbourne-logo-svg-vector.svg" width=15% align=left> SWEN90017-2023-TEAM-R-August-Robotics

This repository is created for [University of Melbourne](https://www.unimelb.edu.au)

\***\*August-Robotics\*\*** project development.

---

## Team members

| Name | Role | Contact | 
| :---- | :---- | :---- | 
| Andrew Liu| Quality Assurance Lead | ahliu@student.unimelb.edu.au | 
| Michael Hannon | Product Owner | mhannon@student.unimelb.edu.au |
| Kritnand Suwanna-Arj | Scrum Master | ksuwannaarj@student.unimelb.edu.au |
| Lipeng Zhang | Developer | lipengz@student.unimelb.edu.au |
| Wenxuan XIE | Back-end Lead | wexie2@student.unimelb.edu.au |
| Wei Zhao | Architecture Lead | weizhao1@student.unimelb.edu.au |
| Himaja Ramesh Kakade | UI/UX Lead | hkakade@student.unimelb.edu.au |
| Poorvith Gowda Gavenahalli Divakar | Risk Management Lead | pgowda@student.unimelb.edu.au |
| Haiyao Yan | Front-end Lead | haiyao@student.unimelb.edu.au |
| Jiyang XIN | Deployment Lead | jiyxin@student.unimelb.edu.au |

## Recommended Development Tools

- [PyCharm](https://www.jetbrains.com/pycharm/)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Docker](https://www.docker.com/)
- [PostgreSQL](https://www.postgresql.org/download/)

## Prerequisites

- python==3.11.3
- asgiref==3.6.0
- Django==4.2.1
- django-cors-headers==3.14.0
- psycopg2-binary==2.9.6
- PyJWT==2.6.0
- sqlparse==0.4.4
- tzdata==2023.3
- PostgreSQL==15.2
- asgiref==3.6.0

## Install PostgreSQL

### Step 1 - Download the latest [PostgreSQL](https://www.postgresql.org/download/) for Windows x86-64  

### Step 2 - Setup PostgreSQL  
  
### Step 3 - Select Components: PostgreSQL Server, pgAdmin4, Stack Builder, Command Line Tool  
  
### Step 4 - Select Data Directory
  
### Step 5 - Set Password and Port Number
  
### Step 6 - Finish Installation  

## Option 1 : Run the django program on localhost

### Install Django and related dependencies

```bash

## make sure you are in the working directory Django-backend/

python -m venv venv

## Create virtual environment

## for windows
source venv/Scripts/activate

## for mac os
source venv/bin/activate

pip install -r requirements.txt

```

### Setting Up A Database Server

#### Step 1 : Open the settings

Go to the following directory AugustRoboticsBackend/settings.py

#### Step 2 : Edit settings.py

```python

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',

        ## Optional, you can change the database name to whatever you want
        'NAME': 'db_augustRobotics', 
        'USER': 'weizhao1', 
        'PASSWORD': 'pass4teamR!',  
        'HOST': 'backend-data.postgres.database.azure.com', 
        'PORT': 5432,

    }
}

```

#### Step 3 : If you set the database name, please create a database with the same name using pgAdmin4 or psql command line tool

#### Step 4 : Migrage the database to localhost

```bash

python manage.py migrate

```

### Start the Django Server directly on localhost

**Note:**

Change the 'HOST' to 'localhost' to start the Django Server

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',

        ## Optional, you can change the database name to whatever you want
        'NAME': 'db_augustRobotics', 
        'USER': 'weizhao1', 
        'PASSWORD': 'pass4teamR!',  
        'HOST': 'backend-data.postgres.database.azure.com', 
        'PORT': 5432,

    }
}

```

```bash
python manage.py runserver
```

## Option 2 : Start the Django app with Docker

If you are not familier with docker or have not installed docker yet, feel free to check the WiKi for [Docker](https://github.com/EcZww/SWEN90017-2023-TEAM-R-August-Robotics/wiki/Docker-Setup)

You can use this Dockerfile to build a Docker image for your Django project. To build the image, navigate to the directory that contains the Dockerfile and enter the following command:

**Note:**

when using Docker Compose, the services are running in separate containers, and you should use the service name as the hostname for connecting to the database. In this case, the service name is db.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',

        ## Optional, you can change the database name to whatever you want
        'NAME': 'db_augustRobotics', 
        'USER': 'weizhao1', 
        'PASSWORD': 'pass4teamR!',  
        'HOST': 'backend-data.postgres.database.azure.com', 
        'PORT': 5432,

    }
}

```

```bash
cd Django-backend

# This will create a Docker image named django-backend. 
docker compose up -d
```

That's it! Now we have a Docker container running Django app.

## How to write the pytest and run the tests?

### go to the directory Django-backend/AugustRoboticsBackend/tests/

### write the tests for your endpoint

for example, we have a endpoint on 'localhost:8000/' we could test the endpoint by the following code

```python
@pytest.mark.django_db
def test_home_page(client):

    ## you could use reverse or replace with the whole url: 
    ## url = '/'
    url = reverse('hello_world')
    response = client.get(url)
    assert response.status_code == 200
```

```python

from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),  # The name of the URL pattern is 'home_view'
]
```

### Run the pytest

```bash
## run on your local machine
pytest


## docker
docker compose exec -T backend pytest

```

## Visualize the PostgreSQL database via docker

### Manually configure the database using pgAdmin4

After starting pgAdmin, you have to manually connect to your PostgreSQL database. Here's how to do it:

- Open your web browser and navigate to http://localhost:8080.

- Log in to pgAdmin using the email: admin@admin.com, password: Admin

- Once you're logged in, right-click on Servers in the left-hand pane and select Register > Server....

- In the Register - Server dialog box that appears, fill in the following information:

- General > Name: Enter any name you like. This name will be used to identify this server connection in pgAdmin.

- Connection > Host name/address: Enter db. This is the name of the PostgreSQL service in your Docker Compose file, which Docker uses as the hostname for connecting between services.

- Connection > Username: Enter postgres (or the username you specified in your Docker Compose file).

- Connection > Password: Enter postgres (or the password you specified in your Docker Compose file).

- Click Save.

You should now see your PostgreSQL server in the pgAdmin sidebar, and you can browse your databases, tables, and other database objects.

If you still can't see your PostgreSQL database, make sure that your PostgreSQL service is running correctly. You can check its status by running docker-compose ps in the terminal. If it's not running, you may need to check your Docker Compose configuration and PostgreSQL logs for any issues.

### How to view the data rows in the database

To view your data, you need to navigate to the specific database and table where your data is stored. Here's how you can do it:

- In the pgAdmin sidebar, expand the server you've added.

- You will see a list of categories including Databases, Login/Group Roles, Tablespaces, etc.

- Expand the Databases category. You will see a list of all the databases in your PostgreSQL server.

- Click on the specific database that contains your data.

- In the expanded database, navigate to Schemas > public > Tables.

- Here, you should see a list of all your tables. Click on the table that contains your data.

- Then, you can select View/Edit Data > All Rows from the context menu (right-click menu).

- You should now be able to view all the data in that table.

Note: The data you can see here will depend on what data your application has stored in the PostgreSQL server. If your application hasn't stored any data yet, or if it's using a different database or table, then you might not see your data here.
