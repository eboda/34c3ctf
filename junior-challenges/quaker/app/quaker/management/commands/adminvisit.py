import os
import requests

from django.core.management.base import BaseCommand, CommandError
from quaker.models import *

s = requests.Session()
url = 'http://127.0.0.1/'

def login():
    user = 'admin'
    pw = 'awueh23r7Q2hiu1!'

    s.get(url)
    token = s.cookies['csrftoken']
    s.post(url, data=dict(
        username=user,
        password=pw,
        csrfmiddlewaretoken=token))

    return s.cookies['sessionid']

def logout():
    s.get(url + 'logout')


class Command(BaseCommand):
    help = 'Let the admin visit his new quaks'

    def handle(self, *args, **options):
        script = os.path.dirname(os.path.realpath(__file__)) + '/../../scripts/visit.js'
        admin = User.objects.filter(pk=1).get()
        admin_session = login()
        self.stdout.write(self.style.SUCCESS('Admin session: {}'.format(admin_session)))

        # feeds
        feed_visit = []
        for follower in admin.profile.following.all():
            quaks = follower.profile.quaks.filter(seen_by_admin=False)
            if quaks.count() > 0:
                feed_visit.append(follower)
                for quak in quaks.all():
                    quak.seen_by_admin = True
                    quak.save()

        self.stdout.write(self.style.SUCCESS('Need to visit {} feeds.'.format(len(feed_visit))))

        for feed in feed_visit:
            self.stdout.write(self.style.SUCCESS('\tVisiting feed {}.'.format(feed.profile.token)))

            os.system("timeout 1 phantomjs {} {} {}".format(script,
                admin_session,
                url + 'feed/{}'.format(feed.profile.token)))


        # messages
        all_users = Message.objects.filter(user_to=admin,seen=False).order_by('user_from').values_list('user_from', flat=True).distinct()
        visit_msgs = []
        for user in all_users:        # only take top3 msgs per user
            visit_msgs.extend(Message.objects.filter(
                user_to=admin, 
                seen=False, 
                user_from=User.objects.get(pk=user)).all()[:3])

        self.stdout.write(self.style.SUCCESS('Need to visit {} messages.'.format(len(visit_msgs))))

        for msg in visit_msgs:
            os.system("timeout 1 phantomjs {} {} {}".format(script, 
                admin_session,
                url + 'messages/{}'.format(msg.token)))
        

        logout()
        self.stdout.write(self.style.SUCCESS('Logged out.'))
            
