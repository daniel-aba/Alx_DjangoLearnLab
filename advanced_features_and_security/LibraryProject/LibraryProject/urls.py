# C:\Users\PPIS OUTLET\Documents\GITHUB REPOSITORY\Alx_DjangoLearnLab\advanced_features_and_security\LibraryProject\LibraryProject\urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # This line includes all URLs from your bookshelf app.
    # The 'bookshelf.urls' part tells Django where to find them.
    path('', include('bookshelf.urls')), 
]