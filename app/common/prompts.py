import os
from jinja2 import Environment, FileSystemLoader

def render_template(template_name: str, **kwargs) -> str:
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts")
    env = Environment(loader=FileSystemLoader(template_dir))
    tpl = env.get_template(template_name)
    return tpl.render(**kwargs)
