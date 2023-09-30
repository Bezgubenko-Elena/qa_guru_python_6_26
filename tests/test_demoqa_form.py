import requests
from selene.support.shared import browser

from data.users import User
from models.page import RegistrationPage, LoginPage
import allure
from allure_commons.types import Severity

from utils import helper
from utils.helper import get_data_auth


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

    login_page.login(user1)

    # login_page.login_success_check(user1)







