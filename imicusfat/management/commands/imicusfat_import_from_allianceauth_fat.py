# coding=utf-8

"""
import FAT data from alliance auth fat module
"""

from django.conf import settings
from django.core.management.base import BaseCommand

from imicusfat.models import IFatLink, IFat

from allianceauth.fleetactivitytracking.models import Fatlink, Fat


def get_input(text):
    """
    wrapped input to enable import
    """

    return input(text)


def aa_fat_installed() -> bool:
    """
    check if aa-timezones is installed
    :return: bool
    """

    return "allianceauth.fleetactivitytracking" in settings.INSTALLED_APPS


class Command(BaseCommand):
    """
    Initial import of FAT data from AA FAT module
    """

    help = "Imports FAT data from AA FAT module"

    def _import_from_aa_fat(self) -> None:
        # check if AA FAT is active
        if aa_fat_installed():
            self.stdout.write(
                self.style.SUCCESS("Alliance Auth FAT module is active, let's go!")
            )

            # first we check if the target tables are really empty ...
            current_ifat_links_count = IFatLink.objects.all().count()
            current_ifat_count = IFat.objects.all().count()

            if current_ifat_count > 0 or current_ifat_links_count > 0:
                self.stdout.write(
                    self.style.WARNING(
                        "You already have FAT data with the ImicusFAT module. "
                        "Import cannot be continued."
                    )
                )

                return

            aa_fatlinks = Fatlink.objects.all()
            for aa_fatlink in aa_fatlinks:
                self.stdout.write(
                    "Importing FAT link for fleet '{fleet}' with hash '{fatlink_hash}'.".format(
                        fleet=aa_fatlink.fleet, fatlink_hash=aa_fatlink.hash
                    )
                )

                ifatlink = IFatLink()

                ifatlink.id = aa_fatlink.id
                ifatlink.ifattime = aa_fatlink.fatdatetime
                ifatlink.fleet = aa_fatlink.fleet
                ifatlink.hash = aa_fatlink.hash
                ifatlink.creator_id = aa_fatlink.creator_id

                ifatlink.save()

            aa_fats = Fat.objects.all()
            for aa_fat in aa_fats:
                self.stdout.write(
                    "Importing FATs for FAT link ID '{fatlink_id}'.".format(
                        fatlink_id=aa_fat.id
                    )
                )

                ifat = IFat()

                ifat.id = aa_fat.id
                ifat.system = aa_fat.system
                ifat.shiptype = aa_fat.shiptype
                ifat.character_id = aa_fat.character_id
                ifat.ifatlink_id = aa_fat.fatlink_id

                ifat.save()

            self.style.SUCCESS(
                "Import complete! "
                "You can now deactivate the Alliance Auth FAT module in your local.py"
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "Alliance Auth FAT module is not active. "
                    "Please make sure you have it in your INSTALLED_APPS in your local.py!"
                )
            )

    def handle(self, *args, **options):
        """
        ask before running ...
        :param args:
        :param options:
        """

        self.stdout.write(
            "Importing all FAT/FAT link data from Alliance Auth's built in FAT module. "
            "This can only be done once during the very first installation. "
            "As soon as you have data collected with your ImicusFAT module, this import will fail!"
        )

        user_input = get_input("Are you sure you want to proceed? (yes/no)?")

        if user_input == "yes":
            self.stdout.write("Starting import. Please stand by.")
            self._import_from_aa_fat()
        else:
            self.stdout.write(self.style.WARNING("Aborted."))
