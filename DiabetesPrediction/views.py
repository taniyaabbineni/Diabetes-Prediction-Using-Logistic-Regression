# code
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponse, Http404, HttpResponseRedirect


from django.shortcuts import render
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# for call home.html
def home(request):
	return render(request, 'home.html')

# for call predict.html
def predict(request):
	return render(request, 'predict.html')

# for display result on same page
def result(request):
        data = pd.read_csv(r"diabetes.csv")
        X = data.drop("Outcome", axis=1)
        Y = data["Outcome"]

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

        model = LogisticRegression()
        model.fit(X_train, Y_train)

        val1 = float(request.GET['n1'])
        val2 = float(request.GET['n2'])
        val3 = float(request.GET['n3'])
        val4 = float(request.GET['n4'])
        val5 = float(request.GET['n5'])
        val6 = float(request.GET['n6'])
        val7 = float(request.GET['n7'])
        val8 = float(request.GET['n8'])
        pred = model.predict([[val1, val2, val3,val4, val5, val6, val7, val8]])

        result1 = ""
        if pred == [1]:
            result1 = "<span style='color: red;'>Oops! You have TYPE 1 DIABETES...</span>"
        elif pred == [2]:  # Type 2 Diabetes
            result1 = "<span style='color: blue;'>Oops! You have TYPE 2 DIABETES...</span>"
        else:
            result1 = "<span style='color: green;'>Great! You DON'T have diabetes...</span>"

        return render(request, "predict.html", {"result2": result1})

def register(request):
    
    if request.method=='POST':
        username = request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        
        user=User.objects.create_user(username=username,email=email,password=password)
        user.save()

        return redirect('home')

    return render(request,'register.html')




def login_user(request):
    
    if request.method =='POST':
        username=request.POST['username']
        password=request.POST['pwd']
        
        user=authenticate(username=username,password=password) 
        
        if user is not None:
            login(request,user)
            
            return redirect('home')
        
        else:
        
            return render(request,'login.html') 
            
    return render(request,'login.html')   

def logout_user(request):
    logout(request)
    
    return redirect('home')