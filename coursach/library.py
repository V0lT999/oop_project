from tkinter import *
from tkinter import scrolledtext
from tkinter.ttk import Combobox, Treeview
from PIL import Image, ImageTk
import xlrd
import xml.etree.ElementTree as ET


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

        self.Readers_table_img = ImageTk.PhotoImage(Image.open("../resources/readers_table_ico.ico").resize((40, 40)))
        readertableButton = Button(toolbar, image=self.Readers_table_img, relief=FLAT, command=self.read_readers)
        readertableButton.pack(side=LEFT, padx=3, pady=1)

        self.Print_img = ImageTk.PhotoImage(Image.open("../resources/print_ico.png").resize((40, 40)))
        printButton = Button(toolbar, image=self.Print_img, relief=FLAT, command=self.print_func)
        printButton.pack(side=LEFT, padx=4, pady=1)

        self.Delete_img = ImageTk.PhotoImage(Image.open("../resources/delete_book_ico.ico").resize((40, 40)))
        deleteButton = Button(toolbar, image=self.Delete_img, relief=FLAT, command=self.delete_book_func)
        deleteButton.pack(side=LEFT, padx=5, pady=1)

        self.Exit_img = ImageTk.PhotoImage(Image.open("../resources/exit_ico.png").resize((40, 40)))
        exitButton = Button(toolbar, image=self.Exit_img, relief=FLAT, command=self.exit)
        exitButton.pack(side=LEFT, padx=6, pady=1)

        autorCombo = Combobox(toolbar_bot)
        autorCombo['values'] = (1, 2, 3)
        autorCombo.pack(side=LEFT, padx=1, pady=1)

        self.searchLabel = Entry(toolbar_bot, width=20)
        self.searchLabel.pack(side=LEFT, padx=5, pady=1)

        searchButton = Button(toolbar_bot, text="Search", command=self.search_Clicked)
        searchButton.pack(side=LEFT, padx=9, pady=1)

        toolbar.pack(side=TOP, fill=X)
        toolbar_bot.pack(side=BOTTOM, fill=X)

        self.table_read()

        self.pack()

    def table_read(self):
        table = Treeview(self)

        rb = xlrd.open_workbook('../resources/books.xls', formatting_info=False)
        sheet = rb.sheet_by_index(0)

        table.grid(columnspan=sheet.ncols)

        table["columns"] = sheet.row_values(0)
        table["show"] = "headings"
        for cols in range(sheet.ncols):
            table.heading(sheet.row_values(0)[cols], text=sheet.row_values(0)[cols])

        index = iid = 0
        for i in range(1, sheet.nrows):
            table.insert('', index, iid, values=sheet.row_values(i))
            index = iid = index + 1


    def exit(self):
        self.quit()

    def new_func(self):
        print("new")

    def print_func(self):
        print("print")

    def save_func(self):
        print("save")

    def delete_book_func(self):
        print('delete')

    def search_Clicked(self):
        print(self.searchLabel.get())

    def read_readers(self):
        readers_window = Toplevel(self)
        readers_window.title("Readers")
        readers_window.iconbitmap("../resources/readers_table_ico.ico")
        readers_window.geometry("800x400")

        readers_app = Readers(readers_window)


