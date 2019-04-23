# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random

from django.shortcuts import render, redirect
from random import randrange
from django.forms.models import model_to_dict
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import loader
from .forms import SomeForm
import sys
import StringIO
import contextlib
import json
from random import randrange,randint


# def compiler(request):
# 	context = {"form":SomeForm}
# 	template=loader.get_template('mirror/editor.html')
# 	return HttpResponse(template.render(context,request))


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

# def compileCode(code):
# 	return eval(code)

def pyExec(request):
	if request.method == "POST":
		with stdoutIO() as s:
			exec(request.POST.get("pyscript"))
		context = {"output":s.getvalue()}
		print context["output"]
		return JsonResponse(context)
	

	
		
	
def compiler(request):
	context = {}
	template=loader.get_template('mirror/editor.html')
	return HttpResponse(template.render(context,request))