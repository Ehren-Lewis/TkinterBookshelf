from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox



"""
Version 1.0
This is a bookshelf application
The user will have the option to choose between philosophy, business, and political books as of now
The user can add, modify, and delete books as they please. 

for version 2.0:
Make the code concise. Do all queries and data display through the database class
The goal is to make it to where the user can add as many bookshelves as they like
This will like result in one single class that will inherit the name based on a title of the icon
on the first page.
most important functions: create table, add bookshelf, for loop, only 3 icons per line on start page
a plus button for new bookshelves, where to define each individual widget 

more features for 2.1:
The database will be completely empty on first loadup
use a for loop to display each available table if there are any to
1st goal, replace all code with code that is scalable {tables} functions really
2nd goal, revamp home page to allow user tailored experience

maybe make it to where individuals can delete an entire table if they choose to.

to add:
button with modify and delete, as well as a limit of 9 table or perhaps a bigger frame
"""


class Database:
    database = 'Bookshelf.db'

    @staticmethod
    def check_available_tables():
        conn = sqlite3.connect('Bookshelf.db')
        c = conn.cursor()
        c.execute("""SELECT name FROM sqlite_master where type='table'""")
        print(c.fetchall())
        conn.commit()
        conn.close()

    @staticmethod
    def pull_all(table):
        with sqlite3.connect('Bookshelf.db') as conn:
            c = conn.cursor()
            query = c.execute(f'SELECT rowid, * FROM {table}')
            conn.commit()
        return query

    """
    For later iterations, have all queries (add, modify, delete) run through database class
    
    add table method(table_name):
        if table name in database, message and return
    """


class StartPage:
    def __init__(self, base_root):
        self.root = base_root
        self.main_page()

    def main_page(self):
        self.main_window = LabelFrame(self.root, bg='blue').grid(row=0, column=1)
        self.label = Label(self.main_window, text='Personal Bookshelf', height=5).grid(row=0, column=3, columnspan=2)
        Button(self.label, text='Philosophy', command=self.philosophy_button_pressed,
               width=15, height=4).grid(row=1, column=1, padx=25, pady=25)
        Button(self.label, text='Politics', command=self.politics_button_pressed,
               width=15, height=4).grid(row=1, column=3, padx=25, pady=25)
        Button(self.label, text='Business', command=self.business_button_pressed,
               width=15, height=4).grid(row=1, column=5, padx=25, pady=25)

    @staticmethod
    def philosophy_button_pressed():
        new_root = Toplevel()
        new_root.title('Philosophy Books')
        new_root.geometry('500x400')
        new_root.resizable(width=False, height=False)
        PhilosophyPage(new_root)
        new_root.protocol("WM_DELETE_WINDOW", PhilosophyPage.ask_quit)
        root.withdraw()
        new_root.mainloop()

    @staticmethod
    def politics_button_pressed():
        new_root = Toplevel()
        new_root.title('Political Books')
        new_root.geometry('500x400')
        new_root.resizable(width=False, height=False)
        PoliticsPage(new_root)
        new_root.protocol("WM_DELETE_WINDOW", PoliticsPage.ask_quit)
        root.withdraw()
        new_root.mainloop()

    @staticmethod
    def business_button_pressed():
        new_root = Toplevel()
        new_root.title('Political Books')
        new_root.geometry('500x400')
        new_root.resizable(width=False, height=False)
        BusinessPage(new_root)
        new_root.protocol("WM_DELETE_WINDOW", BusinessPage.ask_quit)
        root.withdraw()
        new_root.mainloop()


class PhilosophyPage:
    def __init__(self, root):
        self.root = root
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
        self.book_test = Label(self.book_title, text='Philosophy')
        self.book_test.grid(row=1, column=1)
        self.book_test.place(x=50, y=35, anchor='center')

    # These methods below will be going on a different page

    def back_button(self):
        Button(self.root, text='Back', fg='white', bg='red', command=self.on_back_button_pressed,
               width=5, height=1).grid(row=0, column=0, sticky=W)

    def on_back_button_pressed(self):
        self.root.destroy()
        root.deiconify()

    @staticmethod
    def ask_quit():
        if messagebox.askokcancel("Notice", "Are you sure to close the application?"):
            # close the application
            root.destroy()

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
        entries = Database.pull_all('philosophy')
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


