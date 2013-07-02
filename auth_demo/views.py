from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from auth_demo.models import Member
import json

def home(request):
    login_member = request.session.get('login_member')
    return render_to_response('home.html', {'login_member': login_member})

def me(request):
    login_member = request.session.get('login_member')
    if login_member is None:
        return HttpResponseRedirect('/login')
    return render_to_response('me.html', {'login_member': login_member})

def register(request):
    if request.method == 'GET':
        return render_to_response('register.html', {})
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        passwordagain = request.POST.get('password2')

        if passwordagain != password:
            return render_to_response('register.html', {'alert':'passwords are not same'})
        # todo: data validation here

        m = Member()
        m.username = username
        m.password = password
        m.save()

        request.session['login_member'] = m
        return HttpResponseRedirect('/home')


def login(request):
    if request.method == 'GET':
        return render_to_response('login.html', {})
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            m = Member.objects.get(username=username)
        except ObjectDoesNotExist as e:
            return render_to_response('login.html', {'alert':'user does not exist'})

        if m.password != password:
            return render_to_response('login.html', {'alert':'password error'})

        request.session['login_member'] = m
        return HttpResponseRedirect('/home')

def json_response(dict):
    return HttpResponse(json.dumps(dict), mimetype="application/json")

def login_ajax(request):
    if request.method == 'GET':
        return render_to_response('login_ajax.html', {})
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username is None or username == '':
            return json_response({'result':'error', 'message':'plz input username'})
        elif password is None or password == '':
            return json_response({'result':'error', 'message':'plz input password'})

        try:
            m = Member.objects.get(username=username)
        except ObjectDoesNotExist as e:
            return json_response({'result':'error', 'message':'user does not exist'})

        if m.password != password:
            return json_response({'result':'error', 'message':'password error'})
        else:
            request.session['login_member'] = m
            return json_response({'result':'ok', 'message':'success'})

def logout(request):
    request.session['login_member'] = None
    return HttpResponseRedirect('/home')

