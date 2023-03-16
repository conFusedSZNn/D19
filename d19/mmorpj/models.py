from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
   categ_name = models.CharField(max_length=255, unique=True, default='Неизвестная категория')

   def __str__(self):
      return f'{self.categ_name}'


class Post(models.Model):
   author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец объявления', blank= True, null= True)
   date_of_post = models.DateTimeField(auto_now_add=True)
   category_link = models.ManyToManyField(Category, default='Неизвестная категория')
   title = models.CharField(max_length=255)
   text = models.TextField(max_length=5000, default='')
   post = models.IntegerField(blank=True, null=True, unique=True)

   def __str__(self):
      return f'{self.title}: {self.text[:20]} ' \
             f' Дата публикации: {self.date_of_post}'



class Reply(models.Model):
   author_reply = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор отклика', blank= True, null= True)
   reply_link_post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Объявление', blank= True, null= True, related_name='comments_articles')
   reply_text = models.TextField(verbose_name= '')
   status = models.BooleanField(verbose_name='Видимость статьи', default= False)


