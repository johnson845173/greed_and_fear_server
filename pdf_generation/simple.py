from sqlalchemy import text
from pylatex import Document, MiniPage,LargeText,LineBreak,LongTable, MultiColumn
from pylatex.utils import bold,NoEscape
import pylatex as pl
from pylatex.package import Package
from pylatex import PageStyle, Head, Foot, LargeText, MediumText, LineBreak, simple_page_number
from pylatex import Section, UnsafeCommand, Command
from pylatex.base_classes import Environment, CommandBase, Arguments
import os
import datetime
import pytz
import pandas as pd
import time

class Student_login:
    def __init__(self,file_name) -> None:
        os.chdir(os.path.dirname(__file__))
        self.file_name = file_name
        self.main()


    def get_lib(self):
        self.doc.packages.append(Package('fontenc', options=['T1']))
        self.doc.packages.append(Package('datetime', options=['ddmmyyyy']))
        self.doc.packages.append(Package('hyphenat', options=['none']))
        self.doc.packages.append(Package('xcolor', options=['table']))
        self.doc.packages.append(Package('draftwatermark'))
        self.doc.packages.append(Package('color'))
        self.doc.packages.append(Package('ragged2e'))
        self.doc.packages.append(Package('array'))
        self.doc.packages.append(Package('longtable'))
        self.doc.packages.append(Package('fancyhdr'))
        self.doc.packages.append(Package('float'))
        self.doc.preamble.append(NoEscape(r'\definecolor{blue}{HTML}{E9EBF5}'))
    
    def add_custom_commands(self):        
        new_comm = UnsafeCommand('newcommand', '\hdr', options=2,extra_arguments=r'''
            {\Large \centering \textbf{#1}} \\ 
            {\large \centering \textbf{#2}}
                ''')
        self.doc.preamble.append(new_comm)

        new_comm = UnsafeCommand('newcommand', r'\onehdr', options=1,extra_arguments=r'''\noindent \RaggedRight \large \textbf{#1}''')
        self.doc.preamble.append(new_comm)

        new_comm = UnsafeCommand('newcommand', r'\onehdrc', options=1,extra_arguments=r'''\centering \large \textbf{#1} \bigskip ''')
        self.doc.preamble.append(new_comm)

        new_comm = UnsafeCommand('newcommand', r'\rightaligh', options=1,extra_arguments=r'''\RaggedLeft \large \textbf{#1} \hspace{2cm} ''')
        self.doc.preamble.append(new_comm)

        new_comm = UnsafeCommand('newcommand', r'\threelinehdr', options=3,extra_arguments=r'''
            {\Large \centering \textbf{#1}} \\ \vspace{2mm} 
            {\Large \centering \textbf{#2}} \\ \vspace{2mm}
            {\Large \centering \textbf{#3}}
                        ''')
        self.doc.preamble.append(new_comm)

        new_comm = UnsafeCommand('newcommand', r'\ch', options=3,extra_arguments=r'''
            \noindent \large \textbf{Chapter Name:} #1 \medskip \\ 
            \large \textbf{Concept Covered:} #2 \medskip \\ 
            \large \textbf{Test link:} #3 \\
                        ''')
        self.doc.preamble.append(new_comm)

        # new_comm = UnsafeCommand('newcommand', '\dateseparator', options=0,
        #                             extra_arguments=r'''/''')
        # self.doc.preamble.append(new_comm)

    
    def add_watermark(self):
        bodypage = PageStyle("bodypage")
        with bodypage.create(Foot("L")):
            bodypage.append(NoEscape(r"""\vspace{0cm}"""))
            bodypage.append("Learn Basics")
            # bodypage.append(NoEscape(r"""\hspace{3cm}"""))
        with bodypage.create(Foot("C")):
            bodypage.append(NoEscape(r"""\vspace{0cm}"""))
            bodypage.append(NoEscape(r""))
            # bodypage.append(fr"{self.school_name} - Class {self.current_standard}")
        with bodypage.create(Foot("R")):
            bodypage.append(NoEscape(r"""\vspace{0cm}"""))
            bodypage.append(NoEscape(r"\today \; \currenttime"))

        # with bodypage.create(Head("L")):
            # bodypage.append(NoEscape(r"""\includegraphics[width = 3.0cm, height=1.125cm]{../img/logo.png}"""))

        with bodypage.create(Head("C")):
            bodypage.append(NoEscape(r"\hdr{Learn Baiscs }{Daily Test Report}"))

                    
        bodypage.append(pl.Command('renewcommand', arguments=[pl.NoEscape(r'\footrulewidth'),'1pt']))
        bodypage.append(pl.Command('renewcommand', arguments=[pl.NoEscape(r'\headrulewidth'),'1pt']))

        self.doc.preamble.append(bodypage)
        self.doc.change_document_style("bodypage")


        self.doc.append(NoEscape(r'''\SetWatermarkLightness{ 0.95 }
        \SetWatermarkText{Learn Basics}
        \SetWatermarkScale{ 0.7 }

        \setlength{\headsep}{1.8cm}'''))

    def add_data(self):
        self.doc.append(NoEscape(r"File Name:"+str(self.file_name)))

    def main(self):
        if not os.path.exists("daily_test_report"):
            os.makedirs("daily_test_report")
        geometry_options = {"top": "1.8cm", "bottom" : "2.2cm", "left" : "0.5cm", "right" : "0.5cm"}
        self.doc = Document(geometry_options=geometry_options)
        self.doc.documentclass = Command('documentclass', options=['10pt', 'a4paper'], arguments=['article'])
        # self.get_lib()
        # self.add_custom_commands()
        # self.add_watermark()
        self.add_data()
        self.doc.generate_pdf(f"../shared_pdf/{self.file_name}", clean_tex=False, compiler = 'pdflatex')   
 


if __name__ == '__main__':
    # school_test_id = 12
    # ly_test_id_list =  [405199,405205,405209,405212,405194]
    os.chdir(os.path.dirname(__file__))
    obj = Student_login(file_name="8")
     
