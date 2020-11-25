from tkinter import *
from BanglaUI2 import Bangla_UI2
from Twitter import twitter

splash_root = Tk()
splash_root.title("Emotos")
splash_root['background']='#add8e6'
app_height = 250
app_width = 500

screen_width = splash_root.winfo_screenwidth()
screen_height= splash_root.winfo_screenheight()
x=  (screen_width/2) - (app_width/2)
y = (screen_height/2) -(app_height/2)

print(x)
print(y)

splash_root.geometry(f'{app_width}x{app_height}+{500}+{100}')
# Hide the title bar
splash_root.overrideredirect(True)

splash_label = Label(splash_root, text = 'EMOTOS', font=("Helvetica",80))
splash_label.pack(pady=20)


def getNext1():
    b =Bangla_UI2()
    b.bangla_UI2()

def getNext():
    twitter_UI = twitter()
    twitter_UI.analyze_twitter()

def main_window():
    splash_root.destroy()
    top = Tk()
    C = Canvas(top, bg="blue", height=700, width=900)
    filename = PhotoImage(file="C:\\Users\\Dell\\Pictures\\abcd2.png")
    background_label = Label(top, image=filename)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    label1 = Label(top, text='EMOTOS')
    label1.config(font=('helvetica', 40, 'bold'),bg="white")
    C.create_window(450, 150, window=label1)


    button1 = Button(text='Bangla Language', command=getNext1, bg='#FFFF99', fg='black',
                        font=('helvetica', 20, 'bold'))
    button2 = Button(text='Twitter', command=getNext, bg='#FFFF99', fg='black',
                     font=('helvetica', 20, 'bold'))
    C.create_window(600, 300, window=button1)
    C.create_window(300, 300, window=button2)
    C.pack()
    top.mainloop()



# #splash Screen timer
splash_root.after(2000, main_window)

mainloop()