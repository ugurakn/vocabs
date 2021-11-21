from tkinter import *
from tkinter import messagebox
import sqlite3 as sq
import random
import os
import sys
import time
from threading import Thread

win = Tk()
win.title("Vocabs")
win.resizable(False, False)
win.configure(bg="#345")
win.columnconfigure(0, weight=1)

# color constants
L_GRAY     = "#d3d3d3"
D_BLUE     = "#cbdce7"
DARK_GREEN = "#008000"
L_GREEN    = "#e5f2e5"
L_YELLOW   = "#FFFFE0"
L_ORANGE   = "#ddddc5"

# option/preference variables
word_recent = False
spl_recent = False
#this_week = False
#this_month = False

#print(word_recent.get())

# set window size and its place on screen
scr_width = win.winfo_screenwidth()
scr_height = win.winfo_screenheight()
width  = 400
height = 500
x_pos = int((scr_width / 2) - (width / 2))
y_pos = int((scr_height / 2) - (height / 2))
win.geometry(f"{width}x{height}+{x_pos}+{y_pos}")

# function to initialize database
def init_db():
    
    # check if program is running for first time (check if db exists)
    first_run = False
    if not os.path.exists("vocab.db"):
        first_run = True
        
        
    
    # create a database or connect to one
    conn = sq.connect("vocab.db")
    cur = conn.cursor()
    
    # create table for db
    cur.execute("""CREATE TABLE IF NOT EXISTS words (
                word text,
                article text,
                meaning text,
                gender text,
                type text,
                time_added integer
                )""")
    # commit changes made to the database and close it
    conn.commit()
    conn.close()

    # first run instructions
    if first_run:
        messagebox.showinfo("Welcome", "Welcome to Vocabs! Please first add a few words (at least one) to your personal dictionary. Check HELP section for help.") 
        add_btn()

        
# FUNCTIONS FOR BUTTONS

def word_exercise(): # function for word exercise button
    def sec_win():
        def wait(*args):
            wait_time = args[0]
            
            for i in range(wait_time):
                time.sleep(1)

            if exercise_win.winfo_exists():
                new()
            else:
                #print("thread ended")
                return
            
        def submit(*event): # check if entered meaning is correct button
            # check if e.get() equals meaning
            meaning = word[1]
            mnng_list = meaning.split(",")
                
            
            if e.get().lower() in mnng_list:
                text= "CORRECT!\n{}: {}".format(word[0], word[1])
                word_l.config(text=text, fg=DARK_GREEN, font=("Helvetica", 18)) 
                submit_btn.config(state=DISABLED)
                wait_for = (1, )
            else:
                text= "WRONG:(\n{}: {}".format(word[0], word[1])
                word_l.config(text=text, fg="#FF0000", font=("Helvetica", 18)) # bg red 
                submit_btn.config(state=DISABLED)
                wait_for = (3, )

            # delete the entrybox
            e.delete(0, END)
                
            # make "new" button active and submit inactive
            #new_btn.config(state=ACTIVE)
            submit_btn.config(state=DISABLED)

            # start wait thread
            wait_ = Thread(target=wait, args=wait_for, daemon=True)
            wait_.start()
            
        def new(): # get new word button
            word_l.config(text="")
            sec_win()

        # filter data acc to user preferences (if any, else use default)
        # only use the 10 most recently added words 
        filtered_data = list()
        if word_recent:
            data.sort(key=lambda entry: entry[-1], reverse=True)
            
            for num, entry in enumerate(data):
                filtered_data.append(entry)
                if num == 49:
                    break

        else:
            filtered_data = data
            
        
        # create label to display the word
        word = random.choice(filtered_data)
        word_l = Label(exercise_win, text=word[0], width=30, font=("Helvetica", 22), bg=L_GREEN)
        word_l.grid(row=0, column=0, columnspan=2, padx=30, pady=30)
        # entry box label
        entry_l = Label(exercise_win, text="enter meaning below", bg=L_GREEN, font=("Helvetica", 10))
        entry_l.grid(row=1, column=0, pady= (10,0))
        # entry box to enter word's meaning
        e = Entry(exercise_win, width=15, font=("Helvetica", 14))
        e.grid(row=2, column=0, pady=10)
        e.focus()
        # submit button
        submit_btn = Button(exercise_win, text="submit (enter)", width=20, bg="white", fg="black", relief=RIDGE, font=("Helvetica", 14), command=submit)
        submit_btn.grid(row=3, column=0, columnspan=2, pady=(20,20))
        # new word button(REMOVED)
        #new_btn = Button(exercise_win, text="new", width=20, font=("Arial", 12), state=DISABLED, command=new)
        #new_btn.grid(row=4, column=0, columnspan=2, pady=(0,20))

        # key bind <Return> to submit function
        exercise_win.bind("<Return>", submit)
        

        
    # create a database or connect to one
    conn = sq.connect("vocab.db")
    cur = conn.cursor()
    # select and fetch all words from db
    cur.execute("""SELECT *, oid FROM words""")
    data = cur.fetchall()
    if len(data) == 0:
        messagebox.showinfo("no words", "please add a few words first!")
        return
    #print(data)
    # commit changes made to the database and close it
    conn.commit()
    conn.close()

    # call toplevel win to display the exercise
    exercise_win = Toplevel()
    exercise_win.title("word exercise")
    # determine where the window pops on the screen
    #exercise_win.update_idletasks()
    width, height = 600, 300
    x_pos = int((scr_width / 2) - (width / 2))
    y_pos = int((scr_height / 2) - (height / 2))
    
    exercise_win.geometry(f"{width}x{height}+{x_pos}+{y_pos}")
    exercise_win.configure(bg=L_GREEN)
    exercise_win.resizable(False, False)
    exercise_win.columnconfigure(0, weight=1)
    exercise_win.focus_set()
    exercise_win.grab_set()
    sec_win()
    

