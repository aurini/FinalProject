import tkinter as tk
from Bangla_Analyzer import Bangla_analyzer

class Bangla_website():

  def bangla_UI(self):
    root = tk.Toplevel()

    canvas1 = tk.Canvas(root, width=800, height=700, relief='raised')

    filename = tk.PhotoImage(file="C:\\Users\\Dell\\Pictures\\abcd2.png")
    background_label = tk.Label(root, image=filename)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    canvas1.pack()


    label1 = tk.Label(root, text='EMOTOS')
    label1.config(font=('helvetica', 44))
    canvas1.create_window(400, 35, window=label1)

    label2 = tk.Label(root, text='Input Single Sentence')
    label2.config(font=('helvetica', 30))
    canvas1.create_window(400, 100, window=label2)

    entry1 = tk.Entry(root,width=50,font=('Helvetica', 20))
    canvas1.create_window(400, 240, window=entry1)


    def getSentiment():
      sentence = entry1.get()
      bangla_analyzer_class = Bangla_analyzer(sentence)
      prediction = bangla_analyzer_class.start_analysis()
      if (prediction == 'neg') :
        label4 = tk.Label(root, text=str('Negative'), font=('helvetica', 40, 'bold'))
      elif (prediction == 'pos') :
        label4 = tk.Label(root, text=str('Positive'), font=('helvetica', 40, 'bold'))
      else :
        label4 = tk.Label(root, text=str('Nutral'), font=('helvetica', 40, 'bold'))
      canvas1.create_window(400, 450, window=label4)

    button1 = tk.Button(root,text='Get Sentiment', command=getSentiment, bg='#FFFF99', fg='black',
                        font=('helvetica',20, 'bold'))
    canvas1.create_window(400, 380, window=button1)

    root.mainloop()