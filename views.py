from datetime import date

from bfe_framework.templator import render
from patterns.creational_patterns import Engine, Logger
from patterns.architectural_system_pattern_mappers import MapperRegistry
from patterns.structural_patterns import AppRoute, Debug
from patterns.behavioral_patterns import BaseSerializer, ListView, PostGetView, \
    TemplateView, SmsNotifier, EmailNotifier
from patterns.architectural_system_pattern_unit_of_work import UnitOfWork

site = Engine()
logger = Logger('main')

email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()

routes = {}

UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


@AppRoute(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)


@AppRoute(routes=routes, url='/about/')
class About:
    @Debug(name='About')
    def __call__(self, request):
        return '200 OK', render('about.html')


@AppRoute(routes=routes, url='/study-programs/')
class StudyPrograms:
    @Debug(name='StudyPrograms')
    def __call__(self, request):
        return '200 OK', render('study-programs.html', data=date.today())


@AppRoute(routes=routes, url='/create-course/')
class CreateCourse(PostGetView):
    template_name = 'create_course.html'
    category_id = -1

    def control_get(self, params):
        id = params['id']
        category = MapperRegistry.get_current_mapper('category').find_by_id(id)
        params['category_name'] = category.name
        return params

    def control_post(self, data: dict):
        if data['name']:
            name = data['name']
        else:
            name = f'some course'
        name = site.decode_value(name)
        type_ = data['type_']

        self.category_id = self.local_data['id']
        if self.category_id != -1:
            category = MapperRegistry.get_current_mapper('category').\
                find_by_id(int(self.category_id))

            course = site.create_course(type_, name, category.id)

            course.observers.append(email_notifier)
            course.observers.append(sms_notifier)

            category.courses.append(course)

            course.mark_new()
            UnitOfWork.get_current().commit()


# @AppRoute(routes=routes, url='/update-course/')
# class UpdateCourse:
#     id = -1
#     category_id = -1
#
#     @Debug(name='UpdateCourse')
#     def __call__(self, request):
#         if request['method'] == 'POST':
#             course = site.get_course_by_id(int(self.id))
#             print(course)
#             print(request)
#             data = request['data']
#
#             if data['name']:
#                 name = data['name']
#             else:
#                 name = f'some course'
#             name = site.decode_value(name)
#
#             course.update_course(name)
#
#             category = site.find_category_by_id(self.category_id)
#             print(category)
#
#             return '200 OK', render('course_list.html', objects_list=category.courses,
#                                     name=category.name, id=category.id)
#
#         else:
#             print(request)
#             data = request['request_params']
#             self.id = int(data['id'])
#             self.category_id = int(data['category_id'])
#             course = site.get_course_by_id(int(self.id))
#             print(course)
#
#             return '200 OK', render('update_course.html', course=course)


@AppRoute(routes=routes, url='/courses-list/')
class CoursesList(PostGetView):
    template_name = 'course_list.html'

    def control_get(self, params):
        category_id = params['id']
        category = MapperRegistry.get_current_mapper('category').find_by_id(category_id)
        params['category_name'] = category.name

        mapper = MapperRegistry.get_current_mapper('course')

        params['objects_list'] = mapper.find_by_category_id(category_id)

        return params


class NotFound404:
    def __call__(self, request):
        return '404 WHAT', render('404.html')


@AppRoute(routes=routes, url='/create-category/')
class CreateCategory(PostGetView):
    template_name = 'create_category.html'

    def control_get(self, params):
        # заглушка. Пока нет реализации подкатегорий
        params = {'category_id': '0'}
        return params

    def control_post(self, data: dict):
        if data['name']:
            name = data['name']
        else:
            name = 'some category'
        name = site.decode_value(name)
        print('----------', self.local_data)
        category_id = int(self.local_data['category_id'])

        if category_id != 0:
            category = MapperRegistry.get_current_mapper('category').find_by_id(category_id)
        else:
            category = None

        new_category = site.create_category(name, category)

        site.categories.append(new_category)

        new_category.mark_new()
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/category-list/')
class CategoryList(PostGetView):
    template_name = 'category_list.html'

    def control_get(self, params):
        mapper = MapperRegistry.get_current_mapper('category')
        params['objects_list'] = mapper.all()

        for item in params['objects_list']:
            courses = MapperRegistry.get_current_mapper('course').find_by_category_id(item.id)
            for course in courses:
                item.courses.append(course)

        return params


# @AppRoute(routes=routes, url='/copy-course/')
# class CopyCourse:
#     @Debug(name='CopyCourse')
#     def __call__(self, request):
#         request_params = request['request_params']
#
#         try:
#             name = request_params['name']
#             old_course = site.get_course(name)
#             if old_course:
#                 new_name = f'copy_{name}'
#                 new_course = old_course.clone()
#                 new_course.name = new_name
#                 site.courses.append(new_course)
#
#             return '200 OK', render('course_list.html', objects_list=site.courses)
#         except KeyError:
#             return '200 OK', 'No courses have been added yet'


@AppRoute(routes=routes, url='/student-list/')
class StudentListView(ListView):
    template_name = 'student_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('student')
        return mapper.all()


@AppRoute(routes=routes, url='/create-student/')
class StudentCreateView(PostGetView):
    template_name = 'create_student.html'

    def control_post(self, data: dict):
        if data['name']:
            name = data['name']
        else:
            name = 'some student'
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/add-student/')
class AddStudentByCourseCreateView(PostGetView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = MapperRegistry.get_current_mapper('course').all()
        context['students'] = MapperRegistry.get_current_mapper('student').all()
        print(context)
        return context

    def control_post(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = MapperRegistry.get_current_mapper('course').find_by_name(course_name)

        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = MapperRegistry.get_current_mapper('student').find_by_name(student_name)

        course.add_student(student)

        student.mark_new()
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/api/')
class CourseApi:
    @Debug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()
