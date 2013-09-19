# Create your views here.
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType
from login.models import MenuItem
from login.form import LoginField
from datetime import datetime

def getPerms():
    permsid = ContentType.objects.get(app_label='auth', model='User')
    permstype = Permission.objects.filter(content_type_id=perms.pk).exclude(codename__contains='user')
    return ['auth.'+str(a.codename) for a in permstype]

def getRole(group):
    for roleTp in ['unrestricted','guest','student','ta','headta','faculty','administrator']:
        if group == Group.objects.get(name=roleTp):
            return roleTp
    return None

def userLogin(request):
#    if request.user.is_authenticated():
#        return HttpResponseRedirect('/main/')
    if request.method == 'POST':
        form = LoginField(request.POST)
        if form.is_valid():
            usr = form.cleaned_data['username']
            pwd = form.cleaned_data['password']
            user = authenticate(username=usr,password=pwd)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/main/')
            else:
                return render_to_response('login/login.html',{'form':form,},context_instance=RequestContext(request))
        else:
            return render_to_response('login/login.html',{'form':form,},context_instance=RequestContext(request))
    else:
        form = LoginField()
        return render_to_response('login/login.html',{'form':form,},context_instance=RequestContext(request))

def userLogout(request):
    if request.user.is_authenticated():
        logout(request)
        return HttpResponseRedirect('/login/login.html')

def main(request):
    if request.user.is_authenticated():
        user_perms = list(request.user.get_all_permissions())
        items = []
        for a in user_perms:
            perm = str(a).split('.')[1]
            item = MenuItem.objects.filter(perm_id=Permission.objects.get(codename=perm).pk)
            items.extend(item)
            hour = datetime.now().hour
            if 0 <= hour < 5:
                greet = 'Good Night, '
            elif 5 <= hour < 12:
                greet = 'Good Morning, '
            elif 12 <= hour < 18:
                greet = 'Good Afternoon, '
            else:
                greet = 'Good Evening, '
        return render_to_response( 'login/main.html',
                {'offering':'Chemistry 2A',
                    'items':items,
                    'user':request.user,
                    'greet':greet,
                    },context_instance=RequestContext(request))

        #grp = request.user.groups.all()
        #return HttpResponse('Welcome %s' % str(request.user.username))

    else:
        return HttpResponseRedirect('/login/')
