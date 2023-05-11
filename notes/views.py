from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from datetime import date

# Create your views here.
def Home(request):
    return render(request, 'index.html')

def About(request):
    return render(request, 'about.html')
def Contact(request):
    return render(request, 'contact.html')


def Login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['emailid']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user:
            login(request, user)
            error = "yes"
        else:
            error = "not"
    d = {'error': error}
    return render(request,'login.html',d)

def Login_Admin(request):
    error = False
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user.is_staff:
            login(request, user)
            return redirect('admin_home')
        else:
            error = True
    d = {'error': error}
    return render(request, 'login_admin.html', d)


def Signup1(request):
    error = False
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['emailid']
        p = request.POST['password']
        con = request.POST['contact']
        b = request.POST['branch']
        r = request.POST['role']
        user = User.objects.create_user(username=u, password=p, first_name=f,last_name=l)
        Signup.objects.create(user=user,contact=con,branch=b,role=r)
        error = True
    d = {'error':error}
    return render(request, 'signup.html',d)


def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    pro = Signup.objects.get(user=user)
    d={'pro':pro,'user':user}
    return render(request,'profile.html',d)

def Edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error = False
    user=User.objects.get(id=request.user.id)
    pro = Signup.objects.get(user=user)
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        con = request.POST['contact']
        b = request.POST['branch']
        pro.user.username=u
        user.first_name=f
        user.last_name=l
        pro.contact=con
        pro.branch = b
        pro.save()
        pro.user.save()
        user.save()
        error = True
    d = {'error':error,'pro':pro}
    return render(request, 'edit_profile.html',d)


def Change_Password(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    error = ""
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error = "yes"
        else:
            error = "not"
    d = {'error':error}
    return render(request,'change_password.html',d)

def Logout(request):
    logout(request)
    return redirect('home')

def Delete_Mynotes(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')
    if Notes.objects.filter(id=pid).exists():
        notes = Notes.objects.get(id=pid)
        notes.delete()
        message1 = messages.info(request, 'Notes Deleted')
        return redirect('view_mynotes')

def View_Mynotes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    #profile = Signup.objects.get(user=user)
    notes = Notes.objects.filter(user=user)
    d = {'notes': notes}
    return render(request, 'view_mynotes.html', d)

def ViewAllnotesuser(request):
    if not request.user.is_authenticated:
        return redirect('login')
    notes = Notes.objects.all()
    d = {'notes': notes}
    return render(request, 'viewallnotesuser.html', d)

def Upload_Notes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error = ""
    if request.method=="POST":
        b = request.POST['branch']
        s = request.POST['subject']
        n = request.FILES['notesfile']
        f = request.POST['filetype']
        des = request.POST['description']
        ct = User.objects.filter(username=request.user.username).first()
        try:
            Notes.objects.create(user=ct,uploadingdate=date.today(),branch=b, subject=s, notesfile=n, filetype=f,description=des,status='pending')
            error = "no"
        except:
            error = "yes"
    d = {'error':error}
    return render(request, 'upload_notes.html', d)


def Admin_Home(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Notes.objects.all()
    reject =0
    pending = 0
    accept = 0
    all=0
    for i in notes:
        if i.status == "pending":
            pending+=1
        elif i.status == "Accept":
            accept+=1
        elif i.status == "Reject":
            reject+= 1
        all += 1

    d = {'pending':pending,'reject':reject,'accept':accept,'all':all}
    return render(request,'admin_home.html',d)


def Delete_Users(request, pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('view_users')

def View_Users(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    users = Signup.objects.all()
    d = {'users': users}
    return render(request, 'View_Users.html', d)


def Delete_Notes(request, pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    if Notes.objects.filter(id=pid).exists():
        notes = Notes.objects.get(id=pid)
        notes.delete()
        message1 = messages.info(request, 'Notes Deleted')
        return redirect('view_allnotes')

def view_pendingnotes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    notes = Notes.objects.all()
    d = {'notes': notes}
    return render(request, 'view_pendingnotes.html', d)

def viewacceptednotes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    notes = Notes.objects.all()
    d = {'notes': notes}
    return render(request, 'viewacceptednotes.html', d)

def view_allnotes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    notes = Notes.objects.all()
    d = {'notes': notes}
    return render(request, 'view_allnotes.html', d)

def view_rejectednotes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    notes = Notes.objects.all()
    d = {'notes': notes}
    return render(request, 'view_rejectednotes.html', d)

def Edit_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Notes.objects.get(id=pid)
    error=False
    if request.method == "POST":
        n = request.POST['book']
        s = request.POST['status']
        notes.id = n
        notes.status = s
        notes.save()
        error=True
    d = {'notes': notes,'error':error}
    return render(request, 'status.html', d)
