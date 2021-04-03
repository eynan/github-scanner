from django.db import models

class User(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    login = models.CharField(max_length=250, null=False, blank=False)
    url = models.CharField(max_length=250, null=False, blank=False)
    name = models.CharField(max_length=250, null=True, blank=True)
    company = models.CharField(max_length=250, null=True, blank=True)
    location = models.CharField(max_length=250, null=True, blank=True)
    email = models.CharField(max_length=250, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    twitter_username = models.CharField(max_length=250, null=True, blank=True)
    public_repos = models.IntegerField(null=False)
    public_gists = models.IntegerField(null=False)
    followers = models.IntegerField(null=False)
    following = models.IntegerField(null=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.login
