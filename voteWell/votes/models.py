from django.db import models

class Legislator(models.Model):
    lastname = models.CharField(max_length=20)
    firstname = models.CharField(max_length=20)
    middlename = models.CharField(max_length=20)
    birthday = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=1)
    religion = models.CharField(max_length=20)
    pvsid = models.IntegerField(null=True,blank=True)
    osid = models.CharField(max_length=20)
    bioguideid = models.CharField(max_length=20)
    metavidid = models.CharField(max_length=20)
    youtubeid = models.CharField(max_length=20)
    icpsrid = models.IntegerField(null=True,blank=True)
    facebookgraphid = models.IntegerField(null=True,blank=True)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    district = models.IntegerField(null=True,blank=True)
    party = models.CharField(max_length=10)
    position = models.CharField(max_length=10)
    url = models.CharField(max_length=20)
    def __unicode__(self):
        return self.name
