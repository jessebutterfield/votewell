'''
Created on Dec 8, 2011

@author: jessebutterfield
'''

from os import listdir
from xml.dom.minidom import parse
from votes.models import *
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = 'None'
    helb = 'Updates the legislator info'

    def handle(self, *args, **options):            
        folderName = '/Users/jessebutterfield/workspace/voteWell/voteWell/data/bills/'
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
            except Bill.DoesNotExist:
                b = Bill(session=session,kind=kind,number=number)
            b.updated = bill.attributes['updated'].value
            
            state = bill.getElementsByTagName('state')[0]
            b.state_datetime = state.attributes['datetime'].value
            b.state = state.firstChild.nodeValue
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

            b.save()
            for tit in titles:
                kind = tit.attributes['type'].value
                how = tit.attributes['as'].value
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
    
    
