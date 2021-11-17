from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from LinkedList import Node, LinkedList

database_name = 'test_start.db'


class Database2:
    # maybe ask where they would like the database to be?
    # perhaps define a __enter__ and a __exit__ method for the class???
    database_name = 'test_start.db'
    """
    Create, Read, Update, Delete
    """

    # good
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
        # Only on start page
        current_tables = Database2.check_available_tables()
        # if table_name in current_tables:
        #     # show in message that this bookshelf name is already taken
        #     # raise an error, and then put that in the start page
        #     pass
        # else:
        with sqlite3.connect(Database2.database_name) as conn:
            c = conn.cursor()
            c.execute(f"""CREATE TABLE {table_name} (
                        title TEXT NOT NULL,
                        author TEXT NOT NULL)
                        """)
            conn.commit()
            # if successful, change message box to show as such, will be in startpage class

    @staticmethod
    def pull_all(table):
        with sqlite3.connect(Database2.database_name) as conn:
            c = conn.cursor()
            query = c.execute(f'SELECT rowid, * FROM {table}')
            conn.commit()
        return query


class Start:
    def __init__(self, root):
        self.root = root
        self.main_frame()
        self.present_bookshelf()

    def main_frame(self):
        self.message_frame = Frame(self.root)
        self.message_frame.pack(pady=25, fill='both')
        self.top_message = Label(self.message_frame, text='test')
        self.top_message.pack()
        self.row_1_frame = Frame(self.root, bg='blue')
        self.row_1_frame.pack(expand=True, fill='both')
        self.row_2_frame = Frame(self.root, bg='red')
        self.row_2_frame.pack(expand=True, fill='both')
        self.row_3_frame = Frame(self.root, bg='green')
        self.row_3_frame.pack(expand=True, fill='both')

    def button_name(self, name):
        self.top_message['text'] = name

    def present_bookshelf(self):
        button_binder = None
        table_names = Database2.check_available_tables()
        table_root = LinkedList()
        for i in table_names:
            table_root.set_last_node(i[0])
        node_list = table_root.node_list()

        for i in range(len(table_names)):
            if i == 9:
                self.top_message['text'] = "No more tables can be added, please delete one"
                break

            if i // 3 == 0:
                button_binder = Button(self.row_1_frame,
                                       command=lambda: self.create_bookshelf_window(node_list[i].get_value()),
                                       text=f"{node_list[i].get_value()}", width=12, height=2)
                button_binder.pack(side='left', expand=True)
            elif i // 3 == 1:
                button_binder = Button(self.row_2_frame,
                                       command=lambda: self.create_bookshelf_window(button_binder.cget('text')),
                                       text=f"{node_list[i].get_value()}", width=12, height=2)
                button_binder.pack(side='left', expand=True)
            elif i // 3 == 2:
                button_binder = Button(self.row_3_frame,
                                       command=lambda: self.create_bookshelf_window(node_list[i].get_value()),
                                       text=f"{node_list[i].get_value()}", width=12, height=2)
                button_binder.pack(side='left', expand=True)
            right_click_menu = Menu(button_binder, tearoff=0)
            right_click_menu.add_command(label='Delete',
                                         command=lambda: self.delete_bookshelf_window(button_binder.cget('text')))
            button_binder.bind('<Button-3>', lambda z: right_click_menu.tk_popup(button_binder.winfo_pointerx(),
                                                                                 button_binder.winfo_pointery()))

            # button_binder.bind('<Button-3>', self.button_name(button_binder.cget('text')))
            print(button_binder.cget('text'))
            print(hex(id(button_binder)))
        print(button_binder.cget('text'))
        #
        # need
        # Button(self.frame, command='', text='Create table', width=15,
        #        height=3).pack(side=

    def delete_bookshelf_window(self, table_name):
        answer = messagebox.askyesnocancel(title=table_name, message=f"Do you wish to delete {1}")
        if answer:
            pass

    def create_bookshelf_window(self, table_name):
        new_root = Toplevel()
        # new_root.title(title)
        new_root.geometry('500x400')
        new_root.resizable(width=False, height=False)
        new_app = BookshelfPage(new_root, table_name)
        new_root.protocol("WM_DELETE_WINDOW", BookshelfPage.ask_quit)
        root.withdraw()
        new_root.mainloop()


