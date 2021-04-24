from django.db import models


class User(models.Model):
	name = models.CharField(max_length=20)
	group = models.IntegerField(null=True)
	bf = models.IntegerField(null=True)
	image = models.URLField(default=
    "https://image.ohou.se/i/bucketplace-v2-development/uploads/default_images/avatar.png?gif=1&w=144&h=144&c=c&webp=1", null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'users'


