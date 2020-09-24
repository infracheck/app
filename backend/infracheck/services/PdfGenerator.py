import collections
import json
import os

from fpdf import FPDF

import Configuration
from infracheck import app
from infracheck.model.TestResult import TestResult

ROOT_DIR = Configuration.ROOT_DIR
RESULT_FOLDER = app.config['RESULT_FOLDER']


class PdfGenerator(FPDF):
    def __init__(self):
        if not os.path.exists(F"{ROOT_DIR}/{RESULT_FOLDER}"):
            os.makedirs(F"{ROOT_DIR}/{RESULT_FOLDER}")
        super().__init__('P', 'mm', 'A4')
        self.set_font('Arial', '', 16)
        self.set_text_color(0, 0, 0)

    def header(self):
        self.set_font_size(24)
        self.cell(0, 15, 'InfraCheck - Report', 0, 0, 'L', 0)
        image = os.path.join(ROOT_DIR, 'assets/proficomlogo.png')
        self.image(image, 140, 10, 60)
        self.ln(20)

    def chapter_title(self, num, label):
        self.set_font_size(16)
        self.set_text_color(255, 255, 255)
        self.set_fill_color(11, 114, 181)
        self.cell(0, 15, 'Part %d : %s' % (num, label), 0, 1, 'L', 1)
        self.ln(4)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font_size(8)
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def print_chapter(self, num, title):
        self.add_page()
        self.chapter_title(num, title)

    def print_info(self, name, value):
        self.set_text_color(0, 0, 0)
        self.set_font('Arial', 'b', 12)
        self.multi_cell(190, 4, str(name.title()), 0, 'J', 0, False)
        self.set_font('Arial', '', 10)
        if isinstance(value, (collections.abc.Mapping, list, tuple)):
            self.multi_cell(190, 4, json.dumps(value, sort_keys=True, indent=4), 0, 'J', 0, False)
        else:
            self.multi_cell(190, 4, str(value), 0, 'J', 0, False)
        self.ln(2)

    def generate(self, report: TestResult):
        self.alias_nb_pages()
        self.print_chapter(1, 'General Data')

        for key in report:
            if key == 'plugin_result':
                continue
            self.print_info(key, report[key])

        i = 1
        for plugin_data in report['plugin_result']:
            self.print_chapter(i, F"{plugin_data['plugin_name']}")
            i = i + 1
            for key in plugin_data:
                self.print_info(key, plugin_data[key])

        self.output(F"{ROOT_DIR}/{RESULT_FOLDER}{report['id']}.pdf", 'F')
        del self
