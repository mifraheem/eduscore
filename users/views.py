from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

User = get_user_model()

# -------------------------------
# REGISTER VIEW
# -------------------------------
def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')

        # --- Validation ---
        if not email or not password1 or not password2:
            messages.error(request, "All fields are required.")
            return redirect('register')

        if password1 != password2:
            messages.warning(request, "Passwords do not match.")
            return redirect('register')

        if len(password1) < 6:
            messages.warning(request, "Password must be at least 6 characters long.")
            return redirect('register')

        try:
            if User.objects.filter(email=email).exists():
                messages.error(request, "An account with this email already exists.")
                return redirect('register')

            user = User.objects.create_user(
                email=email,
                password=password1,
                first_name=first_name,
                role=role
            )
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')

        except IntegrityError:
            messages.error(request, "Something went wrong. Please try again.")
            return redirect('register')

    return render(request, 'auth/register.html')

# -------------------------------
# LOGIN VIEW
# -------------------------------
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}!")
            if user.role == 'teacher':
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'auth/login.html')

# -------------------------------
# LOGOUT VIEW
# -------------------------------
@login_required
def logout(request):
    auth_logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')
