from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import RegisterForm, LoginForm, CustomPasswordResetForm, CustomSetPasswordForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')  # Replace with your home URL
    else:
        form = RegisterForm()
    
    return render(request, 'auth/register.html', {'form': form})

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'auth/login.html'
    
    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super().form_valid(form)

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'auth/password_reset.html'
    email_template_name = 'auth/password_reset_email.html'
    subject_template_name = 'auth/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'auth/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')