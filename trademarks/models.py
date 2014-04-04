from django.db import models

class Word(models.Model):
    word = models.CharField(max_length=50)
    ipa = models.CharField(max_length=50)
    meaning = models.CharField(max_length=1000)
    lang = models.CharField(max_length=5)
    transcription = models.CharField(max_length=50)
    def __str__(self):
        return self.word
    def __unicode__(self):
        return self.word
    def serialize(self):
        return {
            "word": self.word,
            "ipa": self.ipa,
            "meaning": self.meaning,
            "lang": self.lang,
            "transcription": self.transcription
        }
