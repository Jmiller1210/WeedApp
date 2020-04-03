import tkinter as tk
import pandas as pd
from os import path
import os
from tkinter import ttk
from datetime import datetime


# Main Window
class MyWeed:
    def __init__(self, master):
        self.master = master
        # set style
        self.style = ttk.Style(master)
        self.style.theme_use('classic')
        master.title("My Weed")
        # change styles, set padding, growth and bg color
        master.configure(background='LemonChiffon3')
        self.style.configure("TButton", padding=10, relief="ridge",
                             foreground="Lemon Chiffon3", background="green4", justify=tk.CENTER)
        self.style.map("TButton",
                       foreground=[('pressed', 'green4'), ('active', 'red2')],
                       background=[('pressed', '!disabled', 'LemonChiffon3'), ('active', 'khaki2')]
                       )
        self.style.configure("TLabel", background="LemonChiffon3", foreground="green", padding=15, justify=tk.CENTER)
        self.style.configure("red.TLabel", background="LemonChiffon3", foreground="red4", padding=15, justify=tk.CENTER)
        self.style.configure(".", font=("Courier", 16))
        for i in range(8):
            master.columnconfigure(i, weight=1, minsize=25)
            master.rowconfigure(i, weight=1, minsize=50)

            for j in range(0, 5):
                frame = ttk.Frame(
                    master=master,
                    relief='flat',
                    borderwidth=4
                )
                frame.grid(row=i, column=j, padx=3, pady=3)
        # make menu buttons
        self.buyweed_b = ttk.Button(master, text="  Buy  \n  Weed  ", state='disabled', command=self.go_to_buy_window)
        self.buyweed_b.grid(row=2, column=2, sticky='w')
        self.data_b = ttk.Button(master, text="  Weed  \n  History  ", state='disabled', command=self.go_to_data)
        self.data_b.grid(row=2, column=2, sticky='')
        self.stats_b = ttk.Button(master, text="My\nStatistics", state='disabled', command=self.open_stats_window)
        self.stats_b.grid(row=2, column=2, sticky='e')
        # get user and make file
        self.welcome_label = ttk.Label(master, text="Hi! Welcome back.\n  Please enter your username below.\n\n"
                                                    "  Then, press the "
                                                    "Make/Modify button to load your data\n before moving on.")
        self.welcome_label.grid(row=0, column=0)
        self.now = datetime.now()
        self.currentDay = self.now.strftime("%m/%d/%y")
        self.currentTime = self.now.strftime("%H:%M:%S")
        if self.currentDay == "04/20/20":
            self.art_lbl = ttk.Label(master,
                                     text=("      )                                                     ____ \n"
                                           "    ( /(                                 )         )    )  |   / \n"
                                           "    )\\())    )                (       ( /(      ( /( ( /(  |  /  \n"
                                           "   ((_)\\  ( /(  `  )   `  )   )\\ )    )\\())  __ )(_)))\\()) | /   \n"
                                           "    _((_) )(_)) /(/(   /(/(  (()/(   ((_)\\  / /((_) ((_)\\  |/    \n"
                                           "   | || |((_)_ ((_)_\\ ((_)_\\  )(_)) | | (_)/ / |_  )/  (_)(      \n"
                                           "   | __ |/ _` || '_ \\)| '_ \\)| || | |_  _|/_/   / /| () | )\\     \n"
                                           "   |_||_|\\__,_|| .__/ | .__/  \\_, |   |_|      /___|\\__/ ((_)    \n"
                                           "             |_|    |_|     |__/                               \n"
                                           "     joint - herb - hemp - hashish - cannabis - grass - pot"),
                                     style="red.TLabel")
            self.art_lbl.grid(row=0, column=2, sticky='w')
        else:
            self.art_lbl = ttk.Label(master, text=("   *                                      \n"
                                                   " (  `          (  (                 (     \n"
                                                   " )\\))(   (     )\\))(   '   (    (   )\\ )  \n"
                                                   "((_)()\\  )\\ ) ((_)()\\ )   ))\\  ))\\ (()/(  \n"
                                                   "(_()((_)(()/( _(())\\_)() /((_)/((_) ((_)) \n"
                                                   "|  \\/  | )(_))\\ \\((_)/ /(_)) (_))   _| |  \n"
                                                   "| |\\/| || || | \\ \\/\\/ / / -_)/ -_)/ _` |  \n"
                                                   "|_|  |_| \\_, |  \\_/\\_/  \\___|\\___|\\__,_|  \n"
                                                   "         |__/                            \n"
                                                   "joint - herb - hemp - hashish - cannabis - grass - pot"),
                                     style="red.TLabel")
            self.art_lbl.grid(row=0, column=2, sticky='w')

        self.user_entry = tk.Entry(master, fg='Lemon Chiffon3', bg='green4', font=('Courier', 15))
        self.user_entry.grid(row=1, column=0)
        self.user_entry.focus_set()

        self.user_login = ttk.Button(master, text="Make/Modify", command=self.make_user_file)
        self.user_login.grid(row=1, column=0, sticky='e')
        self.file_lbl_var = tk.StringVar()
        self.file_lbl = ttk.Label(master, textvariable=self.file_lbl_var)
        self.file_lbl_var.set(" Creating a Smoke Sesh For:\n <null> \n\n                       Options: ")
        self.file_lbl.grid(row=1, column=2, sticky='w')

        # define instance variables
        self.df = None
        self.grams = 0
        self.price = 0
        self.total_grams = 0
        self.p_grams = 0
        self.label_var = tk.StringVar()
        self.cw_lbl = ttk.Label(master, textvariable=self.label_var)
        self.label_var.set("\n Current available weed: " + str(round(self.grams, 3)) + " grams.")
        self.cw_lbl.grid(row=3, column=0)
        self.day_tracker = 0

        # smoke weed
        self.did_smoke_lbl = ttk.Label(master, text="How much did you smoke? (g): ")
        self.did_smoke_lbl.grid(row=4, column=0)
        self.did_smoke_amt = tk.Entry(master, state='disabled', fg='Lemon Chiffon3', bg='green4')
        self.did_smoke_amt.grid(row=5, column=0)
        self.smoked_amt_lbl = ttk.Label(master,
                                        text="You smoked:\n{} grams of weed on\n <null>".format(self.day_tracker))
        self.smoked_amt_lbl.grid(row=5, column=1, sticky='w')
        self.enter_data_button3 = ttk.Button(master, text='Enter Data', state='disabled', command=self.smoke_weed)
        self.enter_data_button3.grid(row=6, column=0)

        # close button
        self.close_button = ttk.Button(master, text="Close", command=master.quit)
        self.close_button.grid(row=8, column=0, sticky='nw')

    # update time function
    def update_time(self):
        self.now = datetime.now()
        self.currentDay = self.now.strftime("%m/%d/%y")
        self.currentTime = self.now.strftime("%H:%M:%S")

    # function to update smoked amount label back to normal
    def set_SA_label(self):
        self.update_time()
        self.smoked_amt_lbl.destroy()
        self.smoked_amt_lbl = ttk.Label(self.master,
                                        text="You smoked:\n{} grams of weed on\n".format(self.day_tracker)
                                             + self.currentDay)
        self.smoked_amt_lbl.grid(row=5, column=1, sticky='w')

    # function to update welcome label back to normal
    def set_welcome_label(self):
        self.welcome_label.destroy()
        self.welcome_label = ttk.Label(self.master, text="Hi! Welcome back.\n  Please enter your username below.\n\n"
                                                         "  Then, press the "
                                                         "Make/Modify button to load your data\n before moving on.")
        self.welcome_label.grid(row=0, column=0)

    # makes or modifies user file depending on user input
    def make_user_file(self):
        user = self.user_entry.get()
        self.update_time()
        if (len(user) <= 8) and (len(user) >= 2):
            if path.exists("myWeed_{}.xlsx".format(user)):
                self.df = pd.read_excel("myWeed_{}.xlsx".format(user), index_col=None)
                self.did_smoke_amt['state'] = 'normal'
                self.did_smoke_amt.focus_set()
                self.buyweed_b['state'] = 'normal'
                self.data_b['state'] = 'normal'
                self.stats_b['state'] = 'normal'
                self.enter_data_button3['state'] = 'normal'
                self.file_lbl = ttk.Label(self.master,
                                          textvariable=self.file_lbl_var)
                self.file_lbl_var.set(" Creating a Smoke Sesh For:\n " + user + "\n\n                       Options:")
                self.file_lbl.grid(row=1, column=2, sticky='w')
                self.day_tracker = self.df.Smoked_Now[self.df.Date == self.currentDay]
                self.day_tracker = round(sum(self.day_tracker), 3)
                self.smoked_amt_lbl = ttk.Label(self.master,
                                                text="You smoked:\n{} grams of weed on\n".format(
                                                    self.day_tracker) + self.currentDay)
                self.smoked_amt_lbl.grid(row=5, column=1)
                try:
                    self.grams = self.df['Current Weed'].iloc[-1]
                    self.price = self.df['Total Spent'].iloc[-1]
                    self.total_grams = self.df['Total Bought'].iloc[-1]
                except IndexError:
                    self.grams = 0
                    self.price = 0
                    self.total_grams = 0
                self.cw_lbl = ttk.Label(self.master,
                                        textvariable=self.label_var)
                self.label_var.set("\n Current available weed: " + str(round(self.grams, 3)) + " grams.")
                self.cw_lbl.grid(row=3, column=0)
            else:
                WS_data = []
                df = pd.DataFrame(WS_data,
                                  columns=['Date', 'Time', 'Smoked_Now', 'Current Weed',
                                           'Total Bought', 'Total Spent', "User"])
                df.to_excel("myWeed_{}.xlsx".format(user), index=False)
                self.df = pd.read_excel("myWeed_{}.xlsx".format(user), index_col=None)
                self.did_smoke_amt['state'] = 'normal'
                self.did_smoke_amt.focus_set()
                self.buyweed_b['state'] = 'normal'
                self.data_b['state'] = 'normal'
                self.stats_b['state'] = 'normal'
                self.enter_data_button3['state'] = 'normal'
                self.file_lbl = ttk.Label(self.master,
                                          textvariable=self.file_lbl_var)
                self.file_lbl_var.set("\n~~~~~~~~~ \nFile to store data created successfully! "
                                      "\n~~~~~~~~~\nCreating a Smoke Sesh For:\n" + user + "\n\n                      "
                                                                                           " Options:")
                self.file_lbl.grid(row=1, column=2, sticky='w')
                self.grams = 0
                self.price = 0
                self.total_grams = 0
                self.cw_lbl = ttk.Label(self.master,
                                        textvariable=self.label_var)
                self.label_var.set("\n Current available weed: " + str(round(self.grams, 3)) + " grams.")
                self.cw_lbl.grid(row=3, column=0)
        else:
            self.welcome_label = ttk.Label(self.master, text="Hi! Welcome back.\n  Please enter your username "
                                                             "below.\n\n "
                                                             "  Then, press the "
                                                             "Make/Modify button to load your data\n before moving "
                                                             "on.\n "
                                                             "You must enter a username between 2 and 8 characters.")
            self.welcome_label.grid(row=0, column=0)
            self.master.after(2000, self.set_welcome_label)

    # smoke weed, add the relevant data to the excel file and export it
    def smoke_weed(self):
        try:
            amount = float(self.did_smoke_amt.get())
            if self.grams >= amount > 0:
                self.update_time()
                self.grams -= amount
                df1 = self.df.append({'Date': self.currentDay, 'Time': self.currentTime, 'Smoked_Now': round(amount, 3),
                                      'Current Weed': round(self.grams, 3), 'Total Bought': round(self.total_grams, 3),
                                      'Total Spent': self.price, 'ppg': None,
                                      "User": self.user_entry.get()}, ignore_index=True)
                df1.to_excel("myWeed_{}.xlsx".format(self.user_entry.get()), index=False)
                self.df = df1
                self.day_tracker = df1.Smoked_Now[df1.Date == self.currentDay]
                self.day_tracker = round(sum(self.day_tracker), 3)
                if self.grams == 0.0:
                    self.smoked_amt_lbl.destroy()
                    self.smoked_amt_lbl = ttk.Label(self.master,
                                                    text="Oh no! you ran out!")
                    self.smoked_amt_lbl.grid(row=5, column=1, sticky='w')
                    self.master.after(2000, self.set_SA_label)
                else:
                    self.set_SA_label()
                self.cw_lbl = ttk.Label(self.master,
                                        text="\n Current available weed: " + str(round(self.grams, 3)) + " grams.")
                self.cw_lbl.grid(row=3, column=0)
            elif amount > self.grams:
                self.smoked_amt_lbl.destroy()
                self.smoked_amt_lbl = ttk.Label(self.master,
                                                text="That's impossible bro.")
                self.smoked_amt_lbl.grid(row=5, column=1, sticky='w')
                self.master.after(2000, self.set_SA_label)
            elif amount == 0:
                self.smoked_amt_lbl.destroy()
                self.smoked_amt_lbl = ttk.Label(self.master,
                                                text="Can't smoke air bro \n")
                self.smoked_amt_lbl.grid(row=5, column=1, sticky='w')
                self.master.after(2000, self.set_SA_label)
        except ValueError:
            self.smoked_amt_lbl.destroy()
            self.smoked_amt_lbl = ttk.Label(self.master,
                                            text='You must enter a \nnumerical value')
            self.smoked_amt_lbl.grid(row=5, column=1, sticky='w')
            self.master.after(2000, self.set_SA_label)

    # second window
    def go_to_buy_window(self):
        buy_window = tk.Toplevel()

        def close_window():
            buy_window.destroy()

        # settings
        buy_window.title("Purchase Manager")
        style = ttk.Style()
        style.theme_use('classic')
        buy_window.configure(background='green4')
        style.configure("buy.TButton", padding=6, relief="ridge",
                        foreground="green4", background="LemonChiffon3", font=("Courier", 14))
        style.map("buy.TButton",
                  foreground=[('pressed', 'LemonChiffon3'), ('active', 'red2')],
                  background=[('pressed', '!disabled', 'green4'), ('active', 'khaki2')]
                  )
        style.configure("buy.TLabel", background="green4", foreground="LemonChiffon3", padding=15, font=("Courier", 14))
        for i in range(4):
            buy_window.columnconfigure(i, weight=1, minsize=25)
            buy_window.rowconfigure(i, weight=1, minsize=50)

            for j in range(0, 3):
                frame = ttk.Frame(
                    master=buy_window,
                    relief='flat',
                    borderwidth=4
                )
                frame.grid(row=i, column=j, padx=3, pady=3)
        window_greeting = ttk.Label(buy_window, text="Welcome to the Purchase Manager", style='buy.TLabel')
        window_greeting.grid(row=0, column=0)
        close_button = ttk.Button(buy_window, text='Close', command=close_window, style='buy.TButton')
        close_button.grid(row=0, column=1)
        # how much did you purchase and how much did it cost?
        how_much_grams = ttk.Label(buy_window, text="Enter amount purchased (g): ", style='buy.TLabel')
        how_much_grams.grid(row=2, column=0, sticky='w')
        weed_amt_entry1 = tk.Entry(buy_window, state='normal', fg='green4', bg='LemonChiffon3', font=("Courier", 14))
        weed_amt_entry1.grid(row=2, column=1, sticky='w')
        how_much_cost = ttk.Label(buy_window, text="Enter how much the weed cost ($): ", style='buy.TLabel')
        how_much_cost.grid(row=3, column=0, sticky='w')
        cost_entry = tk.Entry(buy_window, state='disabled', fg='green4', bg='LemonChiffon3', font=("Courier", 14))
        cost_entry.grid(row=3, column=1, sticky='w')

        def add_to_grams():
            if weed_amt_entry1.get() != "":
                amount = float(weed_amt_entry1.get())
                if amount > 0:
                    self.grams += amount
                    self.total_grams += amount
                    self.p_grams += amount
                    self.cw_lbl = ttk.Label(self.master,
                                            textvariable=self.label_var)
                    self.label_var.set("\n Current available weed: " + str(round(self.grams, 3)) + " grams.")
                    self.cw_lbl.grid(row=3, column=0)
                    if weed_amt_entry1.get():
                        cost_entry['state'] = 'normal'
                        cost_entry.focus_set()
                        weed_amt_entry1['state'] = 'disabled'
                    else:
                        cost_entry['state'] = 'disabled'
            else:
                purchased_lbl = ttk.Label(buy_window,
                                          text='You must enter an amount first',
                                          style='buy.TLabel')
                purchased_lbl.grid(row=4, column=0)
                purchased_lbl.after(3000, purchased_lbl.destroy)

        def add_to_price():
            if cost_entry.get() != "":
                amount = float(cost_entry.get())
                amount_g = float(weed_amt_entry1.get())
                ppg = round(amount / amount_g, 5)
                if amount >= 0:
                    self.update_time()
                    self.price += amount
                    cost_entry['state'] = 'disabled'
                    enter_data_button2['state'] = 'disabled'
                    if amount > 0:
                        purchased_lbl = ttk.Label(buy_window,
                                                  text="\n You spent: $" + str(amount) + " on "
                                                       + str(self.p_grams) + " grams of weed on " + str(
                                                      self.currentDay) + "\n\nThat's " + str(ppg) + " per gram!",
                                                  style='buy.TLabel')
                        purchased_lbl.grid(row=4, column=0)
                    else:
                        purchased_lbl = ttk.Label(buy_window,
                                                  text="\n You spent: $" + str(amount) + " on "
                                                       + str(self.p_grams) + " grams of weed on " + str(
                                                      self.currentDay + ".\n\nSweet! free weed!"),
                                                  style='buy.TLabel')
                        purchased_lbl.grid(row=4, column=0)
                    df1 = self.df.append({'Date': self.currentDay, 'Time': self.currentTime, 'Smoked_Now': 0,
                                          'Current Weed': round(self.grams, 3),
                                          'Total Bought': round(self.total_grams, 3),
                                          'Total Spent': self.price, 'ppg': ppg,
                                          "User": self.user_entry.get()}, ignore_index=True)
                    df1.to_excel("myWeed_{}.xlsx".format(self.user_entry.get()), index=False)
                    self.df = df1
                    self.smoked_amt_lbl = ttk.Label(self.master,
                                                    text="You smoked:\n{} grams of weed on\n".format(
                                                        self.day_tracker) + self.currentDay)
                    self.smoked_amt_lbl.grid(row=5, column=1)
                    buy_window.after(5000, buy_window.destroy)
            else:
                purchased_lbl = ttk.Label(buy_window,
                                          text='You must enter an amount first',
                                          style='buy.TLabel')
                purchased_lbl.grid(row=4, column=0)
                purchased_lbl.after(3000, purchased_lbl.destroy)

        enter_data_button1 = ttk.Button(buy_window,
                                        text='Enter Data',
                                        command=add_to_grams,
                                        style='buy.TButton')
        enter_data_button1.grid(row=2, column=2)
        enter_data_button2 = ttk.Button(buy_window, text='Enter Data', command=add_to_price,
                                        style='buy.TButton')
        enter_data_button2.grid(row=3, column=2)
        buy_window.mainloop()

    # third window
    def go_to_data(self):
        data = tk.Toplevel()

        def go_to_excel():
            user = self.user_entry.get()

            def openexcel():
                file_path = "myWeed_{}.xlsx".format(user)
                os.system("open -a 'Microsoft Excel.app' '%s'" % file_path)

            if (len(user) <= 8) and (len(user) >= 2):
                if os.path.exists("myWeed_{}.xlsx".format(user)):
                    openexcel()
                    data.after(1000, data.destroy)

        def close_window():
            data.destroy()

        # settings
        data.title("{}'s Weed Data".format(self.user_entry.get()))
        style = ttk.Style()
        style.theme_use('classic')
        data.configure(background='green4')
        style.configure("buy.TButton", padding=6, relief="ridge",
                        foreground="green4", background="LemonChiffon3", font=("Courier", 14))
        style.map("buy.TButton",
                  foreground=[('pressed', 'LemonChiffon3'), ('active', 'red2')],
                  background=[('pressed', '!disabled', 'green4'), ('active', 'khaki2')]
                  )
        style.configure("buy.TLabel", background="green4", foreground="LemonChiffon3", padding=15, font=("Courier", 15))
        for i in range(4):
            data.columnconfigure(i, weight=1, minsize=25)
            data.rowconfigure(i, weight=1, minsize=50)

            for j in range(0, 3):
                frame = ttk.Frame(
                    master=data,
                    relief='flat',
                    borderwidth=4
                )
                frame.grid(row=i, column=j, padx=3, pady=3)
        window_greeting = ttk.Label(data,
                                    text="History of smoke seshes:\n",
                                    style='buy.TLabel')
        window_greeting.grid(row=0, column=0)
        close_button = ttk.Button(data, text='Close', command=close_window, style='buy.TButton')
        close_button.grid(row=0, column=2)
        excel_button = ttk.Button(data,
                                  text='View in\n Excel',
                                  command=go_to_excel,
                                  style='buy.TButton')
        excel_button.grid(row=0, column=1)
        data_lbl = ttk.Label(data, text=str(self.df), style='buy.TLabel')
        data_lbl.grid(row=1, column=0, columnspan=2)

    # fourth window
    def open_stats_window(self):
        stats = tk.Toplevel()

        def close_window():
            stats.destroy()

        # aggregate function button labels
        def set_avg_pday_lbl():
            filter1 = self.df.groupby("Date").Smoked_Now.sum()
            filter2 = filter1.mean()
            avg_pday = round(filter2, 5)
            avg_pday_lbl = ttk.Label(stats, text="Average amount smoked per day (g):\n" + str(avg_pday),
                                     style='buy.TLabel')
            avg_pday_lbl.grid(row=3, column=1, sticky='')
            avg_pday_lbl.after(5000, avg_pday_lbl.destroy)

        def set_avg_ppg_lbl():
            avg_ppg = self.df.loc[~self.df["ppg"].astype(str).str.isdigit(), 'ppg']
            avg_ppg = avg_ppg.mean()
            avg_ppg = round(avg_ppg, 5)
            avg_ppg_lbl = ttk.Label(stats, text="Average price paid per gram:\n$" + str(avg_ppg), style='buy.TLabel')
            avg_ppg_lbl.grid(row=3, column=1, sticky='')
            avg_ppg_lbl.after(5000, avg_ppg_lbl.destroy)

        def set_avg_pweek_lbl():
            dates = self.df.Date.unique()
            N = 7

            if len(dates) % 7 == 0:
                daily_avgs = self.df.groupby("Date").Smoked_Now.sum()
                avg_pweek = daily_avgs.values.reshape(-1, N).sum(1)
                avg_total = avg_pweek.mean()
                avg_total_lbl = ttk.Label(stats, text="Average amount smoked per week (g):\n" + str(avg_total),
                                          style='buy.TLabel')
                avg_total_lbl.grid(row=3, column=1, sticky='')
                avg_total_lbl.after(5000, avg_total_lbl.destroy)
            else:
                avg_total_lbl = ttk.Label(stats, text="Total days smoked must be a multiple of 7\n",
                                          style='buy.TLabel')
                avg_total_lbl.grid(row=3, column=1, sticky='')
                avg_total_lbl.after(5000, avg_total_lbl.destroy)

        def set_days_smoked():
            days_smoked = len(self.df['Date'].unique())
            days_smoked_lbl = ttk.Label(stats, text="Total Days Smoked:\n" + str(days_smoked),
                                        style='buy.TLabel')
            days_smoked_lbl.grid(row=3, column=1, sticky='')
            days_smoked_lbl.after(5000, days_smoked_lbl.destroy)

        # settings
        stats.title("{}'s Weed Statistics".format(self.user_entry.get()))
        for i in range(5):
            stats.columnconfigure(i, weight=1, minsize=25)
            stats.rowconfigure(i, weight=1, minsize=50)

            for j in range(0, 4):
                frame = ttk.Frame(
                    master=stats,
                    relief='flat',
                    borderwidth=4
                )
                frame.grid(row=i, column=j, padx=3, pady=3)
        style = ttk.Style()
        style.theme_use('classic')
        stats.configure(background='green4')
        style.configure("buy.TButton", padding=6, relief="ridge",
                        foreground="green4", background="LemonChiffon3", font=("Courier", 14))
        style.map("buy.TButton",
                  foreground=[('pressed', 'LemonChiffon3'), ('active', 'red2')],
                  background=[('pressed', '!disabled', 'green4'), ('active', 'khaki2')]
                  )
        style.configure("buy.TLabel", background="green4", foreground="LemonChiffon3", padding=15, font=("Courier", 15))
        window_greeting = ttk.Label(stats,
                                    text="Some functions to calculate\n various usage statistics:\n",
                                    style='buy.TLabel')
        window_greeting.grid(row=0, column=0)
        close_button = ttk.Button(stats, text='Close', command=close_window, style='buy.TButton')
        close_button.grid(row=0, column=2)
        avg_ppg_b = ttk.Button(stats,
                               text="Average Price\n"
                                    "Per Gram",
                               state='normal',
                               command=set_avg_ppg_lbl,
                               style='buy.TButton')
        avg_ppg_b.grid(row=1, column=0, sticky='n')
        avg_pday_b = ttk.Button(stats,
                                text="Average Smoked\nPer Day",
                                state='normal',
                                command=set_avg_pday_lbl,
                                style='buy.TButton')
        avg_pday_b.grid(row=1, column=1, sticky='n')
        avg_pweek_b = ttk.Button(stats,
                                 text="Average Smoked\nPer Week",
                                 command=set_avg_pweek_lbl,
                                 style='buy.TButton')
        avg_pweek_b.grid(row=1, column=3, sticky='n')
        days_smoked_button = ttk.Button(stats,
                                        text="# Days\nSmoked",
                                        command=set_days_smoked,
                                        style='buy.TButton')
        days_smoked_button.grid(row=2, column=0, sticky='s')


def main():
    root = tk.Tk()
    MyWeed(root)
    root.mainloop()


main()
