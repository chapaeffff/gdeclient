from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # ex: /scanner/2/
    path('<int:city_id>/', views.search, name='search'),
    # ex: /polls/5/results/
    path('<int:city_id>/results/', views.results, name='results'),
]