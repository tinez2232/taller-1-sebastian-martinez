import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from news.models import News

class Command(BaseCommand):
    help = 'Carga 5 noticias desde Fake.csv'

    def handle(self, *args, **kwargs):
        csv_path = os.path.join(os.path.dirname(__file__), 'Fake.csv')

        with open(csv_path, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                if count >= 5:
                    break

                headline = row.get('title') or ''
                body = row.get('text') or ''
                date_str = row.get('date') or ''

                try:
                    date_value = datetime.strptime(date_str, '%B %d, %Y').date()
                except ValueError:
                    # Si la fecha no tiene el formato esperado (a veces el dataset trae URLs u otros valores raros), se salta esa fila
                    continue

                News.objects.create(
                    headline=headline[:200],  # el modelo limita a 200 caracteres
                    body=body,
                    date=date_value
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Se cargaron {count} noticias exitosamente.'))