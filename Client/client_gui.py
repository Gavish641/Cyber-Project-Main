from tkinter import *
from tkinter import messagebox
from client import MultiThreadedClient
import hashlib

BG_COLOR = "#212121"
EXIT_BG_COLOR = "#fc0303"

class GUI:
    def __init__(self, client):
        self.username = ''
        self.password = ''
        self.client = client
        self.top_levels = {}
        self.main_frame = ""

    def run(self):
        self.first_screen()

    def first_screen(self):
        window = Tk()
        window.attributes('-fullscreen', True)
        window.title("Gavish's Project")
        window['background'] = BG_COLOR 

        self.top_levels["first_window"] = window

        frame_login = Frame(window, bg="white")
        frame_login.place(relx=0.5, rely=0.5, width=1200, height=1000 , anchor="center")
        # laptop: width=900, height=700
        
        # Title & Subtitle
        title_name = Label(window, text="LuminaMentia", font=("Impact", 35, "bold"), fg="black", bg="white")
        title_name.place(relx=0.5, rely=0.1, anchor="center")
        title_name = Label(window, text="In order to continue, please login/sign up.", font=("Goudy old style", 15, "bold"), fg="black", bg="white")
        title_name.place(relx=0.25, rely=0.25)

        # Exit Button
        exit_button = Button(window, text="Exit", bd=0, font=("Goudy old style", 15), bg="red", fg="white", width=8, height=1, command=lambda: self.exit(window))
        exit_button.place(relx=0.5, rely=0.9, anchor="center")

        # Login & Sign Up Buttons
        login_button = Button(window, text="Login", bd=0, font=("Goudy old style", 15), bg="#6162FF", fg="white", width=10, command=self.login_window)
        login_button.place(relx=0.38, rely=0.5)
        login_button = Button(window, text="Sign Up", bd=0, font=("Goudy old style", 15), bg="#6162FF", fg="white", width=10, command=self.signup_window)
        login_button.place(relx=0.55, rely=0.5)

        window.mainloop()
        
    def login_window(self):
        login_frame = Tk()
        login_frame.attributes('-fullscreen', True)
        login_frame.title("login")
        login_frame['background'] = BG_COLOR

        self.top_levels["registration"] = login_frame

        frame_login = Frame(login_frame, bg="white")
        frame_login.place(relx=0.5, rely=0.5, width=1200, height=1000 , anchor="center")

        # Back & Exit Buttons
        back_button = Button(login_frame, text="Back", bd=0, font=("Goudy old style", 15), bg="grey", fg="white", width=8, height=1, command=lambda: self.back(login_frame))
        back_button.place(relx=0.73, rely=0.25)
        exit_button = Button(login_frame, text="Exit", bd=0, font=("Goudy old style", 15), bg="red", fg="white", width=8, height=1, command=lambda: self.exit(login_frame))
        exit_button.place(relx=0.5, rely=0.9, anchor="center")

        # Title & Subtitle
        title_name = Label(login_frame, text="LuminaMentia", font=("Impact", 35, "bold"), fg="black", bg="white")
        title_name.place(relx=0.5, rely=0.1, anchor="center")
        title = Label(login_frame, text="Login", font=("Impact", 25, "bold"), fg="#6162FF", bg="white")
        title.place(relx=0.5, rely=0.2, anchor="center")
        subtitle = Label(login_frame, text="Welcome back!", font=("Goudy old style", 15, "bold"), fg="#1d1d1d", bg="white")
        subtitle.place(relx=0.25, rely=0.25)

        # Username
        lbl_user = Label(login_frame, text="Username", font=("Goudy old style", 15, "bold"), fg="grey", bg="white")
        lbl_user.place(relx=0.46, rely=0.45, anchor="center")
        entry_login_username = Entry(login_frame, font=("Goudy old style", 15), bg="#E7E6E6")
        entry_login_username.place(relx=0.43, rely=0.47)

        # Password
        lbl_password = Label(login_frame, text="Password", font=("Goudy old style", 15, "bold"), fg="grey", bg="white")
        lbl_password.place(relx=0.46, rely=0.55, anchor="center")
        entry_login_password = Entry(login_frame, font=("Goudy old style", 15), bg="#E7E6E6", show="*")
        entry_login_password.place(relx=0.43, rely=0.57)

        # Submit Button
        submit = Button(login_frame, text="Login", bd=0, font=("Goudy old style", 15), bg="#6162FF", fg="white", width=15, command=lambda: self.login(entry_login_username, entry_login_password))
        submit.place(relx=0.44, rely=0.7)

    def login(self, entry_login_username, entry_login_password):
        entered_username = entry_login_username.get()
        entered_password = entry_login_password.get()
        bytes_password = entered_password.encode('utf-8')
        hashed_password = hashlib.sha256(bytes_password).hexdigest()
        self.client.send_message(["login", entered_username, hashed_password])
        while self.client.messages == []:
            pass # waiting till the client receives data after his signup request (ping)
        if self.client.messages[1] == "success":
            while self.client.username == "":
                pass
            self.client.messages = []
            self.main_screen()
        else:
            self.top_levels.master.iconify() # keeps the login screen
            if not self.client.messages[2]:
                messagebox.showwarning("Login Failed!", "Could not find username: " +  entered_username)
            else:
                messagebox.showwarning("Login Failed!", "The password does not match")
            self.client.messages = []

    def signup_window(self):
        sign_up_frame = Tk()
        sign_up_frame.attributes('-fullscreen', True)
        sign_up_frame.title("sign up")
        sign_up_frame['background'] = BG_COLOR

        self.top_levels["registration"] = sign_up_frame

        frame_login = Frame(sign_up_frame, bg="white")
        frame_login.place(relx=0.5, rely=0.5, width=1200, height=1000 , anchor="center")

        # Back & Exit Buttons
        back_button = Button(sign_up_frame, text="Back", bd=0, font=("Goudy old style", 15), bg="grey", fg="white", width=8, height=1, command=lambda: self.back(sign_up_frame))
        back_button.place(relx=0.73, rely=0.25)
        exit_button = Button(sign_up_frame, text="Exit", bd=0, font=("Goudy old style", 15), bg="red", fg="white", width=8, height=1, command=lambda: self.exit(sign_up_frame))
        exit_button.place(relx=0.5, rely=0.9, anchor="center")

        # Title & Subtitle
        title_name = Label(sign_up_frame, text="LuminaMentia", font=("Impact", 35, "bold"), fg="black", bg="white")
        title_name.place(relx=0.5, rely=0.1, anchor="center")
        title = Label(sign_up_frame, text="Sign Up", font=("Impact", 25, "bold"), fg="#6162FF", bg="white")
        title.place(relx=0.5, rely=0.2, anchor="center")
        subtitle = Label(sign_up_frame, text="Welcome!", font=("Goudy old style", 15, "bold"), fg="#1d1d1d", bg="white")
        subtitle.place(relx=0.25, rely=0.25)

        # Username
        lbl_user = Label(sign_up_frame, text="Username", font=("Goudy old style", 15, "bold"), fg="grey", bg="white")
        lbl_user.place(relx=0.46, rely=0.45, anchor="center")
        entry_login_username = Entry(sign_up_frame, font=("Goudy old style", 15), bg="#E7E6E6")
        entry_login_username.place(relx=0.43, rely=0.47)

        # Password
        lbl_password = Label(sign_up_frame, text="Password", font=("Goudy old style", 15, "bold"), fg="grey", bg="white")
        lbl_password.place(relx=0.46, rely=0.55, anchor="center")
        entry_login_password = Entry(sign_up_frame, font=("Goudy old style", 15), bg="#E7E6E6", show="*")
        entry_login_password.place(relx=0.43, rely=0.57)

        # Submit Button
        submit = Button(sign_up_frame, text="Sign Up", bd=0, font=("Goudy old style", 15), bg="#6162FF", fg="white", width=15, command=lambda: self.sign_up(entry_login_username, entry_login_password))
        submit.place(relx=0.44, rely=0.7)

    def sign_up(self, entry_signup_username, entry_signup_password):
        entered_username = entry_signup_username.get()
        entered_password = entry_signup_password.get()
        bytes_password = entered_password.encode('utf-8')
        hashed_password = hashlib.sha256(bytes_password).hexdigest()
        self.client.send_message(["signup", entered_username, hashed_password])
        while self.client.messages == []:
            pass # waiting till the client receives data after his signup request (ping)
        if self.client.messages[1] == "success":
            while self.client.username == "":
                pass
            self.client.messages = []
            self.main_screen()
        else:
            self.top_levels.master.iconify() # keeps the login screen
            messagebox.showwarning("Sign Up Failed!", "This username is already exists")
            self.client.messages = []

    def main_screen(self):
        main_frame = Tk()
        main_frame['background'] = BG_COLOR
        main_frame.attributes('-fullscreen', True)
        main_frame.title("LuminaMentia Main")

        self.top_levels["registration"].destroy()
        self.top_levels["first_window"].destroy()

        frame_login = Frame(main_frame, bg="white")
        frame_login.place(relx=0.5, rely=0.5, width=1600, height=1000 , anchor="center")

        # Exit Button
        back_button = Button(main_frame, text="Exit", bd=0, font=("Goudy old style", 15), bg="red", fg="white", width=8, height=1, command=lambda: self.exit(main_frame))
        back_button.place(x=920, y=1000)

        # Title & Username
        title_name = Label(main_frame, text="LuminaMentia", font=("Impact", 35, "bold"), fg="black", bg="white")
        title_name.place(x=820, y=100)
        username = Label(main_frame, text="Hello " + self.client.username, font=("Goudy old style", 15, "bold"), fg="black", bg="white")
        username.place(x=1500, y=120)

        # Disconnect button
        back_button = Button(main_frame, text="Disconnect", bd=0, font=("Ariel", 13), bg="grey", fg="white", width=9, height=0, command=lambda: self.disconnect(main_frame))
        back_button.place(x=1500, y=160)

        # Sorting Numbers Game
        sorting_numbers_button = Button(main_frame, text="Sort Numbers", bd=0, font=("Goudy old style", 15), bg="#6162FF", fg="white", width=15, command=self.sorting_numbers)
        sorting_numbers_button.place(relx=0.5, rely=0.5, anchor="center")

    def sorting_numbers(self):
        sorting_numbers_frame = Tk()
        sorting_numbers_frame['background'] = BG_COLOR
        sorting_numbers_frame.attributes('-fullscreen', True)
        sorting_numbers_frame.title("LuminaMentia Main")

        self.top_levels["game"] = sorting_numbers_frame

        frame_login = Frame(sorting_numbers_frame, bg="white")
        frame_login.place(relx=0.5, rely=0.5, width=1600, height=1000 , anchor="center")

        # Title & Username
        title_name = Label(sorting_numbers_frame, text="LuminaMentia", font=("Impact", 35, "bold"), fg="black", bg="white")
        title_name.place(x=820, y=100)
        username = Label(sorting_numbers_frame, text="Hello " + self.client.username, font=("Goudy old style", 15, "bold"), fg="black", bg="white")
        username.place(x=1500, y=120)

        self.client.send_message(["game", "sorting numbers", "start"])
        while self.client.messages == []:
            pass

        numbers_to_sort = self.client.messages[2]
        task_label = Label(sorting_numbers_frame, text=f"Sort the numbers: {numbers_to_sort}", font=("Ariel", 20, "bold"), fg="black", bg="white")
        task_label.place(relx=0.5, rely=0.35, anchor="center")
        entry_numbers = Entry(sorting_numbers_frame, font=("Goudy old style", 15), bg="#E7E6E6")
        entry_numbers.place(relx=0.5, rely=0.4, anchor="center")

        sort_button = Button(sorting_numbers_frame, text="Check Sorting", command=lambda: self.check_sorting(entry_numbers, sorting_numbers_frame))
        sort_button.place(relx=0.5, rely=0.45, anchor="center")
    
    def check_sorting(self, entry_numbers, sorting_numbers_frame):
        self.client.messages = []
        self.client.send_message(["game", "sorting numbers", "check sorted numbers", entry_numbers.get()])
        while self.client.messages == []:
            pass
        if self.client.messages[2] == "success":
            self.client.messages = []
            self.top_levels["game"].deiconify()
            messagebox.showinfo("Congratulations", "You sorted the numbers correctly!")
        else:
            self.client.messages = []
            self.top_levels["game"].deiconify()
            messagebox.showerror("Incorrect Sorting", "Try again! The numbers are not sorted correctly.")

    def exit(self, window):
        if window.master:
            window.master.destroy()
        else:
            window.destroy()
        self.client.disconnect()

    def back(self, window):
        self.top_levels["registration"] = None
        window.destroy()
        if window.master and isinstance(window.master, Tk):
            window.master.deiconify() # keeps the first screen

    def disconnect(self, window):
        window.destroy()
        self.top_levels.destroy()
        self.top_levels.master.deiconify() # keeps the first screen
        self.top_levels = ""
        self.client.username = ""


if __name__ == '__main__':
    client = MultiThreadedClient('127.0.0.1', 12345)
    client.run()
    app = GUI(client)
    app.run()
