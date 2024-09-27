from events.views import *
from django.urls import path


urlpatterns = [
    path('', EVENTSVIEW.as_view(),name='events_post_get'),
    path('<str:id>/', EVENTSVIEW.as_view(),name='events_put_delete'),
    path('contestants/data/', ContestantView.as_view(),name='contestants'),
    path('contestants/data/<str:id>/', ContestantView.as_view(),name='contestants'),
    path('contestants/select_prime_contestant_image/<str:id>/', select_prime_contestant_image,name='select_prime_contestant_image'),
    path('votes/post/', Vote.as_view(),name='vote'),
    
]