def spl_exercise(): # function for spelling exercise button

    def spl_win():
        
        def wait(*args): # thread to get a new word after a few seconds automatically
            wait_time = args[0]
            
            for i in range(wait_time):
                  time.sleep(1)

            if spell_win.winfo_exists():
                new()
            else:
                #print("thread ended")
                return
                
            
                
        def submit(*event): # button for submitting spelled word
            
            # check if entered word is correctly spelled
            if e.get().lower() == word[0]:
                word_l.config(fg=DARK_GREEN, text= "CORRECT!\n{}".format(word[0]), font=("Helvetica", 18))
                wait_for = (1,) # make it a tuple to pass it as iterable to thread's args
                
            else:
                word_l.config(fg="#FF0000", text= "WRONG:(\n{}".format(word[0]), font=("Helvetica", 18))
                wait_for = (3,)

            # update button states
            submit_btn.config(state=DISABLED)

            # delete the entrybox
            e.delete(0, END)
            
            # start wait thread
            wait_ = Thread(target=wait, args=wait_for, daemon=True)
            wait_.start()

        def new(): # button for getting new word to spell
            word_l.config(text="")
            spl_win()
            


        # filter data acc to user preferences (if any, else use default)
        # only use the 50 most recently added words 
        filtered_data = list()
        if spl_recent:
            data.sort(key=lambda entry: entry[-1], reverse=True)
            
            for num, entry in enumerate(data):
                filtered_data.append(entry)
                if num == 49:
                    break
            

        else:
            filtered_data = data
            

        # designate and format the word to spell (only first and last letter given to user)
        word = random.choice(filtered_data)
        word_list = list(word[0])
        rand_pos = random.randint(1, (len(word_list)-1))
        if (len(word_list) <= 4):
            rand_pos = None
            
        spl_word = "".join([letter+" " if (i == 0 or i == rand_pos) else "_ " for i, letter in enumerate(word_list)]) # this line took me an hour 
        
        # create label to display the word
        word_l = Label(spell_win, text=spl_word, width=25, bg=D_BLUE, font=("Helvetica", 20))
        word_l.grid(row=0, column=0, columnspan=2, padx=30, pady=(30,10))
        # label to display word's meaning
        mnng_l = Label(spell_win, text="meaning: {}".format(word[1]), width=30, bg=D_BLUE, font=("Helvetica", 14))
        mnng_l.grid(row=1, column=0, columnspan=2, padx=30, pady=20)
        # entry box label
        entry_l = Label(spell_win, text="spell the word below", bg=D_BLUE, font=("Helvetica", 10))
        entry_l.grid(row=2, column=0, pady=(10,0))
        # entry box to enter full word
        e = Entry(spell_win, width=15, bg="white", font=("Helvetica", 14))
        e.grid(row=3, column=0, pady=10)
        e.focus()
        # submit button
        submit_btn = Button(spell_win, text="submit (enter)", width=20, bg="white", fg="black", relief=RIDGE, font=("Helvetica", 14), command=submit)
        submit_btn.grid(row=4, column=0, columnspan=2, pady=(5,10))
        # new word button (REMOVED)
        #new_btn = Button(spell_win, text="new", width=20, font=("Arial", 12), state=DISABLED, command=new)
        #new_btn.grid(row=5, column=0, columnspan=2, pady=(0,20))
        
        # key-bind Enter to submit function
        spell_win.bind("<Return>", submit)
        

   
        
    # connect to db
    conn = sq.connect("vocab.db")
    cur = conn.cursor()
    # select and fetch all words from db
    cur.execute("""SELECT *, oid FROM words""")
    data = cur.fetchall()
    if len(data) == 0:
        messagebox.showinfo("no words", "please add a few words first!")
        return
    #print(data)
    # commit changes made to the database and close it
    conn.commit()
    conn.close()

    # call toplevel win to display spelling exercise
    spell_win = Toplevel()
    spell_win.title("spelling exercise")
    # determine where on the screen the window appears
    width, height = 600, 300
    x_pos = int((scr_width / 2) - (width / 2))
    y_pos = int((scr_height / 2) - (height / 2))
    spell_win.geometry(f"{width}x{height}+{x_pos}+{y_pos}")
    
    spell_win.resizable(False, False)
    spell_win.columnconfigure(0, weight=1)
    spell_win.configure(bg=D_BLUE)
    spell_win.focus_set()
    spell_win.grab_set()
    spl_win()
    
    


