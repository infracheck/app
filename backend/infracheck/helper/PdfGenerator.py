import os

from fpdf import FPDF

from Environment import Environment


class PdfGenerator(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.set_font('Arial', '', 16)
        self.set_text_color(0, 0, 0)
        self.data = {}
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
        self.cell(30, 12, str(name), border=1)
        self.cell(160, 12, str(value), border=1)
        self.ln(12)

    def generate(self, report):
        self.alias_nb_pages()
        self.print_chapter(1, 'General Data')

        self.print_info("name", report['name'])
        self.print_info("description", report['description'])
        self.print_info("id", report['id'])
        self.print_info("date", report['date'])
        self.print_info("total", report['total'])
        self.print_info("succeeded", report['succeeded'])
        self.print_info("errors", report['errors'])
        self.print_info("failures", report['failures'])
        self.print_info("message", report['message'])

        self.print_chapter(2, 'Plugin Data')

        self.output(F"{Environment.RESULT_FOLDER}{report['id']}.pdf", 'F')
