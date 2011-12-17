'''
Created on Dec 4, 2011

@author: jessebutterfield
'''

from xml.dom.minidom import parse
from django.conf import settings
from votes.models import Legislator
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = 'None'
    help = 'Updates the legislator info'

    def handle(self, *args, **options):            
        fileName = settings.DATA_DIR+'people.xml'
        xml = parse(fileName)
        people = xml.getElementsByTagName('person')
        for person in people:
            nid = person.attributes['id'].value
            print nid
            role = person.getElementsByTagName('role')[0]
            try:
                p = Legislator.objects.get(id=nid)
            except Legislator.DoesNotExist:
                p = Legislator(id=nid)
            p.lastname = person.attributes['lastname'].value
            p.firstname = person.attributes['firstname'].value
            try:
                p.middlename = person.attributes['middlename'].value
            except:
                pass
            try:
                p.birthday = person.attributes['birthday'].value
            except:
                pass
            p.gender = person.attributes['gender'].value
            try:
                p.religion = person.attributes['religion'].value
            except:
                pass
            try:
                p.pvsid = person.attributes['pvsid'].value
            except:
                pass
            try:
                p.osid = person.attributes['osid'].value
            except:
                pass
            try:
                p.bioguideid = person.attributes['bioguideid'].value
            except:
                pass
            try:
                p.metavidid = person.attributes['metavidid'].value
            except:
                pass
            try:
                p.youtubeid = person.attributes['youtubeid'].value
            except:
                pass
            try:
                p.icpsrid = person.attributes['icpsrid'].value
            except:
                pass
            try:
                p.facebookgraphid = person.attributes['facebookgraphid'].value
            except:
                pass
            p.name = person.attributes['name'].value
            p.title = person.attributes['title'].value
            p.state = person.attributes['state'].value
            try:
                p.district = person.attributes['district'].value
            except:
                pass
            
            p.party = role.attributes['party'].value
            p.position = role.attributes['type'].value
            try:
                p.url = role.attributes['url'].value
            except:
                pass
            p.save()
        self.stdout.write('Successfully updated reps\n')
    
    
