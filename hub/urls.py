from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # --- Home Page ---
    path('', views.home, name='home'),

    # --- Authentication ---
    path('login/', auth_views.LoginView.as_view(template_name='hub/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/influencer/', views.influencer_signup, name='influencer_signup'),
    path('signup/brand/', views.brand_signup, name='brand_signup'),
    
    # --- Profile & Dashboard ---
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/', views.profile_view, name='profile_view'),
    
    # 🚨 SMART DASHBOARD: No .as_view() because these are now functions!
    path('dashboard/', views.dashboard, name='dashboard'),
    path('brand/dashboard/', views.dashboard, name='brand_dashboard'),

    # --- Campaign & Gigs ---
    path('brand/campaign/new/', views.CampaignCreateView.as_view(), name='campaign_create'),
    path('feed/', views.CampaignFeedView.as_view(), name='campaign_feed'),
    path('campaign/<int:pk>/apply/', views.apply_to_campaign, name='apply_to_campaign'),
    path('campaign/<int:pk>/applicants/', views.campaign_applicants, name='campaign_applicants'),
    path('application/<int:pk>/status/<str:status>/', views.update_application_status, name='update_application_status'),
]