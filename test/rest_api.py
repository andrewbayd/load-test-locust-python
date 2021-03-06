from http import HTTPStatus
from os import getenv

from locust import HttpUser, SequentialTaskSet, task, between
import uuid
import json

from log import logger


class UserBehaviour(SequentialTaskSet):

    def __init__(self, parent):
        super().__init__(parent)
        self.token = getenv("apitoken")
        self.random_id = None
        self.project_id = None
        self.task_id = None

    def on_start(self):
        # Create project
        logger.info("Create project")
        response = self.client.post(
            "/projects",
            data=json.dumps({"name": "Test project"}),
            headers={
                "Content-Type": "application/json",
                "X-Request-Id": str(uuid.uuid4()),
                "Authorization": f"Bearer {self.token}"
            },
            name="Create a project")
        assert response.status_code == HTTPStatus.OK, f"Failed to create a project, {response.text}"
        self.project_id = response.json()["id"]

    @task
    def create_task(self):
        logger.info("Create task")
        response = self.client.post(
            "/tasks",
            data=json.dumps({
                "content": "My appointment",
                "due_lang": "en",
                "project_id": self.project_id
            }),
            headers={
                "Content-Type": "application/json",
                "X-Request-Id": str(uuid.uuid4()),
                "Authorization": f"Bearer {self.token}"
            },
            name="Create a task")
        assert response.status_code == HTTPStatus.OK, f"Failed to create a task, {response.text}"
        self.task_id = response.json()["id"]

    @task
    def complete_task(self):
        logger.info("Complete task")
        response = self.client.post(
            f"/tasks/{self.task_id}/close",
            headers={"Authorization": f"Bearer {self.token}"},
            name="Complete a task")
        assert response.status_code == HTTPStatus.NO_CONTENT, f"Failed to complete a task, {response.text}"

    def on_stop(self):
        logger.info("Delete a project")
        self.client.delete(
            f"/projects/{self.project_id}",
            headers={"Authorization": f"Bearer {self.token}"},
            name="Delete a project")


class WebsiteUser(HttpUser):
    tasks = [UserBehaviour]
    host = "https://api.todoist.com/rest/v1"
    wait_time = between(2, 5)
