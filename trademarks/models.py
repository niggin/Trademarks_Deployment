from django.db import models

class Word(models.Model):
    word = models.CharField(max_length=50)
    ipa = models.CharField(max_length=50)
    meaning = models.CharField(max_length=1000)
    def __str__(self):
        return self.word
