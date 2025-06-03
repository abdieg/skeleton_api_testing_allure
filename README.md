# Sample of API testing suite in Python using Pytest

- **token.py** contains the function to work with oauth
- **conftest.py** has the fixture to allocate the session and the bearer token
- **pytest.ini** has main execution information, including flags for reports and suites

## Pycharm configuration

- VENV is enabled using **requirements.txt**
- Target (script path) = .../tests
- Parameters (if pytest.ini not configured) = --alluredir=reports/allure-results --clean-alluredir
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

## Jenkins and CI/CD implications
- Since we are using Docker, both APP and TESTING parts must belong to the same network. This was ensured using **stage('Ensure docker network exists')** in Jenkinsfile
- Jenkins credentials were used to address environment variables:
```
QA_IP
QA_PORT
```
- Those variables were used because they were defined in such way under settings.py file
- Due to project being inside a VPN and using Docker, the HOST will be the container's docker name
- Jenkins must enable Allure plugin
- Jenkins must configure Allure Commandline inside Manage Jenkins > Tools menu
- It is important to install Allure inside the host where Jenkins server is:
```shell
sudo dpkg -i allure_2.34.0-1_all.deb
allure --version
which allure
ls -l /usr/bin/allure
```
- Do not forget to double check the Allure reports path
- The suite and environment can be selected using Jenkins parameters