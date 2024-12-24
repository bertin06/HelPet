from django.db import models
from django.contrib.auth.models import User

class TBRooms(models.Model):
    fkusercli = models.ForeignKey(User, models.CASCADE, related_name = 'cli')
    fkuserpro = models.ForeignKey(User, models.CASCADE, related_name = 'pro', null = True, blank = True)
    status = models.IntegerField()

    class Meta:
        db_table = 'tbrooms'

class TBMessages(models.Model):
    message = models.CharField(max_length = 250)
    date = models.DateTimeField(auto_now_add = True)
    fkuser = models.ForeignKey(User, on_delete = models.CASCADE)
    fkroom = models.ForeignKey(TBRooms, on_delete = models.CASCADE)

    class Meta:
        db_table = 'tbmessages'
