from django.db import connection
from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def add_participant(request, group_id):
    if request.POST:
        name = request.POST.get('name')
        with connection.cursor() as cursor:
            utc_now = timezone.now()
            cursor.execute(
                "INSERT INTO participant (name, created_at, updated_at, group_id) VALUES (%s, %s, %s, %s) RETURNING *", [
                    name,
                    utc_now,
                    utc_now,
                    group_id
                ]
            )
        return redirect('bill_group:index')


    context = {
        'group_id': group_id,
    }
    return render(request, "participant/create.html", context)
