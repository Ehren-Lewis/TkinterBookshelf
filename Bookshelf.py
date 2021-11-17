from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from LinkedList import LinkedList

from ttkthemes import themed_tk as tkk


class Database2:
    database_name = 'test_start.db'

    @staticmethod
    def check_available_tables():
        with sqlite3.connect(Database2.database_name):
            conn = sqlite3.connect(Database2.database_name)
            c = conn.cursor()
            c.execute("""SELECT name FROM sqlite_master where type='table'""")
            conn.commit()
            return c.fetchall()

    @staticmethod
    def create_table(table_name):
        with sqlite3.connect(Database2.database_name) as conn:
            c = conn.cursor()
            c.execute(f"""CREATE TABLE {table_name} (
                        title TEXT NOT NULL,
                        author TEXT NOT NULL)
                        """)
            conn.commit()

    @staticmethod
    def delete_table(table_name):
        with sqlite3.connect(Database2.database_name) as conn:
            c = conn.cursor()
            c.execute(f"""DROP TABLE {table_name}""")
            conn.commit()

    @staticmethod
    def pull_all(table):
        with sqlite3.connect(Database2.database_name) as conn:
            c = conn.cursor()
            query = c.execute(f'SELECT rowid, * FROM {table}')
            conn.commit()
        return query


