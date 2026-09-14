from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('podcasts/', views.podcast_list, name='podcast_list'),
    path('podcasts/<int:id>/', views.podcast_detail, name='podcast_detail'),
    path('episodes/<int:id>/', views.episode_detail, name='episode_detail'),
    path('podcasts/<int:id>/review/', views.add_review, name='add_review'),
    path('podcasts/<int:id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('search/', views.search, name='search'),
    path('delete/<int:podcast_id>/', views.delete_podcast, name='delete_podcast'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
]