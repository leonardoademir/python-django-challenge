from django.urls import path

from heyurl import views

urlpatterns = [
    path('', views.index, name='index'),
    path('u/<short_url>', views.short_url, name='short_url'),
    path('store', views.store, name='store'),
]
