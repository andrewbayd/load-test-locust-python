# LOAD TESTS WITH LOCUST

Example of load tests using python + locust.
I use next websites for testing:
* demo site for booking flights and tours http://newtours.demoaut.com/
* demo site of insurance company http://demo.borland.com/InsuranceWebExtJS/
* todo list REST api https://developer.todoist.com/rest/v1/

You can clone this repo and try to run it locally. For this you need next simple steps:
1. Clone repo
2. Create virtual environment https://docs.python.org/3/library/venv.html
3. Install requirements `pip install -r requirements.txt`
4. Execute command `locust -f test/name_of_locustfile.py` (please note, in order to run tests against todoist api you have to register at https://todoist.com/, copy API token in settings and provide it as env variable *before* `locust` command, e.g. `apitoken=your_token locust -f test/rest_api.py`)
