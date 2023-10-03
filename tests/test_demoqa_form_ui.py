import requests
from selene.support.shared import browser
from data.users import User, Book
from models.page import LoginPage, ProfilePage, BookStorePage, BookPage
import allure
from allure_commons.types import Severity

from utils import helper
from utils.helper import login_in_profile_api, add_some_book_api


@allure.tag("web")
@allure.severity(Severity.BLOCKER)
@allure.label("owner", "ebezgubenko")
@allure.feature("Авторизация пользователя")
@allure.story("web")
@allure.link("https://demoqa.com/login", name="Page for login")
def test_success_login(create_and_delete_user):
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


@allure.tag("web")
@allure.severity(Severity.CRITICAL)
@allure.label("owner", "ebezgubenko")
@allure.feature("Авторизация пользователя")
@allure.story("web")
@allure.link("https://demoqa.com/login", name="Page for login")
def test_success_log_out():
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

    login_page.submit_log_out()

    login_page.check_not_login()


@allure.tag("web")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "ebezgubenko")
@allure.feature("Авторизация пользователя")
@allure.story("web")
@allure.link("https://demoqa.com/login", name="Page for login")
def test_unsuccess_login_invalid_user():
    login_page = LoginPage()

    user2 = User(
        user_name='ruslan',
        password='Ww!12345'
    )

    login_page.open()

    login_page.fill_user_name(user2)

    login_page.fill_password(user2)

    login_page.submit_login()

    login_page.check_login_unsuccess()


@allure.tag("web")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "ebezgubenko")
@allure.feature("Авторизация пользователя")
@allure.story("web")
@allure.link("https://demoqa.com/login", name="Page for login")
def test_unsuccess_login_invalid_password():
    login_page = LoginPage()

    user3 = User(
        user_name='ivan',
        password='Ww!12345'
    )

    login_page.open()

    login_page.fill_user_name(user3)

    login_page.fill_password(user3)

    login_page.submit_login()

    login_page.check_login_unsuccess()


@allure.tag("web")
@allure.severity(Severity.BLOCKER)
@allure.label("owner", "ebezgubenko")
@allure.feature("Взаимодействие с корзиной пользователя")
@allure.story("web")
@allure.link("https://demoqa.com/profile", name="Profile")
def test_add_book(delete_all_books_after_test):
    login_page = LoginPage()
    profile_page = ProfilePage()
    book_store_page = BookStorePage()
    book_page = BookPage()

    user1 = User(
        user_name='ivan',
        password='Qq!12345'
    )

    book1 = Book(
        title='Git Pocket Guide',
        ISBN='9781449325862'
    )

    login_page.open()

    login_page.fill_user_name(user1)

    login_page.fill_password(user1)

    login_page.submit_login()

    profile_page.go_to_book_store()

    book_store_page.search_book(book1)

    book_store_page.go_to_book_page(book1)

    book_page.add_book()

    profile_page.go_to_login()

    login_page.go_to_profile()

    profile_page.search_book(book1)

    profile_page.check_book_in_profile(book1)


@allure.tag("web")
@allure.severity(Severity.BLOCKER)
@allure.label("owner", "ebezgubenko")
@allure.feature("Взаимодействие с корзиной пользователя")
@allure.story("web")
@allure.link("https://demoqa.com/profile", name="Profile")
def test_delete_book():
    login_page = LoginPage()
    profile_page = ProfilePage()
    book_store_page = BookStorePage()
    book_page = BookPage()

    user1 = User(
        user_name='ivan',
        password='Qq!12345'
    )

    book1 = Book(
        title='Git Pocket Guide',
        ISBN='9781449325862'
    )

    add_some_book_api(1)

    login_page.open()

    login_page.fill_user_name(user1)

    login_page.fill_password(user1)

    login_page.submit_login()

    profile_page.go_to_book_store()

    book_store_page.search_book(book1)

    book_store_page.go_to_book_page(book1)

    book_page.add_book()

    profile_page.go_to_login()

    login_page.go_to_profile()

    profile_page.search_book(book1)

    profile_page.delete_book(book1)

    profile_page.check_not_books_in_profile()


@allure.tag("web")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "ebezgubenko")
@allure.feature("Взаимодействие с корзиной пользователя")
@allure.story("web")
@allure.link("https://demoqa.com/profile", name="Profile")
def test_delete_all_books():
    login_page = LoginPage()
    profile_page = ProfilePage()
    book_store_page = BookStorePage()
    book_page = BookPage()

    user1 = User(
        user_name='ivan',
        password='Qq!12345'
    )

    book1 = Book(
        title='Git Pocket Guide',
        ISBN='9781449325862'
    )

    add_some_book_api(4)

    login_page.open()

    login_page.fill_user_name(user1)

    login_page.fill_password(user1)

    login_page.submit_login()

    profile_page.delete_all_books()

    profile_page.check_not_books_in_profile()


@allure.tag("web")
@allure.severity(Severity.BLOCKER)
@allure.label("owner", "ebezgubenko")
@allure.feature("Взаимодействие с корзиной пользователя")
@allure.story("web")
@allure.link("https://demoqa.com/profile", name="Profile")
def test_save_added_books_after_relogin():
    login_page = LoginPage()
    profile_page = ProfilePage()
    book_store_page = BookStorePage()
    book_page = BookPage()

    user1 = User(
        user_name='ivan',
        password='Qq!12345'
    )

    book1 = Book(
        title='Git Pocket Guide',
        ISBN='9781449325862'
    )

    login_page.open()

    login_page.fill_user_name(user1)

    login_page.fill_password(user1)

    login_page.submit_login()

    profile_page.go_to_book_store()

    book_store_page.search_book(book1)

    book_store_page.go_to_book_page(book1)

    book_page.add_book()

    profile_page.go_to_login()

    login_page.submit_log_out()

    login_page.fill_user_name(user1)

    login_page.fill_password(user1)

    login_page.submit_login()

    profile_page.search_book(book1)

    profile_page.check_book_in_profile(book1)
