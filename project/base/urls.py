from django import views
from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name = 'expenses'),
    path('addexpense', views.add_expense, name = 'addexpense'),
    path('expense_edit/<int:id>', views.expense_edit, name = 'expense_edit'),
    path('expense-delete/<int:id>', views.delete_expense, name = 'expense-delete'),

]
