# urls.py
from django.conf.urls import url
from django.urls import path
from .views import ProjectListView, export_to_pdf, dashboard_view, project_detail, report_detail, \
    project_general_report, download_all_from_project, credentials_table, export_table_as_csv, export_general_report

urlpatterns = [
    path('projects/', ProjectListView.as_view(), name="projects"),
    path('projects/<int:pk>/', project_detail, name="project_detail"),
    path('projects/credentials/<int:pk>/', credentials_table, name="credentials_table"),
    path('projects/general_report/<int:pk>/', project_general_report, name="project_general_report"),
    path('projects/exports/<int:pk>/', download_all_from_project, name="export_all_from_project"),
    path('projects/exports/general_report/<int:pk>/', export_general_report, name="export_general_report"),
    # path('reports/', ReportListView.as_view()),
    path('reports/<int:pk>/', report_detail, name="report_detail"),
    path('reports/export/<int:pk>/', export_to_pdf, name="export_pdf"),
    path('reports/export/credentials/<int:pk>/', export_table_as_csv, name="export_credentials_csv"),
    path('', dashboard_view, name="dashboard"),
]