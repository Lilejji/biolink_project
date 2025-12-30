from django.urls import path
from django.contrib.auth import views as auth_views
from .views import ProfileDetailView, SignUpView, DashboardView, EditProfileView, add_link, delete_link, reorder_links

urlpatterns = [
    # --- SPECIFIC PAGES MUST BE FIRST ---
    
    # User Auth & Dashboard
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='links/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile'),
    
    # Link Actions
    path('add-link/', add_link, name='add_link'),
    path('delete-link/<int:link_id>/', delete_link, name='delete_link'),

    # --- GENERIC PROFILE CATCH-ALL MUST BE LAST ---
    # This only runs if none of the above match
    path('<slug:slug>/', ProfileDetailView.as_view(), name='profile'),
    path('reorder-links/', reorder_links, name='reorder_links'),
]