from django.db import models


class Rater(models.Model):
    email = models.CharField(max_length=200)
    batch_id = models.IntegerField(default=0)


class Segment(models.Model):
    translation = models.TextField(max_length=2000)
    reference = models.TextField(max_length=2000)
    batch_id = models.IntegerField()


class Rating(models.Model):
    rater = models.ForeignKey(Rater)
    segment = models.ForeignKey(Segment)
    rating = models.IntegerField(default=0)