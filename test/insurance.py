import re
from http import HTTPStatus

from locust import task, HttpUser, SequentialTaskSet, between, TaskSet


class UserBehaviour(TaskSet):

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
        login_res = self.client.post(
            "/index.jsf",
            data={
                "login-form": "login-form",
                "login-form:email": "andriitest@fakemail.com",
                "login-form:password": "locusttest",
                "login-form:login.x": "57",
                "login-form:login.y": "9",
                "javax.faces.ViewState": self.view_state
            },
            cookies=self.cookies,
            name="Login")
        assert login_res.status_code == HTTPStatus.OK, "Failed to login"
        self.cookies["UserSessionFilter.sessionId"] = login_res.cookies["UserSessionFilter.sessionId"]
        self.update_view_state(login_res)

    @task(1)
    class AutoQuoteModule(SequentialTaskSet):

        @task
        def select_autoquote(self):
            print("Select Auto Quote in menu")
            response = self.client.get("/quote_auto.jsf", name="Select Auto Quote", cookies=self.parent.cookies)
            assert response.status_code == HTTPStatus.OK, "Failed to select Auto Quote"
            self.parent.update_view_state(response)

        @task
        def complete_step_1(self):
            print("Complete step 1 of Auto Quote")
            response = self.client.post(
                "/quote_auto.jsf",
                data={
                    "autoquote": "autoquote",
                    "autoquote:zipcode": "10101",
                    "autoquote:e-mail": "andriitest@fakemail.com",
                    "autoquote:vehicle": "car",
                    "autoquote:next.x": "54",
                    "autoquote:next.y": "9",
                    "javax.faces.ViewState": self.parent.view_state
                },
                cookies=self.parent.cookies,
                name="Auto Quote step 1")
            assert response.status_code == HTTPStatus.OK, "Failed to complete Auto Quote step 1"
            self.parent.update_view_state(response)

        @task
        def complete_step_2(self):
            print("Complete step 2 of Auto Quote")
            response = self.client.post(
                "/quote_auto2.jsf",
                data={
                    "autoquote": "autoquote",
                    "autoquote:age": "030",
                    "autoquote:gender": "Male",
                    "autoquote:type": "Good",
                    "autoquote:next.x": "30",
                    "autoquote:next.y": "8",
                    "javax.faces.ViewState": self.parent.view_state
                },
                cookies=self.parent.cookies,
                name="Auto Quote step 2")
            assert response.status_code == HTTPStatus.OK, "Failed to complete Auto Quote step 2"
            self.parent.update_view_state(response)

        @task
        def complete_step_3(self):
            print("Complete step 3 of Auto Quote")
            response = self.client.post(
                "/quote_auto3.jsf",
                data={
                    "autoquote": "autoquote",
                    "autoquote:year": "2018",
                    "makeCombo": "Toyota",
                    "autoquote:make": "Toyota",
                    "modelCombo": "Camry",
                    "autoquote:model": "Camry",
                    "autoquote:finInfo": "Own",
                    "autoquote:next.x": "35",
                    "autoquote:next.y": "15",
                    "javax.faces.ViewState": self.parent.view_state
                },
                cookies=self.parent.cookies,
                name="Auto Quote step 3")
            assert response.status_code == HTTPStatus.OK, "Failed to complete Auto Quote step 3"
            self.parent.update_view_state(response)

        @task
        def proceed_to_result(self):
            print("Proceed to Auto Quote result")
            response = self.client.post(
                "/quote_result.jsf",
                data={
                    "quote-result": "quote-result",
                    "autoquote:next.x": "38",
                    "autoquote:next.y": "12",
                    "javax.faces.ViewState": self.parent.view_state
                },
                cookies=self.parent.cookies,
                name="Proceed to quote result")
            assert response.status_code == HTTPStatus.OK, "Failed to proceed to quote result"
            self.parent.update_view_state(response)

        @task
        def purchase_quote(self):
            print("Purchase an auto quote")
            payload = {

            }
            response = self.client.post(
                "/purchase_quote.jsf",
                data={
                    "purchaseQuote": "purchaseQuote",
                    "purchaseQuote:cardname": "Andrii Test",
                    "purchaseQuote:cardnumber": "1294 4863 2356 3975",
                    "purchaseQuote:expiration": "02/09",
                    "purchaseQuote:purchase.x": "42",
                    "purchaseQuote:purchase.y": "9",
                    "javax.faces.ViewState": self.parent.view_state
                },
                cookies=self.parent.cookies,
                name="Purchase quote")
            assert response.status_code == HTTPStatus.OK, "Failed to purchase a quote"

        @task
        def stop(self):
            self.interrupt()

    @task(2)
    class AgentLookupModule(SequentialTaskSet):

        @task
        def select_agent_lookup(self):
            print("Select Agent lookup in menu")
            response = self.client.get(
                "/agent_lookup.jsf",
                cookies=self.parent.cookies,
                name="Select agent lookup")
            assert response.status_code == HTTPStatus.OK, "Failed to select agent lookup"
            assert "Find an Insurance Co. Agent" in response.text, "Agent lookup page is not open"
            self.parent.update_view_state(response)

        @task
        def search_all_agents(self):
            print("Perform search for all agents")
            response = self.client.post(
                "/agent_lookup.jsf",
                data={
                    "show-all": "show-all",
                    "show-all:search-all.x": "30",
                    "show-all:search-all.y": "10",
                    "javax.faces.ViewState": self.parent.view_state
                },
                cookies=self.parent.cookies,
                name="Search all agents")
            assert response.status_code == HTTPStatus.OK, "Failed to search for all agents"
            assert "Insurance Agent Search Results" in response.text, "Search results table is not displayed"

        @task
        def stop(self):
            self.interrupt()


class MyUser(HttpUser):
    tasks = [UserBehaviour]
    wait_time = between(1, 2)
    host = "http://demo.borland.com/InsuranceWebExtJS"
