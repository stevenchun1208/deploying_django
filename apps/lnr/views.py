from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from .models import User
import bcrypt
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "blackbelt_app/index.html")

def processreg(request):
    request.session['email'] = request.POST['email']
    errors = []
    if len(request.POST['name'])<3:
        errors.append(("Name should be more than two letters", 'extra_tags="fnameerror"'))
    if len(request.POST['alias'])<3:
        errors.append(("Alias should be more than two letters", 'extra_tags="lnameerror"'))
    if str.isalpha(str(request.POST['alias'])) == False:
        errors.append(("Alias should only be in letters", 'extra_tags="lnameerror"'))
    if User.userManager.validateemail(request.POST['email']) == 'fail':
        errors.append(("Please enter valid email address", 'extra_tags="emailerror"'))
    if User.userManager.get(request.POST['email'])!="fail":
        errors.append(("This user already exists", 'extra_tags="usererror"'))
    if len(request.POST['password'])<8:
        errors.append(("Password should be no less than 8 characters!", 'extra_tags="pwerror"'))
    if request.POST['password'] != request.POST['confirmpw']:
        errors.append(("Password and the confirm PW should match!", 'extra_tags="cfpwerror"'))
    if User.userManager.date(request.POST['birthdate']) == 'fail':
        errors.append(("Birth date should be in mm/dd/yyyy format!", 'extra_tags="bdayerror"'))
    else:
        if User.userManager.datecheck(request.POST['birthdate']) == 'fail':
            errors.append(("Birth date should be from the past!", 'extra_tags="bdayerror"'))
    if len(errors) > 0:
        for error in errors:
            messages.error(request, error[0], error[1])
        return render(request,"blackbelt_app/index.html")
    else:
        User.objects.create(email = request.POST['email'])
        currentUser = User.objects.get(email = request.POST['email'])
        currentUser.name = request.POST['name']
        currentUser.alias = request.POST['alias']
        currentUser.password = User.userManager.cryptfy(request.POST['password'])
        currentUser.save()
        return redirect(reverse('pokes'))


def processlog(request):
    errors = []
    if User.userManager.get(request.POST['logemail'])=="fail":
        errors.append(("Incorrect username or password"))
    else:
        speciUser = User.objects.get(email = request.POST['logemail'])
        userPW = speciUser.password
        if not bcrypt.hashpw(request.POST['logpassword'].encode(), userPW.encode()) == userPW:
            errors.append(("Incorrect username or password"))
    if len(errors) > 0:
        context = {
            "error" : errors
        }
        return render(request,"blackbelt_app/index.html", context)
    else:
        request.session['email'] = speciUser.email
        return redirect(reverse('pokes'))