def add_btn():
    def submit(*event): # func for submit button
        # create a database or connect to one
        conn = sq.connect("vocab.db")
        cur = conn.cursor()

        # check if word and meaning are entered
        if len(word_e.get()) == 0 or len(meaning_e.get()) == 0:
            messagebox.showinfo("entry warning", "You need to enter at least WORD and MEANING!")
            return
            
        # put entries into proper format (remove spaces and lowercase)
        ent_word    = ("".join(word_e.get().split(" "))).lower()
        ent_mnng    = ("".join(meaning_e.get().split(" "))).lower()
        ent_article = ("".join(article_e.get().split(" "))).lower()
        ent_gender  = ("".join(gender_e.get().split(" "))).lower()
        ent_type    = ("".join(type_e.get().split(" "))).lower()
        
        # add entry boxes' contents into db table
        cur.execute("INSERT INTO words VALUES (:word, :meaning, :article, :gender, :type, :time_added)",
                    { "word": ent_word,
                      "meaning": ent_mnng,
                      "article": ent_article,
                      "gender": ent_gender,
                      "type": ent_type,
                      "time_added": int(time.time()),
                     })
        # commit changes made to the database and close it
        conn.commit()
        conn.close()
        # clear entry boxes
        word_e.delete(0, END)
        meaning_e.delete(0, END)
        article_e.delete(0,END)
        gender_e.delete(0, END)
        type_e.delete(0, END)

        # set focus to word_e
        word_e.focus()
        
    add_win = Toplevel()
    add_win.configure(bg=L_ORANGE)
    # determine where on the screen the window appears
    #width, height = add_win.winfo_reqwidth(), add_win.winfo_reqheight() # get the width/height the window requests
    width, height = 350, 400
    x_pos = int((scr_width / 2) - (width / 2))
    y_pos = int((scr_height / 2) - (height / 2))
    add_win.geometry(f"{width}x{height}+{x_pos}+{y_pos}")

    add_win.title("add words")
    add_win.resizable(False, False)
    add_win.focus_set()
    add_win.grab_set()
    # add labels and entry boxes to add words to db
    word_l = Label(add_win, text="Word", bg=L_ORANGE, width=15, font=("Arial", 12))
    word_l.grid(row=1, column=0, pady=20, padx=15, sticky=W)
    meaning_l = Label(add_win, text="Meaning", bg=L_ORANGE, width=15, font=("Arial", 12))
    meaning_l.grid(row=2, column=0, pady=20, padx=15, sticky=W)
    type_l = Label(add_win, text="Type", bg=L_ORANGE, width=15, font=("Arial", 12))
    type_l.grid(row=3, column=0, pady=20, padx=15, sticky=W)
    article_l = Label(add_win, text="Article", bg=L_ORANGE, width=15, font=("Arial", 12))
    article_l.grid(row=4, column=0, pady=20, padx=15, sticky=W)
    gender_l = Label(add_win, text="Gender", bg=L_ORANGE, width=15, font=("Arial", 12))
    gender_l.grid(row=5, column=0, pady=20, padx=15, sticky=W)

    #entry boxes
    word_e = Entry(add_win, width=15, font=("Arial", 12))
    word_e.grid(row=1, column=1, pady=20, padx=15)
    meaning_e = Entry(add_win, width=15, font=("Arial", 12))
    meaning_e.grid(row=2, column=1, pady=20, padx=15)
    type_e = Entry(add_win, width=15, font=("Arial", 12))
    type_e.grid(row=3, column=1, pady=20, padx=15)
    article_e = Entry(add_win, width=15, font=("Arial", 12))
    article_e.grid(row=4, column=1, pady=20, padx=15)
    gender_e = Entry(add_win, width=15, font=("Arial", 12))
    gender_e.grid(row=5, column=1, pady=20, padx=15)

    # set focus to word_e
    word_e.focus()
    
    # submit button
    submit_btn = Button(add_win, width=20, text="submit (enter)", relief=GROOVE, bd=4, font=("Arial",12), command=submit)
    submit_btn.grid(row=6, column=0, columnspan=2, pady=20)

    # key-bind enter to submit button
    add_win.bind("<Return>", submit)
    

