from django.utils import timezone
from TI_Management_app.models import Vote


def voting_count(request):
    vote_obj_count = Vote.objects.filter(
        date_start__lte=timezone.now(),
        date_end__gte=timezone.now()
    ).count()

    return {
        'voting_count': vote_obj_count
    }
