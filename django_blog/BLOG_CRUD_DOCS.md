# Blog CRUD Functionality and Permissions Documentation

This document outlines the implementation of the Create, Read, Update, and Delete (CRUD) operations for the blog posts, emphasizing the security layers provided by Django's Mixins.

***

## 1. Feature Usage Summary

| Operation | HTTP Method | URL Pattern | Required Permission |
| :--- | :--- | :--- | :--- |
| **Read All** | GET | `/` (Home Page) | Public (No login required) |
| **Read Detail** | GET | `/post/<int:pk>/` | Public (No login required) |
| **Create** | GET/POST | `/post/new/` | **Logged-In User** |
| **Update** | GET/POST | `/post/<int:pk>/update/` | **Logged-In User** + **Author Only** |
| **Delete** | GET/POST | `/post/<int:pk>/delete/` | **Logged-In User** + **Author Only** |

***

## 2. Role of Permission Mixins

The security and permission checks for the blog are enforced at the view level using built-in Django **Mixins**.

### A. LoginRequiredMixin (Authentication)

* **Views Used:** `PostCreateView`, `PostUpdateView`, `PostDeleteView`
* **Purpose:** This Mixin ensures that **only authenticated users** (those who are logged in) can access the view. If an unauthenticated user tries to access the view, they are automatically redirected to the `/login/` URL defined in `settings.py`.
* **Implementation Example:**
    ```python
    class PostCreateView(LoginRequiredMixin, CreateView):
        # ... view code
        pass
    ```

### B. UserPassesTestMixin (Authorization/Ownership)

* **Views Used:** `PostUpdateView`, `PostDeleteView`
* **Purpose:** This Mixin adds an extra layer of **authorization**. It ensures that the logged-in user who is attempting to modify or delete a post is, in fact, the original **author** of that specific post instance.
* **Implementation Details:**
    1.  The Mixin requires a method named **`test_func()`** to be defined in the view.
    2.  The `test_func` retrieves the post object being accessed.
    3.  It then compares the post's `author` field with the currently logged-in user (`self.request.user`).
    4.  If the comparison returns `True`, the user is allowed access. If it returns `False`, Django returns a **403 Forbidden** error, preventing unauthorized modification.
* **Implementation Example (in views.py):**
    ```python
    from django.contrib.auth.mixins import UserPassesTestMixin

    class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
        # ...
        def test_func(self):
            post = self.get_object()
            return self.request.user == post.author
    ```

***

## 3. Post Testing Checklist

The following checks confirm the CRUD permissions are functioning as intended:

* ✅ Anonymous users can **read** all posts.
* ✅ Only logged-in users can **create** new posts.
* ✅ A user can **update** a post they created.
* ✅ A user **cannot update** a post created by another user (returns 403 error).
* ✅ A user can **delete** a post they created.
* ✅ A user **cannot delete** a post created by another user (returns 403 error).