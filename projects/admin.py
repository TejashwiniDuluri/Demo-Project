# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Project)
admin.site.register(Milestone)
admin.site.register(RegisteredProject)
admin.site.register(ProjectTest)
admin.site.register(ProjectQuestion)
admin.site.register(ProjectAnswer)
admin.site.register(ProjectTestResult)
admin.site.register(ProjectAssignment)
admin.site.register(RegisteredMilestone)
admin.site.register(Tagging)
