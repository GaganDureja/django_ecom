# just a hi to test custom command


from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Just a hi to test custom command'

    def handle(self, *args, **options):
        username = input("Enter Name:")
        msg = "Hi " + username        
        self.stdout.write(self.style.SUCCESS(msg))