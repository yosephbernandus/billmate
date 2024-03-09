from django.db import connection
from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required


def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


@login_required
def index(request):
    rows = []
    user_id = request.user.id
    with connection.cursor() as cursor:
        cursor.execute("SELECT group_id, description, category FROM bill_group where auth_user_id = %s", [user_id])
        rows = dictfetchall(cursor)

    context = {
        "bill_groups": rows
    }

    return render(request, "bill_group/index.html", context)


@login_required
def create(request):
    if request.POST:
        category = request.POST.get('category')
        description = request.POST.get('description')
        user_id = request.user.id
        with connection.cursor() as cursor:
            utc_now = timezone.now()
            cursor.execute(
                "INSERT INTO bill_group (description, category, created_at, updated_at, auth_user_id) VALUES (%s, %s, %s, %s, %s) RETURNING *", [
                    description,
                    category,
                    utc_now,
                    utc_now,
                    user_id
                ]
            )
        return redirect('bill_group:index')

    return render(request, "bill_group/create.html")
