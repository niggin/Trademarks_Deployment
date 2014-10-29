from django.db import models


class Word(models.Model):
    word = models.CharField(max_length=50)
    ipa = models.CharField(max_length=50)
    meaning = models.CharField(max_length=1000)
    meaning_eng = models.CharField(max_length=1000)
    lang = models.CharField(max_length=5)
    transcription = models.CharField(max_length=50)
    fullipa = models.CharField(max_length=50)

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
            "transcription": self.transcription,
            "meaning_eng": self.meaning_eng,
            "fullipa": self.fullipa
        }


class History(models.Model):
    word = models.CharField(max_length=50, unique=True)
    requests = models.IntegerField(default=0)

    def __str__(self):
        return self.word

    def __unicode__(self):
        return self.word


class Session(models.Model):
    word = models.ForeignKey(History)
    user_id = models.CharField(max_length=40)

    def __str__(self):
        return self.word

    def __unicode__(self):
        return self.word


class UserReaction(models.Model):
    input_word = models.CharField(max_length=50)
    to_word = models.ForeignKey(Word)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)


    def __str__(self):
        return self.input_word

    def __unicode__(self):
        return self.input_word