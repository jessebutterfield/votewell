from django.db import models
from django.contrib.auth.models import User

class Bill(models.Model):
    session = models.IntegerField()
    kind = models.CharField(max_length=10)
    number = models.IntegerField()
    mainTitle = models.TextField()
    updated = models.DateTimeField()
    state_datetime = models.DateTimeField()
    state = models.CharField(max_length=20)
    introduced = models.DateField()
    sponsor = models.ForeignKey('Legislator')
    cosponsors = models.ManyToManyField('Legislator',related_name='cosponsored')
    summary = models.TextField()
    relatedbills = models.ManyToManyField('self',through='Relationship',symmetrical=False)
    subjects = models.ManyToManyField('Subject')
    def __unicode__(self):
        return str(self.session)+'--'+self.kind+str(self.number)
    

class Legislator(models.Model):
    lastname = models.TextField()
    firstname = models.TextField()
    middlename = models.TextField()
    birthday = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=1)
    religion = models.TextField()
    pvsid = models.IntegerField(null=True,blank=True)
    osid = models.TextField()
    bioguideid = models.TextField()
    metavidid = models.TextField()
    youtubeid = models.TextField()
    icpsrid = models.IntegerField(null=True,blank=True)
    facebookgraphid = models.BigIntegerField(null=True,blank=True)
    name = models.TextField()
    title = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    district = models.IntegerField(null=True,blank=True)
    party = models.CharField(max_length=20)
    position = models.CharField(max_length=20)
    url = models.TextField()
    def __unicode__(self):
        return self.name
    
class Roll(models.Model):
    category = models.CharField(max_length=30)
    kind = models.CharField(max_length=30)
    question = models.TextField()
    bill = models.ForeignKey(Bill,null=True,blank=True)
    where = models.CharField(max_length=20)
    session = models.IntegerField()
    year = models.IntegerField()
    number = models.IntegerField()
    source = models.CharField(max_length=20)
    when = models.DateTimeField()
    updated = models.DateTimeField()
    aye = models.IntegerField()
    nay = models.IntegerField()
    novote = models.IntegerField()
    present = models.IntegerField()
    keys = models.ManyToManyField('VoteKey')
    required = models.CharField(max_length=5)
    result = models.CharField(max_length=30)
    votes = models.ManyToManyField(Legislator,through='Vote')
    def __unicode__(self):
        return self.question
    
class Vote(models.Model):
    roll = models.ForeignKey(Roll)
    voter = models.ForeignKey(Legislator)
    vote = models.CharField(max_length=1)
    argument = models.TextField()
    
class VoteKey(models.Model):
    symbol = models.CharField(max_length=1)
    vote = models.CharField(max_length=50)
    def __unicode__(self):
        return self.symbol+'='+self.vote    
    

class Title(models.Model):
    bill = models.ForeignKey(Bill)
    kind = models.CharField(max_length=15)
    how = models.CharField(max_length=15)
    title = models.TextField()
    def __unicode__(self):
        return self.title
    
class Subject(models.Model):
    name = models.TextField()
    def __unicode__(self):
        return self.name
    
class Committee(models.Model):
    code = models.CharField(max_length=10)
    name = models.TextField()
    bills = models.ManyToManyField(Bill,through='Activity')
    def __unicode__(self):
        return self.name
    
class Relationship(models.Model):
    srcBill = models.ForeignKey(Bill)
    destBill = models.ForeignKey(Bill,related_name='reverseRelated')
    kind = models.TextField()
    
class Activity(models.Model):
    committee = models.ForeignKey(Committee)
    bill = models.ForeignKey(Bill)
    activity = models.TextField()
    
class Comment(models.Model):
    user = models.ForeignKey(User)
    created = models.DateTimeField()
    bill = models.ForeignKey(Bill,null=True,blank=True)
    roll = models.ForeignKey(Roll,null=True,blank=True)
    sentiment = models.CharField(max_length=1)
    text = models.TextField()

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)
    follows = models.ManyToManyField(User,related_name="followers")
    legislators = models.ManyToManyField(Legislator)
    

    
