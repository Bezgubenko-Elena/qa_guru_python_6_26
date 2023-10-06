from selene import browser
from selene import have
import allure


class LoginPage:
    @allure.step("Вводим данные для логина")
    def login_user(self, user):
        self._open()
        self._fill_user_name(user)
        self._fill_password(user)
        self._submit_login()

    @allure.step("Переходим на страницу профиля")
    def go_to_profile(self):
        browser.element('[href*="profile"]').click()

    @allure.step("Разлогиниваемся")
    def submit_log_out(self):
        browser.element('[id="submit"]').click()

    @allure.step("Проверяем нахождение на странице авторизации авторизованным пользователем")
    def check_login_success(self, user):
        browser.element('[id="loading-label"]').should(have.text('You are already logged in.'))
        browser.element('[id="userName-value"]').should(have.text(user.user_name))

    @allure.step("Проверяем нахождение на странице авторизации (пользователь не авторизован)")
    def check_not_login(self):
        browser.element('[id="userForm"]').should(have.text('Login in Book Store'))

    @allure.step("Проверяем валидацию данных при логине")
    def check_login_unsuccess(self):
        browser.element('[id="userForm"]').should(have.text('Login in Book Store'))
        browser.element('[id="name"]').should(have.text('Invalid username or password!'))

    def _open(self):
        browser.open('https://demoqa.com/login')
        browser.execute_script('document.querySelector("#fixedban").remove()')
        browser.element('footer').execute_script('element.remove()')

    def _fill_user_name(self, user):
        browser.element('[id="userName"]').type(user.user_name)

    def _fill_password(self, user):
        browser.element('[id="password"]').type(user.password)

    def _submit_login(self):
        browser.element('[id="login"]').click()


class ProfilePage:

    @allure.step("Удаляем книгу из корзины")
    def delete_book(self, book):
        self._search_book(book)
        self._click_cart(book)

    @allure.step("Удаляем все книги")
    def delete_all_books(self):
        browser.element('[class="text-right button di"]').click()
        browser.element(('[id="closeSmallModal-ok"]')).click()

    @allure.step("Переходим на страницу логина")
    def go_to_login(self):
        browser.all('[class="element-group"]').element_by(have.text('Login')).click()

    @allure.step("Переходим на страницу Book Store")
    def go_to_book_store(self):
        browser.element('[id="gotoStore"]').click()

    @allure.step("Проверяем наличие книги в списке")
    def check_book_in_profile(self, book):
        browser.all('[class="rt-tr-group"]').element_by(have.text(book.title)).should(have.text(book.title))

    @allure.step("Проверяем, что в корзина пустая")
    def check_not_books_in_profile(self):
        browser.element('[class="rt-noData"]').should(have.text('No rows found'))

    def _search_book(self, book):
        browser.element('[id="searchBox"]').type(book.title).press_enter()

    def _click_cart(self, book):
        browser.all('[class="rt-tr-group"]').element_by(have.text(book.title)).element('[title="Delete"]').click()
        browser.element(('[id="closeSmallModal-ok"]')).click()


class BookStorePage:
    @allure.step("Переходим на страницу с информацией о книге")
    def go_to_book_page(self, book):
        self._search_book(book)
        self._click_on_book(book)

    def _search_book(self, book):
        browser.element('[id="searchBox"]').type(book.title).press_enter()

    def _click_on_book(self, book):
        browser.all('[class="rt-tr-group"]').element_by(have.text(book.title)).element(
            '[id="see-book-Git Pocket Guide"]').click()


class BookPage:
    @allure.step("Добавляем книгу в корзину")
    def add_book(self):
        browser.element('[class="text-right fullButton"]').click()
