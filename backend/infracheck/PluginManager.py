import json
import logging
import subprocess
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from infracheck import app
from infracheck.Persistence import Persistence
from infracheck.helper.load_packages import load_packages
from infracheck.model.Plugin import Plugin
from infracheck.model.TestInput import TestInput
from infracheck.model.TestResult import TestResult, PluginResult

log = logging.getLogger()


class PluginManager(object):
    """Upon creation, this class will read the plugins package for modules
    that contain a class definition that is inheriting from the Plugin class
    """

    def __init__(self):
        """Constructor that initiates the reading of all available plugins
        when an instance of the PluginCollection object is created
        """
        self.database = Persistence()

    @property
    def _plugins(self) -> Dict[str, Plugin]:
        plugins: List[Plugin] = load_packages("plugins", Plugin)
        return {
            plugin.__id__: plugin
            for plugin in plugins
        }

    @property
    def json(self) -> json:
        """
        A JSON format that is displayed by the api
        :return:
        """
        return {
            plugin_id: plugin_class.json
            for plugin_id, plugin_class
            in self._plugins.items()
        }

    def _get_plugin_instance(self, plugin_id):
        """
        Creates a fresh instance of a plugin by its plugin id

        :param plugin_id:
        :return:
        """
        return self._plugins[plugin_id].__class__()

    def launch_tests(self, test_input: TestInput) -> TestResult:
        """ Run all tests defined in the json

        :param test_input:
        :return:
        """
        uid = uuid.uuid4().hex
        plugin_results: List[PluginResult] = []

        for plugin_input in test_input.plugins:
            plugin: Plugin = self._get_plugin_instance(plugin_input.id)
            plugin._set_props(plugin_input.props)
            plugin_results.append(plugin.test(plugin_input))

        # Create results
        result = self._serialize_result(uid, test_input, plugin_results)
        result = self.remove_passwords(result)
        # PdfGenerator().generate(result)
        self.database.add_result(result)
        return result

    def _reload_plugins(self):
        """Reset the list of all plugins and initiate the walk over the main
        provided plugin package to load all available plugins
        """
        # Install requirements for all plugins
        log.info(F"|- INSTALL REQUIREMENTS -|")
        self._install_requirements()
        # Load all plugins
        log.info(F"|- INSTALL PLUGINS -|")
        self.plugins: List[Plugin] = load_packages('plugins', Plugin)

    @staticmethod
    def _install_requirements():
        """
        Before loading plugins it is necessary to install their requirements
        This function search for requirements.txt files inside the plugin folder and installs them

        :return:
        """
        requirements = []
        for path in Path('plugins').rglob('requirements.txt'):
            with open(path) as requirements_file:
                requirements = requirements + requirements_file.read().splitlines()

        # Remove duplicates
        requirements = sorted(list(dict.fromkeys(requirements)))

        # Check version conflicts
        mapped_requirements = [entry.split("==")[0] for entry in requirements]
        conflicts = set([x for x in mapped_requirements if mapped_requirements.count(x) > 1])
        [
            log.warning(F"Different '{conflict}' versions detected.")
            for conflict in conflicts
        ]

        # Install every package, but remove duplicates beforehand
        for package in requirements:
            try:
                sp = subprocess.Popen(['pip', 'install', package], stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT)
                sp.communicate()
                if sp.returncode == 0:
                    log.info(F"|---- {package}")
                else:
                    log.error(F"{package} was not installed")
            except Exception as e:
                log.error(e)

    @staticmethod
    def _serialize_result(uid: str, input_data: TestInput, plugin_results: List[PluginResult]) -> TestResult:
        """ Takes multiple plugin results and serialize them to one response
        """
        result = TestResult(
            id=uid,
            pdf_link=F"/{app.config['RESULT_FOLDER']}{uid}.pdf",
            name=input_data.name,
            description=input_data.description,
            success_count=sum(c.success_count for c in plugin_results),
            failure_count=sum(c.failure_count for c in plugin_results),
            total_count=sum(c.total_count for c in plugin_results),
            message="PLEASE IMPLEMENT",
            date=datetime.now(),
            plugin_result=plugin_results
        )
        if result.failure_count == 0:
            result.message = 'Test complete. No failure_count.'
        else:
            result.message = F"Test complete but {result.failure_count} failure detected."
        return result

    @staticmethod
    def remove_passwords(data: TestResult) -> TestResult:
        return data
