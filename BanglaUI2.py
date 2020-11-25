import tkinter as tk
from BanglaUI import Bangla_website
from BrowseFile import File_dialog


class Bangla_UI2():


    def bangla_UI2(self):
        root = tk.Toplevel()

        canvas1 = tk.Canvas(root, width=800, height=700, relief='raised')

        filename = tk.PhotoImage(file="C:\\Users\\Dell\\Pictures\\abcd2.png")
        background_label = tk.Label(root, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        canvas1.pack()

        def getNext1():
            b = Bangla_website()
            b.bangla_UI()

        def getNext():
            file = File_dialog()
            file.fileBrowser()

        label1 = tk.Label(root, text='EMOTOS')
        label1.config(font=('helvetica', 44))
        canvas1.create_window(400, 35, window=label1)

        button11 = tk.Button(root,text='Single Sentence', command=getNext1, bg='#FFFF99', fg='black',
                         font=('helvetica', 20, 'bold'))
        button22 = tk.Button(root,text='File', command=getNext, bg='#FFFF99', fg='black',
                         font=('helvetica', 20, 'bold'))
        canvas1.create_window(600, 300, window=button11)
        canvas1.create_window(300, 300, window=button22)


        root.mainloop()