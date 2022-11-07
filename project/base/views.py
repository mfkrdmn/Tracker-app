from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
# Create your views here.
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference
import datetime


@login_required(login_url='/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'index.html', context)

@login_required(login_url='login')
def add_expense(request):

    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST #bunu html ve burada koymazsak biri eksik submit edildiğinde yazılan veriyi de
        #siliyor
    }
    if request.method == 'GET':
        return render(request, 'addexpense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount: #that means user didnt submşt amount
            messages.error(request, 'Amount is required')
            return render(request, 'addexpense.html', context)
        description = request.POST['description'] 
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description: #that means user didnt submşt description
            messages.error(request, 'Description is required')
            return render(request, 'addexpense.html', context)


        Expense.objects.create(owner=request.user, amount=amount, date=date,
                               category=category, description=description)
        messages.success(request, 'Expense saved successfully')

        return redirect('expenses')

@login_required(login_url='/authentication/login')
def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'edit-expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'edit-expense.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'edit-expense.html', context)

        expense.owner = request.user
        expense.amount = amount
        expense. date = date
        expense.category = category
        expense.description = description

        expense.save()
        messages.success(request, 'Expense updated  successfully')

        return redirect('expenses')

def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('expenses')
