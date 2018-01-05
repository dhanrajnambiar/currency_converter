from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class client(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    def create_client(sender, instance, created, **kwargs):
        if created:
            client.objects.create(user=instance)

    post_save.connect(create_client, sender=User)

    def add_transactions(self, trans):
       transaction.objects.create(creator = self, text = trans)

    def list_transactions(self):
        return list(transaction.objects.filter(creator = self).order_by('trans_time'))

    def __str__(self):
        return self.user.username

class transaction(models.Model):
    creator = models.ForeignKey(client, on_delete = models.CASCADE)
    trans_time = models.DateTimeField(auto_now_add = True, auto_now = False)
    text = models.TextField(max_length = 200)

    def __str__(self):
        return self.text
