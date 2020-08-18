import os

from fpdf import FPDF

from Environment import Environment
from infracheck.model.ITestResult import ITestResult


class PdfGenerator(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.set_font('Arial', '', 16)
        self.set_text_color(0, 0, 0)
        if not os.path.exists(Environment.RESULT_FOLDER):
            os.makedirs(Environment.RESULT_FOLDER)

    def header(self):
        self.set_font_size(24)
        self.cell(0, 15, 'InfraCheck - Report', 0, 0, 'L', 0)
        self.image('assets/proficomlogo.png', 140, 10, 60)
        self.ln(20)

    def chapter_title(self, num, label):
        self.set_font_size(16)
        self.set_text_color(255, 255, 255)
        self.set_fill_color(45, 133, 191)
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
        self.cell(45, 12, str(name), border=1)
        self.cell(145, 12, str(value), border=1)
        self.ln(12)

    def generate(self, report: ITestResult):
        self.alias_nb_pages()
        self.print_chapter(1, 'General Data')

        for key in report:
            if key == 'plugin_data':
                continue
            self.print_info(key, report[key])

        for plugin_data in report['plugin_data']:
            self.print_chapter(2, 'Plugin Data')
            for key in plugin_data:
                self.print_info(key, plugin_data[key])

        self.output(F"{Environment.RESULT_FOLDER}{report['id']}.pdf", 'F')
        del self
