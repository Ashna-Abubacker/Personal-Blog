from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from blogs.models import Blog, Category
from accounts.models import Profile
from accounts.forms import ProfileForm
from .forms import AddUserForm, BlogPostForm, CategoryForm, EditUserForm

# Dashboard Overview
@login_required(login_url='login')
def dashboard(request):
    category_count = Category.objects.count()
    blogs_count = Blog.objects.filter(author=request.user).count()
    context = {
        'category_count': category_count,
        'blogs_count': blogs_count,
    }
    return render(request, 'dashboard/dashboard.html', context)


# ----------------------------
# Category Views
# ----------------------------
@login_required(login_url='login')
def categories(request):
    categories = Category.objects.all()
    return render(request, 'dashboard/categories.html', {'categories': categories})

@login_required(login_url='login')
def add_category(request):
    form = CategoryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Category added successfully.")
        return redirect('dashboard:categories')
    return render(request, 'dashboard/add_category.html', {'form': form})

@login_required(login_url='login')
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Category updated successfully.")
        return redirect('dashboard:categories')
    return render(request, 'dashboard/edit_category.html', {'form': form, 'category': category})

@require_POST
@login_required(login_url='login')
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, "Category deleted successfully.")
    return redirect('dashboard:categories')


# ----------------------------
# Blog Post Views
# ----------------------------
@login_required(login_url='login')
def posts(request):
    posts = Blog.objects.filter(author=request.user)
    return render(request, 'dashboard/posts.html', {'posts': posts})

@login_required(login_url='login')
def add_post(request):
    form = BlogPostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        post.slug = slugify(post.title) + '-' + str(post.id)
        post.save()
        messages.success(request, "Post added successfully.")
        return redirect('dashboard:posts')
    return render(request, 'dashboard/add_post.html', {'form': form})

@login_required(login_url='login')
def edit_post(request, pk):
    post = get_object_or_404(Blog, pk=pk, author=request.user)
    form = BlogPostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.slug = slugify(post.title) + '-' + str(post.id)
        post.save()
        messages.success(request, "Post updated successfully.")
        return redirect('dashboard:posts')
    return render(request, 'dashboard/edit_post.html', {'form': form, 'post': post})

@require_POST
@login_required(login_url='login')
def delete_post(request, pk):
    post = get_object_or_404(Blog, pk=pk, author=request.user)
    post.delete()
    messages.success(request, "Post deleted successfully.")
    return redirect('dashboard:posts')


# ----------------------------
# Profile Views
# ----------------------------
@login_required(login_url='login')
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    posts = Blog.objects.filter(author=request.user)
    return render(request, 'dashboard/profile.html', {
        'user': request.user,
        'profile': profile,
        'posts': posts
    })

@login_required(login_url='login')
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('dashboard:profile')
    return render(request, 'dashboard/edit_profile.html', {'form': form})

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password updated successfully.")
            return redirect('dashboard:profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'dashboard/change_password.html', {'form': form})

@login_required(login_url='login')
def delete_account(request):
    if request.method == "POST":
        request.user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('/')
    return render(request, 'dashboard/delete_account.html')


# ----------------------------
# User Management (Staff Only)
# ----------------------------
@staff_member_required(login_url='login')
def users(request):
    users = User.objects.all()
    return render(request, 'dashboard/users.html', {'users': users})

@staff_member_required(login_url='login')
def add_user(request):
    form = AddUserForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "User added successfully.")
        return redirect('dashboard:users')
    return render(request, 'dashboard/add_user.html', {'form': form})

@staff_member_required(login_url='login')
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = EditUserForm(request.POST or None, instance=user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "User updated successfully.")
        return redirect('dashboard:users')
    return render(request, 'dashboard/edit_user.html', {'form': form})

@require_POST
@staff_member_required(login_url='login')
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect('dashboard:users')
