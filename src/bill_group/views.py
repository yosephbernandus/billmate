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
        cursor.execute("SELECT name, group_id, description, category FROM bill_group where auth_user_id = %s order by group_id desc", [user_id])
        rows = dictfetchall(cursor)

    context = {
        "bill_groups": rows
    }

    return render(request, "bill_group/index.html", context)


@login_required
def create(request):
    if request.POST:
        name = request.POST.get('name')
        category = request.POST.get('category')
        description = request.POST.get('description')
        user_id = request.user.id
        with connection.cursor() as cursor:
            utc_now = timezone.now()
            cursor.execute(
                "INSERT INTO bill_group (name, description, category, created_at, updated_at, auth_user_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *", [
                    name,
                    description,
                    category,
                    utc_now,
                    utc_now,
                    user_id
                ]
            )
        return redirect('bill_group:index')

    return render(request, "bill_group/create.html")


@login_required
def update(request, group_id):
    user_id = request.user.id
    if request.POST:
        name = request.POST.get('name')
        category = request.POST.get('category')
        description = request.POST.get('description')
        with connection.cursor() as cursor:
            utc_now = timezone.now()
            cursor.execute(
                "UPDATE bill_group SET name = %s, description = %s, category = %s, updated_at = %s WHERE auth_user_id = %s and group_id = %s RETURNING *", [
                    name,
                    description,
                    category,
                    utc_now,
                    user_id,
                    group_id,
                ]
            )
        return redirect('bill_group:index')

    row = {}
    with connection.cursor() as cursor:
        cursor.execute("SELECT group_id, name, description, category FROM bill_group where group_id = %s and auth_user_id = %s", [
            group_id, user_id
        ])
        row = cursor.fetchone()
        row = {
            'group_id': row[0],
            'name': row[1],
            'description': row[2],
            'category': row[3],
        }

    context = {
        'group': row,
    }

    return render(request, "bill_group/update.html", context)
