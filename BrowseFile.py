import tkinter as tk
from tkinter import filedialog
import xlrd
from matplotlib import pyplot as plt
from functools import partial
from Bangla_Analyzer import Bangla_analyzer
from tkinter import messagebox as mbox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)

class File_dialog():
    csv_filename = ''
    def fileBrowser(self):
        root = tk.Toplevel()

        readListofSentences = []

        canvas1 = tk.Canvas(root, width=800, height=700, relief='raised')

        filename = tk.PhotoImage(file="C:\\Users\\Dell\\Pictures\\abcd2.png")
        background_label = tk.Label(root, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        canvas1.pack()

        label1 = tk.Label(root, text='EMOTOS')
        label1.config(font=('helvetica', 44))
        canvas1.create_window(400, 35, window=label1)

        def Analyze_text():
            button_file.destroy()
            positive_count = 0
            negative_count = 0
            neutral_count = 0
            predicted_data = ['Postive', 'Negative', 'Neutral']

            prediction_count = []

            for sentence in readListofSentences:
                bangla_analyzer_class = Bangla_analyzer(sentence)
                prediction = bangla_analyzer_class.start_analysis()

                print(prediction, 'anse')
                if prediction == 'pos':
                    positive_count = positive_count + 1
                elif prediction == 'neg':
                    negative_count = negative_count + 1
                else:
                    neutral_count = neutral_count + 1

            prediction_count.append(positive_count)
            prediction_count.append(negative_count)
            prediction_count.append(neutral_count)

            button_pie = tk.Button(root, text='Show Pie Chart',
                                   command=partial(show_pie, prediction_count, predicted_data), bg='#FFFF99',
                                   fg='black',
                                   font=('helvetica', 20, 'bold'))

            canvas1.create_window(400, 300, window=button_pie)

        def show_pie(predicted_data, prediction_count):
            # fig = plt.figure(figsize=(10, 7))
            # print("data", len(predicted_data))
            # print("count0", len(prediction_count))
            # plt.pie(predicted_data, labels=prediction_count)
            # plt.show()
            root1= tk.Toplevel()
            fig1= Figure(figsize=(10, 7),dpi=100)
            ax = fig1.add_subplot(111)
            ax.pie(predicted_data, labels=prediction_count)
            canvas = FigureCanvasTkAgg(fig1, root1)
            canvas.draw()
            canvas.get_tk_widget().pack()

        def Browse_a_File():

            try:
                excel_filename = filedialog.askopenfilename(initialdir="/", title="Select A File", filetype=
                (("XLSX files", "*.xlsx"), ("all files", "*.*")))
                label2 = tk.Label(root, text=excel_filename)
                label2.config(font=('helvetica', 14))
                canvas1.create_window(400, 350, window=label2)
                read_excel(excel_filename)
                button_file.destroy()
                button_analysis = tk.Button(root, text='Analyze Text', command=Analyze_text, bg='#FFFF99', fg='black',
                                        font=('helvetica', 20, 'bold'))
                canvas1.create_window(400, 300, window=button_analysis)
                print(excel_filename)
            except :
                mbox.showerror('Error Message', 'Please input valid data')

        def read_excel(excel_fileName):
            wb = xlrd.open_workbook(excel_fileName)
            sheet = wb.sheet_by_index(0)
            sheet.cell_value(0, 0)

            for i in range(sheet.nrows):
                readListofSentences.append(sheet.cell_value(i, 0))
                print(sheet.cell_value(i, 0))

        button_file = tk.Button(root, text='Browser A File', command=Browse_a_File, bg='#FFFF99', fg='black',
                                font=('helvetica', 20, 'bold'))
        canvas1.create_window(400, 300, window=button_file)

        root.mainloop()