
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create the initial LocalLens administrator from environment variables."

    def handle(self, *args, **options):
        username = os.environ.get("BOOTSTRAP_ADMIN_USERNAME")
        email = os.environ.get("BOOTSTRAP_ADMIN_EMAIL")
        password = os.environ.get("BOOTSTRAP_ADMIN_PASSWORD")

        # Allow normal restarts after the temporary credentials are removed.
        if not any([username, email, password]):
            self.stdout.write("No bootstrap credentials configured; skipping.")
            return

        if not all([username, email, password]):
            raise CommandError("Set all three BOOTSTRAP_ADMIN variables.")

        User = get_user_model()

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.is_superuser and user.is_staff:
                self.stdout.write("Administrator already exists; skipping.")
                return
            raise CommandError(
                "This username already exists but is not an administrator. "
                "Choose a different username."
            )

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        self.stdout.write(self.style.SUCCESS("Administrator created successfully."))
