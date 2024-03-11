from playwright.sync_api import sync_playwright
from utils.datagenerator import DataGenerator


def test_create_and_delete_project_simple(browser):
    project_name = DataGenerator.fake_name()
    project_id = DataGenerator.fake_project_id()

    browser.goto('http://localhost:8111/login.html')
    browser.fill('#username', 'admin')
    browser.fill('#password', 'admin')
    browser.click('.loginButton')
    browser.wait_for_url('http://localhost:8111/favorite/projects?mode=builds')

    browser.goto(
        'http://localhost:8111/admin/createObjectMenu.html?projectId=_Root&showMode=createProjectMenu#createManually')
    browser.fill('input#name', project_name)
    browser.fill('input#externalId', project_id)
    browser.fill('input#description', 'Описание тестового проекта')
    browser.click('input.submitButton')

    browser.wait_for_url(f'http://localhost:8111/admin/editProject.html?projectId={project_id}')
    assert project_name in browser.text_content('body')

    # Delete project
    browser.goto(f'http://localhost:8111/admin/editProject.html?projectId={project_id}')
    browser.locator(f'xpath=//*[@id="sp_span_prjActions{project_id}"]/button').click()
    browser.locator(f'xpath=//*[@id="sp_span_prjActions{project_id}Content"]/div/ul/li[9]/a').click()

    browser.wait_for_url('http://localhost:8111/admin/editProject.html?projectId=_Root')

    browser.goto('http://localhost:8111/favorite/projects?mode=builds')
    assert project_name not in browser.text_content('body')

    browser.close()
