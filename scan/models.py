from django.db import models

MAXIMUM_VARCHAR_SIZE_MYSQL = 191  # becase of utf8mb4


class User(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    login = models.CharField(max_length=MAXIMUM_VARCHAR_SIZE_MYSQL, null=False, blank=False)
    url = models.CharField(max_length=MAXIMUM_VARCHAR_SIZE_MYSQL, null=False, blank=False)

    def __str__(self):
        return self.login


class Repository(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    description = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=MAXIMUM_VARCHAR_SIZE_MYSQL, null=False, blank=False)
    full_name = models.CharField(max_length=MAXIMUM_VARCHAR_SIZE_MYSQL, null=False, blank=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    pushed_at = models.DateTimeField()
    language = models.CharField(max_length=MAXIMUM_VARCHAR_SIZE_MYSQL, null=True, blank=True)
    forks_count = models.IntegerField(null=False)
    stargazers_count = models.IntegerField(null=False)
    watchers_count = models.IntegerField(null=False)

    def __str__(self):
        return self.name
