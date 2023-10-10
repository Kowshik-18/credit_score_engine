from django.urls import path
from . import views

urlpatterns = [
    # path('loan_prediction/', views.loan_prediction, name='loan_prediction'),
    path('upload_csv/', views.upload_csv_customer_info, name='upload_csv'),
    # path('success/', views.success, name='success'),
    path('transaction_history_csv/', views.transaction_history_csv, name='transaction_history_csv'),
    path('calculate_transaction_frequencies/', views.calculate_transaction_frequencies, name='calculate_transaction_frequencies'),
    # path('cv_calculation/', views.calculate_coefficient_of_variation, name='cv_calculation'),
   

]
