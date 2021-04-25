from django.urls import path
from . import views

urlpatterns = [
	path('', views.apiOverview, name="api-overview"),
	path('upload-cve/', views.uploadCve, name="upload-cve"),
]