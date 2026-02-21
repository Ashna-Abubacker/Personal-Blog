
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Profile
from .forms import ProfileForm

@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    posts = request.user.blog_set.all()  # adjust 'blog_set' if your related_name is different

    context = {
        'profile': profile,
        'posts': posts,
    }
    return render(request, 'dashboard/profile.html')
@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    posts = request.user.posts.all()
  
    return render(request, 'dashboard/profile.html', {'profile': profile, 'user': request.user, 'posts': posts})


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
            user=request.user
        )

        if form.is_valid():
            form.save()
            return redirect('accounts:profile')

    else:
        form = ProfileForm(
            instance=profile,
            user=request.user
        )

    return render(request, 'dashboard/edit_profile.html', {
        'form': form
    })


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # keep user logged in
            messages.success(request, 'Password updated successfully.')
            return redirect('accounts:profile')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'dashboard/change_password.html', {'form': form})


@login_required
def delete_account(request):
    if request.method == "POST":
        request.user.delete()
        return redirect('/')
    
    return render(request, 'dashboard/delete_account.html')
