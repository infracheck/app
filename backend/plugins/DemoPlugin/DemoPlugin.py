from dataclasses import dataclass

from infracheck.model.Plugin import Plugin
from infracheck.model.Types import Types


class DemoPlugin(Plugin):
    """These docs will be parsed and used by the API and the frontend"""
    __version__ = 0.5

    @dataclass
    class props:
        """
        Definition of Plugin input
        These props are available inside the Plugin functions and their modules
        These are exposed to the API and should be configured by the user,
        when he launches tests.
        Please define the input type, using the Types available.
         -> Type.Text, Type.Pass
        """
        global_var: Types.Password = "I'm just a default value"

    """
    Define as many private attributes as you need.
    They don't get exposed
    """
    private_value: str = "I am a private attribute"

    def setup(self):
        """
        This method is executed before the test modules
        You can setup your environment, databases, ssh connection,
        or whatever you need before the actual tests start
        :return:
        """

        # You can pass new variables to the modules by adding them to the 'props' object
        # This way, they don't get exposed to the API
        self.props.new_global_variable = "I am a new plugin variable"
        print("no after action")

    def tear_down(self):
        """
        You can do some post processing of your test results here,
        or clean up your test environment
        :return:
        """
        print("no before action")
