import PySimpleGUI as sg
import csv
from datetime import date
import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username text PRIMARY KEY, password text)''')
conn.commit()

username = 'Charles'
password = 'magic'
sg.theme('DarkAmber')

#creat log in csv log (to be database) for username password and account settings
Accnt_create_layout = [[sg.Text('create your account')],
        [sg.Text('username'),sg.Input()],
        [sg.Text('Create Password'),sg.InputText()],
        [sg.Text('Verify Password'),sg.InputText()],
        [sg.Button('Create Account'),sg.Button('Cancel')]]

# Create the layout for the window
main_layout = [[sg.Text('Food and Symptom Tracker')],
          [sg.Input(),sg.CalendarButton('Date of Entry',format='%Y-%m-%d')],
          [sg.InputText(),sg.Text('Breakfast')],
          [sg.InputText(),sg.Text('Lunch')],
          [sg.InputText(),sg.Text('Dinner')],
          [sg.InputText(),sg.Text('Nausea 1-10')],
          [sg.InputText(),sg.Text('Diarrea 1-10')],
          [sg.InputText(),sg.Text('Reflux 1-10')],
          [sg.Button('Log')],
          [sg.Button('Exit')]]

login_layout = [
    [sg.Text('Sign In',size=(10,10))],
    [sg.Text('Username'),sg.InputText()],
    [sg.Text('Password'),sg.InputText()],
    [sg.Button('Sign In'),sg.Button('Cancel')],
    [sg.Button('Create Account')]]


# Create the window
login_window = sg.Window('Sign In',login_layout)
window = sg.Window('My IBS tracker', main_layout)
Create_Account = sg.Window('New Account',Accnt_create_layout)

# Main event loop

while True:
    event, values = login_window.read()
    #close
    if event == sg.WINDOW_CLOSED or event == 'Cancel':
        break
    #create account
    if event == 'Create Account':
        event, values = Create_Account.read()
        if event == sg.WINDOW_CLOSED or event == 'Cancel':
                break
        if event == 'Create Account':
            if values[0] != '' and values[1] != '' and values[2] == values[1]:
                c.execute("INSERT INTO users VALUES (?, ?)", (values[0],values[1]))
                conn.commit()
                with open('accounts.csv', 'a', newline='') as accountfile:
                    write = csv.writer(accountfile)
                    write.writerow([values[0],values[1]])
                Create_Account.close()
                event = sg.popup('Account created')
            elif values[2] != values[1]:
                sg.popup('Error: password verification does not match password.')
            elif values[1] or values[1] == '':
                sg.popup('Please enter a Password')
    #sign in button
    if event == 'Sign In':
        if values[0] == username and values[1] == password:
            event, values = window.read()
            login_window.close()
            if event == sg.WINDOW_CLOSED or event == 'Exit':
                break
            if event == 'Log':
                if values[1].isnumeric():
                    sg.popup('enter a food dumby')
                elif values[2].isnumeric():
                    sg.popup('enter a food stupd')
                elif values[3].isnumeric():
                    sg.popup('enter a food fool')
                # Write the values to a CSV file
                else:
                    with open('mylog.csv', 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([values[0], values[1],values[2],values[3],values[4],values[5],values[6]])
                    sg.popup('Logged successfully!')
        else:
            sg.popup('Incorrect password')

sg.WINDOW_CLOSED
