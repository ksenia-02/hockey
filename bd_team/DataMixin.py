menu = [{'title': "Игроки", 'url_name': 'list_players'},
        {'title': "Расписание матчей", 'url_name': 'list_game'},
        {'title': "Архив сыгранных матчей", 'url_name': 'archive_game'},
        {'title': "Выход", 'url_name': 'logout'},
        ]

class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context

def get_user_context():
    context = {
        'menu': menu,
    }
    return context