def see_words(): # see_w_btn command function to see all added words in db
    
    def display_words(): # toplevel win to display data
        def see(event): # button for seeing the details for the word selected
            try: # pass see function if no item in lb is selected (pass exception as well)
                lb.get(lb.curselection())
            except Exception:
                pass
                return
            else:
                cur_word = lb.get(lb.curselection())
                
        
            # get index of current selected word
            index = lb.get(0, END).index(cur_word)
            word, meaning, article, gender, type_, time_added = data[index][0], data[index][1], data[index][2], data[index][3], data[index][4], data[index][5]
            
            # format details acc to type of word
            if type_.strip() != "":
                details = "{} ({}): {}".format(word, type_, meaning)
            #if type_ == "verb" or type_ == "v":
                #details = "{} ({}): {}".format(word, type_, meaning)
            #elif type_ == "noun" or type_ == "n":
                #details = "{} ({}): {}".format(word, type_, meaning)
            #elif type_ != "":
                #details = "{} ({}): {}".format(word, type_, meaning)
            else:
                details = "{}: {}".format(word, meaning)
            # details on screen    
            details_l.config(text=details)
            # activate del button
            del_btn.config(state=ACTIVE)
            # make click label invisible
            click_l.config(text="")

        def delete(): # button for deleting a record from db
            if lb.get(lb.curselection()) != "":
                cur_record = lb.get(lb.curselection())
            else:
                return
                
            # connect to db
            conn = sq.connect("vocab.db")
            cur = conn.cursor()
            # select and fetch all words from db
            cur.execute("""SELECT *, oid FROM words""")
            mix_data = cur.fetchall()
            # get the string to search for in mix_data
            index = cur_record.find(":")
            # slice the string to get the word in db
            cur_record = cur_record[0:index]
            
            for entry in mix_data:
                if entry[0] == cur_record:
                    oid = entry[-1]
                    break

            # delete the record using its oid from db
            cur.execute("DELETE from words WHERE oid={}".format(oid))
            # delete record from data list as well
            for entry in data:
                if oid == entry[-1]:
                    data.remove(entry)
                    break
                
            # commit changes made to the database and close it
            conn.commit()
            conn.close()

            # sort words based on new data of words
            sort_data(sort_var.get())
            
            # restart window
            #nonlocal all_w_win
            #all_w_win.destroy()
            #display_words()

        def sort_data(event): # function for sort_menu to choose how to sort words
            nonlocal data
            
            if event == sort_options[0]:
                sorted_data = sorted(data, key= lambda entry: entry[0])
            elif event == sort_options[1]:
                sorted_data = sorted(data, key= lambda entry: entry[-1], reverse=True)
            elif event == sort_options[2]: # include only the words entered this week
                sorted_data = sorted(data, key= lambda entry: entry[-2], reverse=True)
                sorted_data = [i for i in sorted_data if time.time() - i[-2] < 600000]
            elif event == sort_options[3]: # include only the words entered this month
                sorted_data = sorted(data, key= lambda entry: entry[-2], reverse=True)
                sorted_data = [i for i in sorted_data if time.time() - i[-2] < 2500000]
            
            # delete contents of listbox before inserting re-sorted words
            lb.delete(0, END)
            
            #data = sorted_data
            # put words into listbox
            for entry in sorted_data:
                text = "{}: {}".format(entry[0], entry[1])
                lb.insert(END, text)
                
                
            

        # minimize main window when toplevel win opens (test)
        #win.iconify()

        # initialize toplevel win    
        all_w_win = Toplevel()
        all_w_win.title("all words")
        # determine where on screen the win appears
        width, height = 400, 400
        x_pos = int((scr_width / 2) - (width / 2))
        y_pos = int((scr_height / 2) - (height / 2))
        all_w_win.geometry(f"{width}x{height}+{x_pos}+{y_pos}")

        all_w_win.config(bg=L_YELLOW)
        all_w_win.resizable(False, False)
        all_w_win.focus_set()
        all_w_win.grab_set()

        
        # default sorting of data (alphabetical)
        data.sort(key=lambda entry: entry[0])
                
        # add optionMenu to choose the order of words
        sort_var = StringVar()
        sort_var.set(sort_options[0])
        sort_menu = OptionMenu(all_w_win, sort_var, *sort_options, command=sort_data)
        sort_menu.pack()
        # add scrollbar and pack it
        scroll = Scrollbar(all_w_win, orient=VERTICAL)
        scroll.pack(side=RIGHT, fill=Y)
        # create listbox to hold the words
        lb = Listbox(all_w_win, font=("parable", 14), height=10, width=35, yscrollcommand=scroll.set)
        #lb.config(height=lb.size()) # adjust lb size automatically
        scroll.config(command=lb.yview)
        lb.pack()
        
        # click label
        click_l = Label(all_w_win, text="click on a word to see details", bg=L_YELLOW, font=("Arial", 10))
        click_l.pack(pady=(10,0))
        # details of selected word label  (empty at first)    
        details_l = Label(all_w_win, text="", bg=L_YELLOW, font=("parable", 14))
        details_l.pack(pady=(5,10))
        # delete record button
        del_btn = Button(all_w_win, text= "delete word", bg="white", width=30, font=("arial", 12), state=DISABLED, command=delete)
        del_btn.pack(pady=(15,15))
        # key bind left-click to see word
        all_w_win.bind("<Button-1>", see)

        # put words into listbox
        for entry in data:
            text = "{}: {}".format(entry[0], entry[1])
            lb.insert(END, text)
        

        
        
            
            
            
    # create a database or connect to one
    conn = sq.connect("vocab.db")
    cur = conn.cursor()
    # select and fetch all words from db
    cur.execute("""SELECT *, oid FROM words""")
    data = cur.fetchall()

    #list to hold ordering options
    sort_options = ["alphabetical", "last added", "added this week", "added this month"]
    
    
    # commit changes made to the database and close it
    conn.commit()
    conn.close()

    # call inner func to display words on toplevel win
    display_words()

