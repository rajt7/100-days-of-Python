from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)

    password_input.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()
    new_data = {
        website : {
            'email': email,
            'password': password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open('data.json', 'r') as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open('data.json', 'w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open('data.json', 'w') as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_input.delete(0, END)
            password_input.delete(0, END)

            website_input.focus()


# ---------------------------- SAVE PASSWORD ------------------------------- #
def search_password():
    website = website_input.get()

    try:
        with open('data.json', 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found")
    else:
        if website in data:
            email = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
window.grid_columnconfigure(0, weight=1, uniform="foo")

canvas = Canvas(width=250, height=250)
pass_img = PhotoImage(file='logo.png')
canvas.create_image(125, 125, image=pass_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0, sticky=W, pady=3)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0, sticky=W, pady=3)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0, sticky=W, pady=3)

# Entry
website_input = Entry(width=35)
website_input.grid(row=1, column=1, columnspan=2, sticky=W, padx=10, pady=3)
website_input.focus()
email_input = Entry(width=35)
email_input.insert(0, 'raj@gmail.com')
email_input.grid(row=2, column=1, columnspan=2, sticky=W, padx=10, pady=3)
password_input = Entry(width=17)
password_input.grid(row=3, column=1, sticky=W, padx=10, pady=3)

# Buttons
search_btn = Button(text="Search", command=search_password)
search_btn.grid(row=1, column=2, pady=3)

generate_pass_btn = Button(text="Generate Password", command=generate_password)
generate_pass_btn.grid(row=3, column=2, sticky=W, padx=0, pady=3)

add_btn = Button(text="Add", width=33, command=save_data)
add_btn.grid(row=4, column=1, columnspan=2, sticky=W, pady=3)

window.mainloop()
