from django.db import models

class Bill(models.Model):
    session = models.IntegerField()
    kind = models.CharField(max_length=10)
    number = models.IntegerField()
    mainTitle = models.CharField(max_length=100)
    updated = models.DateTimeField()
    state_datetime = models.DateTimeField()
    state = models.CharField(max_length=20)
    introduced = models.DateField()
    sponsor = models.ForeignKey('Legislator')
    cosponsors = models.ManyToManyField('Legislator',related_name='cosponsored')
    summary = models.TextField()
    relatedbills = models.ManyToManyField('self',through='Relationship',symmetrical=False)
    subjects = models.ManyToManyField('Subject')
    

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

class Title(models.Model):
    bill = models.ForeignKey(Bill)
    kind = models.CharField(max_length=15)
    how = models.CharField(max_length=15)
    title = models.CharField(max_length=100)
    
class Subject(models.Model):
    name = models.CharField(max_length=50)
    
class Committee(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    bills = models.ManyToManyField(Bill,through='Activity')
    
class Relationship(models.Model):
    srcBill = models.ForeignKey(Bill)
    destBill = models.ForeignKey(Bill,related_name='reverseRelated')
    kind = models.CharField(max_length=15)
    
class Activity(models.Model):
    committee = models.ForeignKey(Committee)
    bill = models.ForeignKey(Bill)
    activity = models.CharField(max_length=30)
    

    