class Readers(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        toolbar = Frame(self.parent, bd=1, relief=RAISED)
        toolbar_bot_readers = Frame(self.parent, bd=1, relief=RAISED)

        self.New_img = ImageTk.PhotoImage(Image.open('../resources/new_ico.png').resize((40, 40)))
        newButton = Button(toolbar, image=self.New_img, relief=FLAT, command=self.new_reader_func)
        newButton.pack(side=LEFT, padx=1, pady=1)

        self.Print_img = ImageTk.PhotoImage(Image.open("../resources/print_ico.png").resize((40, 40)))
        printButton = Button(toolbar, image=self.Print_img, relief=FLAT, command=self.print_reader_func)
        printButton.pack(side=LEFT, padx=2, pady=1)

        self.Delete_img = ImageTk.PhotoImage(Image.open("../resources/delete_reader_ico.ico").resize((40, 40)))
        deleteButton = Button(toolbar, image=self.Delete_img, relief=FLAT, command=self.delete_reader_func)
        deleteButton.pack(side=LEFT, padx=3, pady=1)

        self.Delete_book_img = ImageTk.PhotoImage(Image.open("../resources/delete_book_ico.ico").resize((40, 40)))
        deletebookButton = Button(toolbar, image=self.Delete_book_img, relief=FLAT, command=self.delete_book_reader_func)
        deletebookButton.pack(side=LEFT, padx=4, pady=1)

        toolbar.pack(side=TOP, fill=X)

        self.list_readers()

        self.pack()

    def list_readers(self):

        tree = ET.parse("../resources/readers.xml")
        self.root = tree.getroot()

        self.readers = Combobox(self, state='readonly')
        elements = []

        for reader in self.root:
            elements.append(reader.attrib['name'])

        self.readers['values'] = tuple(elements)
        self.readers.current(0)
        self.readers.grid(column=0, row=0)

        books = scrolledtext.ScrolledText(self, width=40, height=10)
        books.grid(column=0, row=5)

        text = ""
        current = self.root[0]
        current_name = self.readers.get()
        for i in self.root:
            if i.attrib['name'] == current_name:
                current = i
                break
        for book in current:
            text = book.attrib['code'] + ' ' + book[0].text + ' ' + book[1].text + '\n'
        books.insert(INSERT, text)


    def new_reader_func(self):
        def clicked():
            name = fio_txt.get()
            reader = ET.SubElement(self.root, 'reader')
            reader.set('name', name)

            new_xml = ET.tostring(self.root, 'UTF-8')
            xml_file = open("../resources/readers.xml", 'wb')
            xml_file.write(new_xml)
            xml_file.close()

            success_window = Toplevel(new_reader_window)
            success_window.title("Success")
            lbl = Label(success_window, text="Читатель успешно добавлен")
            lbl.grid(column=0, row=0)
            button = Button(success_window, text="OK", command=close_reader_window)
            button.grid(column=0, row=3)

            self.list_readers()

        def close_reader_window():
            new_reader_window.destroy()

        new_reader_window = Toplevel(self)
        new_reader_window.title("New_reader")
        name_reader_lbl = Label(new_reader_window, text="Введите ФИО читателя")
        name_reader_lbl.grid(column=0, row=0)
        fio_txt = Entry(new_reader_window, width=20)
        fio_txt.grid(column=1, row=0)
        ok_button = Button(new_reader_window, text='OK', command=clicked)
        ok_button.grid(column=2, row=0)

    def print_reader_func(self):
        print('print readers')

    def delete_reader_func(self):
        current_name = self.readers.get()
        current = self.root[0]
        for i in self.root:
            if i.attrib['name'] == current_name:
                current = i
                break
        self.root.remove(current)

        new_xml = ET.tostring(self.root, 'UTF-8')
        xml_file = open("../resources/readers.xml", 'wb')
        xml_file.write(new_xml)
        xml_file.close()

        self.list_readers()

    def delete_book_reader_func(self):

        def delete_book():
            current_book_name = books.get()
            current_book = current[0]
            for i in current:
                if i[0].text == current_book_name:
                    current_book = i
                    break
            current.remove(current_book)

            new_xml = ET.tostring(self.root, 'UTF-8')
            xml_file = open("../resources/readers.xml", 'wb')
            xml_file.write(new_xml)
            xml_file.close()

            success_window = Toplevel(books_reader_window)
            success_window.title("Success")
            lbl = Label(success_window, text="Книга успешно списана")
            lbl.grid(column=0, row=0)
            button = Button(success_window, text="OK", command=close_reader_window)
            button.grid(column=0, row=3)

            self.list_readers()

        def close_reader_window():
            books_reader_window.destroy()

        books_reader_window = Toplevel(self)
        books_reader_window.title('Reader\'s books')

        books = Combobox(books_reader_window, state='readonly')
        current = self.root[0]
        current_name = self.readers.get()
        for i in self.root:
            if i.attrib['name'] == current_name:
                current = i
                break
        elements = []
        for book in current:
            elements.append(book.attrib['code'] + ' ' + book[0].text + ' ' + book[1].text + '\n')

        lbl = Label(books_reader_window, text="Выберите книгу для списания")
        lbl.grid(column=0, row=0)

        books['values'] = tuple(elements)
        books.current(0)
        books.grid(column=0, row=2)

        DeleteButton = Button(books_reader_window, text="Списать", command=delete_book)
        DeleteButton.grid(column=0, row=5)




def main():
    window = Tk()
    window.title("library")
    window.iconbitmap('../resources/library_ico.ico')
    window.geometry("800x400")
    app = Library(window)
    window.mainloop()


if __name__ == "__main__":
    main()