class BookshelfPage:
    def __init__(self, new_root, table_name):
        self.root = new_root
        self.table_name = table_name

        self.book_title = None
        self.book_test = None
        self.message = None
        self.book_tree = None
        self.scrollbar = None
        self.add_window = None
        self.new_title = None
        self.new_author = None
        self.new_message = None
        self.modify_window = None
        self.old_title = None
        self.author = None
        self.iid = None
        self.new_book_title = None

        self.create_gui()

    def create_gui(self):
        self.create_label_frame()
        self.back_button()
        self.book_buttons()
        self.message_field()
        self.tree_view()
        self.scroll_bar()
        self.view_tree()
        self.create_label_frame()

    def create_label_frame(self):
        self.book_title = LabelFrame(self.root, text='', width=100, height=70, bd=0,
                                     labelanchor='s')
        self.book_title.grid(row=0, column=2)
        self.book_test = Label(self.book_title, text=self.table_name)  # check later, refactor
        self.book_test.grid(row=1, column=1)
        self.book_test.place(x=50, y=35, anchor='center')

    def back_button(self):
        ttk.Button(self.root, text='Back', command=self.on_back_button_pressed,
                   width=5).grid(row=0, column=0, sticky=W)
        # fg=white, bg=red

    def on_back_button_pressed(self):
        self.root.destroy()
        root.deiconify()

    def book_buttons(self):
        ttk.Button(self.root, text="Add", command=self.add_method,
                   width=7).grid(row=4, column=1, pady=15)
        # bg= blue, fg=white
        ttk.Button(self.root, text="Modify", command=self.modify_button_pressed,
                   width=7).grid(row=4, column=2, pady=15)
        # bg=green, fg=white
        ttk.Button(self.root, text='Delete', command=self.on_deleted_clicked,
                   width=7).grid(row=4, column=3, pady=15)
        # bg=red, fg=white

    def message_field(self):
        self.message = Label(self.root, text='')
        self.message.grid(row=6, column=2)

    def tree_view(self):
        self.book_tree = ttk.Treeview(self.root, height=10, columns=("Book Title", "Author"))
        self.book_tree.grid(row=5, column=1, columnspan=3)
        self.book_tree.column("#0", stretch=NO, width=0)
        self.book_tree.column('Book Title', anchor='center')
        self.book_tree.column('Author', anchor='center')
        self.book_tree.heading('Book Title', text='Book Title')
        self.book_tree.heading('Author', text='Author')

    def view_tree(self):
        items = self.book_tree.get_children()
        for item in items:
            self.book_tree.delete(item)

        entries = Database2.pull_all(self.table_name)
        for item in entries:
            self.book_tree.insert('', 0, text='', iid=item[0], values=(item[1], item[2]))

    def scroll_bar(self):
        self.scrollbar = Scrollbar(self.root, orient='vertical', command=self.book_tree.yview)
        self.scrollbar.grid(row=5, column=4, rowspan=10, stick='sn')

    def add_method(self):
        self.add_window = Tk()
        self.add_window.geometry('250x100')
        self.add_window.resizable(width=False, height=False)
        self.add_window.title('Add Book and Author')
        Label(self.add_window, text='Book Title: ').grid(row=0, column=1)
        self.new_title = Entry(self.add_window)
        self.new_title.grid(row=0, column=2, sticky=W)
        Label(self.add_window, text='Author: ').grid(row=1, column=1)
        self.new_author = Entry(self.add_window)
        self.new_author.grid(row=1, column=2, sticky=W)
        self.new_message = Label(self.add_window, text='')
        self.new_message.grid(row=3, column=2, sticky=W)
        Button(self.add_window, text='Submit', command=self.on_add_submit_clicked).grid(row=4, column=2)

        self.add_window.mainloop()

    def on_add_submit_clicked(self):
        if len(self.new_title.get()) > 0 and len(self.new_author.get()) > 0:
            with sqlite3.connect(Database2.database_name) as conn:
                c = conn.cursor()
                c.execute(f"""INSERT INTO {self.table_name} VALUES 
                                    ('{self.new_title.get()}', '{self.new_author.get()}')""")
                conn.commit()

            self.message.config(text=f'{self.new_title.get()} add successfully')
            self.view_tree()
            self.add_window.destroy()
        else:
            self.new_message.config(text='Input proper title and author')

    def delete_method(self):
        self.message['text'] = ""
        title = self.book_tree.item(self.book_tree.selection())['values'][0]
        with sqlite3.connect(Database2.database_name) as conn:
            c = conn.cursor()
            c.execute(f"DELETE FROM {self.table_name} WHERE title = '{title}'")
            conn.commit()

        self.message['text'] = f"{title} deleted"
        self.view_tree()

    def on_deleted_clicked(self):
        self.message['text'] = ''
        try:
            self.book_tree.item(self.book_tree.selection())['values'][0]
        except IndexError:
            self.message['text'] = 'Please select a valid book'
            return

        self.delete_method()

    def open_modify_window(self):
        self.modify_window = Toplevel()
        self.modify_window.title("Modify Book")
        self.modify_window.geometry('200x100')
        self.modify_window.resizable(width=False, height=False)
        self.old_title = self.book_tree.item(self.book_tree.selection())['values'][0]
        self.author = self.book_tree.item(self.book_tree.selection())['values'][1]
        self.iid = self.book_tree.focus()
        Label(self.modify_window, text='Author: ').grid(row=0, column=1)
        Entry(self.modify_window, textvariable=StringVar(self.modify_window, value=self.author),
              state='readonly').grid(row=0, column=2)
        Label(self.modify_window, text='Old Title: ').grid(row=1, column=1)
        Entry(self.modify_window, textvariable=StringVar(self.modify_window, value=self.old_title),
              state='readonly').grid(row=1, column=2)
        Label(self.modify_window, text='New Title: ').grid(row=2, column=1)
        self.new_book_title = Entry(self.modify_window)
        self.new_book_title.grid(row=2, column=2)
        Button(self.modify_window, text='Submit', command=self.on_modify_submit_clicked).grid(row=3, column=2)

    def on_modify_submit_clicked(self):
        with sqlite3.connect(Database2.database_name) as conn:
            c = conn.cursor()
            c.execute(f"""UPDATE {self.table_name}
                                 SET title = '{self.new_book_title.get()}'
                                 WHERE author = '{self.author}'
                                AND title = '{self.old_title}'
                                AND rowid = '{self.iid}'""")
            conn.commit()

        self.message['text'] = f"{self.new_book_title.get()} changed successfully"
        self.view_tree()
        self.modify_window.destroy()

    def modify_button_pressed(self):
        self.message['text'] = ''
        try:
            self.book_tree.item(self.book_tree.selection())['values'][0]
        except IndexError:
            self.message['text'] = 'Please select a book to modify'
            return

        self.open_modify_window()

    @staticmethod
    def ask_quit():
        if messagebox.askokcancel("Notice", "Are you sure to close the application?"):
            root.destroy()


