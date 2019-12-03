from tkinter import *
from tkinter.ttk import Combobox
from PIL import Image, ImageTk


class Library(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):

        toolbar = Frame(self.parent, bd=1, relief=RAISED)
        toolbar_bot = Frame(self.parent, bd=1, relief=RAISED)

        self.New_img = ImageTk.PhotoImage(Image.open("../resources/new_ico.png").resize((40, 40)))
        newButton = Button(toolbar, image=self.New_img, relief=FLAT, command=self.new_func)
        newButton.pack(side=LEFT, padx=1, pady=1)

        self.Save_img = ImageTk.PhotoImage(Image.open("../resources/save_ico.png").resize((40, 40)))
        saveButton = Button(toolbar, image=self.Save_img, relief=FLAT, command=self.save_func)
        saveButton.pack(side=LEFT, padx=2, pady=1)

        self.Print_img = ImageTk.PhotoImage(Image.open("../resources/print_ico.png").resize((40, 40)))
        printButton = Button(toolbar, image=self.Print_img, relief=FLAT, command=self.print_func)
        printButton.pack(side=LEFT, padx=3, pady=1)

        self.Exit_img = ImageTk.PhotoImage(Image.open("../resources/exit_ico.png").resize((40, 40)))
        exitButton = Button(toolbar, image=self.Exit_img, relief=FLAT, command=self.exit)
        exitButton.pack(side=LEFT, padx=4, pady=1)

        autorCombo = Combobox(toolbar_bot)
        autorCombo['values'] = (1, 2, 3)
        autorCombo.pack(side=LEFT, padx=1, pady=1)

        self.searchLabel = Entry(toolbar_bot, width=20)
        self.searchLabel.pack(side=LEFT, padx=5, pady=1)

        searchButton = Button(toolbar_bot, text="Search", command=self.search_Clicked)
        searchButton.pack(side=LEFT, padx=9, pady=1)

        toolbar.pack(side=TOP, fill=X)
        toolbar_bot.pack(side=BOTTOM, fill=X)
        self.pack()

    def exit(self):
        self.quit()

    def new_func(self):
        print("new")

    def print_func(self):
        print("print")

    def save_func(self):
        print("save")

    def search_Clicked(self):
        print(self.searchLabel.get())

def main():
    window = Tk()
    window.title("library")
    window.iconbitmap('../resources/library_ico.ico')
    window.geometry("400x400")
    app = Library(window)
    window.mainloop()


if __name__ == "__main__":
    main()