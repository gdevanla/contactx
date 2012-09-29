from django.db import  models
from singly.models import UserProfile

class UserResume(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile)
    file_name = models.CharField(max_length=50)
    file_location = models.CharField(max_length=50)

    class Meta:
        db_table = u'user_resume'

class CandidateRating(models.Model):
    id = models.AutoField(primary_key=True)
    user_resume = models.ForeignKey(UserResume)
    rating = models.IntegerField(default=0)
    email = models.CharField(max_length=50)

    class Meta:
        db_table = u'candidate_rating'
