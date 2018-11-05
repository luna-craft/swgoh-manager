from django.core.management.base import BaseCommand, CommandError
from manager.crawler import update_guilds

class Command(BaseCommand):
    help = 'Обновляет данные по всем активным гильдиям'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        update_guilds()
        #self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))