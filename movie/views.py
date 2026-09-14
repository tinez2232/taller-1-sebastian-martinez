from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
import matplotlib
import io
import base64

from .models import Movie
# Create your views here.


def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)  
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies': movies})    

def about(request):
    #return HttpResponse("<h1>welcome to the About page</h1>")
    return render(request, 'about.html')    

def statistics_view(request):
    matplotlib.use('Agg')

    all_movies = Movie.objects.all()
    
    movie_counts_by_year = {}

    for movie in all_movies:
        year = movie.year if movie.year else "None"
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1

    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_year))

    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return render(request, 'statistics.html', {'graphic': graphic})


def statistics_view(request):
    matplotlib.use('Agg')

    # ===== Gráfica 1: Películas por año =====
    all_movies = Movie.objects.all()
    movie_counts_by_year = {}

    for movie in all_movies:
        year = movie.year if movie.year else "None"
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1

    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_year))

    plt.figure()
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic_year = base64.b64encode(image_png).decode('utf-8')

    # ===== Gráfica 2: Películas por género (solo el primer género) =====
    movie_counts_by_genre = {}

    for movie in all_movies:
        if movie.genre:
            first_genre = movie.genre.split(',')[0].strip()
        else:
            first_genre = "None"

        if first_genre in movie_counts_by_genre:
            movie_counts_by_genre[first_genre] += 1
        else:
            movie_counts_by_genre[first_genre] = 1

    bar_positions_genre = range(len(movie_counts_by_genre))

    plt.figure()
    plt.bar(bar_positions_genre, movie_counts_by_genre.values(), width=0.5, align='center', color='green')
    plt.title('Movies per genre (first only)')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions_genre, movie_counts_by_genre.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer2 = io.BytesIO()
    plt.savefig(buffer2, format='png')
    buffer2.seek(0)
    plt.close()

    image_png2 = buffer2.getvalue()
    buffer2.close()
    graphic_genre = base64.b64encode(image_png2).decode('utf-8')

    return render(request, 'statistics.html', {'graphic': graphic_year, 'graphic_genre': graphic_genre})

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})
