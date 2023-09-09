
from django.urls import path
from . import views


app_name= 'teamview'
urlpatterns = [
    path('hitters/',views.HittersTeamView.as_view(),name="hteam"),
    path('pitchers/',views.PitchersTeamView.as_view(),name="pteam"),
    
]
