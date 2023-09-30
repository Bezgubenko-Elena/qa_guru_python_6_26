import os
from time import sleep

from selene import browser, command
from selene import have, be, by
import allure
from selenium.webdriver.support import expected_conditions
from webdriver_manager.core import driver

from tests.conftest import base_url


class LoginPage:
    @allure.step("Открываем страницу для заполнения формы логина")
    def open(self):
        browser.open('https://demoqa.com/login')
        browser.execute_script('document.querySelector("#fixedban").remove()')
        browser.element('footer').execute_script('element.remove()')

    @allure.step("Вводим имя пользователя")
    def fill_user_name(self, user):
        browser.element('[id="userName"]').type(user.user_name)

    @allure.step("Вводим пароль")
    def fill_password(self, user):
        browser.element('[id="password"]').type(user.password)

    @allure.step("Отправляем введенные данные для авторизации")
    def submit_login(self):
        browser.element('[id="login"]').click()

    @allure.step("Проверяем нахождение на странице авторизации (пользователь не авторизован)")
    def check_not_login(self):
        browser.element('[id="userForm"]').should(have.exact_texts('Login in Book Store'))

    @allure.step("Проверяем нахождение на странице авторизации авторизованным пользователем")
    def check_login_success(self, user):
        browser.element('[id="loading-label"]').should(have.text('You are already logged in.'))
        browser.element('[id="userName-value"]').should(have.text(user.user_name))

    @allure.step("Разлогиниваемся")
    def submit_log_out(self):
        browser.element('[id="submit"]').click()


class ProfilePage:
    @allure.step("Открываем профиль")
    def open(self):
        browser.open('https://demoqa.com/profile')
        browser.execute_script('document.querySelector("#fixedban").remove()')
        browser.element('footer').execute_script('element.remove()')
    @allure.step("Ищем элемент в списке")
    def search_book(self, value):
        browser.element('[id="searchBox"]').type(value).press_enter()
    @allure.step("Проверяем наличие книги в списке")
    def check_book_in_profile(self):
        browser.element('.rt-table').element('rt-tr-group').should(have.exact_texts()) # либо rt-tbody внутри rt-table

    @allure.step("Удаляем книгу из корзины")
    def go_to_book_page(self):
        browser.element('.rt-table').element('rt-tr-group').element('delete-record-undefined').click()
        browser.config.driver.switch_to.alert.accept()
        browser.config.driver.switch_to.alert.accept()

    @allure.step("Переходим на страницу Book Store")
    def go_to_book_store(self):
        browser.element('[id="gotoStore"]').click()

    @allure.step("Удаляем аккаунт")
    def delete_account(self):
        browser.element('[class="buttonWrap" class="text-center button" id="submit"]').click()

    @allure.step("Удаляем все книги")
    def delete_all_books(self):
        browser.element('[class="buttonWrap" class="text-right button" id="submit"]').click()

    @allure.step("Переходим на страницу логина")
    def go_to_login(self):
        # browser.all('.accordion').element_by(have.exact_text('Book Store Application')).click()
        browser.all('[class="element-group"]').element_by(have.text('Login')).click()

class BookStorePage:
    @allure.step("Открываем страницу Book Store")
    def open(self):
        browser.open('https://demoqa.com/books')
        browser.execute_script('document.querySelector("#fixedban").remove()')
        browser.element('footer').execute_script('element.remove()')

    @allure.step("Ищем элемент в списке книг")
    def search_book(self, value):
        browser.element('[id="searchBox"]').type(value).press_enter()

    @allure.step("Переходим на страницу книги")
    def go_to_book_page(self):
        browser.element('.rt-table').element('rt-tr-group').element('action-buttons').click()


class BookPage:
    @allure.step("Переходим на страницу Book Store")
    def back_to_book_store(self):
        browser.element('[class="text-left fullButton"]').click()

    @allure.step("Добавляем книгу в корзину")
    def add_book(self):
        browser.element('[class="text-right fullButton"]').click()
        browser.config.driver.switch_to.alert.accept()
