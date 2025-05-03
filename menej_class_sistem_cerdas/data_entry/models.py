from django.db import models

class Pengguna(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=100)
    address_1 = models.TextField()
    address_2 = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=20, help_text='Enter your city')
    state = models.TextField()
    zip_code = models.CharField(max_length=7)
    tanggal_join = models.DateField(auto_now=True)  # Tanggal bergabung

    def _str_(self):
        return self.email

class Content(models.Model):
    author = models.ForeignKey(Pengguna, on_delete=models.CASCADE)  # Relasi dengan Pengguna
    data_created = models.DateTimeField(auto_now_add=True)  # Tanggal pembuatan artikel
    artikel = models.TextField()  # Isi artikel
    set_view = models.BooleanField(default=False)  # Flag untuk menandakan apakah artikel sudah dilihat

    def _str_(self):
        return f"Artikel oleh {self.author.email}"  # Menampilkan email pengarang artikel