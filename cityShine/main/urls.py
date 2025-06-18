from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('issues/create/', views.create_issue, name='create_issue'),
    path('issues/<int:pk>/', views.issue_detail, name='issue_detail'),
    path('issues/my/', views.my_issues, name='my_issues'),
    path('issues/map/', views.issues_map, name='issues_map'),
    path('field-staff/dashboard/', views.field_staff_dashboard, name='field_staff_dashboard'),
    path('officer/dashboard/', views.officer_dashboard, name='officer_dashboard'),
    path('officer/analytics/', views.analytics, name='analytics'),
    path('issues/<int:pk>/update-status/', views.update_issue_status, name='update_issue_status'),
]