from django.db import connection
from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, redirect
from bill_group.utils import create_public_group_link
from base.utils import dictfetchall

from django.contrib.auth.decorators import login_required


@login_required(login_url="")
def create(request):
    return render(request, "bill/create.html")
