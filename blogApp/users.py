from django.core.management.base import BaseCommand
from .models import User

class Command(BaseCommand):
    help = "Seed database with sample users"

    def handle(self, *args, **kwargs):
        users = [
            ("alice@gmail.com", "alice", "Alice Johnson"),
            ("bob@gmail.com", "bob", "Bob Smith"),
            ("charlie@gmail.com", "charlie", "Charlie Brown"),
            ("david@gmail.com", "david", "David Wilson"),
            ("emma@gmail.com", "emma", "Emma Stone"),
        ]

        for email, username, fullname in users:
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(
                    email=email,
                    username=username,
                    password="password123"
                )
                user.fullname = fullname
                user.save()

        self.stdout.write(self.style.SUCCESS("✅ Users seeded successfully"))
