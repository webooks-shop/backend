from django.db import models
from user.models import *


class Book(models.Model):
	"""책 자체의 정보"""
	title = models.CharField(max_length=200)
	cover_image = models.CharField(max_length=200,null=True)
	author = models.CharField(max_length=50, null=True)
	publisher = models.CharField(max_length=20, null=True)

	def __str__(self):
		return f"{self.title}"

	class Meta:
		db_table = "books"


class Comment(models.Model):
	"""유저와 책 사이의 댓글 테이블"""
	user = models.ForeignKey('user.User', on_delete=models.CASCADE)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	comment = models.CharField(max_length=200)

	class Meta:
		db_table = "comments"


class Recommend(models.Model):
	user = models.ForeignKey('user.User', on_delete=models.CASCADE)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	recommend = models.IntegerField()

	class Meta:
		db_table = "recommends"


class Rating(models.Model):
	user = models.ForeignKey('user.User', on_delete=models.CASCADE)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	rating = models.IntegerField()

	class Meta:
		db_table = "ratings"


class ReadTime(models.Model):
	user = models.ForeignKey('user.User', on_delete=models.CASCADE)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	read_time = models.IntegerField()

	class Meta:
		db_table = "readtimes"
