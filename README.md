# Rule Engine API

A simple rule engine implemented with FastAPI and PostgreSQL. This application allows users to create, combine, evaluate rules, and download rules in JSON format.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Contributing](#contributing)
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

2. **Install requirements:**
    ```bash
    pip install -r requirements.txt

3. **Create Database**
    Create your own database with a user who is granted all permissions to it and replace your db link with DATABASE_URL in main.py. I have used postgres, so it would be great if you have postgres already setup. otherwise MySql,etc. will also work.

4. **Run Backend:**
    ```bash
    uvicorn main:app --reload

5. **Run Frontend:**
    In separate terminal, 
    ```bash
    start .\index.html


## Running with Docker image using Docker Hub

1. **Log in with docker in terminal:**

    ```bash
    docker login

2. **Pull the docker image from docker hub:**
    ```bash
    docker pull sanyamgarg12/rule-engine-app

## Using .tar file instead of Docker Hub

1. **Log in with docker in terminal:**

    ```bash
    docker login

2. **Pull the docker image from docker hub:**

    ```bash
    docker load -i rule-engine-app.tar

