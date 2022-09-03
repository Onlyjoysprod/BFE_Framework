import sys
import jsonpickle

sys.path.append("..")
from bfe_framework.templator import render


class Observer:

    def update(self, subject):
        pass


class Subject:
    def __init__(self):
        self.observers = []

    def notify(self):
        print('observers: ', self.observers)
        for item in self.observers:
            item.update(self)


class SmsNotifier(Observer):

    def update(self, subject):
        print('SMS --->', 'присоединился', subject.students[-1].name)


class EmailNotifier(Observer):

    def update(self, subject):
        print('EMAIL --->', 'присоединился', subject.students[-1].name)


class BaseSerializer:
    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return jsonpickle.dumps(self.obj)

    @staticmethod
    def load(data):
        return jsonpickle.loads(data)


class TemplateView:
    local_data = []
    context = {}
    template_name = 'template.html'

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self):
        template_name = self.get_template()
        context = self.get_context_data()
        return '200 OK', render(template_name, **context)

    def render_template_with_params(self, params):
        template_name = self.get_template()
        return '200 OK', render(template_name, **params)

    def __call__(self, requests):
        return self.render_template_with_context()


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context

    # def __call__(self, request):
    #     pass


class PostGetView(TemplateView):
    queryset = []
    template_name = 'create.html'
    context_object_name = 'request_params'

    # data из post
    @staticmethod
    def get_request_data(request):
        return request['data']

    # params из get
    def get_request_params(self, request):
        if request['request_params']:
            return request['request_params']
        else:
            return {'request_params': []}

    def control_post(self, data):
        pass

    def control_get(self, params):
        pass

    def get_queryset(self):
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.control_post(data)
            params = self.local_data
            try:
                return self.render_template_with_params(params)
            except TypeError:
                return self.render_template_with_context()
        else:
            try:
                params = self.get_request_params(request)
                params = self.control_get(params)
                self.local_data = params
                return self.render_template_with_params(params)
            except TypeError:
                print('FAAAIL')
                return super().__call__(request)


class ConsoleWriter:

    def write(self, text):
        print(text)


class FileWriter:
    def __init__(self, file_name):
        self.file_name = file_name

    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')
