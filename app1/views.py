import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

# Create your views here.
from app1.forms import TrainerForm, Product, AddBill, CustomerForm
from app1.models import Login, Equipments, Bill, Attendance


def home(request):
    return render(request, 'home.html')

#####################ADMIN###################
def admin_panel(request):
    return render(request, 'admintemp/admin_home.html')


def trainer_register(request):
    login_form = TrainerForm()
    if request.method == 'POST':
        login_form = TrainerForm(request.POST, request.FILES)
        if login_form.is_valid():
            user = login_form.save(commit=False)
            user.is_trainer = True
            user.save()
            messages.info(request, 'register successfully')
            return redirect('trainer_register')
    return render(request, 'admintemp/trainer_register.html', {'login_form': login_form})


def trainer_view(request):
    data = Login.objects.filter(is_trainer=True)
    return render(request, 'admintemp/trainer_view.html', {'data': data})


def trainer_update(request, id):
    data = Login.objects.get(id=id)
    if request.method == 'POST':
        form = TrainerForm(request.POST or None, request.files, instance=data)
        if form.is_valid():
            form.save()
            return redirect('trainer_view')
    else:
        form = TrainerForm(instance=data)
    return render(request, 'admintemp/trainer_update.html', {'form': form})


def trainer_delete(request, id):
    data = Login.objects.get(id=id)
    if request.method == 'POST':
        data.delete()
        return redirect('trainer_view')
    else:
        return redirect('trainer_view')


def equipments_add(request):
    data = Product()
    if request.method == 'POST':
        data = Product(request.POST, request.FILES)
        if data.is_valid():
            data.save()
            return redirect('equipments_view')
    return render(request, 'admintemp/equipments.html', {'data': data})


def equipments_view(request):
    data = Equipments.objects.all()
    return render(request, 'admintemp/equipments_view.html', {'data': data})


def equipments_update(request, id):
    data = Equipments.objects.get(id=id)
    if request.method == 'POST':
        data = Product(request.POST or None, request.FILES, instance=data)
        if data.is_valid():
            data.save()
            return redirect('equipments_view')
    else:
        data = Product(instance=data)
    return render(request, 'admintemp/equipments_update.html', {'data': data})


def equipments_delete(request, id):
    data = Equipments.objects.get(id=id)
    if request.method == 'POST':
        data.delete()
        return redirect('equipments_view')
    else:
        return redirect('equipments_view')


def add_bill(request):
    card = AddBill()
    if request.method == 'POST':
        card = AddBill(request.POST)
        if card.is_valid():
            card.save()
            return redirect('add_bill')
    return render(request, 'admintemp/add_bill.html', {'card': card})


def view_bill(request):
    bill = Bill.objects.all()
    return render(request, 'admintemp/view_bill.html', {'bill': bill})


def customer_register(request):
    register_form = CustomerForm()
    if request.method == 'POST':
        register_form = CustomerForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.is_customer = True
            user.save()
            messages.info(request, 'register successfully')
            return redirect('customer_register')
    return render(request, 'customer_register.html', {'register_form': register_form})


def customer_view(request):
    data = Login.objects.filter(is_customer=True)
    return render(request, 'admintemp/customer_view.html', {'data': data})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_panel')
            elif user.is_trainer:
                return redirect('trainer_panel')
            elif user.is_customer:
                return redirect('customer_panel')
        else:
            messages.info(request, 'INVALID CREDENTIALS')
    return render(request, 'login.html')


#########################################TRAINER############################################
def trainer_panel(request):
    return render(request, 'trainerpanel/trainer_home.html')


def trainer_customer_view(request):
    data = Login.objects.filter(is_customer=True)
    return render(request, 'trainerpanel/trainer_customer_view.html', {'data': data})


#########################################CUSTOMER###################################################
def customer_panel(request):
    return render(request, 'customerpanel/customer_home.html')


def trainer_view_customer(request):
    data = Login.objects.filter(is_trainer=True)
    return render(request, 'customerpanel/trainer_view_customer.html', {'data': data})


def equipments_view_customer(request):
    data = Equipments.objects.all()
    return render(request, 'customerpanel/equipments_view_customer.html', {'data': data})


def user_customer_view(request):
    data = Login.objects.filter(is_customer=True)
    return render(request, 'customerpanel/user_customer_view.html', {'data': data})


def view_bill_customer(request):
    bill = Bill.objects.all()
    return render(request, 'customerpanel/view_bill_customer.html', {'bill': bill})


def add_attendance(request):
    customer = Login.objects.filter(is_customer=True)
    return render(request, 'admintemp/customer_list.html', {'customer': customer})


now = datetime.datetime.now()


def mark(request, id,):
    user = Login.objects.get(id=id)
    att = Attendance.objects.filter(name=user, date=datetime.date.today())
    if att.exists():
        messages.info(request, 'today attendance already marked')
        return redirect('add_attendance')
    else:
        if request.method =='POST':
            attndc = request.POST.get('attendance')
            print("h")
            Attendance(name=user, date=datetime.date.today(), attendance=attndc).save()
            messages.info(request, 'Attendance Added Successfully')
            return redirect('add_attendance')
        return render(request, 'mark_attendance.html')


def view_attendance(request):
    value_list = Attendance.objects.values_list('date', flat=True).distinct()
    attendance = {}
    for value in value_list:
        attendance[value] = Attendance.objects.filter(date=value)
    return render(request, 'admintemp/view_attendance.html', {'attendance': attendance})


def day_attendance(request, date):
    attendance = Attendance.objects.filter(date=date)
    context = {
        'attendance': attendance,
        'date': date
    }
    return render(request, 'admintemp/day_attendance.html', context)