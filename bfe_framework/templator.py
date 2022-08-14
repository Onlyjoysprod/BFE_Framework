from jinja2 import Template, FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    """
    :param template_name: имя шаблона
    :param kwargs: параметры
    :return:
    """
    env = Environment()
    env.loader = FileSystemLoader(folder)
    template = env.get_template(template_name)
    return template.render(**kwargs)
