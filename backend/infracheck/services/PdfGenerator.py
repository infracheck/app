import collections
import json
import os

from fpdf import FPDF

from infracheck import app
from infracheck.model.TestResult import TestResult

RESULT_FOLDER = app.config['RESULT_FOLDER']
ROOT_DIR = app.config['ROOT_DIR']


class PdfGenerator(FPDF):
    """
    Class that generates a pdf file based on the TestResults
    """

    def __init__(self):
        if not os.path.exists(RESULT_FOLDER):
            os.makedirs(RESULT_FOLDER)
        super().__init__('P', 'mm', 'A4')
        self.set_font('Arial', '', 16)
        self.set_text_color(0, 0, 0)
        self.add_page()

    def header(self):
        """
        Creates a fancy header with the proficom logo.
        :return:
        """
        self.set_font_size(18)
        self.cell(0, 15, 'InfraCheck - Report', 0, 0, 'L', 0)
        image = os.path.join(ROOT_DIR, 'infracheck/assets/proficomlogo.png')
        self.image(image, 140, 10, 60)
        self.ln(18)

    def chapter_title(self, num, label):
        """
        Creates a title chapter and it's divider.
        This is used for plugin sections
        :param num:
        :param label:
        :return:
        """
        self.set_font_size(14)
        self.set_text_color(255, 255, 255)
        self.set_fill_color(11, 114, 181)
        self.cell(0, 12, 'Part %d : %s' % (num, label), 0, 1, 'L', 1)
        self.ln(1)
        self.set_text_color(0, 0, 0)

    def footer(self):
        """
        Adds a footer element displaying page index
        :return:
        """
        self.set_y(-15)
        self.set_font_size(8)
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def print_module_chapter(self, title):
        """
        Creates a module sub chapter
        with slightly bigger font
        and a colored background
        :param title:
        :return:
        """
        self.set_font_size(12)
        self.set_text_color(255, 255, 255)
        self.set_fill_color(43, 114, 115)
        self.cell(0, 10, 'Module <<%s>>' % title, 0, 1, 'L', 1)
        self.ln(2)
        self.set_text_color(0, 0, 0)

    def print_info(self, name, value):
        """
        Print simple information in a <key, value> format.
        It recognise json values and formats them properly.
        :param name:
        :param value:
        :return:
        """
        self.set_text_color(0, 0, 0)
        self.set_font('Arial', '', 10)
        if isinstance(value, (collections.abc.Mapping, list, tuple)):
            self.multi_cell(190, 4, str(name.title()), 0, 'J', 0, False)
            self.multi_cell(190, 4, json.dumps(value, sort_keys=True, indent=4), 0, 'J', 0, False)
        else:
            self.multi_cell(190, 4, str(name.title()) + ': ' + str(value), 0, 'J', 0, False)
        self.ln(2)

    def generate(self, report: TestResult):
        """
        Generates the document
        TODO: Refactor massive amount of method calls
        :param report:
        :return:
        """
        self.alias_nb_pages()
        self.chapter_title(1, 'General Data')
        self.print_info("id", report.id)
        self.print_info("name", report.label)
        self.print_info("description", report.description)
        self.print_info("message", report.message)
        self.print_info("date", report.date)
        self.print_info("total_count", report.total_count)
        self.print_info("success_count", report.success_count)
        self.print_info("failure_count", report.failure_count)

        i = 1
        for plugin_data in report.plugin_result:
            i = i + 1
            self.chapter_title(i, F"{plugin_data.plugin_name}")
            self.print_info("name", plugin_data.plugin_name)
            self.print_info("version", plugin_data.plugin_version)
            self.print_info("message", plugin_data.message)
            self.print_info("input properties", plugin_data.props)
            self.print_info("total test count", plugin_data.total_count)
            self.print_info("successful tests", plugin_data.success_count)
            self.print_info("failed tests", plugin_data.failure_count)

            for module_data in plugin_data.module_result:
                self.print_module_chapter(module_data["module_name"])
                self.print_info("name", module_data["module_name"])
                self.print_info("version", module_data["module_version"])
                self.print_info("properties", module_data["props"])
                self.print_info("successful", module_data["result_successful"])
                self.print_info("message", module_data["result_message"])
                self.print_info("result data", module_data["result_data"])

        self.output(F"{RESULT_FOLDER}{report.id}.pdf", 'F')
