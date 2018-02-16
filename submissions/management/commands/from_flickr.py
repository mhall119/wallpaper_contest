from django.core.management.base import BaseCommand, CommandError
from rest_framework.parsers import JSONParser

import requests
import datetime
import simplejson

from submissions.models import Contest, Submission

class Command(BaseCommand):
    help = 'Imports images from Flickr group'

    def add_arguments(self, parser):
        parser.add_argument('contest_id', type=int)
        parser.add_argument('url', type=str)

    def handle(self, *args, **options):
    
        if 'contest_id' not in options:
            print("No contest id in options!")
            return 1
        if 'url' not in options:
            print("No URL in options!")
            return 1
        try:
            contest = Contest.objects.get(id=options['contest_id'])
        except:
            print("Could not find contest with id %s" % options['contest_id'])
            return 2
            
        more_data = True
        photos = []
        print("Calling: "+options['url'])
        resp = requests.get(options['url'])
        if resp.status_code != 200:
            print("Request failed: %s" % resp.status_code)
            return 1
        data = simplejson.loads(resp.text)
        if data['stat'] != 'ok':
            print(data['message'])
            return 1
        print("Adding %s photos" % len(data['photos']['photo']))
        for photo in data['photos']['photo']:
            photo_url = "https://c1.staticflickr.com/%(farm)s/%(server)s/%(id)s_%(secret)s_b.jpg" % photo
            created, submission = Submission.objects.update_or_create(image_url=photo_url, defaults={
                'title': photo['title'],
                'author': photo['ownername'],
                'contest': contest
            })
            if created:
                print("Added '%s' %s" % (photo['title'], photo_url))
