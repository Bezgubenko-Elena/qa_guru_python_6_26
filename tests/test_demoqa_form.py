import requests
from selene.support.shared import browser

from data.users import User, Book
from models.page import LoginPage, ProfilePage, BookStorePage, BookPage
import allure
from allure_commons.types import Severity

from utils import helper
from utils.helper import get_data_auth


@allure.tag("web")
@allure.severity(Severity.CRITICAL)
@allure.label("owner", "ebezgubenko")
@allure.feature("Авторизация пользователя")
@allure.story("web")
@allure.link("https://demoqa.com/login", name="Page for login")
def test_success_login():
    login_page = LoginPage()
    profile_page = ProfilePage()

    user1 = User(
        user_name='ivan',
        password='Qq!12345'
    )

    login_page.open()

    login_page.fill_user_name(user1)

    login_page.fill_password(user1)

    login_page.submit_login()

    profile_page.go_to_login()

    login_page.check_login_success(user1)

def test_success_log_out():
    pass

def test_unsuccess_login_invalid_user():
    pass


def test_unsuccess_login_invalid_password():
    pass


def test_registration_user():
    user1 = User(
        user_name='Ivanz',
        password='Qq!12345'
    )

    payload = {
        "userName": user1.user_name,
        "password": user1.password
    }

    response = requests.post(
        url="https://demoqa.com/Account/v1/User",
        data=payload,
        allow_redirects=False
    )
    print(response.content)



def test_delete_user():
    userID = '50d3ac45-ef1c-4d78-a5ff-bfe7dff6f43a'
    response = requests.delete(
        url=f"https://demoqa.com/Account/v1/User/{userID}"
    )
    print(response.status_code)
    assert response.status_code == 204