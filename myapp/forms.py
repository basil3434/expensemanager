from django import forms
from myapp.models import Category, Transactions
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CategoryForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        self.user=kwargs.pop("user")
        return super().__init__(*args,**kwargs)
    
    class Meta:

        model=Category
        fields=[
            "name",
            "budget",
            "image",
            ]
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control mb-3"}),
            "budget":forms.NumberInput(attrs={"class":"form-control mb-3"}),
            "image":forms.FileInput(attrs={"class":"form_control"})
        }
    
    def clean(self):
        self.cleaned_data=super().clean()
        budget_amount=self.cleaned_data.get("budget")
        if budget_amount<150:
            self.add_error("budget","budget amount should be grater than 150")
        return self.cleaned_data
        
        # if not self.instance.pk:
        #     # create block
        #     is_exist = Category.objects.filter(name__iexact = category_name,owner=owner).exists()

        #     if is_exist:

        #         self.add_error("name","Category already exists !!!")
        # else:
        #     # edit block
        #     is_exist = Category.objects.filter(name__iexact = category_name,owner=owner).exclude(pk = self.instance.pk).exists()

        #     if is_exist:

        #         self.add_error("name","Category already exists !!!")
        # return self.cleaned_data




class TransactionForm(forms.ModelForm):

    class Meta:

        model=Transactions
        fields=[
            "title",
            "amount",
            "category_option",
            "payment_method",
        ]
        widgets={
            "title":forms.TextInput(attrs={"class":"form-control mb-3"}),
            "amount":forms.NumberInput(attrs={"class":"form-control mb-3"}),
            "category_option":forms.Select(attrs={"class":"form-control form-select mb-3"}),
            "payment_method":forms.Select(attrs={"class":"form-control form-select mb-3"}),
        }
        


class TransactionFilterForm(forms.Form):
    start_date=forms.DateField(widget=forms.DateInput(attrs={"type":"date", "class":"form-control"}))
    end_date=forms.DateField(widget=forms.DateInput(attrs={"type":"date", "class":"form-control"}))



class RegistrationForm(UserCreationForm):

    password1=forms.CharField(widget=forms.PasswordInput(attrs=("class":"form-control mb-2")))
    password2=forms.CharField(widget=forms.PasswordInput(attrs=("class":"form-control mb-2")))

    class Meta:

        model=User
        fields=["username", "email", "password1", "password2"]
        widgets={
            "username":forms.TextInput(attrs=("class":"form-control"))
            "email":forms.TextInput(attrs=("class":"form-control"))
        }
        



class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-3"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control mb-3"}))