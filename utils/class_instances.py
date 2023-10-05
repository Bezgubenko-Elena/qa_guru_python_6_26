from data.users import User, Book

registered_user = User(
    user_name='ivan',
    password='Qq!12345'
)
registered_user_with_invalid_password = User(
    user_name='ivan',
    password='Ww!12345'
)
not_registered_user = User(
    user_name='ruslan',
    password='Ww!12345'
)

book_for_add = Book(
    title='Git Pocket Guide',
    ISBN='9781449325862'
)

book1 = Book(
    title='Git Pocket Guide',
    ISBN='9781449325862'
)

book2 = Book(
    title="You Don't Know JS",
    ISBN='9781491904244'
)

book3 = Book(
    title='Book is not in Book Store',
    ISBN='0000000000000'
)