from django.db import models

class FXRate(models.Model):
    pair = models.CharField(max_length=10)  # e.g., "EURUSD"
    date = models.DateField()
    rate = models.FloatField()

    class Meta:
        unique_together = ("pair", "date")
        ordering = ["-date", "pair"]

    def __str__(self):
        return f"{self.pair} {self.date}: {self.rate}"


class NewsItem(models.Model):
    pair = models.CharField(max_length=10)  # e.g., "EURUSD"
    title = models.CharField(max_length=500)
    source = models.CharField(max_length=200, blank=True)
    published_at = models.DateTimeField()
    url = models.URLField(max_length=1000)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return f"{self.pair} {self.published_at}: {self.title[:50]}"