class BookshelfPage:
    def __init__(self, new_root, table_name):
        self.root = new_root
        self.table_name = table_name
        self.create_label_frame()
        self.back_button()
        self.book_buttons()
        self.message_field()
        self.tree_view()
        self.scroll_bar()
        self.view_tree()
        self.create_label_frame()
        # self.root.wm_protocol("WM_DELETE_WINDOW", root.destroy)
        # self.root.protocol("WM_DELETE_WINDOW", root.destroy())

    def create_label_frame(self):
        self.book_title = LabelFrame(self.root, text='', width=100, height=70, bd=0,
                                     labelanchor='s')
        self.book_title.grid(row=0, column=2)
        self.book_test = Label(self.book_title, text=self.table_name)
        self.book_test.grid(row=1, column=1)
        self.book_test.place(x=50, y=35, anchor='center')

        # These methods below will be going on a different page

    def back_button(self):
        Button(self.root, text='Back', fg='white', bg='red', command=self.on_back_button_pressed,
               width=5, height=1).grid(row=0, column=0, sticky=W)

    def on_back_button_pressed(self):
        self.root.destroy()
        root.deiconify()

    def book_buttons(self):
        Button(self.root, text="Add", fg='white', bg='blue', command=self.add_method,
               width=5, height=1).grid(row=4, column=1, pady=15)
        Button(self.root, text="Modify", fg='white', bg='green', command=self.modify_button_pressed,
               width=5, height=1).grid(row=4, column=2, pady=15)
        Button(self.root, text='Delete', fg='white', bg='red', command=self.on_deleted_clicked,
               width=5, height=1).grid(row=4, column=3, pady=15)

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
        # Convert basic dict to database, each page has different tables
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
            with sqlite3.connect('Bookshelf.db') as conn:
                c = conn.cursor()
                c.execute(f"""INSERT INTO philosophy VALUES 
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
        with sqlite3.connect('Bookshelf.db') as conn:
            c = conn.cursor()
            c.execute(f"DELETE FROM philosophy WHERE title = '{title}'")
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
        with sqlite3.connect('Bookshelf.db') as conn:
            c = conn.cursor()
            c.execute(f"""UPDATE philosophy
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
            # close the application
            root.destroy()


class TestPage:
    def __init__(self, root, table_name):
        self.root = root
        self.table_name = table_name
        self.main_frame()
        self.present_bookshelf()

    def main_frame(self):
        self.message_frame = Frame(self.root)
        self.message_frame.pack(pady=25, fill='both')
        self.top_message = Label(self.message_frame, text='test')
        self.top_message.pack()
        self.row_1_frame = Frame(self.root, bg='blue')
        self.row_1_frame.pack(expand=True, fill='both')
        self.row_2_frame = Frame(self.root, bg='red')
        self.row_2_frame.pack(expand=True, fill='both')
        self.row_3_frame = Frame(self.root, bg='green')
        self.row_3_frame.pack(expand=True, fill='both')
        self.row_4_frame = Frame(self.root, bg='teal')
        self.row_4_frame.pack(expand=True, fill='both')
        self.message_frame.update()

    def present_bookshelf(self):
        button_binder = None
        create_button = None
        table_names = Database2.check_available_tables()
        table_root = LinkedList()
        for i in table_names:
            table_root.set_last_node(i[0])
        node_list = table_root.node_list()
        self.name_list = table_root.print_list()




        d = {}

        for i in node_list:
            d[i.get_value()] = Button()

        # print(d)
        self.button_list = []
        new_d = {}
        reverse_new_d = {}
        for i in range(len(table_names)):
            if i == 9:
                self.top_message['text'] = "No more tables can be added, please delete one"
                break

            if i // 3 == 0:
                button_binder = Button(self.row_1_frame, text=f"{node_list[i].get_value()}", width=12, height=2)
                button_binder.pack(side='left', expand=True)
                button_binder['command'] = lambda x = node_list[i].get_value(): self.create_bookshelf_window(x)
            elif i // 3 == 1:
                button_binder = Button(self.row_2_frame, text=f"{node_list[i].get_value()}", width=12, height=2)
                button_binder.pack(side='left', expand=True)
                button_binder['command'] = lambda x = node_list[i].get_value(): self.open_bookshelf_window(x)

            elif i // 3 == 2:
                button_binder = Button(self.row_3_frame, text=f"{node_list[i].get_value()}", width=12, height=2)
                button_binder.pack(side='left', expand=True)
                button_binder['command'] = lambda x = node_list[i].get_value(): self.open_bookshelf_window(x)

            new_d[node_list[i].get_value()] = button_binder
            self.button_list.append(button_binder)

            right_click_menu = Menu(button_binder, tearoff=0)
            right_click_menu.add_command(label='Delete',
                                         command=lambda: self.delete_bookshelf_window(button_binder.cget('text')))
            button_binder.bind('<Button-3>', lambda z: right_click_menu.tk_popup(button_binder.winfo_pointerx(),
                                                                                 button_binder.winfo_pointery()))

        create_button = Button(self.row_4_frame, text="Create Bookshelf", width=12, height=2)
        create_button.pack(side='left', expand=True)
        create_button["command"] = self.create_bookshelf_window
    def create_bookshelf_window(self):
        if len(self.name_list) == 9:
            self.top_message["text"] = 'Please delete a bookshelf'
            return
        self.create_window = Toplevel()
        self.create_window.title = 'Create Bookshelf'
        self.create_message = Label(self.create_window)
        self.create_message.grid(row=0, column=1)
        self.top_label = Label(self.create_window, text='Name: ').grid(row=1, column=0)
        self.entry = Entry(self.create_window)
        self.entry.grid(row=1, column=1)
        self.top_button = Button(self.create_window, text='Submit', anchor='center',
                                 command=lambda: self.submit(self.entry.get()))
        self.top_button.grid(row=2, column=1)

        self.create_window.mainloop()

    def submit(self, table_name):
        print(self.name_list)
        table_name = str(table_name)
        if table_name in self.name_list:
            self.create_message['text'] = 'Please choose a different table name'
            return
        Database2.create_table(table_name)
        self.create_window.destroy()
        for button in self.button_list:
            button.destroy()
        self.present_bookshelf()

    def open_bookshelf_window(self, table_name):
        new_root = Toplevel()
        print(table_name)
        new_root.title(table_name)
        new_root.geometry('500x400')
        new_root.resizable(width=False, height=False)
        new_app = BookshelfPage(new_root, table_name)
        new_root.protocol("WM_DELETE_WINDOW", BookshelfPage.ask_quit)
        root.withdraw()
        new_root.mainloop()

if __name__ == "__main__":
    root = Tk()
    root.geometry('452x500')
    root.title("Personal Bookshelf")
    root.resizable(width=False, height=False)
    # app = Start(root)
    app = TestPage(root, 'test')
    root.mainloop()


def present_bookshelf(self):
    column = 0
    row = 0
    exec = Database2.check_available_tables()
    for i in range(len(exec)):

        if i == 8:
            self.label['text'] = "No more tables can be added, please delete one"
            break

        row = i // 3 + 1
        column += 1
        Button(self.buttonlabel, command='lambda :', text=f"{exec[i][0]}", width=15,
               height=4).grid(row=row, column=column, padx=15, pady=15)
        if column / 3 == 1:
            column = 0
    if len(exec) % 3 == 0:
        row += 1

    Button(self.buttonlabel, command='', text='Create table', width=15,
           height=4).grid(row=row, column=column + 1, padx=15, pady=15)


"""
class Node:
    def __init__(self, value):
        self.value = Node(value)
        self.next_node = None
    
    def get_value(self):
        return self.value
    
    def get_next_node(self):
        return self.next_node
    
    def set_next_node(self, node):
        self.next_node = node

class LinkedList:
    def __init__(self):
        self.head = None
    
    def set_head_node(self, value):
        new_head = Node(value)
        current_head = self.head
    
        self.head = new_head
        if current_head is not None:
            self.head.set_next_node(current_head)
    
    def insert_next_node(self):
"""

table_names = Database2.check_available_tables()
table_root = LinkedList()
