# Registration System Project in django

## framework, tools and languages

- python as main programming language
- django as python backend framework
- sqlite as database
- mailgun as an email service
- hashing algorithm: django build-in hash method that use Argon2 algorithm
- migrations: django has build-in method to generate the migrations. to see them jump to the Hoe to use section point number 7 [here](Document.md?plain=1#L91).

## Project tree

```bash
.
├── Document.md
├── README.md
├── accounts
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── templates
│   │   ├── accounts
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── password-reset
│   │       ├── password_reset_confirm.html
│   │       ├── password_reset_done.html
│   │       └── password_reset_request.html
│   ├── tests
│   │   ├── __init__.py
│   │   ├── test_forms.py
│   │   ├── test_urls.py
│   │   ├── test_views.py
│   │   └── tests_models.py
│   ├── urls.py
│   └── views.py
├── db.sqlite3
├── home
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── static
│   │   ├── css
│   │   │   └── style.css
│   │   └── images
│   │       ├── 404-error.png
│   │       ├── banner.jpg
│   │       ├── banner2.jpg
│   │       └── email.png
│   ├── templates
│   │   ├── base.html
│   │   ├── errors_handler
│   │   │   ├── 403.html
│   │   │   ├── 404.html
│   │   │   └── 500.html
│   │   └── home
│   │       ├── home.html
│   │       └── index.html
│   ├── tests
│   │   ├── __init__.py
│   │   ├── test_urls.py
│   │   └── tests_views.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── registration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── requirements.txt
└── static

```

## how to setup

before of any step you should have python installed in your device and for sure have pip, which is a package manager for Python packages.

- clone the github repo
- create the virtual environment by this command `python -m venv .venv`
- activate the virtual environment by this command `source .venv/bin/activate`
- install the packages by doing this command `pip install -r requirements.txt`
- check the `.env.sample` for the environment variables that used. and add yours.
- make sure to set `DEBUG = False`.
- type this command to reflect the classes (entities) to the local database `python manage.py migrate`
- collect static folder in case `python manage.py collectstatic`, then type yes if it asks.
- run `python manage.py runserver` to run the server locally.

and now you are ready to test and play around the application.

**important note** if you face any problem in installing the packages you can install it manually:

`pip install django django-crispy-forms django-environ whitenoise`

## Entity/Entities

CustomUser: a class hold the user data

### attributes

- first_name
- last_name
- username
- email
- password
- password confirm

### methods

- `__str__` method to decorate the display of the instances in the admin panel.

## Apps

- accounts: hold the core logic and all information to the login, logout and register functionality. [here](./accounts/)

- home: hold the main information about the home page and main page. [here](./home/)

why making the number of apps 2 rather than only one?

1. to separate the logic, so each app will focus on one mission.
2. for growing purposes if we want to grow the application and add more functionality

## Endpoints (urls)

their are variety of endpoints for each app:

- accounts app endpoints [here](./accounts/urls.py):

  - `/login`: for logging in the users in the application if the user is already have an account.
  - `/register`: for register the users in the application and create an account for them.
  - `/logout`: to logout the user from the application
  - `/password-reset/`: to reset the password if the user forget it, by display a page to make the user enter the email.
  - `/password-reset/confirm/<uidb64>/<token>/`: to confirm if the user is the authenticated user to change his/her password, by send an email, and it will display a page to make the user add new password and confirm it.
  - `/password-reset-done`: to display for the user that the link was sent and check your email.

- home app endpoints [here](./home/urls.py):

  - `/`: show the main page. all users can fetch it.
  - `/home`: this page for authenticated users only, that logged in.

- project endpoint

  - `/admin`: this to login in to the dashboard as admin/user, what you will do inside it, it will be determined with the role you have. what i mean if you have admin role that means you can do anything and see all the tables without any privilege.
  - if you want to enter the dashboard as an admin, type `python manage.py createsuperuser` and fill your data, then try to login in with your admin credential.

## Views

their are variety of views for each app:

- account app views [here](./accounts/views.py):

  - `login_view`: to handel login logic and functionality. by check if the user valid credentials are correct and in the database, after that redirect the user to the home page.
  - `register_view`: to handel register logic and functionality. by adding new user valid credentials into the system, after that redirect the user into the home page.
  - `logout_view`: to handel logout logic and functionality in secure way, and redirect the user to the main page.
  - `password_reset_request`: to handel reset password logic and functionality, by check if the entered email is valid and in the database. then create a new token for the user and send an email include the link to the reset password page.
  - `password_reset_confirm`: to handel reset confirm logic and functionality, by check if the link that sent is correct and the token is valid, then display a page to add the new password for the authenticated user, finally redirect the user to the login page.
  - `password_reset_done`: to display to the authenticated user that the link sent to the email.

- home app views [here](./home/views.py):

  - `index_view`: to display the main page for all users.
  - `home_page_view`: to display the home page for authenticated user only.
  - `custom_permission_denied_403`: to display for the user 403 page if 403 error request happen. (if unauthorized request happen)
  - `custom_permission_denied_404`: to display for the user 404 page if 404 error request happen. (page not found)
  - `custom_permission_denied_500`: to display for the user 500 page if 500 error request happen. (if something wrong happen to the sever)

## Templates

in all templates i use jinja (template language).

- account app templates [here](./accounts/templates/)
  - `login.html`: login template have form for login (username and password)
  - `register.html`: register template have form for register (firstname, lastname, username, email, password, confirm_password)
  - `password_reset_confirm.html`: confirm reset template show the user a form to enter new password and confirm.
  - `password_reset_done.html`: done template to display a message that a link is sent to your email
  - `password_reset_request.html`: reset template that show the user a form to enter the email.

- home app templates [here](./home/templates)
  - `base.html`: core template have the main components and all the other templates inherit from it
  - `index.html`: main template
  - `home.html`: home template, displayed for authenticated user only
  - `403.html`: 403 error template
  - `404.html`: 404 error template
  - `500.html`: 500 error template

## forms

only accounts app has forms, [here](./accounts/forms.py)

- form for the user, for login and register.
- user form `NewUserForm` for changing some constrains but mainly to add widgets into forms and some validation for each attribute. to make sure every thing is in the right way, and consider all the edge cases that might happen when user interact with the form.
- form for the reset password `CustomPasswordResetForm` form to add widget for it.

## Tests

- accounts app tests [here](./accounts/tests/)

  - [forms testing](./accounts/tests/test_forms.py)
  - [endpoints testing](./accounts/tests/test_urls.py)
  - [views testing](./accounts/tests/test_views.py)
  - [models testing](./accounts/tests/test_models.py)

- home app tests [here](./home/tests/)

  - [endpoints testing](./home/tests/test_urls.py)
  - [views testing](./home/tests/tests_views.py)

- to run the tests `python manage.py test`
- this project has 44 tests
- tests might be improved in the future.
- you can add your tests also that might i did not catch it
