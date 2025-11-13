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
