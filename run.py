from bfe_framework.main import DebugApplication, FakeApplication
from urls import fronts
from views import routes
from wsgiref.simple_server import make_server
import argparse


def arg_parser(default_port, default_mode):
    parser = argparse.ArgumentParser(description='Chose port and launch mode')
    parser.add_argument('port', type=int, help='Input port', default=default_port, nargs='?')
    parser.add_argument('mode', type=str, help='Input mode', default=default_mode, nargs='?')
    namespace = parser.parse_args()
    port = namespace.port
    mode = namespace.mode
    return port, mode


def main():
    port, mode = arg_parser(8080, 'debug')
    modes = {'debug': DebugApplication(routes, fronts),
             'fake': FakeApplication(routes, fronts)}

    application = modes[mode]
    print(application)

    with make_server('', 8080, application) as httpd:
        print("Сервер запущен. Порт: 8080...")
        httpd.serve_forever()


if __name__ == '__main__':
    main()
