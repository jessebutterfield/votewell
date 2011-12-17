'''
Created on Dec 10, 2011

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
        folderName = settings.DATA_DIR + 'rolls/'
        files = listdir(folderName)
        nonPassage = {}
        for fileName in files:
            print fileName
            fileName = folderName + fileName
            xml = parse(fileName)
            roll = xml.getElementsByTagName('roll')[0]
            cat = roll.getElementsByTagName('category')[0].firstChild.nodeValue
            if(cat!='passage'):
                try:
                    nonPassage[cat] = nonPassage[cat]+1
                except:
                    nonPassage[cat] = 1
                continue
            kind = roll.getElementsByTagName('type')[0].firstChild.nodeValue
            where = roll.attributes['where'].value
            session = roll.attributes['session'].value
            year = roll.attributes['year'].value
            number = roll.attributes['roll'].value
            
            try:
                r = Roll.objects.get(where=where,session=session,year=year,number=number,
                                     category=cat,kind=kind)
            except:
                r = Roll(where=where,session=session,year=year,number=number,
                         category=cat,kind=kind)
            
            bill = roll.getElementsByTagName('bill')[0]
            session = bill.attributes['session'].value
            kind = bill.attributes['type'].value
            number = bill.attributes['number'].value
            #get or create bill, for some reason get or create wasn't working
            b = Bill.objects.get(session=session,kind=kind,number=number)
            r.bill = b
            r.source = roll.attributes['source'].value
            r.when = roll.attributes['datetime'].value
            r.updated = roll.attributes['updated'].value
            r.aye = roll.attributes['aye'].value
            r.nay = roll.attributes['nay'].value
            r.novote = roll.attributes['nv'].value
            r.present = roll.attributes['present'].value
            r.question = roll.getElementsByTagName('question')[0].firstChild.nodeValue
            r.required = roll.getElementsByTagName('required')[0].firstChild.nodeValue
            r.result = roll.getElementsByTagName('result')[0].firstChild.nodeValue

            r.save()
            
            options = roll.getElementsByTagName('option')
            
            for opt in options:
                symbol = opt.attributes['key'].value
                vote = opt.firstChild.nodeValue
                key,discard = VoteKey.objects.get_or_create(symbol=symbol,vote=vote)
                r.keys.add(key)
            
            votes = roll.getElementsByTagName('voter')
            for vote in votes:
                idx = vote.attributes['id'].value
                key = vote.attributes['vote'].value
                v = Vote(voter_id=idx,roll=r,vote=key)
                v.save()
            r.save()
        print nonPassage
        self.stdout.write('Successfully updated rolls\n')
    
    
