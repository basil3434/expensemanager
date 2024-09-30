"""
URL configuration for ExpenseManager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # category
    path('category/add/',views.CategoryCreateView.as_view(), name="cat-add"),
    path('category/list/',views.CategoryListView.as_view(), name="cat-list"),
    path('category/<int:pk>/change/',views.CategoryUpdateView.as_view(), name="cat-edit"),
    path('category/<int:pk>/remove/',views.CategoryDeleteView.as_view(), name="cat-delete"),
    # transaction
    path('transaction/add/',views.TransactionCreateView.as_view(), name='tran-add'),
    path('transaction/list/',views.TransactionListView.as_view(), name="tran-list"),    #to list entire transactions
    path('transaction/<int:pk>/change/',views.TransactionUpdateView.as_view(), name="tran-edit"),
    path('transaction/<int:pk>/remove/',views.TransactionDeleteView.as_view(), name="tran-delete"),
    path('transaction/summary/',views.TransactionSummaryView.as_view(), name="tran-summary"),
    # expense summary
    path('expense/summary/', views.ExpenseSummaryView.as_view(), name="exp-summary"),
    # chart
    path('chart/', views.ChartView.as_view(), name="chart"),
    # registration and login 
    path('registration/', views.SignUpView.as_view(), name="signup"),
    path('', views.SignInView.as_view(), name="signin"),
    path('signout/', views.SignOutView.as_view(), name="signout"),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
