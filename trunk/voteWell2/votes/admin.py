from votes.models import Legislator, Subject, Bill, Roll, Vote
from django.contrib import admin

admin.site.register(Legislator)
admin.site.register(Subject)
admin.site.register(Bill)
admin.site.register(Roll)
admin.site.register(Vote)