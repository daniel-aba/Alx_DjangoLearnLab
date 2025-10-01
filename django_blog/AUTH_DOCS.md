# User Authentication System Documentation

This document details the architecture, usage, and testing procedures for the Django user authentication system implemented in the blog application.

***

## 1. System Architecture and Implementation Details

The authentication system leverages Django's robust built-in features, coupled with custom views and forms for user registration.

| Component | Files/Classes Used | Description & Implementation |
| :--- | :--- | :--- |
| **Database Tables** | `auth_user`, `auth_group`, etc. | These are managed by the `django.contrib.auth` app and created via `python manage.py migrate`. PostgreSQL is the backend. |
| **Custom Form** | `blog/forms.py` (`UserRegisterForm`) | Extends Django's `UserCreationForm`. It was customized primarily to explicitly include and handle the **email** field during registration. |
| **Registration View** | `blog/views.py` (`register`) | A custom function-based view that handles: <br> - **GET** requests: Renders the blank `UserRegisterForm`. <br> - **POST** requests: Validates the submitted data, saves the new user, and displays a success message using the `messages` framework before redirecting to the login page. |
| **Built-in Views** | `django_blog/urls.py` | Uses Django's `LoginView` and `LogoutView` from `django.contrib.auth.views` (`auth_views`). <br> **Note:** These views are configured to use custom templates (`blog/login.html`, `blog/logout.html`) via the `template_name` argument in `urls.py`. |
| **Profile View** | `blog/views.py` (`profile`) | A custom function-based view that uses the **`@login_required`** decorator to prevent access by unauthenticated users. It serves as the secure landing page for logged-in users. |
| **URL Configuration** | `django_blog/urls.py` and `blog/urls.py` | Global `urls.py` includes the app-specific routes and explicitly maps the built-in login/logout views to their respective custom templates. |

***

## 2. Usage Instructions (Register, Login, Logout)

### A. Registering a New Account

1.  Navigate to the registration page: `http://127.0.0.1:8000/register/`
2.  Fill out the **Username**, **Email**, and **Password** fields.
3.  Click the **"Register"** button.
4.  Upon successful creation, a success message will appear, and you will be redirected to the login page.

### B. Logging In

1.  Navigate to the login page: `http://127.0.0.1:8000/login/`
2.  Enter the **Username** and **Password** for your account.
3.  Click the **"Login"** button.
4.  You will be automatically redirected to the secure **Profile Page** (`/profile/`).

### C. Viewing Profile

* Access the secure profile area at: `http://127.0.0.1:8000/profile/`
* If you are not logged in, this view will automatically redirect you to the login page, enforcing security.

### D. Logging Out

1.  Navigate to the logout page: `http://127.0.0.1:8000/logout/` (or click the link on the profile page).
2.  You will be logged out and presented with a message confirming the action and a link to log in again.

***

## 3. Testing and Security Checklist

### A. Pre-Test Setup (Essential)

1.  **Database Creation:** Ensure the database (`django_blog_db`) exists.
2.  **Migrations:** **Crucially**, run migrations to create the necessary core tables:
    ```bash
    python manage.py migrate
    ```
3.  **Run Server:** Start the development server:
    ```bash
    python manage.py runserver
    ```

### B. Core Functionality Test Cases

| Test Case | Steps | Expected Result |
| :--- | :--- | :--- |
| **Registration** | Navigate to `/register/`, fill out all fields, and submit. | Account created, success message displayed, redirection to `/login/`. |
| **Login** | Navigate to `/login/`, enter valid credentials, and submit. | Successful authentication, redirection to `/profile/`. |
| **Logout** | Log in, then navigate to `/logout/`. | User is logged out, presented with the logout confirmation template. |
| **Profile Access (Authenticated)** | Log in, then access `/profile/`. | Profile page renders successfully, displaying username/email. |
| **Profile Access (Unauthenticated)** | Log out, then try to access `/profile/`. | User is immediately redirected to the `/login/` page. |

### C. Security Features

* ✅ **Password Hashing:** Handled automatically by Django's `UserCreationForm` and authentication system.
* ✅ **CSRF Protection:** Implemented in all forms (`register.html`, `login.html`) using the `{% csrf_token %}` template tag.
* ✅ **Authentication Check:** Enforced on the sensitive profile view using the `@login_required` decorator.