from django.shortcuts import render, redirect
from django.views.generic import View
from myapp.forms import CategoryForm, TransactionForm, TransactionFilterForm, RegistrationForm, LoginForm
from myapp.models import Category, Transactions
from django.utils import timezone
from django.db.models import Sum, Avg, Count
from datetime import timedelta, datetime
from django.contrib.auth import authenticate, login, logout
# Create your views here. 

# category
class CategoryCreateView(View):

    def get(self, request, *args,**kwargs):
        form_instance=CategoryForm(user=request.user)
        qs=Category.objects.filter(owner=request.user)
        return render(request,"category_add.html",{"form":form_instance,"categories":qs})
    
    def post(self, request,*args,**kwargs):
        form_instance=CategoryForm(request.POST,user=request.user,files=request.FILES)
        if form_instance.is_valid():
            form_instance.instance.owner=request.user
            cat_name=form_instance.cleaned_data.get("name")
            user_object=request.user
            is_excist=Category.objects.filter(name__iexact=cat_name,owner=user_object).exists()
            if is_excist:
                print("category aldready exist")
                return render(request,"category_add.html",{"form":form_instance,"message":"record exists"})
            else:
                form_instance.save()
                return redirect("cat-list")
        else:
            return render(request,"category_add.html",{"form":form_instance})



class CategoryListView(View):

    def get(self, request, *args, **kwargs):
        qs=Category.objects.all()
        return render(request,"category_list.html",{"categories":qs})



class CategoryUpdateView(View):

    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        category_object=Category.objects.get(id=id)
        form_instance=CategoryForm(instance=category_object)
        return render(request, "category_edit.html",{"form":form_instance})

    def post(self, request,*args,**kwargs):
        id=kwargs.get("pk")
        category_object=Category.objects.get(id=id)
        form_instance=CategoryForm(request.POST, instance=category_object)
        if form_instance.is_valid():
            form_instance.save()
            return redirect("cat-list")
        else:
            return render(request,"category_edit.html",{"form":form_instance})



class CategoryDeleteView(View):
    def get(self, request, *args, **kwargs):
        id=kwargs.get("pk")
        Category.objects.get(id=id).delete()
        return redirect("cat-list")      

# transactions
class TransactionCreateView(View):

    def get(self, request, *args, **kwargs):
        form_instance=TransactionForm()
        user_categories=Category.objects.filter(owner=request.user)
        return render(request,"transaction_add.html",{"form":form_instance,"user_categories":user_categories})
    
    def post(self, request, *args, **kwargs):
        form_instance=TransactionForm(request.POST)
        if form_instance.is_valid():
            form_instance.instance.owner=request.user
            form_instance.save()
            return  redirect("tran-list")
        else:
            return render(request,"transaction_add.html",{"form":form_instance})



class TransactionListView(View):


    def get(self, request, *args, **kwargs):
        # current_month=timezone.now().month
        # current_year=timezone.now().year
        # qs=Transactions.objects.filter(created_date__month=current_month, created_date__year=current_year)  #to list current month transaction data
        qs=Transactions.objects.all()   #to list all transaction data
        return render(request, "transaction_list.html",{"transactions":qs})
    


class TransactionUpdateView(View):

    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        transaction_object=Transactions.objects.get(id=id)
        form_instance=TransactionForm(instance=transaction_object)
        return render(request, "transaction_edit.html",{"form":form_instance})

    def post(self, request,*args,**kwargs):
        id=kwargs.get("pk")
        transaction_object=Transactions.objects.get(id=id)
        form_instance=TransactionForm(request.POST, instance=transaction_object)
        if form_instance.is_valid():
            form_instance.save()
            return redirect("tran-list")
        else:
            return render(request,"transaction_edit.html",{"form":form_instance})
        


class TransactionDeleteView(View):
    def get(self, request, *args, **kwargs):
        id=kwargs.get("pk")
        Transactions.objects.get(id=id).delete()
        return redirect("tran-list")      
    


# summary View
class ExpenseSummaryView(View):

    def get(self, request, *args, **kwargs):
        current_month=timezone.now().month
        current_year=timezone.now().year
        qs=Transactions.objects.filter(created_date__month=current_month, created_date__year=current_year,owner=request.user)
        total_expense=qs.values("amount").aggregate(total=Sum("amount"))
        category_summary=qs.values("category_option__name").annotate(total=Sum("amount"))
        payment_summary=qs.values("payment_method").annotate(total=Sum("amount"))
        data={
            "total_expense":total_expense.get("total"),
            "category_summary":category_summary,
            "payment_summary":payment_summary,
            }

        return render(request, "expense_summary.html", data)



class TransactionSummaryView(View):

    def get(self, request, *args, **kwargs):
        form_instance=TransactionFilterForm()
        if "start_date" in request.GET and "end_date" in request.GET:
            start_date=datetime.strptime(request.GET.get("start_date"), "%Y-%m-%d")
            end_date=datetime.strptime(request.GET.get("end_date"), "%Y-%m-%d")+timedelta(days=1)
            qs = Transactions.objects.filter(created_date__gte=start_date, created_date__lte=end_date)
            # start_date=request.GET.get("start_date")
            # end_date=request.GET.get("end_date")
            # qs=Transactions.objects.filter(created_date__range=(start_date, end_date))        
        else:
            current_month=timezone.now().month
            current_year=timezone.now().year 
            qs=Transactions.objects.filter(created_date__month=current_month, created_date__year=current_year)
        total_expense=qs.values("amount").aggregate(total=Sum("amount"))
        data={
            "total_expense":total_expense.get("total"),
            "transactions":qs, 
            "form":form_instance
            }
        return render(request, "transaction_summary.html", data)
    


class ChartView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "chart.html")
    

# Auth View
class SignUpView(View):

    def get(self, request, *args, **kwargs):
        form_instance=RegistrationForm()
        return render(request, "reg.html", {"form":form_instance})
    
    def post(self, request, *args, **kwargs):
        form_instance=RegistrationForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            print("-------------Successful-------------------------")
            return redirect("signin")
        else:
            print("-------------Unsuccessful------------------------")
            return render(request, "reg.html", {"form":form_instance})



class SignInView(View):

    def get(self, request, *args, **kwargs):
        form_instance=LoginForm()
        return render(request, "login.html",{"form":form_instance})
    
    def post(self, request, *args, **kwargs):
        form_instance=LoginForm(request.POST)
        if form_instance.is_valid():
            # data=form_instance.cleaned_data
            # user_name=data.get("username")
            # user_password=data.get("password")
            # user_object=authenticate(request, username=user_name, password=user_password)
            user_object=authenticate(request, **form_instance.cleaned_data)     # easy way were above 4 lines are not needed, Note that : only if the forms variable name is "username" and "password" if not the  above 4 lines need to be used and this line can be removed 
            if user_object:
                login(request, user_object)
                return redirect("exp-summary")
        return render(request, "login.html", {"form":form_instance})            # works as else for both "if" conditions
    


class SignOutView(View):
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("signin")