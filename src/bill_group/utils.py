from hashids import Hashids

from django.conf import settings


def create_public_group_link(group_id):
    base_name = settings.SERVER_HOST_NAME
    hashids = Hashids(salt=settings.HASH_IDS_SALT, min_length=6)

    hashid = hashids.encode(group_id)

    return f"{base_name}/group/{hashid}"
