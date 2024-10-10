from django.shortcuts import render

# Create your views here.
from .models import Article
from django.views.generic import ListView, DetailView

class ShowAllView(ListView):
    '''Create a subclass of ListView to display all blog articles.'''
    model = Article # retrieve objects of type Article from the database
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' # how to find the data in the template file

class RandomArticleView(DetailView):
    ''' Show one random article '''
    model = Article
    Template_name = 'blog/article.html'
    context_object_name = 'article'