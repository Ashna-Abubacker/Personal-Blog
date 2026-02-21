from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from blogs import views as BlogsView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home
    path('', views.home, name='home'),

    # Blog
    path('blogs/<slug:slug>/', BlogsView.blogs, name='blogs'),
    path('search/', BlogsView.search, name='search'),
    path('category/', include('blogs.urls')),

    # Register
    path('register/', views.register, name='register'),

    # Login / Logout
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # Password Change
    path(
        'password-change/',
        auth_views.PasswordChangeView.as_view(
            template_name='change_password.html',
            success_url='/'
        ),
        name='password_change'
    ),

    # Dashboard
    path('dashboard/', include('dashboard.urls')),

    # Accounts app
    path('accounts/', include('accounts.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

