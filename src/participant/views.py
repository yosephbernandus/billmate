from django.db import connection
from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render
from base.utils import dictfetchall

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest


@login_required
def add_participant(request, group_id):
    if request.POST:
        user_id = request.user.id
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

        participants = []
        with connection.cursor() as cursor:
            cursor.execute(
                "select p.participant_id, p.name from participant p join bill_group bg on bg.group_id = p.group_id where p.group_id = %s and bg.auth_user_id = %s",
                [group_id, user_id]
            )
            participants = dictfetchall(cursor)

        context = {
            'group_id': group_id,
            'participants': participants
        }
        return render(request, 'participant/list_participant.html', context)
    else:
        return HttpResponseBadRequest("Invalid request method")


@login_required
def delete_participant(request, group_id, participant_id):
    user_id = request.user.id
    with connection.cursor() as cursor:
        cursor.execute(
            "DELETE from participant p using bill_group bg where bg.auth_user_id = %s and p.participant_id = %s",
            [user_id, participant_id]
        )

    participants = []
    with connection.cursor() as cursor:
        cursor.execute(
            "select p.participant_id, p.name from participant p join bill_group bg on bg.group_id = p.group_id where p.group_id = %s and bg.auth_user_id = %s",
            [group_id, user_id]
        )
        participants = dictfetchall(cursor)

    context = {
        'group_id': group_id,
        'participants': participants
    }
    return render(request, 'participant/list_participant.html', context)
