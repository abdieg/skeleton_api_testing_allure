# Sample of API testing suite in Python using Pytest

- **token.py** contains the function to work with oauth
- **conftest.py** has the fixture to allocate the session and the bearer token
- **pytest.ini** has main execution information, including flags for reports and suites

## Pycharm configuration

- VENV is enabled using **requirements.txt**
- Target (script path) = .../tests
- Parameters (if pytest.ini not configured) = --html=pytest_report.html --self-contained-html
- Python interpreter
- Working directory = root of the project
- Add content roots to PYTHONPATH (checked)
- Add source roots to PYTHONPATH (checked)

## Pytest.ini
- Configure **addopts** flag as needed
- Three environments are set: dev, qa, prod. Default is qa in case no flag is set

## Execute

1. Enable VENV
2. Go to root of the project
3. Directly execute "pytest" command