class PoliticsPage:
    def __init__(self, root):
        self.root = root
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
        self.book_test = Label(self.book_title, text='Political')
        self.book_test.grid(row=1, column=1)
        self.book_test.place(x=50, y=35, anchor='center')

    # These methods below will be going on a different page

    def back_button(self):
        Button(self.root, text='Back', fg='white', bg='red', command=self.on_back_button_pressed,
               width=5, height=1).grid(row=0, column=0, sticky=W)

    def on_back_button_pressed(self):
        self.root.destroy()
        root.deiconify()

    @staticmethod
    def ask_quit():
        if messagebox.askokcancel("Notice", "Are you sure to close the application?"):
            # close the application
            root.destroy()

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
        entries = Database.pull_all('politics')
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
                c.execute(f"""INSERT INTO politics VALUES 
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
            c.execute(f"DELETE FROM politics WHERE title = '{title}'")
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
            c.execute(f"""UPDATE politics
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


class BusinessPage:
    def __init__(self, root):
        self.root = root
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
        self.book_test = Label(self.book_title, text='Business')
        self.book_test.grid(row=1, column=1)
        self.book_test.place(x=50, y=35, anchor='center')

    # These methods below will be going on a different page

    def back_button(self):
        Button(self.root, text='Back', fg='white', bg='red', command=self.on_back_button_pressed,
               width=5, height=1).grid(row=0, column=0, sticky=W)

    def on_back_button_pressed(self):
        self.root.destroy()
        root.deiconify()

    @staticmethod
    def ask_quit():
        if messagebox.askokcancel("Notice", "Are you sure to close the application?"):
            # close the application
            root.destroy()

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
        # for business rn
        entries = Database.pull_all('business')
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
                c.execute(f"""INSERT INTO business VALUES 
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
            c.execute(f"DELETE FROM business WHERE title = '{title}'")
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
            c.execute(f"""UPDATE business
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


if __name__ == "__main__":
    root = Tk()
    root.title("Bookshelf")
    root.geometry('500x400')
    root.resizable(width=False, height=False)
    # application = Bookshelf(root)
    application = StartPage(root)
    root.mainloop()


# kinda like some test cases
political_book_list = ["State and Revolution- Vladimir Lenin", "Rules For Radicals- Saul Alinsky",
                       "Oneness vs the 1%- Vandana Shiva", "Capital is Dead- McKenzie Wark",
                       "So Damn Much Money- Robert Kaiser",
                       "The Socialist Challenge Today- Leo Panitch",
                       "The Leaderless Revolution- Carne Ross", "Revolution in Reverse- David Graeber",
                       "The End of History- Francis Fukuyama", "Shadow Masters- Daniel Estulin"]
business_book_list = ["The One Minute Manager- Ken Blanchard", "The Psychology of Money- Morgan Housel",
                      "The 12 Week Year- Brian Morgan", "Your Next 5 Moves- Greg Dinkin", "The Art of War- Sun Tzu",
                      "The 48 Laws of Power- Robert Greene", "The 4 Hour Work Week- Tim Ferriss",
                      "Tools For Titans-Tim Ferriss", "Zero to One- Blake Masters",
                      "It Takes What It Takes- Andy Staples"]
philosophy_book_list = ["Thus Spoke Zarathustra- Friedrich Nietzsche", "Existentialism is  A Humanism- Jean-Paul Sartre"
                                                                       'Being and Nothingness- Jean-Paul Sartre',
                        'Breaking The Habit of Being Yourself- Joe Dispenza']
science_book_list = ["The Burning Question- Duncan Clark", "The Singularity is Near- Ray Kurzweil",
                     "The Whole Shebang- Tim Ferriss"]
fantasy_book_list = ['1000 Arabian Nights- Christian Habicht', "Scythe- Neal Shusterman"]


class Database2:
    database_name = 'Bookshelf.db'
    """
    Create, Read, Update, Delete
    """

    @staticmethod
    def check_available_tables():
        with sqlite3.connect(Database2.database_name):
            conn = sqlite3.connect(Database2.database_name)
            c = conn.cursor()
            c.execute("""SELECT name FROM sqlite_master where type='table'""")
            conn.commit()

    @staticmethod
    def create_table(table_name):
        # Only on start page
        current_tables = Database2.check_available_tables()
        if table_name in current_tables:
            # show in message that this bookshelf name is already taken
            return
        else:
            with sqlite3.connect(Database2.database_name) as conn:
                c = conn.cursor()
                c.execute("""CREATE TABLE {table_name} VALUES (
                        title TEXT NOT NULL
                        author TEXT NOT NULL
                        """)
                conn.commit()
            # if successful, change message box to show as such, will be in startpage class




    """
    For later iterations, have all queries (add, modify, delete) run through database class

    add table method(table_name):
        if table name in database, message and return
    """

