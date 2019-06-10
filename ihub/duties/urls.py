from django.contrib import admin
from django.urls import path, include
from .views import (
    duty_api_start_view, duty_api_detail_view
)

app_name = 'duties'

api_urlpath = [
    path('create/', duty_api_start_view, name='duty-create'),
    path('details/', duty_api_detail_view, name='duty-details'),
]

urlpatterns = [
    # path('', include(page_urlpath)),
    path('api/', include(api_urlpath)),
]
