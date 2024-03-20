from django.db import connection
from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import render, redirect
from bill_group.utils import create_public_group_link
from base.utils import dictfetchall
from django.contrib import messages

from django.contrib.auth.decorators import login_required


@login_required(login_url="")
def index(request):
    rows = []
    user_id = request.user.id
    with connection.cursor() as cursor:
        cursor.execute("SELECT name, group_id, description, category FROM bill_group where auth_user_id = %s order by group_id desc", [user_id])
        all_groups = cursor.fetchall()

        for group in all_groups:
            public_link = create_public_group_link(group[1])
            data = {
                'name': group[0],
                'group_id': group[1],
                'description': group[2],
                'category': group[3],
                'public_link': public_link,
            }
            rows.append(data)

    context = {
        "bill_groups": rows
    }

    return render(request, "bill_group/index.html", context)


@login_required(login_url="")
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


@login_required(login_url="")
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


@login_required(login_url="")
def bill_index(request, group_id):
    user_id = request.user.id
    participants = []

    bills = []
    with connection.cursor() as cursor:
        cursor.execute(
            "select p.participant_id, p.name from participant p join bill_group bg on bg.group_id = p.group_id where p.group_id = %s and bg.auth_user_id = %s",
            [group_id, user_id]
        )
        participants = dictfetchall(cursor)

        cursor.execute(
            "select b.bill_id, b.name, b.sub_total_bill, b.total_bill, b.description from bill b join bill_group bg on bg.group_id = b.group_id where b.group_id = %s and bg.auth_user_id = %s",
            [group_id, user_id]
        )
        bills = dictfetchall(cursor)

    context = {
        'group_id': group_id,
        'participants': participants,
        'bills': bills,
    }
    return render(request, "bill_group/bill_index.html", context)


def group_index(request, hash_ids: str):
    # TODO: Will add this later
    return render(request, "bill_group/index.html")


@login_required(login_url="")
def add_bill(request, group_id):
    user_id = request.user.id

    if request.POST:
        # TODO: Add condition to check group_id is related to user_id or not

        name = request.POST.get('name')
        subtotal = request.POST.get('subtotal')
        total = request.POST.get('total')
        tax = request.POST.get('tax')
        fee = request.POST.get('fee')
        discount = request.POST.get('discount')
        description = request.POST.get('description')
        paid_by = request.POST.get('paid_by')
        participant_ids = request.POST.getlist('participants')

        utc_now = timezone.now()

        bill_id = None
        query = """
        INSERT INTO bill (name, sub_total_bill, total_bill, tax_rate, fee_rate, discount_rate, description, group_id, paid_by_participant_id, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING bill_id
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [
                name, subtotal, total, tax, fee, discount, description, group_id, paid_by, utc_now, utc_now
            ])
            bill_id = cursor.fetchone()
            bill_id = bill_id[0]

            delete_query = "DELETE from bill_participant_owes where bill_id = %s"
            cursor.execute(delete_query, [bill_id])

            insert_data = [(bill_id, participant_id) for participant_id in participant_ids]
            insert_query = """
            INSERT INTO bill_participant_owes (bill_id, participant_id)
            VALUES (%s, %s)
            """
            cursor.executemany(insert_query, insert_data)

        return redirect(reverse('bill_group:group_bill_index', kwargs={'group_id': group_id}))

    participants = []
    with connection.cursor() as cursor:
        cursor.execute(
            "select p.participant_id, p.name, p.group_id from participant p join bill_group bg on bg.group_id = p.group_id where p.group_id = %s and bg.auth_user_id = %s",
            [group_id, user_id]
        )
        participants = dictfetchall(cursor)

    context = {
        'group_id': group_id,
        'participants': participants
    }
    return render(request, "bill_group/add_bill.html", context)
