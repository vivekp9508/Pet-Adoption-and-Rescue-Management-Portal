from django.urls import path
from . import views
from .views import update_report_status

urlpatterns = [
    # Pages
    path('report/', views.report_form_page, name='report-form'),
    path('my-reports/', views.my_reports_page, name='my-reports'),
    path('list/', views.pet_list_page, name='pet-list'),
    path('search/', views.search_page, name='search'),
    path('admin-login/', views.admin_login_page, name='admin-login'),
    path('admin-dashboard/', views.admin_dashboard_page, name='admin-dashboard'),

    # APIs
    path('api/reports/', views.list_reports, name='api-list-reports'),
    path('api/reports/create/', views.create_report, name='api-create-report'),
    path('api/reports/mine/', views.my_reports, name='api-my-reports'),
    path('api/reports/search/', views.search_matching_pets, name='api-search'),
    path('api/admin/reports/', views.admin_all_reports, name='api-admin-reports'),
    path('api/admin/reports/<int:pk>/status/', views.update_report_status, name='api-update-status'),

    # Notification APIs
    path('api/notifications/', views.user_notifications, name='api-user-notifications'),
    path('api/notifications/read/', views.mark_user_notifications_read, name='api-mark-read'),
    path('api/admin/notifications/', views.admin_notifications, name='api-admin-notifications'),
    path('api/admin/notifications/read/', views.mark_notifications_read, name='api-admin-mark-read'),
]