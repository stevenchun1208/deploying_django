from django.shortcuts import render
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import Friendships
from ..lnr.models import User
from django.db.models import Count

# Create your views here.
def pokes(request):
    if request.session['email']:
        currentUser = User.objects.get(email = request.session['email'])
        users = User.objects.all()
        poked = Friendships.objects.filter(friendpoked__email = request.session['email']).values('user').annotate(count = Count('user__id'))
        pokedsort = Friendships.objects.filter(friendpoked__email = request.session['email']).values('user__name').annotate(count = Count('user')).order_by('-count')
        pokehistory = Friendships.objects.all().values('friendpoked__id').annotate(count = Count('user'))
        context = {
            'name' : currentUser.name,
            'email': currentUser.email,
            'users': users,
            'poked': poked,
            'pokedsort': pokedsort,
            'pokehistory': pokehistory
        }
        return render(request, "blackbelt_app/poke.html", context)
    else:
        return redirect(reverse('home'))


def poked(request, id):
    currentUser = User.objects.get(email = request.session['email'])
    friendpoked = User.objects.get(id = id)
    Friendships.objects.create(user = currentUser, friendpoked = friendpoked)
    return redirect(reverse('pokes'))

def logout(request):
    request.session['email'] = ''
    return redirect(reverse('home'))
