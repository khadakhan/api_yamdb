from django.core.management.base import BaseCommand

from ._constants import NAME_TO_SETTINGS
from ._csv_parsers import csv_parse, standart_row_parse, many_to_many_row_parse


class Command(BaseCommand):
    help = 'Load data to database from CSV'

    def handle(self, *args, **options):
        settings = NAME_TO_SETTINGS[options['model'][0]]
        model = settings['model']
        foreign_keys = settings['foreign_keys']
        redirect = settings['redirect']
        is_many_to_many = settings['is_many_to_many']
        files = options['files']
        row_parser = standart_row_parse
        if is_many_to_many:
            row_parser = many_to_many_row_parse

        for file in files:
            csv_parse(file, row_parser, redirect, foreign_keys, model)

    def add_arguments(self, parser):
        parser.add_argument(
            '-f',
            '--files',
            action='append',
            type=open,
            nargs='+',
            help='CSV files to load'
        )
        parser.add_argument(
            '-m',
            '--model',
            action='store',
            choices=NAME_TO_SETTINGS.keys(),
            nargs=1,
            required=True,
            help='Model into which the values are loaded')
