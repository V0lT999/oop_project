"""Library project"""
from tkinter import *
from tkinter import scrolledtext, messagebox
from tkinter.ttk import Combobox, Treeview
from fpdf import FPDF
from PIL import Image, ImageTk
import xlrd, xlwt
import xml.etree.ElementTree as ET
from lxml import html, etree
import logging
import unittest
import threading
import unittest
import jinja2

class Unittestclass(unittest.TestCase):
    def test_def(self):
        self.assertEqual(5 + 5, 10)


class Library(Frame):
    """Library class"""
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

        self.Info_img = ImageTk.PhotoImage(Image.open("../resources/info.ico").resize((40, 40)))
        infoButton = Button(toolbar, image=self.Info_img, relief=FLAT, command=self.get_info)
        infoButton.pack(side=LEFT, padx=6, pady=1)

        self.Exit_img = ImageTk.PhotoImage(Image.open("../resources/exit_ico.png").resize((40, 40)))
        exitButton = Button(toolbar, image=self.Exit_img, relief=FLAT, command=self.exit)
        exitButton.pack(side=LEFT, padx=7, pady=1)

        self.searchLabel = Entry(toolbar_bot, width=20)
        self.searchLabel.pack(side=LEFT, padx=5, pady=1)

        searchButton = Button(toolbar_bot, text="Search", command=self.search_Clicked)
        searchButton.pack(side=LEFT, padx=9, pady=1)

        toolbar.pack(side=TOP, fill=X)
        toolbar_bot.pack(side=BOTTOM, fill=X)

        self.books_values = []
        self.table_read()

        autorCombo = Combobox(toolbar_bot)
        autorCombo['values'] = tuple(self.books_values)
        autorCombo.pack(side=LEFT, padx=1, pady=1)

        self.pack()

    def table_read(self):
        """books info reading function"""
        self.table = Treeview(self)

        rb = xlrd.open_workbook('../resources/books.xls', formatting_info=False)
        sheet = rb.sheet_by_index(0)

        self.table.grid(columnspan=sheet.ncols)

        self.table["columns"] = sheet.row_values(0)
        self.table["show"] = "headings"
        for cols in range(sheet.ncols):
            self.table.heading(sheet.row_values(0)[cols], text=sheet.row_values(0)[cols])

        index = iid = 0
        for i in range(1, sheet.nrows):
            self.table.insert('', index, iid, values=sheet.row_values(i))
            self.books_values.append(sheet.row_values(i)[2])
            index = iid = index + 1

    def exit(self):
        """exit function"""
        self.quit()

    def get_info(self):
        def close_window():
            info_window.destroy()

        info_file = open("../resources/report.txt", 'r')
        txt = info_file.read()
        count_readers = txt[0]
        count_new_readers = txt[2]
        count_books = txt[4]
        info_file.close()

        info_window = Toplevel(self)
        info_window.title("Info")
        count_readers_lbl = Label(info_window, text="Количество читателей: ")
        count_readers_lbl.grid(column=0, row=0)
        count_readers_lbl_c = Label(info_window, text=count_readers)
        count_readers_lbl_c.grid(column=2, row=0)
        count_new_readers_lbl = Label(info_window, text="Количество новых читателей: ")
        count_new_readers_lbl.grid(column=0, row=1)
        count_new_readers_lbl_c = Label(info_window, text=count_new_readers)
        count_new_readers_lbl_c.grid(column=2, row=1)
        count_books_lbl = Label(info_window, text="Количество взятых книг: ")
        count_books_lbl.grid(column=0, row=2)
        count_books_lbl_c = Label(info_window, text=count_books)
        count_books_lbl_c.grid(column=2, row=2)
        button = Button(info_window, text="OK", command=close_window)
        button.grid(column=0, row=4)

    def change_info(self, argument, count):
        info_file = open("../resources/report.txt", 'r')
        txt = info_file.read()
        info_mas = []
        info_mas.append(txt[0]) #count_readers
        info_mas.append(txt[2]) #count_new_readers
        info_mas.append(txt[4]) #count_new_books
        info_mas[argument] = int(info_mas[argument]) + count
        info_file.close()
        info_file = open("../resources/report.txt", 'w')
        info_file.write(info_mas[0] + '\n' + info_mas[1] + '\n' + info_mas[2] + '\0')
        info_file.close()


    def new_func(self):
        """Adding of reader function"""
        def add_reader():
            n = self.table["height"]
            new_book = []
            new_book.append(n + 1)
            new_book.append(name_txt.get())
            new_book.append(autor_book_field.get())
            new_book.append('есть')
            self.table["height"] = n + 1
            self.table.insert('', n + 1, n + 1, values=new_book)
            res = messagebox.showinfo('Добавление книги', 'Успешно')
            new_book_window.destroy()

        new_book_window = Toplevel(self)
        new_book_window.title("New_book")
        name_book_lbl = Label(new_book_window, text="Введите название книги")
        name_book_lbl.grid(column=0, row=0)
        name_txt = Entry(new_book_window, width=20)
        name_txt.grid(column=1, row=0)
        autor_book_lbl = Label(new_book_window, text="Введите автора")
        autor_book_lbl.grid(column=0, row=1)
        autor_book_field = Entry(new_book_window, width=20)
        autor_book_field.grid(column=1, row=1)
        button = Button(new_book_window, text="OK", command=add_reader)
        button.grid(column=0, row=2)

    def print_func(self):
        """printing function"""
        unittest.main()

    def save_func(self):
        """saving data function"""
        txt = ""
        rw = xlwt.Workbook('../resources/books_write.xls')
        sheet = rw.add_sheet('Sheet1', cell_overwrite_ok=True)
        for i in range(4):
            sheet.write(0, i, self.table.heading(i)["text"])
        for i in range(self.table["height"]):
            value = ""
            for j in range(4):
                #print(self.table.item(i)["values"][j])
                value = value + self.table.item(i)["values"][j] + ' '
                sheet.write(i + 1, j, self.table.item(i)["values"][j])
            txt = txt + value + '\n'
        rw.save('../resources/books_write.xls')

        txt = "some string for pdf"
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', size=12)
        pdf.cell(200, 10, txt=txt)
        pdf.output('../resources/report.pdf')

        html_template = """
        <html>
        <head>
        <title>Отчет номер: {current_date}</title>
        </head>
        <body>
        <table border="1">
        <tr>
        <td>Имя</td>
        <td>Результат</td>
        </tr>
        <tr>
        <td>{arg_w_name}</td>
        <td>{arg_w_res}</td>
        </tr>
        </table>
        </body>
        </html>
        """
        html_file = open("../resources/report_html.html", 'w')
        html_file.write(html_template.format(current_date="2015-03-31", arg_w_name="Vladimir Toropov", arg_w_res="report"))
        mb = messagebox.showinfo('Success', 'Успешно сохранено')


    def delete_book_func(self):
        """removal book function"""
        try:
            a = self.table.selection()
            res = messagebox.askquestion('Deleting', 'Вы хотите удалить книгу?')
            if res:
                self.table.delete(a)
                self.table['height'] = self.table['height'] - 1
        except:
            mb = messagebox.showerror("ERROR", "ошибка при удалении")


    def search_Clicked(self):
        """search function"""
        for i in range(self.table["height"]):
            self.table.selection_remove(i)
        search = self.searchLabel.get()
        for i in range(self.table["height"]):
            if search in self.table.item(i)["values"][1]:
                self.table.selection_add(i)

    def read_readers(self):
        readers_window = Toplevel(self)
        readers_window.title("Readers")
        readers_window.iconbitmap("../resources/readers_table_ico.ico")
        readers_window.geometry("800x400")

        readers_app = Readers(readers_window, self.table)

        self.update()


