from django.core.management.base import BaseCommand, CommandError
from apps.entity.models import Entity, Act, OcurrencyEntity
from django.db.models import Count, F, Case, When
from functools import reduce
from collections import Counter
import operator
import csv
from datetime import datetime
from django.utils.timezone import make_aware
from django.forms.models import model_to_dict
from apps.entity.utils.data_visualization import calculated_percent_entity, calculated_global_all_entities_average
import sys


class Command(BaseCommand):
    help = "Show Act Stats"

    def add_arguments(self, parser):
        parser.add_argument(
            "--start_date",
            help="Start date for stats, valid format DD-MM-YYYY",
        )
        parser.add_argument(
            "--end_date",
            help="End date for stats, valid format DD-MM-YYYY",
        )

    def handle(self, *args, **options):
        filename = "entity_stats"
        extension = "csv"
        range_dates = ""
        value_totals = "totales"
        col_percent = "eficacia"
        column_names = ["nombre", "modelo", "manual", "error"]
        queryset = OcurrencyEntity.objects
        totals = None

        if options["start_date"] and options["end_date"]:
            range_dates = f"_{options['start_date']}-to-{options['end_date']}"
            start = make_aware(datetime.strptime(options["start_date"], "%d-%m-%Y"))
            end = make_aware(datetime.strptime(options["end_date"], "%d-%m-%Y"))
            queryset = queryset.filter(act__created_date__range=(start, end))
            self.stdout.write(self.style.NOTICE(f"Running with date range from {start} to  {end}"))
        else:
            self.stdout.write(self.style.NOTICE("Running without date range"))

        results = (
            queryset.values("entity__name")
            .annotate(
                nombre=F("entity__name"),
                modelo=Count(Case(When(human_marked_ocurrency=False, then=0))),
                manual=Count(Case(When(human_marked_ocurrency=True, then=1))),
                error=Count(Case(When(human_deleted_ocurrency=True, then=1))),
            )
            .values(*column_names)
        )

        if results:
            only_values = [{key: val for key, val in sub.items() if key != column_names[0]} for sub in results]
            totals = reduce(operator.add, map(Counter, only_values))
        else:
            self.stderr.write(self.style.ERROR("No data found, check date range"))
            sys.exit(1)

        resultsPercent = [
            {
                **r,
                **{
                    col_percent: calculated_percent_entity(
                        r[column_names[1]] + r[column_names[2]], r[column_names[3]], r[column_names[2]]
                    )
                },
            }
            for r in results
        ]

        totalsPercent = {
            **{column_names[0]: value_totals},
            **totals,
            **{
                col_percent: calculated_global_all_entities_average(
                    totals[column_names[1]], totals[column_names[2]], totals[column_names[3]]
                )
            },
        }

        output_filename = f"{filename}{range_dates}.{extension}"
        column_names.append(col_percent)
        try:
            with open(output_filename, "w") as fd:
                csv_writer = csv.DictWriter(fd, column_names)
                csv_writer.writeheader()
                csv_writer.writerows(resultsPercent)
                csv_writer.writerow(totalsPercent)
        except EnvironmentError:
            self.stderr.write(self.style.ERROR(f"Error writing to file {output_filename}"))
            sys.exit(2)

        self.stdout.write(self.style.SUCCESS(f"Successfully retrieve stats and write {output_filename}"))
