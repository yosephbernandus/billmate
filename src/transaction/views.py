from django.db import connection
from django.utils import timezone
from base.utils import dictfetchall
from django.http import HttpResponseBadRequest
from django.shortcuts import render

from django.contrib.auth.decorators import login_required


@login_required(login_url="")
def add_transaction(request, bill_id):
    user_id = request.user.id
    # TODO: Add condition to check transaction is related to user_id or not

    if request.POST:
        amount = request.POST.get('amount')
        participant = request.POST.get('participant')
        type = request.POST.get('type')
        status = request.POST.get('status')
        utc_now = timezone.now()

        transactions = []
        with connection.cursor() as cursor:
            query = """
            INSERT INTO transaction (amount, participant_id, type, status, bill_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING transaction_id
            """
            cursor.execute(query, [
                amount, participant, type, status, bill_id, utc_now, utc_now
            ])

            transaction_query = """
            SELECT t.transaction_id, p.name, t.amount, t.type, t.status
            from transaction t join participant p on p.participant_id = t.participant_id where t.bill_id = %s
            order by t.transaction_id desc
            """
            cursor.execute(
                transaction_query, [bill_id]
            )
            transactions = dictfetchall(cursor)

        context = {
            'transactions': transactions,
        }

        return render(request, 'transaction/list_transaction.html', context)
    else:
        return HttpResponseBadRequest("Invalid request method")


@login_required(login_url="")
def delete_transaction(request, transaction_id):
    user_id = request.user.id
    # TODO: Add condition to check transaction is related to user_id or not

    transactions = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT bill_id from transaction where transaction_id = %s", [transaction_id])
        bill_id = cursor.fetchone()
        bill_id = bill_id[0]

        cursor.execute(
            "DELETE from transaction where transaction_id = %s", [transaction_id]
        )

        transaction_query = """
        SELECT t.transaction_id, p.name, t.amount, t.type, t.status
        from transaction t join participant p on p.participant_id = t.participant_id where t.bill_id = %s
        order by t.transaction_id desc
        """
        cursor.execute(
            transaction_query, [bill_id]
        )
        transactions = dictfetchall(cursor)

    context = {
        'transactions': transactions,
    }

    return render(request, 'transaction/list_transaction.html', context)


def mark_as_paid(request, transaction_id):
    user_id = request.user.id
    # TODO: Add condition to check transaction is related to user_id or not

    transactions = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT bill_id from transaction where transaction_id = %s", [transaction_id])
        bill_id = cursor.fetchone()
        bill_id = bill_id[0]

        cursor.execute(
            "UPDATE transaction SET status = 'paid' where transaction_id = %s", [transaction_id]
        )

        transaction_query = """
        SELECT t.transaction_id, p.name, t.amount, t.type, t.status
        from transaction t join participant p on p.participant_id = t.participant_id where t.bill_id = %s
        order by t.transaction_id desc
        """
        cursor.execute(
            transaction_query, [bill_id]
        )
        transactions = dictfetchall(cursor)

    context = {
        'transactions': transactions,
    }

    return render(request, 'transaction/list_transaction.html', context)
