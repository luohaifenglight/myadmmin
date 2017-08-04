#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management import BaseCommand
from backend.accounts.viewmodel import CommandModel

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('param', nargs='+', type=str)

    '''
       init_perms
    '''

    def handle(self, *args, **options):
        for param in options['param']:
            if param == 'init':
                CommandModel.update_model()
                CommandModel.update_perms()

