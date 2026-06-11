from django.shortcuts import render
from .models import Anime, Genre, Komentar, Pengaturan


def home(request):
    selected_genre = request.GET.get('genre', None)

    # Semua genre untuk filter & tag sidebar
    genres = Genre.objects.all()

    # Query dasar
    anime_qs = Anime.objects.select_related('genre')

    # Filter berdasarkan genre jika dipilih
    if selected_genre:
        anime_qs = anime_qs.filter(genre__slug=selected_genre)

    # 10 anime terbaru
    anime_terbaru = anime_qs.order_by('-dibuat')[:10]

    # 10 anime populer (berdasarkan views atau flag is_populer)
    anime_populer = anime_qs.filter(is_populer=True).order_by('-views')[:10]

    # Top 5 tayang (rating tertinggi)
    top_tayang = Anime.objects.select_related('genre').order_by('-rating')[:5]

    # 4 komentar terbaru
    komentar_terbaru = (
        Komentar.objects
        .select_related('user', 'anime')
        .order_by('-dibuat')[:4]
    )

    # Pengumuman dari pengaturan situs
    try:
        pengumuman = Pengaturan.objects.first().pengumuman
    except AttributeError:
        pengumuman = ''

    context = {
        'genres':          genres,
        'anime_terbaru':   anime_terbaru,
        'anime_populer':   anime_populer,
        'top_tayang':      top_tayang,
        'komentar_terbaru': komentar_terbaru,
        'pengumuman':      pengumuman,
        'selected_genre':  selected_genre,
    }

    return render(request, 'sharotta/home.html', context)