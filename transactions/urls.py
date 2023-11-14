from django.urls import path
from . import views

urlpatterns = [
    path('<str:address>/', views.get_transaction_data, name='get_transaction_data'),
]