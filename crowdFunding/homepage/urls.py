from homepage.views import (projectSearchView, products_index)
from django.urls import path

urlpatterns = [
    path('', products_index, name='products.index'),
    path('search', projectSearchView.as_view(), name='projects.search')
]