class StartPage:

    def __init__(self, root):
        self.root = root

        self.message_frame = None
        self.top_message = None
        self.row_1_frame = None
        self.row_2_frame = None
        self.row_3_frame = None
        self.row_4_frame = None
        self.list_of_buttons = None
        self.list_of_bookshelves = None
        self.create_window = None
        self.create_window_message = None

        self.present_gui()

    def present_gui(self):
        self.main_frame()
        self.present_bookshelf()

    def main_frame(self):
        self.message_frame = Frame(self.root)
        self.message_frame.pack(pady=25, fill='both')
        self.top_message = Label(self.message_frame, text='Welcome! Created a bookshelf to get started. '
                                                          'Right click to delete a bookshelf')
        self.top_message.pack()
        self.row_1_frame = Frame(self.root)
        self.row_1_frame.pack(expand=True, fill='both')
        self.row_2_frame = Frame(self.root)
        self.row_2_frame.pack(expand=True, fill='both')
        self.row_3_frame = Frame(self.root)
        self.row_3_frame.pack(expand=True, fill='both')
        self.row_4_frame = Frame(self.root)
        self.row_4_frame.pack(expand=True, fill='both')
        self.message_frame.update()

    def present_bookshelf(self):
        table_names = Database2.check_available_tables()
        bookshelf_linked_list = LinkedList()
        button_binder = None
        self.list_of_buttons = []

        for i in table_names:
            bookshelf_linked_list.set_last_node(i[0])
        self.list_of_bookshelves = bookshelf_linked_list.print_list()

        for i in range(len(table_names)):
            if i == 9:
                self.top_message['text'] = "No more bookshelves can be added, please delete one"
                break

            if i // 3 == 0:
                button_binder = ttk.Button(self.row_1_frame, text=f"{self.list_of_bookshelves[i]}", width=15)
                button_binder.pack(side='left', expand=True)
                button_binder['command'] = lambda x=self.list_of_bookshelves[i]: self.open_bookshelf_window(x)
            elif i // 3 == 1:
                button_binder = ttk.Button(self.row_2_frame, text=f"{self.list_of_bookshelves[i]}", width=15)
                button_binder.pack(side='left', expand=True)
                button_binder['command'] = lambda x=self.list_of_bookshelves[i]: self.open_bookshelf_window(x)

            elif i // 3 == 2:
                button_binder = ttk.Button(self.row_3_frame, text=f"{self.list_of_bookshelves[i]}", width=15)
                button_binder.pack(side='left', expand=True)
                button_binder['command'] = lambda x=self.list_of_bookshelves[i]: self.open_bookshelf_window(x)

            self.list_of_buttons.append(button_binder)
            button_binder.bind('<Button-3>', lambda x=button_binder: self.delete_bookshelf_window(x))

        create_button = ttk.Button(self.row_4_frame, text="Create Bookshelf", width=15)
        create_button.pack(side='left', expand=True)
        create_button["command"] = self.create_bookshelf_window
        self.list_of_buttons.append(create_button)

    def create_bookshelf_window(self):
        if len(self.list_of_bookshelves) == 9:
            self.top_message["text"] = 'Please delete a bookshelf'
            return

        self.create_window = Toplevel()
        self.create_window.title = 'Create Bookshelf'
        self.create_window_message = Label(self.create_window)
        self.create_window_message.grid(row=0, column=1)
        Label(self.create_window, text='Name: ').grid(row=1, column=0)
        entry = Entry(self.create_window)
        entry.grid(row=1, column=1)
        top_button = ttk.Button(self.create_window, text='Submit',
                                command=lambda: self.submit(entry.get()))
        top_button.grid(row=2, column=1)

        self.create_window.mainloop()

    def delete_bookshelf_window(self, event):
        bookshelf_name = event.widget.cget('text')
        if messagebox.askyesnocancel("Notice", f"Are you sure you would like to delete {bookshelf_name}?"):
            Database2.delete_table(bookshelf_name)

        self.top_message['text'] = f'{bookshelf_name} deleted successfully'
        for button in self.list_of_buttons:
            button.destroy()

        self.present_bookshelf()

    def submit(self, table_name):
        if table_name == '':
            self.create_window_message['text'] = 'Please input a name'
            return

        table_name = str(table_name)
        if table_name in self.list_of_bookshelves:
            self.create_window_message['text'] = 'Please choose a different table name'
            return

        Database2.create_table(table_name)
        self.create_window.destroy()
        for button in self.list_of_buttons:
            button.destroy()

        self.present_bookshelf()

    @staticmethod
    def open_bookshelf_window(table_name):
        new_root = Toplevel()
        new_root.title(table_name)
        new_root.geometry('500x400')
        new_root.resizable(width=False, height=False)
        BookshelfPage(new_root, table_name)
        new_root.protocol("WM_DELETE_WINDOW", BookshelfPage.ask_quit)
        root.withdraw()
        new_root.mainloop()


if __name__ == "__main__":
    # root = Tk()
    # root.geometry('452x400')
    # root.title("Personal Bookshelf")
    # root.resizable(width=False, height=False)

    root = tkk.ThemedTk()
    root.get_themes()
    root.set_theme('clearlooks')
    root.geometry('452x400')
    root.title('Bookshelf')

    app = StartPage(root)
    root.mainloop()
