from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from auth_demo.models import Member
import json
from utils.redirect_utils import RedirectUtils

LOGIN_REDIRECT_URL_KEY = 'k_login_redirect_url'

def home(request):
    login_member = request.session.get('login_member')
    return render_to_response('home.html', {'login_member': login_member})


def me(request):
    login_member = request.session.get('login_member')
    if login_member is None:
        RedirectUtils.set_url_to_redirect(request, '/me', LOGIN_REDIRECT_URL_KEY)
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
            return render_to_response('register.html', {'alert': 'passwords are not same'})

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
        except ObjectDoesNotExist:
            return render_to_response('login.html', {'alert': 'user does not exist'})

        if m.password != password:
            return render_to_response('login.html', {'alert': 'password error'})

        request.session['login_member'] = m

        if RedirectUtils.need_redirect(request, LOGIN_REDIRECT_URL_KEY):
            redirect_url = RedirectUtils.redirect_url(request, LOGIN_REDIRECT_URL_KEY)
            RedirectUtils.remove_redirect_url(request, LOGIN_REDIRECT_URL_KEY)
        else:
            redirect_url = '/home'
        return HttpResponseRedirect(redirect_url)


def json_response(json_string):
    return HttpResponse(json.dumps(json_string), mimetype="application/json")


def login_ajax(request):
    if request.method == 'GET':
        return render_to_response('login_ajax.html', {})
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username is None or username == '':
            return json_response({'result': 'error', 'message': 'plz input username'})
        elif password is None or password == '':
            return json_response({'result': 'error', 'message': 'plz input password'})

        try:
            m = Member.objects.get(username=username)
        except ObjectDoesNotExist:
            return json_response({'result': 'error', 'message': 'user does not exist'})

        if m.password != password:
            return json_response({'result': 'error', 'message': 'password error'})
        else:
            request.session['login_member'] = m
            return json_response({'result': 'ok', 'message': 'success'})


def logout(request):
    request.session['login_member'] = None
    return HttpResponseRedirect('/home')
