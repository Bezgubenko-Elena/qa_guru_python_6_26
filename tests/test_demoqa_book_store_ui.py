from models.page import LoginPage, ProfilePage, BookStorePage, BookPage
import allure
from allure_commons.types import Severity

from utils.class_instances import registered_user, not_registered_user, registered_user_with_invalid_password, \
    book_from_list_1
from utils.helper import add_some_book_api


@allure.tag("web")
@allure.severity(Severity.BLOCKER)
@allure.label("owner", "ebezgubenko")
@allure.feature("Авторизация пользователя")
@allure.story("test_ui")
@allure.link("https://demoqa.com/login", name="Page for login")
def test_success_login(create_and_delete_user):
    login_page = LoginPage()

    login_page.login_user(registered_user)

    login_page.check_login_success(registered_user)


@allure.tag("web")
@allure.severity(Severity.CRITICAL)
@allure.label("owner", "ebezgubenko")
@allure.feature("Авторизация пользователя")
@allure.story("test_ui")
@allure.link("https://demoqa.com/login", name="Page for login")
def test_success_log_out(create_and_delete_user):
    login_page = LoginPage()

    login_page.login_user(registered_user)

    login_page.submit_log_out()

    login_page.check_not_login()


@allure.tag("web")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "ebezgubenko")
@allure.feature("Авторизация пользователя")
@allure.story("test_ui")
@allure.link("https://demoqa.com/login", name="Page for login")
def test_unsuccess_login_not_registered_user(create_and_delete_user):
    login_page = LoginPage()

    login_page.login_user(not_registered_user)

    login_page.check_login_unsuccess()


@allure.tag("web")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "ebezgubenko")
@allure.feature("Авторизация пользователя")
@allure.story("test_ui")
@allure.link("https://demoqa.com/login", name="Page for login")
def test_unsuccess_login_invalid_password(create_and_delete_user):
    login_page = LoginPage()

    login_page.login_user(registered_user_with_invalid_password)

    login_page.check_login_unsuccess()


@allure.tag("web")
@allure.severity(Severity.BLOCKER)
@allure.label("owner", "ebezgubenko")
@allure.feature("Взаимодействие с корзиной пользователя")
@allure.story("test_ui")
@allure.link("https://demoqa.com/profile", name="Profile")
def test_add_book(create_and_delete_user):
    login_page = LoginPage()
    profile_page = ProfilePage()
    book_store_page = BookStorePage()
    book_page = BookPage()

    login_page.login_user(registered_user)

    profile_page.go_to_book_store()

    book_store_page.go_to_book_page(book_from_list_1)

    book_page.add_book()

    profile_page.go_to_login()

    login_page.go_to_profile()

    profile_page.check_book_in_profile(book_from_list_1)


@allure.tag("web")
@allure.severity(Severity.BLOCKER)
@allure.label("owner", "ebezgubenko")
@allure.feature("Взаимодействие с корзиной пользователя")
@allure.story("test_ui")
@allure.link("https://demoqa.com/profile", name="Profile")
def test_delete_book(create_and_delete_user):
    login_page = LoginPage()
    profile_page = ProfilePage()
    book_store_page = BookStorePage()
    book_page = BookPage()

    add_some_book_api(1)

    login_page.login_user(registered_user)

    profile_page.go_to_book_store()

    book_store_page.go_to_book_page(book_from_list_1)

    book_page.add_book()

    profile_page.go_to_login()

    login_page.go_to_profile()

    profile_page.delete_book(book_from_list_1)

    profile_page.check_not_books_in_profile()


@allure.tag("web")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "ebezgubenko")
@allure.feature("Взаимодействие с корзиной пользователя")
@allure.story("test_ui")
@allure.link("https://demoqa.com/profile", name="Profile")
def test_delete_all_books(create_and_delete_user):
    login_page = LoginPage()
    profile_page = ProfilePage()

    add_some_book_api(4)

    login_page.login_user(registered_user)

    profile_page.delete_all_books()

    profile_page.check_not_books_in_profile()


@allure.tag("web")
@allure.severity(Severity.BLOCKER)
@allure.label("owner", "ebezgubenko")
@allure.feature("Взаимодействие с корзиной пользователя")
@allure.story("test_ui")
@allure.link("https://demoqa.com/profile", name="Profile")
def test_save_added_books_after_relogin(create_and_delete_user):
    login_page = LoginPage()
    profile_page = ProfilePage()
    book_store_page = BookStorePage()
    book_page = BookPage()

    login_page.login_user(registered_user)

    profile_page.go_to_book_store()

    book_store_page.go_to_book_page(book_from_list_1)

    book_page.add_book()

    profile_page.go_to_login()

    login_page.submit_log_out()

    login_page.login_user(registered_user)

    profile_page.check_book_in_profile(book_from_list_1)
