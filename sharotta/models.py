from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Genre(models.Model):
    WARNA_CHOICES = [
        ('pink', 'Pink'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('purple', 'Purple'),
        ('orange', 'Orange'),
        ('teal', 'Teal'),
        ('red', 'Red'),
    ]

    nama = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)
    warna_class = models.CharField(max_length=10, choices=WARNA_CHOICES, default='pink')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural = 'Genre'


class Anime(models.Model):
    TIPE_CHOICES = [
        ('sub', 'Subtitle'),
        ('dub', 'Dubbing'),
        ('baru', 'Baru'),
    ]
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Selesai'),
        ('upcoming', 'Akan Datang'),
    ]

    judul           = models.CharField(max_length=200)
    slug            = models.SlugField(unique=True, blank=True)
    deskripsi       = models.TextField(blank=True)
    thumbnail       = models.ImageField(upload_to='anime/thumbnails/', blank=True, null=True)
    emoji           = models.CharField(max_length=5, default='🎬', help_text='Emoji pengganti thumbnail')
    warna_bg        = models.CharField(
                        max_length=100,
                        default='linear-gradient(135deg,#1a0a2e,#4a1570)',
                        help_text='CSS gradient untuk background card'
                      )
    genre           = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    tipe            = models.CharField(max_length=5, choices=TIPE_CHOICES, default='sub')
    status          = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ongoing')
    total_episode   = models.PositiveIntegerField(default=0)
    rating          = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    views           = models.PositiveIntegerField(default=0)
    is_populer      = models.BooleanField(default=False)
    dibuat          = models.DateTimeField(auto_now_add=True)
    diperbarui      = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.judul)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.judul

    class Meta:
        ordering = ['-dibuat']


class Komentar(models.Model):
    anime   = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='komentar')
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    episode = models.PositiveIntegerField(default=1)
    isi     = models.TextField()
    dibuat  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} → {self.anime.judul} Ep {self.episode}'

    class Meta:
        ordering = ['-dibuat']


class Pengaturan(models.Model):
    """Model singleton untuk pengaturan situs."""
    pengumuman = models.TextField(
        blank=True,
        help_text='Teks pengumuman yang muncul di sidebar halaman utama'
    )

    def __str__(self):
        return 'Pengaturan Situs'

    class Meta:
        verbose_name = 'Pengaturan Situs'