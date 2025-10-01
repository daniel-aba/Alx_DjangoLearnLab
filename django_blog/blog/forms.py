from django.contrib.auth.forms import UserCreationForm

# Custom form to ensure email is handled during registration,
# though Django's User model doesn't require it to be unique by default.
class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

