# Rule Engine API

A simple rule engine implemented with FastAPI and PostgreSQL. This application allows users to create, combine, evaluate rules, and download rules in JSON format.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Running with Docker Hub](#running-with-docker-image-using-docker-hub)
- [Download Database](#download-current-database)
- [Delete Database](#delete-all-entries-in-the-database)
- [License](#license)

## Features

- Create new rules with names and rule strings.
- Combine multiple rules into a single rule.
- Evaluate rules against user-provided data.
- Download the rules database in JSON format.

## Technologies

- **FastAPI**: A modern web framework for building APIs with Python 3.6+ based on standard Python type hints.
- **PostgreSQL**: A powerful, open-source relational database system.
- **SQLAlchemy**: An SQL toolkit and Object-Relational Mapping (ORM) system for Python.
- **Uvicorn**: A lightning-fast ASGI server for Python.
- **HTML/CSS**: Frontend for interacting with the API.

## Installation

### Prerequisites

- Python 3.7 or later
- PostgreSQL 13 or later
- pip (Python package installer)

### Step-by-Step Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/SanyamGarg12/Rule-Engine-with-AST.git
    ```

2. **Install requirements:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Create Database**

    Create your own database with a user who is granted all permissions to it and replace your db link with DATABASE_URL in main.py. I have used postgres, so it would be great if you have postgres already setup. otherwise MySql, etc. will also work.

4. **Run Backend:**

    ```bash
    uvicorn main:app --reload
    ```

5. **Run Frontend:**

    In separate terminal,

    ```bash
    start .\index.html
    ```

## Running with Docker image using Docker Hub

1. **Log in with docker in terminal:**

    ```bash
    docker login
    ```

    Note: Make sure you have postgres setup

2. **Pull the docker image from docker hub:**

    ```bash
    docker pull sanyamgarg12/rule-engine-app
    ```

3. **Run Backend**

    ```bash
    docker run -p 8000:8000 -e DATABASE_URL=postgresql://your_user_name:your_password@host.docker.internal:5432/database_name sanyamgarg12/rule-engine-app
    ```

- NOTE : Make sure port 5432 is available otherwise change it accordingly. Also replace your_user_name, your password, database_name with your credentials in above bash script.
4. **Run Frontend in separate terminal**

    - **Enter project directory**

        ```bash
        cd RULE-ENGINE-WITH-AST
        ```

    - **Execute index.html**

        ```bash
        start .\index.html
        ```

Open your web browser and navigate to http://localhost:8000 or http://your.ip.address:8000 to access the Rule Engine API.

## How Application will look

1. **CREATE RULE**

    ![alt text](sample_images/image.png)

2. **Combine RULE**
![alt text](sample_images/image-1.png)

3. **Evaluate Rule**

- **Example of an Eligible User**  
  Refer to the JSON file: [EXAMPLE_ELIGIBLE.JSON](./EXAMPLE_ELIGIBLE.JSON)  
  ![Eligible User Example](sample_images/image_3.png)

- **Example of a Not Eligible User**  
  Refer to the JSON file: [EXAMPLE_NOT_ELIGIBLE.JSON](./EXAMPLE_NOT_ELIGIBLE.JSON)  
  ![Not Eligible User Example](sample_images/image_4.png)

## Download Current Database

- **Run the following command in the project directory:**
    ```bash
    python curr_db.py
    ```

## Delete All Entries in the Database

- **To delete all entries, run this command in the project directory:**
    ```bash
    python empty_db.py
    ```
## License
- MIT License : [License](./LICENSE)
