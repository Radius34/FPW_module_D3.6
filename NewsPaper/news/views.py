from django.shortcuts import render
from .models import Article

def news(request):
    articles = Article.objects.all().order_by('-date')  # получаем все статьи в порядке от новых к старым
    context = {
        'articles': articles
    }
    return render(request, 'news.html', context)

