def application(environ, start_response):
    """
    :param environ: словарь данных от сервера
    :param start_response: функция для ответа серверу
    :return:
    """
    # сначала в функцию start_response передаем код ответа и заголовки
    start_response('200 OK', [('Content-Type', 'text/html')])
    # возвращаем тело ответа в виде списка из bite
    return [b'Hello world from a simple WSGI application!']

# для запуска можно использовать gunicorn или uwsgi

# gunicorn simple_wsgi:application

# uwsgi --http :8000 --wsgi-file main.py

