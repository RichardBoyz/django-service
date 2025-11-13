# Django Challenge Template

This project uses [uv](https://docs.astral.sh/uv/) to manage Python dependencies and virtual environments.

---

## Project Structure

```
python_django_challenge_template/
├── sql/
│   └── database.sql
├── src/
│   ├── api/
│   │   ├── migrations/
│   │   ├── viewsets/
│   │   ├── tests.py
│   │   ├── serializers.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── apps.py
│   ├── tests/
│   └── turing_backend/
│       ├── settings/
│       ├── logs/
│       ├── templates/
│       ├── urls.py
│       └── wsgi.py
├── manage.py
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## Technologies Used

| Technology                  | Purpose                                         |
| --------------------------- | ----------------------------------------------- |
| **Python 3.x**              | Backend development                             |
| **Django**                  | Web framework                                   |
| **Django REST Framework**   | REST API development                            |
| **uv**                      | Python dependency & virtual environment manager |
| **Docker / docker-compose** | Containerization & deployment                   |

---

## Development Setup (using uv)

### Development Environment Requirements

Before running the project in a local development environment, ensure that **MySQL** and the **pkg-config** library are installed on your system.  
These dependencies are required by certain Python packages.  
If they are missing, Django services may fail to start during initialization.

#### Verify environment compatibility

Before starting the server, navigate to the `/python_django_challenge_template/src` directory and run:

```bash
uv pip install -r requirements.txt
```

This step ensures that all required packages can be installed correctly in your environment.

### Install dependencies

```bash
uv sync
```

### Activate virtual environment

```bash
uv venv
source .venv/bin/activate  # macOS/Linux
```

Windows:

```bash
.venv\Scripts\activate
```

---

## Run Development Server

```bash
uv run python manage.py runserver
```

Default URL:

```
http://127.0.0.1:8000/
```

---

## Run with Docker Compose

To start the project using Docker Compose:

```bash
docker-compose up --build
```

To stop the containers:

```bash
docker-compose down
```

## Problem

1. The original project used a single Dockerfile to build the entire environment, including both the database and the backend. In this version, Docker Compose is used to separate the services. Additional time was required to ensure that the backend environment, particularly mysqlclient, works correctly.

2. The backend project’s settings need to be updated so that the application can properly connect when running under Docker Compose. Currently, the example uses 'HOST': 'db', meaning the database host is set to the service name defined in Docker Compose. This configuration can be improved by using os.environ.get() to load the values from environment variables for a more production-ready setup.

3. It is recommended to start the project using Docker Compose, as it allows you to modify the code directly on your local machine through the mounted volume.
