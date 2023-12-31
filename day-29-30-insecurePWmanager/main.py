from tkinter import *
from tkinter import messagebox
from random import choice, randint, sample
import pyperclip
import json


# constants
BLACK = '#0f1011'
RED = '#ee1f1f'
FONT_NAME = 'Arial'


# search function
def search_pw():
    url = website.get()
    try:
        with open('passwords.json', mode='r') as pw_file:
            creds = json.load(pw_file)
            creds.update()
            x = False
            for site in creds:
                if site == url:
                    x = True
                    messagebox.showinfo(title=f'{url}', message=f'Username:{creds.get(url, None)["email"]}\nPassword:{creds.get(url, None)["password"]}')
                    break
            if not x:
                messagebox.showerror(title='Error', message='No credentials associated with provided website.')
    except FileNotFoundError:
        messagebox.showerror(title='Error', message='No password history is currently saved.\nPlease save a password.')

# password gen function
def gen_password():
    password.delete(0, END)
    
    generator = {
    'letters':{
        'list':['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], 
        'num':randint(8, 10)
    },
    'numbers':{
        'list':['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 
        'num':randint(2, 4)
    },
    'symbols':{
        'list':['!', '#', '$', '%', '&', '(', ')', '*', '+'], 
        'num':randint(2, 4)
    },
    }

    pre_gen = []
    for key, value in generator.items():
        for _ in range(0, value['num']):
            pre_gen.append(choice(value['list']))

    pw = ''.join(sample(pre_gen, len(pre_gen)))

    pyperclip.copy(pw)
    password.insert(0, pw)


# add function
def save_password():
    if len(website.get()) > 0 and len(username.get()) > 0 and len(password.get()) > 0:
        
        credentials_correct = messagebox.askokcancel(title='Confirmation', message=f'Website: {website.get()}\nEmail/Username: {username.get()}\nPassword: {password.get()}\nAre these Credentials Correct?')
    
        if credentials_correct:

            formatted_creds = {
                website.get(): {
                    'email': username.get(),
                    'password': password.get(),
                }
            }
            try:
                with open('passwords.json', mode='r') as pw_file:
                    # read old data
                    creds = json.load(pw_file)
                    #update the old data with the new stuff
                    creds.update(formatted_creds)

                with open('passwords.json', mode='w') as pw_file:
                    # save the new data
                    json.dump(creds, pw_file, indent=4) # indent = num of spaces in between braces, and adds new lines

                    messagebox.showinfo(title='Success', message=f'Password for {username.get()} on {website.get()} has successfully been saved to .\{pw_file.name}!')
            except FileNotFoundError:
                with open('passwords.json', mode='w') as pw_file:
                    json.dump(formatted_creds, pw_file, indent=4)

                    messagebox.showinfo(title='Success', message=f'Password for {username.get()} on {website.get()} has successfully been saved to .\{pw_file.name}!')

            website.delete(0, END)
            password.delete(0, END)
            website.focus()
        else:
            website.delete(0, END)
            password.delete(0, END)
            website.focus()

            messagebox.showinfo(title='Failure', message=f'Account details were not saved.')
    else:
        messagebox.showerror(title='Error', message='Field left empty')


# screen settings
screen = Tk()
screen.title('Insecure Password Manager')
screen.minsize(width=680, height=450,)
screen.config(padx=25, pady= 20, bg=BLACK)


# placing the logo onto the screen
insecure_logo = Canvas(width=657, height=287, )
logo = PhotoImage(file='insecure_logo.png')
insecure_logo.create_image(328, 143, image=logo)
insecure_logo.config(highlightthickness=0)
insecure_logo.grid(row=1, column=0, columnspan=8)


# text labels
website_label = Label(text='Website:', font=(FONT_NAME, 12), bg=BLACK, fg=RED)
emailuser_label = Label(text='Email/Username:', font=(FONT_NAME, 12), bg=BLACK, fg=RED)
password_label =  Label(text='Password:', font=(FONT_NAME, 12), bg=BLACK, fg=RED)

website_label.grid(row=2, column=1)
emailuser_label.grid(row=3, column=1)
password_label.grid(row=4, column=1)


# entries
website = Entry(width=30)
website.focus()
username = Entry(width=60)
username.insert(0, 'joe@mail.com')
password = Entry(width=30)

website.grid(row=2, column=2, columnspan=2)
username.grid(row=3, column=2, columnspan=5)
password.grid(row=4, column=2, columnspan=2)


# buttons
generate_password = Button(text='Generate Password',highlightthickness=0, width=30, command=gen_password)
add_button = Button(text='Add',highlightthickness=0, width=60, command=save_password)
search_button = Button(text='Search',highlightthickness=0, width=30, command=search_pw)

generate_password.grid(row=4, column=5, columnspan=2)
add_button.grid(row=5, column=2, columnspan=5)
search_button.grid(row=2, column=5, columnspan=2)

screen.mainloop()