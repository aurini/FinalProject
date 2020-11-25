import tkinter as tk
from gingerit.gingerit import GingerIt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from tkinter import *
from tkinter.ttk import *
import tweepy as tw
import sqlite3
import datetime
from langdetect import detect
from Bangla_Analyzer import Bangla_analyzer
from tkcalendar import Calendar
import matplotlib.pyplot as plt
from tkinter import messagebox as mbox

class twitter() :
    start_date = 0
    end_date = 0
    uName = 'abc'
    get_user_tweet_database = []
    get_user_tweet_date = []
    en_tweet =[]
    bn_tweet =[]
    result_en = []
    result_en_polarity =[]
    global button_analyze
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    sentiment_count = []

    def analyze_twitter(self):



        root = tk.Toplevel()

        canvas1 = tk.Canvas(root, width=800, height=700, relief='raised')

        filename = tk.PhotoImage(file="C:\\Users\\Dell\\Pictures\\abcd2.png")
        background_label = tk.Label(root, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        canvas1.pack()

        def show_chat():
            print('show chart')

            conn = sqlite3.connect('twitterUserData.db')
            cur = conn.cursor()

            cur.execute("SELECT * FROM Sentiment_English")

            rows = cur.fetchall()

            for row in rows:
                if row[1] == 'positive' :
                    self.positive_count = self.positive_count +1
                elif row[1] == 'negative' :
                    self.negative_count =self.negative_count +1
                else :
                    self.neutral_count = self.neutral_count + 1
            cur.execute("SELECT * FROM Sentiment_Bangla")
            for row in rows:
                if row[1] == 'positive' :
                    self.positive_count = self.positive_count +1
                elif row[1] == 'negative' :
                    self.negative_count =self.negative_count +1
                else :
                    self.neutral_count = self.neutral_count + 1

            self.sentiment_count.append(self.positive_count)
            self.sentiment_count.append(self.neutral_count)
            self.sentiment_count.append(self.negative_count)

            plt.bar(['postive', 'neutral', 'negative'], self.sentiment_count, label="sentiment count", color='g')
            plt.legend()
            plt.xlabel('sentiment')
            plt.ylabel('Sentiment count')


            # plt.plot(self.get_user_tweet_date, self.result_en_polarity, label="Example two", color='g')
            # plt.legend()
            # plt.xlabel('date')
            # plt.ylabel('polarity')

            plt.title('Epic Graph\nAnother Line! Whoa')

            plt.show()
            conn.close()

        def analyze_data():
            self.button_analyze.destroy()
            conn = sqlite3.connect('twitterUserData.db')
            cur = conn.cursor()

            cur.execute("SELECT * FROM TWEET3")

            rows = cur.fetchall()

            for row in rows:
                self.get_user_tweet_database.append(row[2])

                self.get_user_tweet_date.append(row[3])

            for i in range(len(self.get_user_tweet_database)):
                english = []
                bangla = []
                language = detect(self.get_user_tweet_database[i])

                if language == 'en' :
                    print("I am tweet", self.get_user_tweet_database[i])
                    english.append(self.get_user_tweet_database[i])
                    english.append(self.get_user_tweet_date[i])
                    self.en_tweet.append(english)
                elif language == 'bn' :
                    bangla.append(self.get_user_tweet_database[i])
                    bangla.append(self.get_user_tweet_date[i])
                    self.bn_tweet.append(bangla)
            analyze_english()
            analyze_bangal()
            print(self.result_en)
            insert_database_english()
            button_show = tk.Button(root, text='Show Chart', command=show_chat, bg='#FFFF99', fg='black',
                                        font=('helvetica', 20, 'bold'))
            canvas1.create_window(400, 600, window=button_show)
            conn.close()


        def insert_database_english():
            conn = sqlite3.connect('twitterUserData.db')
            c = conn.cursor()
            result_list = []
            print("enligh " ,self.en_tweet)
            for i in range(len(self.en_tweet)):
                input = self.en_tweet[i]
                print(input)
                tweet = input[0]
                date = input[1]
                for j in range(len(self.result_en)):
                    result1 = self.result_en[j]
                    if result1 == 'positive':
                        result_list.append(result1)
                    elif result1 == 'neutral':
                        result_list.append(result1)
                    elif result1 == 'negative' :
                        result_list.append(result1)
                print("len",result_list[i])
                print("len", len(result_list))
                result = result_list[i]
                c.execute('''INSERT INTO Sentiment_English (Sentiment, Tweet, Created_date,User_Name) VALUES (?,?,?,?)''',(str(result), str(tweet), str(date), self.screen_name))
                conn.commit()
            c.close()

        def insert_database_english():
            conn = sqlite3.connect('twitterUserData.db')
            c = conn.cursor()
            result_list = []
            print("enligh ", self.en_tweet)
            for i in range(len(self.en_tweet)):
                input = self.en_tweet[i]
                print(input)
                tweet = input[0]
                date = input[1]
                for j in range(len(self.result_en)):
                    result1 = self.result_en[j]
                    if result1 == 'positive':
                        result_list.append(result1)
                    elif result1 == 'neutral':
                        result_list.append(result1)
                    elif result1 == 'negative':
                        result_list.append(result1)
                print("len", result_list[i])
                print("len", len(result_list))
                result = result_list[i]
                c.execute(
                    '''INSERT INTO Sentiment_English (Sentiment, Tweet, Created_date,User_Name) VALUES (?,?,?,?)''',
                    (str(result), str(tweet), str(date), self.screen_name))
                conn.commit()
            c.close()

        def analyze_english():
            sentences = []
            for s in self.en_tweet:
                print('len',len(self.en_tweet))
                print("asdasdas", s[0])
                sid = SentimentIntensityAnalyzer()
                ss = sid.polarity_scores(s[0])
                for k in sorted(ss):
                    result = setResult(k, ss[k])
                    self.result_en.append(result)
            print(self.result_en)


        def setResult(type, res):
            if (type == "compound"):
                if (res >= 0.05):
                    self.result_en_polarity.append(res)
                    return 'positive'
                elif (res > -0.05 and res < 0.05):
                    self.result_en_polarity.append(res)
                    return 'neutral'
                elif (res <= -0.05):
                    self.result_en_polarity.append(res)
                    return 'negative'

        # def checkGrammer(text):
        #     print(text)
        #     parser = GingerIt()
        #     item = parser.parse(text)
        #     return item['result']

        def analyze_bangal() :
            conn = sqlite3.connect('twitterUserData.db')
            c = conn.cursor()
            count = 0
            for s in self.bn_tweet:
               result = Bangla_analyzer(s[0])
               date = s[1]
               c.execute('''INSERT INTO Sentiment_Bangla (Sentiment, Tweet, Created_date,User_Name) VALUES (?,?,?,?)''',
                         (result,s,date,self.screen_name))
               conn.commit()
            c.close()

        def button_TO():
            self.uName = entry1.get()
            print('asdas')

            def print_sel():
                self.end_date = cal.selection_get()
                print(cal.selection_get())
                label_EndDate = tk.Label(root, text="To " + str(self.end_date))
                label_EndDate.config(font=('helvetica', 20))
                canvas1.create_window(350, 480, window=label_EndDate)

                top.destroy()

            top = tk.Toplevel()
            cal = Calendar(top,
                           font="Arial 14", selectmode='day',
                           cursor="hand1", year=2020, month=11, day=5)
            cal.pack(fill="both", expand=True)
            tk.Button(top, text="ok", command=print_sel).pack()


        def button_FROM():
           print('asdas')
           print('abcd')

           def print_sel():
               self.start_date = cal.selection_get()
               print(cal.selection_get())
               label_StartDate = tk.Label(root, text='From ' + str(self.start_date))
               label_StartDate.config(font=('helvetica', 20))
               canvas1.create_window(350, 450, window=label_StartDate)
               top.destroy()

           top = tk.Toplevel()
           cal = Calendar(top,
                          font="Arial 14", selectmode='day',
                          cursor="hand1", year=2020, month=11, day=5)
           cal.pack(fill="both", expand=True)
           button_okay = tk.Button(top, text="ok", command=print_sel).pack()


        def sentiment_database_english():
            conn = sqlite3.connect('twitterUserData.db')
            c = conn.cursor()
            if not conn:
                print("not connected")
            else:
                print("connected")
                c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Sentiment_English'  ''')
                conn.commit()

                # if the count is 1, then table exists
                if c.fetchone()[0] == 1:
                    print('Table exists.')
                else:
                    print('Table does not exist.')
                    c.execute(
                        '''CREATE TABLE Sentiment_English (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,Sentiment TEXT    NOT NULL,Tweet   TEXT     NOT NULL,Created_date   TEXT    NOT NULL, User_Name   TEXT  NOT NULL) ''')
                    conn.commit()

            c.close()

        def sentiment_database_bangla():
            conn = sqlite3.connect('twitterUserData.db')
            c = conn.cursor()
            if not conn:
                print("not connected")
            else:
                print("connected")
                c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Sentiment_Bangla'  ''')
                conn.commit()

                # if the count is 1, then table exists
                if c.fetchone()[0] == 1:
                    print('Table exists.')
                else:
                    print('Table does not exist.')
                    c.execute(
                        '''CREATE TABLE Sentiment_Bangla (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,Sentiment TEXT    NOT NULL,Tweet   TEXT     NOT NULL,Created_date   TEXT    NOT NULL, User_Name   TEXT  NOT NULL) ''')
                    conn.commit()

            c.close()


        def check_date():
            today = datetime.date.today()
            print('today ', today)
            print(self.end_date < today)

            if (self.end_date < today or self.start_date < today):
                return True
            else :
                mbox.showerror('Error Message', 'Date input is wrong please try again')
                return False

        def button_collect():
            print('adasdas====', check_date())
            date_checker = check_date()
            if date_checker is True :
                button_collect.destroy()
                sentiment_database_english()
                sentiment_database_bangla()
                print(self.uName)

                consumer_key = 'x7eLfHlTsWtGlM4bGvu44qbSl'
                consumer_secret = '6W1hMccZ2DdgL50dgG5xZllDYm705jicJiAkyojNdpcB0ZmUC9'
                access_token = '44594931-pkEBrq9it8ZmViMUHc38QijzNic7rIVabZ6F4tSu8'
                access_token_secret = '9ogPsSvcYYRbQWXHN71j0SasgSgOdLCYTYjfvN8n1y0CK'

                conn = sqlite3.connect('twitterUserData.db')
                c = conn.cursor()
                if not conn:
                    print("not connected")
                else:
                    print("connected")
                    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='TWEET3'  ''')
                    conn.commit()

                    # if the count is 1, then table exists
                    if c.fetchone()[0] == 1:
                        print('Table exists.')
                    else:
                        print('Table does not exist.')
                        c.execute(
                            '''CREATE TABLE TWEET3 (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,NAME TEXT    NOT NULL,Status   INT     NOT NULL,Created_date   TEXT    NOT NULL) ''')
                        conn.commit()
                auth = tw.OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_token, access_token_secret)
                api = tw.API(auth, wait_on_rate_limit=True)
                self.screen_name = "AmenaAlam5"
                user_tweet = []
                print(self.start_date)
                print(self.end_date)
                sd = self.start_date
                ed = self.end_date
                text = 'Data collected from ' + str(sd) + ' to ' + str(ed)
                self.label_StarDate = tk.Label(root,text=text)
                self.label_StarDate.config(font=("Helvetica", 15))
                canvas1.create_window(500, 560, window=self.label_StarDate)
                endDate = datetime.datetime.combine(ed, datetime.time())
                print(endDate)
                startDate = datetime.datetime.combine(sd, datetime.time())
                for status in tw.Cursor(api.user_timeline, id=self.screen_name, exclude_replies=True).items(10000):
                    print("here inside api")
                    if (not status.retweeted) and ('RT @' not in status.text):
                        print("here inside not retweeted")
                        print(status.created_at)
                        if (status.created_at >= startDate):
                            print("here inside start date")
                            if (status.created_at <= endDate):
                                print("here inside end date")
                                user_tweet.append([status.text, status.created_at])
                                # Print Status
                                print('dasdas--------------------------')
                                print(status.text, ' date ', status.created_at)
                            else:
                                print('no status')
                        else:
                            break
                for u_tweets in user_tweet:
                    user_status = str(u_tweets[0])
                    create_date = str(u_tweets[1])
                    c.execute('''INSERT INTO TWEET3 (NAME, Status, Created_date) VALUES (?,?,?)''',
                              (self.screen_name, user_status, create_date))
                conn.commit()
                conn.close()
                self.label_Name = tk.Label(root,text="finished")
                self.label_Name.config(font=("Helvetica", 15))
                canvas1.create_window(500, 540, window=self.label_Name)
                self.button_analyze = tk.Button(root, text='Analyze Data',command= analyze_data, bg='#FFFF99',fg='black',font=('helvetica', 20, 'bold'))
                canvas1.create_window(400, 600, window=self.button_analyze)
                # button_analyze = tk.Button(root, text='Show Chart', command=show_chat, bg='#FFFF99', fg='black',
                #                            font=('helvetica', 20, 'bold'))
                # canvas1.create_window(400, 600, window=button_analyze)



        label1 = tk.Label(root, text='EMOTOS')
        label1.config(font=('helvetica', 44))
        canvas1.create_window(400, 35, window=label1)


        label_Name = tk.Label(root, text='Enter User Name')
        label_Name.config(font=('helvetica', 30))
        canvas1.create_window(400, 100, window=label_Name)

        entry1 = tk.Entry(root, width=50, font=('Helvetica', 20))
        canvas1.create_window(400, 240, window=entry1)


        self.uName = entry1.get()
        print(self.uName)



        button11 = tk.Button(root, text='DATE TO', command=button_TO, bg='#FFFF99', fg='black',
                             font=('helvetica', 20, 'bold'))
        button22 = tk.Button(root, text='DATE FROM', command=button_FROM, bg='#FFFF99', fg='black',
                             font=('helvetica', 20, 'bold'))
        canvas1.create_window(600, 300, window=button11)
        canvas1.create_window(300, 300, window=button22)

        button_collect = tk.Button(root, text='Collect Data', command=button_collect, bg='#FFFF99', fg='black',
                             font=('helvetica', 20, 'bold'))
        canvas1.create_window(400, 600, window=button_collect)


        root.mainloop()
