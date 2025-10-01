from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required # For profile view
from .forms import UserRegisterForm # Import the custom form

def home(request):
    posts = Post.objects.all().order_by('-published_date')
    return render(request, 'blog/home.html', {'posts': posts})

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