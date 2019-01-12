from django.db import models

class User(models.Model):
    user_id = models.IntegerField()
    first_name = models.CharField(max_length=100, blank = True)
    last_name = models.CharField(max_length=100, blank = True)
    city_id = models.IntegerField()
    show = models.BooleanField(default=True)


    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' ' + str(self.city_id)


class Post(models.Model):
    class Meta:
        unique_together = ('post_id', 'post_owner')

    post_id = models.IntegerField()
    post_owner = models.ForeignKey('User', blank = True, default = 0, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    date = models.IntegerField()
    show = models.BooleanField(default=True)
    search = models.CharField(max_length=100, default=None)

    def __str__(self):
        return self.text[:100]


