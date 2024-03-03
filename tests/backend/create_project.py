import requests

from custom_requester.custom_requester import CustomRequester
from data.project_data import ProjectData


class TestProjectCreate:
    created_build_conf_id = None
    created_project_id = None
    project_data = None
    build_conf_data = None

    @classmethod
    def setup_class(cls):
        cls.project_data = ProjectData.create_project_data()
        cls.created_project_id = cls.project_data["id"]
        cls.build_conf_data = ProjectData.create_build_conf_data(cls.created_project_id)
        cls.created_build_conf_id = cls.build_conf_data["id"]
        cls.run_data = ProjectData.run_build_data(cls.created_build_conf_id)

    def test_project_create(self):
        requester = CustomRequester(requests.Session())
        requester.session.auth = ("admin", "admin")

        # Получение токена
        csrf_token = requester.send_request("GET", "/authenticationTest.html?csrf").text
        requester._update_session_headers(**{"X-TC-CSRF-Token": csrf_token})

        # Создание проекта
        create_response = requester.send_request("POST", "/app/rest/projects", data=self.project_data)
        assert create_response.status_code == 200, "Не удалось создать проект"

        check_project = requester.send_request("GET", endpoint=f"/app/rest/projects/id:{self.created_project_id}")
        assert check_project.status_code == 200, "Не удалось получить данные проекта"

        # Создание билд конфигурации
        create_build_conf = requester.send_request("POST", "/app/rest/buildTypes", data=self.build_conf_data)
        assert create_build_conf.status_code == 200, "Не удалось создать билд конфигурацию"

        # Запустить билд
        run_build = requester.send_request("POST", "/app/rest/buildQueue", data=self.run_data)
        assert run_build.status_code == 200, "что-то пошло не так, билд не запустился"

        # Удаление проекта
        delete_project = requester.send_request("DELETE", endpoint=f"/app/rest/projects/id:{self.created_project_id}", expected_status = 204)
        assert delete_project.status_code == 204, "Не удалось удалить проект"