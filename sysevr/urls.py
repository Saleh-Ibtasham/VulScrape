from django.urls import path
from . import views

urlpatterns = [
	path('', views.apiOverview, name="api-overview"),
	path('upload-code/', views.uploadCode, name="upload-code"),
	path('cve-list/sysevr/', views.sysevrlist, name="cve-list"),
	path('cve-list/vuldeepecker/', views.vuldeepeckerlist, name="cve-list"),
]