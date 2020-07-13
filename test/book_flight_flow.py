from http import HTTPStatus

from locust import HttpUser, SequentialTaskSet, task, between

from helper import verify_response_time


class UserBehaviour(SequentialTaskSet):

    # disabled since this functionality is not working on demo site
    # def on_start(self):
    #     print("Login to account")
    #     payload = {
    #         "action": "process",
    #         "userName": "andriitest",
    #         "password": "locusttest",
    #         "login.x": "41",
    #         "login.y": "12"
    #     }
    #     response = self.client.post("/login.php", name="login", data=payload)
    #     assert response.status_code is HTTPStatus.OK, "Failed to login"
    #     assert verify_response_time(response, 2), "Login request took more than 2 second"

    @task
    def find_flight(self):
        print("Perform request to find a flight")
        payload = {
            "tripType": "roundtrip",
            "passCount": 1,
            "fromPort": "Acapulco",
            "fromMonth": 7,
            "fromDay": 12,
            "toPort": "Acapulco",
            "toMonth": 7,
            "toDay": 12,
            "servClass": "Coach",
            "airline": "No Preference",
            "findFlights.x": 59,
            "findFlights.y": 13
        }
        response = self.client.post("/mercuryreservation2.php", name="Find a flight", data=payload)
        assert response.status_code == HTTPStatus.OK, "Failed to find a flight"
        assert verify_response_time(response, 1), "Request to find a flight took more than 1 second"

    @task
    def select_flight(self):
        print("Perform request to select a flight")
        payload = {
            "fromPort": "Acapulco",
            "toPort": "Acapulco",
            "passCount": 1,
            "toDay": 12,
            "toMonth": 7,
            "fromDay": 12,
            "fromMonth": 7,
            "servClass": "Coach",
            "outFlight": "Pangea Airlines$362$274$9: 17",
            "inFlight": "Pangea Airlines$632$282$16: 37",
            "reserveFlights.x": 53,
            "reserveFlights.y": 7
        }
        response = self.client.post("/mercurypurchase.php", name="Select a flight", data=payload)
        assert response.status_code == HTTPStatus.OK, "Failed to select a flight"
        assert verify_response_time(response, 1), "Request to select a flight took more than 1 second"

    @task
    def book_flight(self):
        print("Perform request to book flight")
        payload = {
            "outFlightName": "Pangea Airlines", "outFlightNumber": "362", "outFlightPrice": "274", "outFlightTime": "9:17",
            "inFlightName": "Pangea Airlines", "inFlightNumber": "632", "inFlightPrice": "282", "inFlightTime": "16:37",
            "fromPort": "Acapulco", "toPort": "Acapulco", "passCount": "1",
            "toDay": "12", "toMonth": "7", "fromDay": "12", "fromMonth": "7",
            "servClass": "Coach",
            "subtotal": "556", "taxes": "45",
            "passFirst0": "Andrii", "passLast0": "Test",
            "creditCard": "AX", "creditnumber": "12345",
            "cc_exp_dt_mn": "01",  "cc_exp_dt_yr": "2010", "cc_frst_name": "Andrii", "cc_last_name": "Test",
            "billAddress1": "1325 Borregas Ave.", "billCity": "Sunnyvale", "billState": "CA", "billZip": "94089",
            "billCountry": "215",
            "delAddress1": "1325 Borregas Ave.", "delCity": "Sunnyvale", "delState": "CA", "delZip": "94089",
            "delCountry": "215",
            "buyFlights.x": "46", "buyFlights.y": "13"
        }
        response = self.client.post("/mercurypurchase2.php", name="Book a flight", data=payload)
        assert response.status_code == HTTPStatus.OK, "Failed to book a flight"
        assert verify_response_time(response, 1), "Request to book a flight took more than 1 second"


class Test(HttpUser):
    wait_time = between(1, 2)
    host = "http://newtours.demoaut.com"
    tasks = [UserBehaviour]
