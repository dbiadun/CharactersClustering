from jinja2 import Environment, FileSystemLoader


class HTMLCreator:
    """
    Class used to create HTML files based on templates.
    """

    @staticmethod
    def create_html(template_path, output_path, **kwargs):
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template(template_path)
        with open(output_path, 'w') as fh:
            fh.write(template.render(**kwargs))
