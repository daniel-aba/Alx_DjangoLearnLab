from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # ⬅️ Permissions
from .models import Post
from .forms import PostForm # We will create this in Step 2
from django.contrib.auth.decorators import login_required

# --- R: Read (List View) ---
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-published_date'] # Order by newest first

# --- R: Read (Detail View) ---
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

# --- C: Create View ---
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    form_class = PostForm # Use our custom ModelForm

    # Override form_valid to automatically set the post author to the logged-in user
    def form_valid(self, form):
        form.instance.author = self.request.user # Set the author field
        return super().form_valid(form)

    # Optional: Set success URL (or define get_absolute_url in the Post model)
    success_url = '/' # Redirect to the home page after creation

# --- U: Update View ---
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    form_class = PostForm

    # Override test_func to ensure only the author can update the post
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    # Optional: Set success URL
    success_url = '/' 

# --- D: Delete View ---
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/' # Redirect to home/list view after deletion

    # Override test_func to ensure only the author can delete the post
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

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