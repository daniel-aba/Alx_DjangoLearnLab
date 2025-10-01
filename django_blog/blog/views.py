from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy 
from django.contrib import messages 
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.contrib.auth.decorators import login_required 
from django.db.models import Q # ⬅️ Import Q object for search

from .models import Post, Comment 
from .forms import PostForm, UserRegisterForm, CommentForm 

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
#               COMMENT VIEWS
# ----------------------------------------------------

# --- C: Create Comment View ---
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/post_detail.html' 

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        form.instance.post = post  # Set the associated post
        form.instance.author = self.request.user # Set the author
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.kwargs.get('pk')})

# --- U: Update Comment View ---
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html' 

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

# --- D: Delete Comment View ---
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    context_object_name = 'comment'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

# ----------------------------------------------------
#               TAGS AND SEARCH VIEWS (UPDATED)
# ----------------------------------------------------

# --- NEW: Tag Filter View (RENAMED to PostByTagListView) ---
class PostByTagListView(ListView): # ⬅️ RENAMED
    model = Post
    template_name = 'blog/post_list.html' # Use the existing list template
    context_object_name = 'posts'
    ordering = ['-published_date'] 

    # Filter posts by the tag slug passed in the URL
    def get_queryset(self):
        # ⬅️ FIX: Use 'tag_slug' as the variable name from the URL
        tag_slug = self.kwargs.get('tag_slug') 
        # Filter posts where the tags field contains the tag name (using __slug for better lookup)
        return Post.objects.filter(tags__slug__in=[tag_slug]).order_by('-published_date')

    # Add the tag name to the context for use in the template header
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ⬅️ FIX: Use 'tag_slug' in context as well (for reference)
        context['current_tag'] = self.kwargs.get('tag_slug')
        return context

# --- NEW: Search View ---
class SearchResultsListView(ListView):
    model = Post
    template_name = 'blog/search_results.html' # NEW template for results
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q') # Get the search query from the URL
        if query:
            # Use Q objects to search title, content, OR tags
            return Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct().order_by('-published_date')
        return Post.objects.none() # Return no results if query is empty

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context


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
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')