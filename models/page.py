import os

from selene import browser, command
from selene import have, be, by
import allure
from selenium.webdriver.support import expected_conditions
from webdriver_manager.core import driver

from tests.conftest import base_url


class RegistrationPage:
    @allure.step("Открываем страницу для заполнения формы")
    def open(self):
        browser.open('https://demoqa.com/register')
        browser.execute_script('document.querySelector("#fixedban").remove()')
        browser.element('footer').execute_script('element.remove()')

    @allure.step("Заполняем данные, отправляем")
    def register(self, user):
        self._fill_first_name(user.first_name)
        self._fill_last_name(user.last_name)
        self._fill_user_name(user.user_name)
        self._fill_password(user.password)
        # self._enter_captcha()
        self._submit_registration()

    @allure.step("Проверяем данные нового пользователя")
    def should_have_registered(self, user):
        browser.element('.table').all('td').even.should(have.exact_texts(
            f'{user.first_name} {user.last_name}'
        ))

    def _fill_first_name(self, value):
        browser.element('[id="firstname"]').type(value)

    def _fill_last_name(self, value):
        browser.element('[id="lastname"]').type(value)

    def _fill_user_name(self, value):
        browser.element('[id="userName"]').type(value)

    def _fill_password(self, value):
        browser.element('[id="password"]').type(value)

    # def _enter_captcha(self):
    #     sleep(5)
    #     browser.element('[class="recaptcha-checkbox-borderAnimation"]').click()

    def _submit_registration(self):
        browser.element('[id="register"]').click()
        # browser.config.driver.switch_to.alert.accept()

    def back_to_login(self):
        browser.element('[id="gotologin"]').click()


class LoginPage:
    @allure.step("Открываем страницу для заполнения формы")
    def open(self):
        browser.open('https://demoqa.com/register')
        browser.execute_script('document.querySelector("#fixedban").remove()')
        browser.element('footer').execute_script('element.remove()')

    @allure.step("Заполняем данные, отправляем")
    def register(self, user):
        self._fill_user_name(user.user_name)
        self._fill_password(user.password)
        self._submit_login()

    def _fill_user_name(self, value):
        browser.element('[id="userName"]').type(value)

    def _fill_password(self, value):
        browser.element('[id="password"]').type(value)

    def _submit_login(self):
        browser.element('[id="login"]').click()


class ProfilePage:
    @allure.step("Открываем профиль")
    def open(self):
        browser.open('https://demoqa.com/profile')
        browser.execute_script('document.querySelector("#fixedban").remove()')
        browser.element('footer').execute_script('element.remove()')

    # @allure.step("Ищем элементы в корзине")
    #  def search_book(self, value):
    #      browser.element('[id="searchBox"]').type(value)

    # @allure.step("Проверка имени залогиненого пользователя")
    # def should_have_registered(self, user):
    #     browser.element('[id="books-wrapper" class="text-right"]').should(have.texts(user.user_name))

    @allure.step("Разлогиниться")
    def log_out(self):
        browser.element('[id="books-wrapper" id="submit"]').click()

    # @allure.step("Переход на страницу в корзине")
    # def (self):
    #     browser.element('[id="login"]').click()
    #
    # @allure.step("Выбрать количество элементов на странице в корзине")
    # def submit_login(self):
    #     browser.element('[id="login"]').click()

    @allure.step("Перейти на страницу Book Store")
    def go_to_book_store(self):
        browser.element('[id="gotoStore"]').click()

    @allure.step("Удалить аккаунт")
    def delete_account(self):
        browser.element('[class="buttonWrap" class="text-center button" id="submit"]').click()

    @allure.step("Удалить все книги")
    def delete_all_books(self):
        browser.element('[class="buttonWrap" class="text-right button" id="submit"]').click()

    # @allure.step("Удалить книгу")
    # def delete_book(self, value):
    #     browser.element('[class="rt-tbody"]').all()


class BookStorePage:
    @allure.step("Открываем страницу Book Store")
    def open(self):
        browser.open('https://demoqa.com/books')
        browser.execute_script('document.querySelector("#fixedban").remove()')
        browser.element('footer').execute_script('element.remove()')

    # @allure.step("Ищем элементы в списке книг")
    #  def search_book(self, value):
    #      browser.element('[id="searchBox"]').type(value)

    @allure.step("Проверка имени залогиненого пользователя")
    def should_have_registered(self, user):
        browser.element('[id="userName-value"]').should(have.exact_texts(user.user_name))

    @allure.step("Разлогиниться")
    def log_out(self):
        browser.element('[id="books-wrapper" id="submit"]').click()

    def log_out(self):
        browser.element('[id="books-wrapper" id="submit"]').click()


class BookPage:
    @allure.step("Открываем страницу Book Store")
    def open(self):
        browser.open('https://demoqa.com/books')
        browser.execute_script('document.querySelector("#fixedban").remove()')
        browser.element('footer').execute_script('element.remove()')

    @allure.step("Проверка имени залогиненого пользователя")
    def should_have_registered(self, user):
        browser.element('[id="userName-value"]').should(have.exact_texts(user.user_name))

    @allure.step("Разлогиниться")
    def log_out(self):
        browser.element('[id="books-wrapper" id="submit"]').click()

    def go_to_website_book(self):
        browser.element('[id="website-wrapper" id="userName-value"]').click()

    def add_book(self):
        browser.element('[class="text-right fullButton"]').click()

    def back_to_book_store(self):
        browser.element('[class="text-left fullButton"]').click()