def help_(*event): # function for the help button (opens toplevel win)

    help_win = Toplevel()
    # determine win size and place it appears
    width, height = 400, 400
    x_pos = int((scr_width / 2) - (width / 2))
    y_pos = int((scr_height / 2) - (height / 2))
    help_win.geometry(f"{width}x{height}+{x_pos}+{y_pos}")
    
    help_win.title("Help")
    help_win.config(bg="#345")
    help_win.resizable(False, False)
    help_win.focus_set()
    help_win.grab_set()

    # create text widget and scrollbar to display help.txt in
    t = Text(help_win, height=21, bg="#345", fg="white", bd=0, font=("Arial",13))
    help_scroll = Scrollbar(help_win, orient=VERTICAL)
    # pack scrollbar and text widget on screen
    help_scroll.pack(side=RIGHT, fill=Y)
    t.pack(padx=10)
    help_scroll.config(command=t.yview)
    t.config(yscrollcommand=help_scroll.set)
    
    # get the help text from help_vocabs.txt
    with open("help_vocabs.txt") as file:
        help_text = file.read()

    # put help text inside text widget
    t.insert(END, help_text)

    # make text widget uneditable
    t.config(state=DISABLED)

def options(*event): # function for the options menu button (opens toplevel win)

    def set_word_recent(): # set word_check to global var
        global word_recent

        word_recent = word_var.get()
            

    def set_spl_recent(): # set spell_check to global var
        global spl_recent

        spl_recent = spl_var.get()



    # init toplevel options menu
    opt_win = Toplevel()

    # determine win size and place it appears on screen
    width, height = 400, 400
    x_pos = int((scr_width / 2) - (width / 2))
    y_pos = int((scr_height / 2) - (height / 2))
    opt_win.geometry(f"{width}x{height}+{x_pos}+{y_pos}")
    
    opt_win.title("Options")
    opt_win.config(bg="#345")
    opt_win.resizable(False, False)
    opt_win.columnconfigure(0, weight=1)
    opt_win.focus_set()
    opt_win.grab_set()

    # checkbox variables
    word_var = BooleanVar()
    spl_var  = BooleanVar()
    #wk_var   = BooleanVar()
    #mth_var = BooleanVar()
    
    # set variables to global values
    word_var.set(word_recent)
    spl_var.set(spl_recent)
    #wk_var.set(this_week)
    #mth_var.set(this_month)
    
    # checkboxes for options
    word_check  = Checkbutton(opt_win, font=("Arial", 12), bg="#345", fg="white", width=40, onvalue=True, offvalue=False, selectcolor="navy", activebackground="#345",
                text="Use only recently added words\nin Word Exercise (last 50)", anchor=W, justify=LEFT, variable=word_var, command=set_word_recent)
    spell_check = Checkbutton(opt_win, font=("Arial", 12), bg="#345", fg="white",width=40, onvalue=True, offvalue=False, selectcolor="navy", activebackground="#345",
                text="Use only recently added words\nin Spelling Exercise (last 50)", anchor=W, justify=LEFT, variable=spl_var, command=set_spl_recent)

    #weekly_check = Checkbutton(opt_win, font=("Arial", 12), bg="#345", fg="white", width=40, onvalue=True, offvalue=False, selectcolor="navy", activebackground="#345",
    #            text="Use only the words added this week\nin Word Exercise", anchor=W, justify=LEFT, variable=wk_var, command=set_weekly)
    #monthly_check = Checkbutton(opt_win, font=("Arial", 12), bg="#345", fg="white", width=40, onvalue=True, offvalue=False, selectcolor="navy", activebackground="#345",
    #            text="Use only the words added this month\nin Spelling Exercise", anchor=W, justify=LEFT, variable=mth_var, command=set_monthly)
    
    # pack chechboxes onto opt_win 
    word_check.grid(row=0, column=0, pady=(40,20), padx=30)
    spell_check.grid(row=1, column=0, pady=(0,20), padx=30)
    #weekly_check.grid(row=2, column=0, pady=(0,20), padx=30)
    #monthly_check.grid(row=3, column=0, pady=(0,20), padx=30)
    

