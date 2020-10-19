# coding=utf-8

"""
import FAT data from bFAT module
"""

from django.conf import settings
from django.core.management.base import BaseCommand

from imicusfat.models import (
    IFat,
    IFatLink,
    IFatDelLog,
    ClickIFatDuration,
    ManualIFat,
)

from bfat.models import (
    ClickFatDuration as BfatClickFatDuration,
    DelLog as BfatDelLog,
    Fat as BfatFat,
    FatLink as BfatFatLink,
    ManualFat as BfatManualFat,
)


def get_input(text):
    """
    wrapped input to enable import
    """

    return input(text)


def bfat_installed() -> bool:
    """
    check if aa-timezones is installed
    :return: bool
    """

    return "bfat" in settings.INSTALLED_APPS


class Command(BaseCommand):
    """
    Initial import of FAT data from AA FAT module
    """

    help = "Imports FAT data from ImicusFAT module"

    def _import_from_imicusfat(self) -> None:
        # check if AA FAT is active
        if bfat_installed():
            self.stdout.write(
                self.style.SUCCESS("ImicusFAT module is active, let's go!")
            )

            # first we check if the target tables are really empty ...
            current_ifat_count = IFat.objects.all().count()
            current_ifat_dellog_count = IFatDelLog.objects.all().count()
            current_ifat_links_count = IFatLink.objects.all().count()
            current_ifat_clickduration_count = ClickIFatDuration.objects.all().count()
            current_ifat_manualfat_count = ManualIFat.objects.all().count()

            if (
                current_ifat_count > 0
                or current_ifat_dellog_count > 0
                or current_ifat_links_count > 0
                or current_ifat_clickduration_count > 0
                or current_ifat_manualfat_count > 0
            ):
                self.stdout.write(
                    self.style.WARNING(
                        "You already have FAT data with the ImicusFAT module. "
                        "Import cannot be continued."
                    )
                )

                return

            # import FAT links
            bfat_fatlinks = BfatFatLink.objects.all()
            for bfat_fatlink in bfat_fatlinks:
                self.stdout.write(
                    "Importing FAT link for fleet '{fleet}' with hash '{fatlink_hash}'.".format(
                        fleet=bfat_fatlink.fleet,
                        fatlink_hash=bfat_fatlink.hash,
                    )
                )

                ifatlink = IFatLink()

                ifatlink.id = bfat_fatlink.id
                ifatlink.ifattime = bfat_fatlink.fattime
                ifatlink.fleet = bfat_fatlink.fleet
                ifatlink.hash = bfat_fatlink.hash
                ifatlink.creator_id = bfat_fatlink.creator_id

                ifatlink.save()

            # import FATs
            bfat_fats = BfatFat.objects.all()
            for bfat_fat in bfat_fats:
                self.stdout.write(
                    "Importing FATs for FAT link ID '{fatlink_id}'.".format(
                        fatlink_id=bfat_fat.id
                    )
                )

                ifat = IFat()

                ifat.id = bfat_fat.id
                ifat.system = bfat_fat.system
                ifat.shiptype = bfat_fat.shiptype
                ifat.character_id = bfat_fat.character_id
                ifat.ifatlink_id = bfat_fat.fatlink_id

                ifat.save()

            # import click FAT durations
            bfat_clickfatdurations = BfatClickFatDuration.objects.all()
            for bfat_clickfatduration in bfat_clickfatdurations:
                self.stdout.write(
                    "Importing FAT duration with ID '{duration_id}'.".format(
                        duration_id=bfat_clickfatduration.id
                    )
                )

                ifat_clickfatduration = ClickIFatDuration()

                ifat_clickfatduration.id = bfat_clickfatduration.id
                ifat_clickfatduration.duration = bfat_clickfatduration.duration
                ifat_clickfatduration.fleet_id = bfat_clickfatduration.fleet_id

                ifat_clickfatduration.save()

            # import dellog
            bfat_dellogs = BfatDelLog.objects.all()
            for bfat_dellog in bfat_dellogs:
                self.stdout.write(
                    "Importing FAT dellogwith ID '{dellog_id}'.".format(
                        dellog_id=bfat_dellog.id
                    )
                )

                ifat_dellog = IFatDelLog()

                ifat_dellog.id = bfat_dellog.id
                ifat_dellog.deltype = bfat_dellog.deltype
                ifat_dellog.string = bfat_dellog.string
                ifat_dellog.remover_id = bfat_dellog.remover_id

                ifat_dellog.save()

            # import manual fat
            bfat_manualfats = BfatManualFat.objects.all()
            for bfat_manualfat in bfat_manualfats:
                self.stdout.write(
                    "Importing manual FAT with ID '{manualfat_id}'.".format(
                        manualfat_id=bfat_manualfat.id
                    )
                )

                ifat_manualfat = ManualIFat()

                ifat_manualfat.id = bfat_manualfat.id
                ifat_manualfat.character_id = bfat_manualfat.character_id
                ifat_manualfat.creator_id = bfat_manualfat.creator_id
                ifat_manualfat.ifatlink_id = bfat_manualfat.fatlink_id

                ifat_manualfat.save()

            self.stdout.write(
                self.style.SUCCESS(
                    "Import complete! "
                    "You can now deactivate the bFAT module in your local.py"
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "bFAT module is not active. "
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
            "Importing all FAT/FAT link data from bFAT module. "
            "This can only be done once during the very first installation. "
            "As soon as you have data collected with your ImicusFAT module, this import will fail!"
        )

        user_input = get_input("Are you sure you want to proceed? (yes/no)?")

        if user_input == "yes":
            self.stdout.write("Starting import. Please stand by.")
            self._import_from_imicusfat()
        else:
            self.stdout.write(self.style.WARNING("Aborted."))
