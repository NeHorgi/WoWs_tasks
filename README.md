**IN PROGRESS**

**Running Tests for Ship Components Validation**

**Prerequisites**

Before running the tests, ensure you have the following installed:

- Python (>= 3.8)
- pytest testing framework
- SQLAlchemy for database session handling
- Any other dependencies required by your project (e.g., a database setup)

**Installation**

- Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/NeHorgi/WoWs_tasks
```

- Create and activate a virtual environment (optional but recommended):

For Windows (Git Bash):
```bash
python -m venv venv
.\venv\Scripts\activate
```
For Linux/macOS:
```bash
python -m venv venv
source venv/bin/activate
```

- Install dependencies:
```bash
pip install -r requirements.txt
```

**Running code**

*task_with_db_working*

To execute the test suite, use the following command:
```bash
pytest
```

To run only the ship component validation tests:
```bash
pytest -k "test_ship_components_change"
```

**Contacts**

Email: lesha.hodus@gmail.com LinkedIn: Aleksei Khodus