# MAIN SCREEN WIDGETS

choose_actv = Label(win, text="Choose Activity", width=30, font=("Arial", 16), bg="#345", fg="white")
choose_actv.grid(row=0, column=0, pady=20, padx=20)

# ... widgets for activities

# word exercise

exercise_btn = Button(win, text="Word Exercise", width=30, font=("Arial", 14), command=word_exercise)
exercise_btn.grid(row=8, column=0, pady=20, padx=20)

# spelling exercise
spell_btn = Button(win, text="Spelling Exercise", width=30, font=("Arial", 14), command=spl_exercise)
spell_btn.grid(row=9, column=0, pady=20, padx=20)

# add new words (opens new window)
add_w_btn = Button(win, text="Add New Words", width=30, font=("Arial", 14), command=add_btn)
add_w_btn.grid(row=10, column=0, pady=20, padx=20)

# see all the words you've added
see_w_btn = Button(win, text="See All Words", width=30, font=("Arial", 14), command=see_words)
see_w_btn.grid(row=11, column=0, pady=20, padx=20)

# help button
help_btn = Button(win, text="HELP", width=20, bg="#345", fg="#b7af6d", activebackground="#345", bd=0, font=("Arial", 12), command=help_)
help_btn.grid(row=15, column=0, pady=(20,5), padx=20)

# options menu button
options_btn = Button(win, text="OPTIONS", width=20, bg="#345", fg="#b7af6d", activebackground="#345", bd=0, font=("Arial", 12), command=options)
options_btn.grid(row=16, column=0, pady=(5,20), padx=20)

# key-bind keyboard to help and options windows
win.bind("h", help_)
win.bind("o", options)



if __name__=="__main__":
    init_db()
    
    win.mainloop()



