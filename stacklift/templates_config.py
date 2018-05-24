import yaml
import os


class TemplatesConfig:
    def __init__(self, templates_config_path):
        with open(templates_config_path) as f:
            self.templates_config = yaml.load(f)
        self.templates_file_dir = os.path.dirname(templates_config_path)

    def get_group(self, group_name):
        group = self.templates_config["Groups"].get(group_name)
        if group is None:
            raise RuntimeError("Group {} is not defined.".format(group_name))
        return group

    def get_templates_dict(self, group_name):
        group = self.get_group(group_name)
        return {template["Name"]: template for template in group["Templates"]}

    def get_template_config(self, group_name, template_name):
        template_dict = self.get_templates_dict(group_name)

        template = template_dict.get(template_name)
        if not template:
            raise RuntimeError("Template {} is not found.".format(template_name))

        return template

    def get_group_template_names(self, group_name):
        template_dict = self.get_templates_dict(group_name)
        return template_dict.keys()
