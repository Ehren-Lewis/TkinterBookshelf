from tkinter import Tk, Button, PhotoImage, Label, LabelFrame, W, E, N, S, Entry, END, StringVar, Scrollbar, Toplevel
from tkinter import ttk
import sqlite3


class Contacts:
    db_filename = "contacts.db"
    def __init__(self, root):
        self.root = root
        self.create_gui()
        ttk.style = ttk.Style()
        ttk.style.configure("Treeview", font=('helvetica', 10))
        ttk.style.configure("Treeview.Heading", font=('helvetica', 12, 'bold'))

    def execute_db_query(self, query, parameters=()):
        with sqlite3.connect(self.db_filename) as conn:
            print("You have successfully connected to the Database")
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
        return query_result

    def create_gui(self):
        self.create_left_icon()
        self.create_label_frame()
        self.create_message_area()
        self.create_tree_view()
        self.create_scrollbar()
        self.create_bottom_buttons()
        self.view_contacts()

    # good
    def create_left_icon(self):
        photo = PhotoImage(file=r"C:\Users\ehren\PycharmProjects\Tkinter\icons\Logo.gif")
        label = Label(image=photo)
        label.image = photo
        label.grid(row=0, column=0)

    def create_label_frame(self):
        labelframe = LabelFrame(self.root, text='Create New Contact', bg='sky blue', font='helvetica 10')
        labelframe.grid(row=0, column=1, padx=8, pady=9, sticky='ew')
        Label(labelframe, text='Name:', bg='green', fg='white').grid(row=1, column=1, sticky=W, pady=2, padx=15)
        self.namefield = Entry(labelframe)
        self.namefield.grid(row=1, column=2, sticky=W, padx=5, pady=2)
        Label(labelframe, text='Email:', bg='brown', fg='white').grid(row=2, column=1, sticky=W, pady=2, padx=15)
        self.emailfield = Entry(labelframe)
        self.emailfield.grid(row=2, column=2, sticky=W, padx=5, pady=2)
        Label(labelframe, text='Number:', bg="black", fg='white').grid(row=3, column=1, sticky=W, pady=2, padx=15)
        self.numfield = Entry(labelframe)
        self.numfield.grid(row=3, column=2, sticky=W, padx=5, pady=2)
        Button(labelframe, text="Add Contact", command=self.on_add_contact_button_clicked, bg='blue', fg='white').grid(row=4, column=2, sticky=E, padx=5, pady=5)

    def create_message_area(self):
        self.message = Label(text='', fg='red')
        self.message.grid(row=3, column=1, sticky=W)

    def create_tree_view(self):
        self.tree = ttk.Treeview(height=10, columns=("email", "number"))
        self.tree.grid(row=6, column=0, columnspan=3)
        self.tree.heading('#0', text='Name', anchor=W)
        self.tree.heading("email", text='Email Address', anchor=W)
        self.tree.heading("number", text='Contact Number', anchor=W)

    def create_scrollbar(self):
        self.scrollbar = Scrollbar(orient='vertical', command=self.tree.yview)
        self.scrollbar.grid(row=6, column=3, rowspan=10, stick='sn')


    def create_bottom_buttons(self):
        Button(text='Delete Selected', command=self.on_delete_selected_button_clicked,
               bg='red', fg='white').grid(row=8, column=0, sticky=W, pady=10,
                                                                              padx=20)
        Button(text="Modify Selected", command=self.on_modify_button_clicked, bg="purple", fg="white").grid(row=8, column=1, sticky=W)

    def new_contact_validated(self):
        return len(self.namefield.get()) != 0 and len(self.emailfield.get()) != 0 and len(self.numfield.get()) != 0

    def add_new_contact(self):
        if self.new_contact_validated():
            query = "INSERT INTO contacts_table VALUES(?, ?, ?)"
            parameters = (self.namefield.get(), self.emailfield.get(), self.numfield.get())
            self.execute_db_query(query, parameters)
            self.message.configure(text=f"New Contact {self.namefield.get()} added")
            self.namefield.delete(0, END)
            self.emailfield.delete(0, END)
            self.numfield.delete(0, END)
        else:
            self.message.configure(text="Name, email, or number cannot be blank")
        self.view_contacts()

    def view_contacts(self):
        items = self.tree.get_children()
        for item in items:
            self.tree.delete(item)
        query = 'SELECT * FROM contacts_table ORDER BY name desc'
        contact_entries = self.execute_db_query(query)
        for row in contact_entries:
            self.tree.insert('', 0, text=row[0], values=(row[1], row[2]))

    def on_add_contact_button_clicked(self):
        self.add_new_contact()

    def delete_contacts(self):
        self.message['text'] = ""
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM contacts_table WHERE name = ?'
        self.execute_db_query(query, (name,))
        self.message['text'] = f"Contacts for {name} deleted"
        self.view_contacts()

    def on_delete_selected_button_clicked(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'No item selected to delete'
            return
        self.delete_contacts()

    def open_modify_window(self):
        name = self.tree.item(self.tree.selection())['text']
        old_number = self.tree.item(self.tree.selection())['values'][1]
        self.transient = Toplevel()
        self.transient.title('Update Contact')
        Label(self.transient, text='Name: ').grid(row=0, column=1)
        Entry(self.transient, textvariable=StringVar(
            self.transient, value=name), state='readonly').grid(row=0, column=2)
        Label(self.transient, text='Old Contact Number: ').grid(row=1, column=1)
        Entry(self.transient, textvariable=StringVar(
            self.transient, value=old_number), state='readonly').grid(row=1, column=2)
        Label(self.transient, text='New Phone Number:').grid(row=2, column=1)
        new_phone_number_entry_widget = Entry(self.transient)
        new_phone_number_entry_widget.grid(row=2, column=2)
        # Lambda functions are required whenever a function requires objects
        Button(self.transient, text='Update Contact', command=lambda: self.update_contact(new_phone_number_entry_widget.get(),
                                                                 old_number, name)).grid(row=3, column=2, sticky=E)

        self.transient.mainloop()

    def update_contact(self, new_phone, old_phone, name):
        query = "UPDATE contacts_table SET number=? WHERE number=? and name = ?"
        parameters = (new_phone, old_phone, name)
        self.execute_db_query(query, parameters)
        self.transient.destroy()
        self.message['text'] = f'Phone number of {name} modified'
        self.view_contacts()

    def on_modify_button_clicked(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'No item selected to modify'
            return
        self.open_modify_window()





class Test:
    def __init__(self, root):
        self.root = root
        self.create_window()
        self.create_button()

    def create_window(self):
        self.first_label = Label(self.root, text='hello')
        self.first_label.grid(row=0, column=0)

    def create_button(self):
        btn = Button(text='Open').grid(row=0, column=1)

    def btn_command(self):
        new_window = Tk()
        second_frame = Label(new_window, text='world').grid(row=0, column=0)

    def btn_action(self,action):
        pass


if __name__ == "__main__":
    root = Tk()
    root.title("Contacts List")
    root.geometry('650x450')
    root.resizable(width=False, height=False)
    application = Contacts(root)
    root.mainloop()