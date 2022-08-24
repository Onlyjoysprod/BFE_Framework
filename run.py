from bfe_framework.main import Framework, DebugApplication, FakeApplication
from urls import fronts
from views import routes
from wsgiref.simple_server import make_server

# application = Framework(routes, fronts)

application = DebugApplication(routes, fronts)

# application = FakeApplication(routes, fronts)

with make_server('', 8080, application) as httpd:
    print("Сервер запущен. Порт: 8080...")
    httpd.serve_forever()
