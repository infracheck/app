import logging
import subprocess
import uuid
from pathlib import Path
from typing import List

from jsonschema import validate

from Environment import Environment
from infracheck.Persistence import Persistence
from infracheck.helper.PdfGenerator import PdfGenerator
from infracheck.helper.load_packages import load_packages
from infracheck.helper.schemes import test_data_scheme
from infracheck.model.IPlugin import IPlugin
from infracheck.model.ITestData import ITestData
from infracheck.model.ITestResult import ITestResult, IPluginResult

log = logging.getLogger()


class PluginManager(object):
    """Upon creation, this class will read the plugins package for modules
    that contain a class definition that is inheriting from the Plugin class
    """

    plugins: List[IPlugin] = []
    database = Persistence()

    def list_plugins(self):
        """Returns a list of plugins that are available
        """
        res = list({
                       "id": x.id,
                       "version": x.version,
                       "documentation": x.documentation,
                       "modules": x.list_modules(),
                       "data": x.data,
                       "type": "plugin"
                   } for x in self.plugins)
        return res

    def __init__(self):
        """Constructor that initiates the reading of all available plugins
        when an instance of the PluginCollection object is created
        """
        self._reload_plugins()

    def _reload_plugins(self):
        """Reset the list of all plugins and initiate the walk over the main
        provided plugin package to load all available plugins
        """
        # Install requirements for all plugins
        log.info(F"|- INSTALL REQUIREMENTS -|")
        self._install_requirements()
        # Load all plugins
        log.info(F"|- INSTALL PLUGINS -|")
        self.plugins: List[IPlugin] = load_packages('plugins', IPlugin)

    def launch_tests(self, data: ITestData) -> ITestResult:
        """ Run all tests defined in the json

        :param data:
        :return:
        """
        uid = uuid.uuid4().hex
        is_not_valid = validate(instance=data, schema=test_data_scheme)
        if is_not_valid:
            raise TypeError(is_not_valid)

        plugin_results: List[IPluginResult] = []
        log.info(F"Launching the test with name: {data['name']}")
        for plugin_test_data in data['plugins']:
            plugin_result: IPluginResult = self._get_test_plugin(plugin_test_data['id']).test(plugin_test_data)
            plugin_results.append(plugin_result)

        # Create results
        result = self._serialize_result(uid, data, plugin_results)
        PdfGenerator().generate(result)
        self.database.insert_test_result(result)

        return result

    def _get_test_plugin(self, plugin_name: str) -> IPlugin:
        """ Returns the right plugin object, receiving id and version

        :param plugin_name:
        :return:
        """
        return list(filter(lambda plugin: plugin.id == plugin_name, self.plugins))[0]

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
    def _serialize_result(uid: str, input_data: ITestData, plugin_results: List[IPluginResult]) -> ITestResult:
        """ Takes multiple plugin results and serialize them to one response
        """
        result: ITestResult = {
            "id": uid,
            "pdf_link": F"/{Environment.RESULT_FOLDER}{uid}.pdf",
            "name": input_data['name'],
            "description": input_data['description'],
            "succeeded": sum(c['succeeded'] for c in plugin_results),
            "failures": sum(c['failures'] for c in plugin_results),
            "errors": sum(c['errors'] for c in plugin_results),
            "total": sum(c['total'] for c in plugin_results),
            "message": "PLEASE IMPLEMENT",
            "plugin_data": plugin_results
        }
        if result["failures"] == 0:
            result["message"] = 'Test complete. No failures.'
        else:
            result["message"] = F"Test complete but {result['failures']} failure detected."
        return result
