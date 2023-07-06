from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django import template

class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.post_set = None

    def update_rating(self):
       postRat = self.post_set.aggregate(Sum('rating'))
       pRat = 0
       pRat += postRat.get('postRating')

       commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
       cRat = 0
       cRat + commentRat.get('commentRating')

       self.ratingauthor = pRat *3 + cRat
       self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post (models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE )

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(max_lenght=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    titel = models.CharField(max_lenght=128)
    text = models.TextField()
    ratingAuthor = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'



class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

register = template.Library()

    @register.filter(name='censor')
    def censor(value):
        censored_words = ['редиска', 'мат', 'оскорбление']  # список нежелательных слов
        for word in censored_words:
            value = value.replace(word, '*' * len(word))
        return value

