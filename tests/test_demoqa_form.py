import requests
from selene.support.shared import browser

from data.users import User
from models.page import RegistrationPage, LoginPage
import allure
from allure_commons.types import Severity

from utils import helper


@allure.tag("web")
@allure.severity(Severity.CRITICAL)
@allure.label("owner", "ebezgubenko")
@allure.feature("Регистрация пользователя")
@allure.story("web")
@allure.link("https://demoqa.com/register", name="Page for register")
def test_success_registration():
    registration_page = RegistrationPage()
    login_page = LoginPage()

    user1 = User(
        first_name='Ivan',
        last_name='Ivanov',
        user_name='Ivan',
        password='12345!Qq'
    )

    registration_page.open()

    registration_page.register(user1)

    registration_page.back_to_login()

    login_page.register(user1)

    response = requests.get(
        url="https://demoqa.com/Account/v1/User/60772660-b17c-47ed-aab7-7db50fcd8984"

    )

    assert response.status_code == 200
    assert response.json()["data"]["first_name"] == "Janet"





