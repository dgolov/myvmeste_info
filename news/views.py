from django.shortcuts import render
from django.views import View


class NewsView(View):
    """ Представление раздела контакты
    """
    def get(self, request, *args, **kwargs):
        context = {
                'user': request.user,
                'title': "Новости",
        }
        return render(request, 'news/news.html', context)
