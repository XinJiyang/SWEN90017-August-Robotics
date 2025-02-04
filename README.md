<!-- <img src="https://images.unsplash.com/photo-1501776192086-602832fae6e6?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"> -->

# <img src="https://cdn.freebiesupply.com/logos/large/2x/the-university-of-melbourne-logo-svg-vector.svg" width=15% align=left> SWEN90017-2023-TEAM-R-August-Robotics
This repository is created for [University of Melbourne](https://www.unimelb.edu.au)

****August-Robotics**** project development.

---

## Project Description
August Robotics is deploying its world leading floor marking robot Lionel in various countries of the world. Part of the Lionel floor marking business is operating under Robot as a Service business model, which means August Robotics’ global robot operation team brings the robot to the client site (e.g., exhibition centers), deploy the robot to complete certain client jobs (e.g., floor marking for several exhibitions), delivers the marked floor to the client and brings the robot back to the office.

In order to optimize the company’s management efficiency and create an overview of the business for internal stakeholders, we need to establish a digitalized client/job database management platform as one of the foundations of the company process.
## Stakeholders
| Name | Role | Contact | 
| :---- | :---- | :---- | 
| Leo Li | Client | leo.li@augustrobotics.com |
| Mingye Li | Supervisor | mingye.li1@unimelb.edu.au |

## Team members
| Name | Role | Contact | 
| :---- | :---- | :---- | 
| Andrew Liu| Quality Assurance Lead | ahliu@student.unimelb.edu.au | 
| Michael Hannon | Product Owner | mhannon@student.unimelb.edu.au |
| Kritnand Suwanna-Arj | Scrum Master| ksuwannaarj@student.unimelb.edu.au |
| Lipeng Zhang | Developer | lipengz@student.unimelb.edu.au |
| Wenxuan XIE | Back-end Lead | wexie2@student.unimelb.edu.au |
| Wei Zhao | Architecture Lead | weizhao1@student.unimelb.edu.au |
| Himaja Ramesh Kakade | UI/UX Lead | hkakade@student.unimelb.edu.au |
| Poorvith Gowda Gavenahalli Divakar | Risk Management Lead | pgowda@student.unimelb.edu.au |
| Haiyao Yan | Front-end Lead | haiyao@student.unimelb.edu.au |
| Jiyang XIN | Deployment Lead | jiyxin@student.unimelb.edu.au |

## Project Timeline

| Sprint | Timeline | Milestone | Status |
| :---- | :---- | :---- | :---|
| Inception Phase | 13th March - 29th March 2023 | <ul><li>Requirements Elicitation</li><li>User Stories</li><li>Design and architecture diagrams</li><li> Low-Fidelity Prototype</li> | <mark style="background-color: green">Completed</mark>
| Sprint 1 | 30th March - 28th April 2023 | <ul><li>High-fidelity Prototype</li><li>Set Up GitHub Repository</li><li>More design and architecture diagrams</li><li>Quality Assurance documentation</li> | <mark style="background-color: green">Completed</mark>
| Sprint 2 | 1st May - 26th May 2023 | <ul><li>Update High-fidelity Prototype</li><li>Review User stories</li><li>Review Design and architecture</li><li>Update Acceptance criteria and tests</li><li>More Testing documentation</li><li>Development of user stories - fixed data</li><li> Deployment Guide </li> | <mark style="background-color: green">Completed</mark>
| Sprint 3 | 31st July - 21st August 2023 | <li>Review Design and architecture</li><li>User Acceptance testing</li><li>Development of user stories - operational data</li><li> Deployment on Heroku </li> | <mark style="background-color: green">Completed</mark>
| Sprint 4 | 29th August - 17th September 2023 | <li>Review Design and architecture</li><li>User Acceptance testing</li><li>Development of user stories - operational data, searching & sorting, access control</li><li> Deployment on Heroku </li> | <mark style="background-color: green">Completed</mark>
| Sprint 5 | 20th September - 15th October 2023 | <li>Development of user stories - operational data, searching & sorting, dashboard </li><li>User acceptance and unit testing</li><li>Updating and adding to documentation</li><li> Deployment on Heroku </li> | <mark style="background-color: green">Completed</mark>
| Sprint 6 | 6th October 2023 - 29th October 2023 | <li>Review Design and architecture</li><li>Development of user stories - dashboard, bug fixing </li><li>User acceptance and unit testing</li><li>Updating final documentation</li><li> Deployment on Heroku </li><li>Endeavour exhibition - Team Video, Poster, Presentation</li><li>Final Handover to client</li> | <mark style="background-color: green">Completed</mark>
</ul>

## High Fidelity Prototype for AR Database Platform
[Figma Interactive Prototype Link](https://www.figma.com/proto/wppLyVtOXpqCN2MCv252zQ/SWEN90017-%3A-High-Fidelity-Prototype?type=design&node-id=812-2&scaling=scale-down&page-id=0%3A1&starting-point-node-id=812%3A2)

## Structure of the repository

├── Project-Documentation: Project Documentation for all artefacts

├── Django-backend: Backend of the AR Database Platform using Django and PostgreSQL, includes tests

└── Vue-frontend: Frontend of the AR Database Platform using Vue and UI library Vuetify

## Front end Setup

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin) to make the TypeScript language service aware of `.vue` types.

If the standalone TypeScript plugin doesn't feel fast enough to you, Volar has also implemented a [Take Over Mode](https://github.com/johnsoncodehk/volar/discussions/471#discussioncomment-1361669) that is more performant. You can enable it by the following steps:

1. Disable the built-in TypeScript Extension
   1. Run `Extensions: Show Built-in Extensions` from VSCode's command palette
   2. Find `TypeScript and JavaScript Language Features`, right click and select `Disable (Workspace)`
2. Reload the VSCode window by running `Developer: Reload Window` from the command palette.

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```

## Back end Setup

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

## Install PostgreSQL

### Step 1
Download the latest [PostgreSQL](https://www.postgresql.org/download/) for Windows x86-64  
### Step 2
Setup PostgreSQL  
### Step 3
Select Components: PostgreSQL Server, pgAdmin4, Stack Builder, Command Line Tool  
### Step 4
Select Data Directory  
### Step 5
Set Password and Port Number  
### Step 6
Finish Installation  

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
        'NAME': 'test-dev', 
        'USER': 'weizhao1', 
        'PASSWORD': 'pass4teamR!',  
        'HOST': 'backend-data.postgres.database.azure.com', 
        'PORT': 5432,

    }
}

```

#### Step 3 : If you set the database name, please create a database with the same name using pgAdmin4 or psql command line tool

#### Step 4 : Run the script

```sh
// build-project-local.sh
python manage.py makemigrations && python manage.py migrate && python manage.py initgroups && python manage.py runserver 0.0.0.0:8000
```

```bash

sh sh build-project-local.sh 
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
        'NAME': 'test-dev', 
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
   
# Then run the docker script
./build-project-docker.sh
```

That's it! Now we have a Docker container running Django app.

```bash
# API Documentation available at the localhost:8000 once the backend is running
http://localhost:8000/
   
```

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
## API Documentation
API's Documentation can be viewed at: [API-Documentation](https://confluence.cis.unimelb.edu.au:8443/display/SWEN900172023RZ/Backend+API+Documentation) 

The API Documentation is also present in our documentation which can be accessed at: [Project-documentation](https://github.com/EcZww/SWEN90017-2023-TEAM-R-August-Robotics/tree/dev/Project-documentation)

## Deployment
Guide to Deploy the application at: [Deployment Guide](https://confluence.cis.unimelb.edu.au:8443/display/SWEN900172023RZ/Deployment+Guide)

The guide to deploy the application is also present in our documentation which can be accessed at: [Project-documentation](https://github.com/EcZww/SWEN90017-2023-TEAM-R-August-Robotics/tree/dev/Project-documentation)

Front-end deployed at: https://ar-vue-app-product-81dff6e65fc4.herokuapp.com/login

Back-end deployed at: [https://ar-django-app-ea02f954ef7b.herokuapp.com/docs/index.html](https://django-backend-main-dde75ed28e39.herokuapp.com/redoc/)


## License
   Available at [LICENSE.md](https://github.com/EcZww/SWEN90017-2023-TEAM-R-August-Robotics/blob/dev/LICENSE)
   
## Changelog

### [Sprint 2] - 2023-05-26

Second sprint in the development of the project. Developed user stories for epic Fixed Data.

#### Added

- [Project-documentation](https://github.com/EcZww/SWEN90017-2023-TEAM-R-August-Robotics/tree/dev/Project-documentation)
  Contains all the requirements and documents produced during semester 1 2023:
  - Requirements
  - Design & Architecture
  - Quality Assurance
  - Development and Deployment Guides

- [Front-end Changelog](https://github.com/EcZww/SWEN90017-2023-TEAM-R-August-Robotics/blob/dev/CHANGELOG.md)
   - Below is the process to login and access the database platform:

### Login
#### Step 1
   Run the backend server and database by following the instruction in section 'Back end Setup'.
#### Step 2
   ```bash
   ## move to frontend directory
   cd Vue-frontend
   
   ## run Vue application
   npm run dev
   ```
#### Step 3
   Open http://localhost:5173/login in browser
#### Step 4
   Enter the username, password for admin and click on 'login' button.
   **Admin credentials account: username: admin, password: 123456**
   **Viewer credentials account: username: viewer, password: 123456**
### Add new client
#### Step 1
   Login at http://localhost:5173/login using admin account, After login into the application, click client icon on the side menu to see all availble clients.<br />
   <img src=https://github.com/EcZww/SWEN90017-2023-TEAM-R-August-Robotics/assets/80369914/1ec3db86-464c-45c9-88e6-9f661eb62167 width=50%>
#### Step 2
   Click 'ADD NEW CLIENT' button on the upper right of client list.
#### Step 3
   Enter the client details in each fields.<br />
   <img src=https://github.com/EcZww/SWEN90017-2023-TEAM-R-August-Robotics/assets/80369914/83f31ee7-c0ec-4dc0-824c-0f1607fcf68f width=50%>
#### Step 4
   Click 'SAVE CLIENT' button and then click 'SAVE' button to confirm client creation.<br />
   <img src=https://github.com/EcZww/SWEN90017-2023-TEAM-R-August-Robotics/assets/80369914/cfbee476-b7ee-454a-aeaf-015254f66415 width=50%><br />
   Then you should see the saved client appear in client list.<br />
   <img src=https://github.com/EcZww/SWEN90017-2023-TEAM-R-August-Robotics/assets/80369914/09f9c18f-4a48-4e5a-bcf5-47189af1f6eb width=50%>
#### Step 5
   Click the 3 dots on the main client list page to edit or delete an existing client


- Back-end Changelog
   - Setup models and views for database including floor marking job details, employees, their performance, client and venue information (available under /Django-backend/DataProcess)
   - Setup authentication for users to login and register
   - User authentication tests (available under /Django-backend/AugustRoboticsBackend/tests)
   - Setup API's for the following (available under /Django-backend/AugustRoboticsBackend/urls)
    1. Login and Register
    2. Add client data and venue data
    3. Edit client data
    4. Get client data


### [Sprint 3] - 2023-08-18

Third sprint in the development of the project. Developing user stories for epic Operational Data.

#### Added

- [Front-end Changelog](https://github.com/EcZww/SWEN90017-2023-TEAM-R-August-Robotics/blob/dev/CHANGELOG.md)
   - Refer to 0.4.0

#### Modified

- [Project-documentation](https://github.com/EcZww/SWEN90017-2023-TEAM-R-August-Robotics/tree/dev/Project-documentation)
  Contains all the requirements and documents produced during semester 1 & continued in Semester 2 2023:
  - Requirements
  - Design & Architecture
  - Quality Assurance
  - Development and Deployment Guides


### [Sprint 4] - 2023-09-15

Fourth sprint in the development of the project. Developing user stories for epic: Operational Data, Access Control & Searching.

#### Added

- [Front-end Changelog](https://github.com/EcZww/SWEN90017-2023-TEAM-R-August-Robotics/blob/dev/CHANGELOG.md)
   - Refer to 0.5.0

#### Modified

- [Project-documentation](https://github.com/EcZww/SWEN90017-2023-TEAM-R-August-Robotics/tree/dev/Project-documentation)
  Contains all the requirements and documents produced during semester 1 & continued in Semester 2 2023:
  - Requirements
  - Design & Architecture
  - Quality Assurance
  - Development and Deployment Guides

### [Sprint 5] - 2023-10-16

Fifth sprint in the development of the project. Developing user stories for epic: Job Data Digitization, Operational Data & Searching.

#### Added

- [Front-end Changelog](https://github.com/EcZww/SWEN90017-2023-TEAM-R-August-Robotics/blob/dev/CHANGELOG.md)
   - Refer to 0.6.0

### [Sprint 6] - 2023-10-29

Sixth sprint in the development of the project. Developing user stories for epic: Job Data Digitization, Operational Data & Searching and fixing bugs.

#### Added

- [Front-end Changelog](https://github.com/EcZww/SWEN90017-2023-TEAM-R-August-Robotics/blob/dev/CHANGELOG.md)
   - Refer to 0.7.0
  
 #### Modified

- [Project-documentation](https://github.com/EcZww/SWEN90017-2023-TEAM-R-August-Robotics/tree/dev/Project-documentation)
  Contains all the requirements and documents produced during semester 1 & continued in Semester 2 2023:
  - Requirements
  - Design & Architecture
  - Quality Assurance
  - Development and Deployment Guides including setup/deployment guide, API documentation, database connection documentation.
