from django.contrib import admin
from .models import Anime, Genre, Komentar, Pengaturan


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display  = ('nama', 'slug', 'warna_class')
    prepopulated_fields = {'slug': ('nama',)}


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display   = ('judul', 'genre', 'tipe', 'status', 'rating', 'views', 'is_populer', 'dibuat')
    list_filter    = ('tipe', 'status', 'genre', 'is_populer')
    search_fields  = ('judul',)
    list_editable  = ('is_populer', 'rating')
    prepopulated_fields = {'slug': ('judul',)}


@admin.register(Komentar)
class KomentarAdmin(admin.ModelAdmin):
    list_display = ('user', 'anime', 'episode', 'dibuat')
    list_filter  = ('anime',)


@admin.register(Pengaturan)
class PengaturanAdmin(admin.ModelAdmin):
    pass