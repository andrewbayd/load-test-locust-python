import re
from http import HTTPStatus

from locust import task, HttpUser, SequentialTaskSet, between


class UserBehaviour(SequentialTaskSet):

    def __init__(self, parent):
        super().__init__(parent)
        self.cookies = {}
        self.view_state = None

    def update_view_state(self, response):
        self.view_state = re.findall("j_id\d+:j_id\d+", response.text)[0]

    def on_start(self):
        print("Launch URL")
        launch_res = self.client.get("/index.jsf", name="Launch URL")
        assert launch_res.status_code == HTTPStatus.OK, "Failed to launch URL"
        self.cookies["JSESSIONID"] = launch_res.cookies["JSESSIONID"]
        self.update_view_state(launch_res)

        print("Perform login")
        payload = {
            "login-form": "login-form",
            "login-form:email": "andriitest@fakemail.com",
            "login-form:password": "locusttest",
            "login-form:login.x": "57",
            "login-form:login.y": "9",
            "javax.faces.ViewState": self.view_state
        }
        login_res = self.client.post("/index.jsf", name="Login", data=payload, cookies=self.cookies)
        assert login_res.status_code == HTTPStatus.OK, "Failed to login"
        self.cookies["UserSessionFilter.sessionId"] = login_res.cookies["UserSessionFilter.sessionId"]
        self.update_view_state(login_res)

    @task
    def select_autoquote(self):
        print("Select Auto Quote")
        response = self.client.get("/quote_auto.jsf", name="Select Auto Quote", cookies=self.cookies)
        assert response.status_code == HTTPStatus.OK, "Failed to select Auto Quote"
        self.update_view_state(response)

    @task
    def complete_step_1(self):
        print("Complete step 1 of Auto Quote")
        print(self.view_state)
        payload = {
            "autoquote": "autoquote",
            "autoquote:zipcode": "10101",
            "autoquote:e-mail": "andriitest@fakemail.com",
            "autoquote:vehicle": "car",
            "autoquote:next.x": "54",
            "autoquote:next.y": "9",
            "javax.faces.ViewState": self.view_state
        }
        response = self.client.post("/quote_auto.jsf", name="Auto Quote step 1", cookies=self.cookies, data=payload)
        assert response.status_code == HTTPStatus.OK, "Failed to complete Auto Quote step 1"
        self.update_view_state(response)

    @task
    def complete_step_2(self):
        print("Complete step 2 of Auto Quote")
        payload = {
            "autoquote": "autoquote",
            "autoquote:age": "030",
            "autoquote:gender": "Male",
            "autoquote:type": "Good",
            "autoquote:next.x": "30",
            "autoquote:next.y": "8",
            "javax.faces.ViewState": self.view_state
        }
        response = self.client.post("/quote_auto2.jsf", name="Auto Quote step 2", cookies=self.cookies, data=payload)
        assert response.status_code == HTTPStatus.OK, "Failed to complete Auto Quote step 2"
        self.update_view_state(response)

    @task
    def complete_step_3(self):
        print("Complete step 3 of Auto Quote")
        payload = {
            "autoquote": "autoquote",
            "autoquote:year": "2018",
            "makeCombo": "Toyota",
            "autoquote:make": "Toyota",
            "modelCombo": "Camry",
            "autoquote:model": "Camry",
            "autoquote:finInfo": "Own",
            "autoquote:next.x": "35",
            "autoquote:next.y": "15",
            "javax.faces.ViewState": self.view_state
        }
        response = self.client.post("/quote_auto3.jsf", name="Auto Quote step 3", cookies=self.cookies, data=payload)
        assert response.status_code == HTTPStatus.OK, "Failed to complete Auto Quote step 3"
        self.update_view_state(response)

    @task
    def proceed_to_result(self):
        print("Proceed to Auto Quote result")
        payload = {
            "quote-result": "quote-result",
            "autoquote:next.x": "38",
            "autoquote:next.y": "12",
            "javax.faces.ViewState": self.view_state
        }
        response = self.client.post("/quote_result.jsf", name="Proceed to quote result", cookies=self.cookies,
                                    data=payload)
        assert response.status_code == HTTPStatus.OK, "Failed to proceed to quote result"
        self.update_view_state(response)

    @task
    def purchase_quote(self):
        print("Purchase an auto quote")
        payload = {
            "purchaseQuote": "purchaseQuote",
            "purchaseQuote:cardname": "Andrii Test",
            "purchaseQuote:cardnumber": "1294 4863 2356 3975",
            "purchaseQuote:expiration": "02/09",
            "purchaseQuote:purchase.x": "42",
            "purchaseQuote:purchase.y": "9",
            "javax.faces.ViewState": self.view_state
        }
        response = self.client.post("/purchase_quote.jsf", name="Purchase quote", cookies=self.cookies, data=payload)
        assert response.status_code == HTTPStatus.OK, "Failed to purchase a quote"


class MyUser(HttpUser):
    tasks = [UserBehaviour]
    wait_time = between(1, 2)
    host = "http://demo.borland.com/InsuranceWebExtJS"
