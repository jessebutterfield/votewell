'''
Created on Dec 8, 2011

@author: jessebutterfield
'''

from os import listdir
from xml.dom.minidom import parse
from django.conf import settings
from votes.models import *
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = 'None'
    helb = 'Updates the legislator info'

    def handle(self, *args, **options):            
        folderName = settings.DATA_DIR + 'bills/'
        files = listdir(folderName)
        for fileName in files:
            fileName = folderName + fileName
            xml = parse(fileName)
            bill = xml.getElementsByTagName('bill')[0]
            session = bill.attributes['session'].value
            kind = bill.attributes['type'].value
            number = bill.attributes['number'].value
            #get or create bill, for some reason get or create wasn't working
            try:
                b = Bill.objects.get(session=session,kind=kind,number=number)
                continue
            except Bill.DoesNotExist:
                b = Bill(session=session,kind=kind,number=number)
            up = bill.attributes['updated'].value.replace('T',' ')
            print len(up)
            if(len(up)>20):
                up = up[:-6]
            b.updated = up
            
            state = bill.getElementsByTagName('state')[0]
            sd = state.attributes['datetime'].value.replace('T',' ')
            print(len(sd))
            if(len(sd)>20):
                sd = sd[:-6]
            print sd
            b.state_datetime = sd
            b.state = state.firstChild.nodeValue[:20]
            introduced = bill.getElementsByTagName('introduced')[0]
            b.introduced = introduced.attributes['datetime'].value
            sponsor = bill.getElementsByTagName('sponsor')[0]
            b.sponsor = Legislator.objects.get(pk=sponsor.attributes['id'].value)
            cosponsors = bill.getElementsByTagName('cosponsor')
            
            #Think about what to do about committees
            committees = bill.getElementsByTagName('committees')[0]
            committees = committees.getElementsByTagName('committee')
            titles = bill.getElementsByTagName('title')
            b.mainTitle = titles[-1].firstChild.nodeValue

            subjects = bill.getElementsByTagName('term')
            summary = bill.getElementsByTagName('summary')[0]
            b.summary = summary.firstChild.nodeValue
            print b.updated

            b.save()
            for tit in titles:
                kind = tit.attributes['type'].value[:15]
                how = tit.attributes['as'].value[:15]
                title = tit.firstChild.nodeValue
                Title.objects.get_or_create(kind=kind,title=title,
                                            how=how,bill=b)
            print fileName
            for com in committees:
                name = com.attributes['name'].value
                code = com.attributes['code'].value
                act = com.attributes['activity'].value
                c,discard = Committee.objects.get_or_create(code=code,name=name)
                a = Activity(bill=b,committee=c,activity=act)
                a.save()
            for term in subjects:
                name = term.attributes['name'].value
                s,discard = Subject.objects.get_or_create(name=name)
                b.subjects.add(s)
            for cosponsor in cosponsors:
                b.cosponsors.add(Legislator.objects.get(pk=cosponsor.attributes['id'].value))

            b.save()
        self.stdout.write('Successfully updated bills\n')
    
    
