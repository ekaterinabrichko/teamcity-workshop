import requests

from custom_requester.custom_requester import CustomRequester
from data.project_data import ProjectData
from enums.roles import Roles


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

    # def test_project_create(self, api_manager):
    #     # Создание проекта
    #     create_project_response = api_manager.project_api.create_project(self.project_data).json()
    #     assert create_project_response.get("id", {}) == self.created_project_id
    #
    #     get_projects_response = api_manager.project_api.get_project().json()
    #     project_ids = [project.get('id', {}) for project in get_projects_response.get('project', [])]
    #     assert self.created_project_id in project_ids
    #
    #     # Создание билд конфигурации
    #     create_build_conf_response = api_manager.project_api.create_build_conf(self.build_conf_data).json()
    #     assert create_build_conf_response.get("id", {}) == self.created_build_conf_id
    #
    #     # Запустить билд
    #     api_manager.project_api.run_build(self.run_data)
    #
    #     # Удаление проекта
    #     api_manager.project_api.clean_up_project(self.created_project_id)

    def test_create_project_as_super_admin(self, super_admin, user_create):
        # Создание проекта
        create_project_response = super_admin.api_manager.project_api.create_project(self.project_data).json()
        assert create_project_response.get("id", {}) == self.created_project_id

        get_projects_response = super_admin.api_manager.project_api.get_project().json()
        project_ids = [project.get('id', {}) for project in get_projects_response.get('project', [])]
        assert self.created_project_id in project_ids

        # Создание билд конфигурации
        create_build_conf_response = super_admin.api_manager.project_api.create_build_conf(self.build_conf_data).json()
        assert create_build_conf_response.get("id", {}) == self.created_build_conf_id

        # Запустить билд
        super_admin.api_manager.project_api.run_build(self.run_data)

        # Удаление проекта
        super_admin.api_manager.project_api.clean_up_project(self.created_project_id)