class Readers(Frame):
    """Readers class"""
    def __init__(self, parent, table):
        Frame.__init__(self, parent)
        self.parent = parent
        self.table = table
        self.initUI()

    def initUI(self):
        toolbar = Frame(self.parent, bd=1, relief=RAISED)
        toolbar_bot_readers = Frame(self.parent, bd=1, relief=RAISED)

        self.New_img = ImageTk.PhotoImage(Image.open('../resources/new_ico.png').resize((40, 40)))
        newButton = Button(toolbar, image=self.New_img, relief=FLAT, command=self.new_reader_func)
        newButton.pack(side=LEFT, padx=1, pady=1)

        self.New_book_img = ImageTk.PhotoImage(Image.open('../resources/library_ico.png').resize((40, 40)))
        newbookButton = Button(toolbar, image=self.New_book_img, relief=FLAT, command=self.add_book_reader)
        newbookButton.pack(side=LEFT, padx=1, pady=1)

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

        t1 = threading.Event()
        t2 = threading.Event()

        self.first_thread = threading.Thread(target=self.threads_word, args=(t1, t2))
        self.second_thread = threading.Thread(target=self.threads_word, args=(t2, t1))

        self.first_thread.start()
        self.second_thread.start()

        t1.set()

        self.first_thread.join()
        self.second_thread.join()

        self.list_readers()

        self.pack()

    def change_info(self, argument, count):
        info_file = open("../resources/report.txt", 'r')
        txt = info_file.read()
        info_mas = []
        info_mas.append(txt[0]) #count_readers
        info_mas.append(txt[2]) #count_new_readers
        info_mas.append(txt[4]) #count_new_books
        info_mas[argument] = str(int(info_mas[argument]) + count)
        info_file.close()
        info_file = open("../resources/report.txt", 'w')
        info_file.write(info_mas[0] + '\n' + info_mas[1] + '\n' + info_mas[2] + '\0')
        info_file.close()

    def threads_word(self, wait_thread, set_thread):
        wait_thread.wait()
        wait_thread.clear()
        txt_file = open('../resources/threads.txt', 'a')
        txt_file.write("Поток")
        txt_file.close()
        set_thread.set()

    def add_book_reader(self):
        def write_book_reader():
            current_name = self.readers.get()
            current_reader = self.root[0]
            for i in self.root:
                if i.attrib['name'] == current_name:
                    current_reader = i
                    break

            current_book = books.get()
            current_book_table = self.table.item(0)
            for i in range(self.table['height']):
                if current_book == self.table.item(i)['values'][1]:
                    self.table.set(i, column=3, value='нет')
                    current_book_table = self.table.item(i)

            # for i in range(self.table['height']):
            #     print(self.table.item(i))

            book = ET.SubElement(current_reader, 'book')
            book.set('code', current_book_table['values'][0])
            book_title = ET.SubElement(book, 'title')
            book_title.text = current_book_table['values'][1]
            book_autor = ET.SubElement(book, 'autor')
            book_autor.text = current_book_table['values'][2]

            rw = xlwt.Workbook('../resources/books.xls')
            sheet = rw.add_sheet('Sheet1', cell_overwrite_ok=True)
            for i in range(4):
                sheet.write(0, i, self.table.heading(i)["text"])
            for i in range(self.table["height"]):
                for j in range(4):
                    sheet.write(i + 1, j, self.table.item(i)["values"][j])
            rw.save('../resources/books.xls')

            new_xml = ET.tostring(self.root, 'UTF-8')
            xml_file = open("../resources/readers.xml", 'wb')
            xml_file.write(new_xml)
            xml_file.close()

            success_window = Toplevel(nb)
            success_window.title("Success")
            lbl_i = Label(success_window, text="Книга успешно добавлена")
            lbl_i.grid(column=0, row=0)
            button_i = Button(success_window, text="OK", command=close_nb_window)
            button_i.grid(column=0, row=3)

            self.change_info(2, 1)
            self.list_readers()

        def close_nb_window():
            nb.destroy()

        nb = Toplevel(self)
        books = Combobox(nb, state='readonly')
        elements = []
        for i in range(self.table["height"]):
            if self.table.item(i)['values'][3] == "есть":
                current = self.table.item(i)['values']
                elements.append(current[1])
        books["values"] = tuple(elements)
        books.current(0)
        books['width'] = 40
        lbl = Label(nb, text="Выберите книгу")
        lbl.grid(column=0, row=0)
        books.grid(column=1, row=0)
        button = Button(nb, text="Добавить", command=write_book_reader)
        button.grid(column=1, row=1)

    def list_readers(self):
        try:
            logging.basicConfig(filename='test_debug.log', level=logging.DEBUG)
            """reading readers function"""
            tree = ET.parse("../resources/readers.xml")
            self.root = tree.getroot()
            self.readers = Combobox(self, state='readonly')
            elements = []
            logging.debug("Файл открыт, combobox создан")

            for reader in self.root:
                elements.append(reader.attrib['name'])

            logging.debug("Прочитаны элементы списка читатели")

            self.readers['values'] = tuple(elements)
            self.readers.current(0)
            self.readers.grid(column=0, row=0)

            button = Button(self, text="Показать книги читателя", command=self.books_of_reader)
            button.grid(column=0, row=1)

            self.books = scrolledtext.ScrolledText(self, width=40, height=10)
            self.books.grid(column=0, row=5)

            logging.debug("Читатели заполнены")

            self.books_of_reader()
        except:
            mb = messagebox.showerror("ERROR", "ошибка при удалении")

    def books_of_reader(self):
        logging.basicConfig(filename='../resources/test_warning.log', level=logging.WARNING)
        self.books.delete(1.0, END)
        text = ""
        current = self.root[0]
        current_name = self.readers.get()

        logging.warning("начало списка мб пустым")

        for i in self.root:
            if i.attrib['name'] == current_name:
                current = i
                break
        for book in current:
            text = text + book.attrib['code'] + ' ' + book[0].text + ' ' + book[1].text + '\n'
        self.books.insert(INSERT, text)

        logging.warning("список может быть пустым")

    def new_reader_func(self):
        """Adding a reader function"""
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

            self.change_info(0, 1)
            self.change_info(1, 1)
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
        """Removal reader function"""
        try:
            current_name = self.readers.get()
            current = self.root[0]
            for i in self.root:
                if i.attrib['name'] == current_name:
                    current = i
                    break
            self.root.remove(current)
            self.change_info(0, -1)
            new_xml = ET.tostring(self.root, 'UTF-8')
            xml_file = open("../resources/readers.xml", 'wb')
            xml_file.write(new_xml)
            xml_file.close()
        except:
            mb = messagebox.showerror("ERROR", "ошибка при удалении")

        self.list_readers()

    def delete_book_reader_func(self):
        """Removal book of reader function"""
        try:
            def delete_book():
                current_book_name = books.get()
                current_book = current[0]
                for i in current:
                    if i[0].text in current_book_name:
                        current_book = i
                        break
                current.remove(current_book)

                for i in range(self.table['height']):
                    if self.table.item(i)['values'][1] in current_book_name:
                        self.table.set(i, column=3, value='есть')

                rw = xlwt.Workbook('../resources/books.xls')
                sheet = rw.add_sheet('Sheet1', cell_overwrite_ok=True)
                for i in range(4):
                    sheet.write(0, i, self.table.heading(i)["text"])
                for i in range(self.table["height"]):
                    for j in range(4):
                        sheet.write(i + 1, j, self.table.item(i)["values"][j])
                rw.save('../resources/books.xls')

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
        except:
            mb = messagebox.showerror("ERROR", "Ошибка при удалении")

def main():
    """Main function"""
    window = Tk()
    window.title("library")
    window.iconbitmap('../resources/library_ico.ico')
    window.geometry("800x400")
    app = Library(window)
    window.mainloop()


if __name__ == "__main__":
    main()