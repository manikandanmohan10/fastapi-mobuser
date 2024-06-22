
# Mobuser

This project is a FastAPI application. Follow the instructions below to set up your development environment, activate the virtual environment, and start the Uvicorn server.

## Prerequisites

- Python 3.8+
- PIP (Python package installer)

## Setup

### 1. Clone the Repository

```bash
git clone -b dev-fastapi https://github.com/ZySec-AI/mobuser.git
cd your-repo
```

### 2. Create a Virtual Environment

#### On Windows

```bash
python -m venv .venv
```

#### On macOS and Linux

```bash
python3 -m venv .venv
```

### 3. Activate the Virtual Environment

#### On Windows

```bash
.venv\Scripts\activate
```

#### On macOS and Linux

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the Uvicorn Server

```bash
uvicorn app.main:app --reload
```

### 6. Access the API

Open your browser and navigate to `http://127.0.0.1:8000/docs` to view the interactive API documentation (Swagger UI).

## Additional Commands

### Deactivate the Virtual Environment

To deactivate the virtual environment, simply run:

```bash
deactivate
```

### Updating Dependencies

If you need to update or add new dependencies, install them using pip and then update the `requirements.txt` file:

```bash
pip install <package-name>
pip freeze > requirements.txt
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
