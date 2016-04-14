from __future__ import unicode_literals

from django.db import models

__belt_names=['white','yellow','gold','orange','green',
                  'blue','purple','brown','red','black']
def belt(idx):
  nidx = idx
  if idx > 9:
    nidx = 9
  return __belt_names[nidx]

# Create your models here.
class Aspect (models.Model):
  name = models.CharField(max_length=100)
  # steps from one belt to the next
  score = models.IntegerField(default=0)
  # belts go from 0 (White) - 9 (black)
  belt = models.IntegerField(default=0)

# the future you want to create
class Future (models.Model):
  aspect = models.ForeignKey(Aspect)
  future = models.CharField(max_length=200)
  # in progress, changed, achieved
  status = models.CharField(max_length=30,default="in progress")
  # personal notes about this.
  notes = models.CharField(max_length=200)
  seq = models.IntegerField(default=0)

# the moments you create in the future
class Moment (models.Model):
  aspect = models.ForeignKey(Aspect)
  moment = models.CharField(max_length=200)
  plan = models.DateTimeField(null=False)
  achieved = models.DateTimeField(null = True)
  proof = models.ImageField(null=True)
  # in progress, achieved, abandoned
  status = models.CharField(max_length=30,default="in progress")

class SimpleValue (models.Model):
  val =  models.CharField(max_length=200)
