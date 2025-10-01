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

## Comment Section

## 4. Commenting System Functionality and Permissions

The comment system is deeply integrated into the post detail page and uses dedicated Class-Based Views (CBVs) for creation, updating, and deletion.

### A. Comment Feature Summary

| Operation | View Class | URL Pattern | Required Permission |
| :--- | :--- | :--- | :--- |
| **Read/Display** | `PostDetailView` | `/post/<int:pk>/` | Public |
| **Create** | `CommentCreateView` | `/post/<int:pk>/comment/new/` | **Logged-In User** |
| **Update** | `CommentUpdateView` | `/comment/<int:pk>/update/` | **Logged-In User** + **Author Only** |
| **Delete** | `CommentDeleteView` | `/comment/<int:pk>/delete/` | **Logged-In User** + **Author Only** |

### B. Implementation Notes

1.  **Creation Logic:** The `CommentCreateView` is responsible for handling the form submission from the `post_detail.html`. It overrides `form_valid` to automatically link the comment to the parent `Post` (using the `pk` from the URL kwargs) and set the current logged-in user as the comment's `author`.
2.  **Redirection:** All comment views (`Create`, `Update`, `Delete`) use the `get_success_url` method, utilizing `reverse_lazy`, to redirect the user back to the specific post's detail page immediately after the action is complete.
3.  **Permissions:** The `CommentUpdateView` and `CommentDeleteView` utilize the **`LoginRequiredMixin`** and **`UserPassesTestMixin`** (with a `test_func` checking comment authorship) to ensure that users can only modify or delete comments they originally authored. The template logic in `post_detail.html` hides the Edit/Delete links from non-authors as an additional usability measure.