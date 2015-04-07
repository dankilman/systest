import os

import argh
import yaml
from path import path


class Settings(object):

    settings_path = path(
        os.path.expanduser(os.environ.get('SYSTEST_SETTINGS',
                                          '~/.cloudify-systest')))

    def __init__(self):
        self._settings = None

    @property
    def main_suites_yaml(self):
        self._load_settings()
        return path(self._settings['main_suites_yaml'])

    @property
    def user_suites_yaml(self):
        self._load_settings()
        return path(self._settings['user_suites_yaml'])

    @property
    def blueprints_yaml(self):
        self._load_settings()
        return path(self._settings['blueprints_yaml'])

    @property
    def basedir(self):
        self._load_settings()
        return path(self._settings['basedir'])

    def _load_settings(self):
        if self._settings:
            return
        if not self.settings_path.exists():
            raise argh.CommandError('Run `systest init` to configure systest')
        self._settings = yaml.safe_load(self.settings_path.text())

    def write_settings(self,
                       basedir,
                       main_suites_yaml_path,
                       user_suites_yaml_path,
                       blueprints_yaml_path):
        blueprints_yaml_path = blueprints_yaml_path or user_suites_yaml_path
        self.settings_path.write_text(yaml.safe_dump({
            'basedir': os.path.expanduser(basedir),
            'main_suites_yaml': os.path.expanduser(main_suites_yaml_path),
            'user_suites_yaml': os.path.expanduser(user_suites_yaml_path),
            'blueprints_yaml': os.path.expanduser(blueprints_yaml_path)
        }, default_flow_style=False))

    def load_suites_yaml(self, variables=True):
        suites_yaml = yaml.load(self.user_suites_yaml.text())
        if variables:
            main_suites_yaml = yaml.load(self.main_suites_yaml.text())
            variables = main_suites_yaml.get('variables', {})
            variables.update(suites_yaml.get('variables', {}))
            suites_yaml['variables'] = variables
        return suites_yaml

    def load_blueprints_yaml(self, variables=True):
        blueprints_yaml = yaml.load(self.blueprints_yaml.text())
        if variables:
            suites_yaml = self.load_suites_yaml(variables=True)
            variables = suites_yaml['variables']
            variables.update(blueprints_yaml.get('variables', {}))
            blueprints_yaml['variables'] = variables
        return blueprints_yaml
