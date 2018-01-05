from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class client(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    transactions = []

    def create_client(sender, instance, created, **kwargs):
        if created:
            client.objects.create(user=instance)

    post_save.connect(create_client, sender=User)

    def add_transactions(self, trans):
        self.transactions.append(trans)

    def list_transactions(self):
        return self.transactions

    def __str__(self):
        return self.user.username
