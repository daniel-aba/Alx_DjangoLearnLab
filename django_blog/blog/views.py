from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy # ⬅️ New Import for redirects
from django.contrib import messages # ⬅️ Re-add for the register view
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # ⬅️ Permissions
from django.contrib.auth.decorators import login_required # ⬅️ For profile view

from .models import Post, Comment # ⬅️ Imported Comment model
from .forms import PostForm, UserRegisterForm, CommentForm # ⬅️ Imported CommentForm and UserRegisterForm

# --- R: Read (List View) ---
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-published_date'] # Order by newest first

# --- R: Read (Detail View - MODIFIED) ---
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    # Override get_context_data to include the CommentForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm() # Pass the empty comment form
        return context

# --- C: Create Post View ---
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    form_class = PostForm

    # Override form_valid to automatically set the post author to the logged-in user
    def form_valid(self, form):
        form.instance.author = self.request.user # Set the author field
        return super().form_valid(form)

    success_url = '/' # Redirect to the home page after creation

# --- U: Update Post View ---
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    form_class = PostForm

    # Override test_func to ensure only the author can update the post
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    success_url = '/' 

# --- D: Delete Post View ---
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/' # Redirect to home/list view after deletion

    # Override test_func to ensure only the author can delete the post
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# ----------------------------------------------------
#               COMMENT VIEWS (NEW)
# ----------------------------------------------------

# --- C: Create Comment View ---
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    # We use this view to handle the POST submission from the post_detail.html
    template_name = 'blog/post_detail.html' 

    # This view MUST be passed the post_pk via the URL kwargs (e.g., /post/<pk>/comment/new/)
    def form_valid(self, form):
        # 1. Get the Post object using the 'pk' passed in the URL
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        
        # 2. Set the foreign key fields (post and author) before saving
        form.instance.post = post  # Set the associated post
        form.instance.author = self.request.user # Set the author
        
        return super().form_valid(form)

    # Redirect back to the post detail page after creation
    def get_success_url(self):
        # The 'pk' is in self.kwargs because the URL pattern includes it
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs.get('pk')})

# --- U: Update Comment View ---
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html' # Use a dedicated template for updating

    # Ensure only the author can update the comment
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    # Redirect back to the post detail page after updating
    def get_success_url(self):
        # The post's pk is retrieved from the comment instance's post field
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

# --- D: Delete Comment View ---
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    context_object_name = 'comment'

    # Ensure only the author can delete the comment
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    # Redirect to the post detail page after deletion
    def get_success_url(self):
        # The post's pk is retrieved from the comment instance's post field
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

# ----------------------------------------------------
#               AUTHENTICATION VIEWS (EXISTING)
# ----------------------------------------------------

# Custom Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            # Success message to display after redirection
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login') # Redirect to the login page after successful registration
    else:
        form = UserRegisterForm()

    return render(request, 'blog/register.html', {'form': form})

# Profile View (Requires user to be logged in)
@login_required 
def profile(request):
    # Implement logic for editing profile details here (Step 4)
    # For now, it just renders the profile template.
    return render(request, 'blog/profile.html')