from selene import browser

from models.page import LoginPage, ProfilePage, BookStorePage, BookPage
import allure
from allure_commons.types import Severity

from utils.class_instances import registered_user, not_registered_user, registered_user_with_invalid_password, book_for_add
from utils.helper import add_some_book_api, login_with_token, login_api_new


@allure.tag("web")
@allure.severity(Severity.BLOCKER)
@allure.label("owner", "ebezgubenko")
@allure.feature("Авторизация пользователя")
@allure.story("web")
@allure.link("https://demoqa.com/login", name="Page for login")
def test_success_login(create_and_delete_user):
    login_page = LoginPage()
    profile_page = ProfilePage()

    login_page.open()

    login_page.fill_user_name(registered_user)

    login_page.fill_password(registered_user)

    login_page.submit_login()

    profile_page.go_to_login()

    login_page.check_login_success(registered_user)


@allure.tag("web")
@allure.severity(Severity.CRITICAL)
@allure.label("owner", "ebezgubenko")
@allure.feature("Авторизация пользователя")
@allure.story("web")
@allure.link("https://demoqa.com/login", name="Page for login")
def test_success_log_out(create_and_delete_user):
    login_page = LoginPage()
    profile_page = ProfilePage()

    login_page.open()

    login_page.fill_user_name(registered_user)

    login_page.fill_password(registered_user)

    login_page.submit_login()

    profile_page.go_to_login()

    login_page.submit_log_out()

    login_page.check_not_login()


@allure.tag("web")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "ebezgubenko")
@allure.feature("Авторизация пользователя")
@allure.story("web")
@allure.link("https://demoqa.com/login", name="Page for login")
def test_unsuccess_login_not_registered_user():
    login_page = LoginPage()

    login_page.open()

    login_page.fill_user_name(not_registered_user)

    login_page.fill_password(not_registered_user)

    login_page.submit_login()

    login_page.check_login_unsuccess()


@allure.tag("web")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "ebezgubenko")
@allure.feature("Авторизация пользователя")
@allure.story("web")
@allure.link("https://demoqa.com/login", name="Page for login")
def test_unsuccess_login_invalid_password(create_and_delete_user):
    login_page = LoginPage()

    login_page.open()

    login_page.fill_user_name(registered_user_with_invalid_password)

    login_page.fill_password(registered_user_with_invalid_password)

    login_page.submit_login()

    login_page.check_login_unsuccess()


@allure.tag("web")
@allure.severity(Severity.BLOCKER)
@allure.label("owner", "ebezgubenko")
@allure.feature("Взаимодействие с корзиной пользователя")
@allure.story("web")
@allure.link("https://demoqa.com/profile", name="Profile")
def test_add_book(create_and_delete_user):
    login_page = LoginPage()
    profile_page = ProfilePage()
    book_store_page = BookStorePage()
    book_page = BookPage()

    login_page.open()

    browser.driver.add_cookie({"name": "token", "value": login_api_new().get("generate_token")})

    # login_page.fill_user_name(registered_user)
    #
    # login_page.fill_password(registered_user)
    #
    # login_page.submit_login()

    login_page.open()

    profile_page.go_to_book_store()

    book_store_page.search_book(book_for_add)

    book_store_page.go_to_book_page(book_for_add)

    book_page.add_book()

    profile_page.go_to_login()

    login_page.go_to_profile()

    profile_page.search_book(book_for_add)

    profile_page.check_book_in_profile(book_for_add)


@allure.tag("web")
@allure.severity(Severity.BLOCKER)
@allure.label("owner", "ebezgubenko")
@allure.feature("Взаимодействие с корзиной пользователя")
@allure.story("web")
@allure.link("https://demoqa.com/profile", name="Profile")
def test_delete_book(create_and_delete_user):
    login_page = LoginPage()
    profile_page = ProfilePage()
    book_store_page = BookStorePage()
    book_page = BookPage()

    add_some_book_api(1)

    login_page.open()

    login_page.fill_user_name(registered_user)

    login_page.fill_password(registered_user)

    login_page.submit_login()

    profile_page.go_to_book_store()

    book_store_page.search_book(book_for_add)

    book_store_page.go_to_book_page(book_for_add)

    book_page.add_book()

    profile_page.go_to_login()

    login_page.go_to_profile()

    profile_page.search_book(book_for_add)

    profile_page.delete_book(book_for_add)

    profile_page.check_not_books_in_profile()


@allure.tag("web")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "ebezgubenko")
@allure.feature("Взаимодействие с корзиной пользователя")
@allure.story("web")
@allure.link("https://demoqa.com/profile", name="Profile")
def test_delete_all_books(create_and_delete_user):
    login_page = LoginPage()
    profile_page = ProfilePage()

    add_some_book_api(4)

    login_page.open()

    login_page.fill_user_name(registered_user)

    login_page.fill_password(registered_user)

    login_page.submit_login()

    profile_page.delete_all_books()

    profile_page.check_not_books_in_profile()


@allure.tag("web")
@allure.severity(Severity.BLOCKER)
@allure.label("owner", "ebezgubenko")
@allure.feature("Взаимодействие с корзиной пользователя")
@allure.story("web")
@allure.link("https://demoqa.com/profile", name="Profile")
def test_save_added_books_after_relogin(create_and_delete_user):
    login_page = LoginPage()
    profile_page = ProfilePage()
    book_store_page = BookStorePage()
    book_page = BookPage()

    login_page.open()

    login_page.fill_user_name(registered_user)

    login_page.fill_password(registered_user)

    login_page.submit_login()

    profile_page.go_to_book_store()

    book_store_page.search_book(book_for_add)

    book_store_page.go_to_book_page(book_for_add)

    book_page.add_book()

    profile_page.go_to_login()

    login_page.submit_log_out()

    login_page.fill_user_name(registered_user)

    login_page.fill_password(registered_user)

    login_page.submit_login()

    profile_page.search_book(book_for_add)

    profile_page.check_book_in_profile(book_for_add)
