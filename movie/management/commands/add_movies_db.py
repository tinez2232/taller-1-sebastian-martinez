import csv
import os
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = 'Carga las primeras 100 películas desde movies_initial.csv'

    def handle(self, *args, **kwargs):
        csv_path = os.path.join(os.path.dirname(__file__), 'movies_initial.csv')

        with open(csv_path, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                if count >= 100:
                    break

                title = row.get('title') or ''
                description = row.get('plot') or ''
                genre = row.get('genre') or ''
                year_value = row.get('year')

                try:
                    year = int(year_value)
                except (TypeError, ValueError):
                    year = None

                Movie.objects.create(
                    title=title,
                    description=description[:250],  # el modelo limita a 250 caracteres
                    genre=genre[:250],
                    year=year,
                    image='movie/images/default.jpg',
                    url=''
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Se cargaron {count} películas exitosamente.'))