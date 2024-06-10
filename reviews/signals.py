from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review

@receiver(post_save, sender=Review)
def update_matrix_on_review_save(sender, instance, **kwargs):
    # Logic to update the matrix
    from .recommandations import update_matrix
    update_matrix()
