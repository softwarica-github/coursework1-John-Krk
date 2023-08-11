import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import hashlib

# Global variable to store the logged-in user's ID
current_user_id = None

# Database initialization and table creation
db_connection = sqlite3.connect("user_data.db")
db_cursor = db_connection.cursor()
db_cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    address TEXT NOT NULL,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                    )''')
db_connection.commit()


def get_username_by_id(user_id):
    db_cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
    result = db_cursor.fetchone()
    return result[0] if result else None


def show_files():
    files = get_user_files()
    list_box.delete(0, tk.END)  # Clear the list box
    for file_data in files:
        file_name = file_data[1]
        list_box.insert(tk.END, file_name)


def get_user_files():
    db_cursor.execute("SELECT file_id, file_name FROM files WHERE user_id = ? OR is_public = 1", (current_user_id,))
    return db_cursor.fetchall()


def update_list_box():
    list_box.delete(0, tk.END)  # Clear the list box
    shared_files = os.listdir("shared_files")
    for file_name in shared_files:
        list_box.insert(tk.END, file_name)


def download_file():
    selected_index = list_box.curselection()
    if not selected_index:
        messagebox.showerror("Error", "Please select a file to download.")
        return

    selected_file = list_box.get(selected_index)
    source_path = os.path.join("shared_files", selected_file)
    destination_path = filedialog.asksaveasfilename(initialfile=selected_file)
    if destination_path:
        try:
            with open(source_path, 'rb') as source_file:
                with open(destination_path, 'wb') as destination_file:
                    destination_file.write(source_file.read())
            messagebox.showinfo("Success", f"File '{selected_file}' downloaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error downloading file: {str(e)}")


def delete_file():
    selected_index = list_box.curselection()
    if not selected_index:
        messagebox.showerror("Error", "Please select a file to delete.")
        return

    selected_file = list_box.get(selected_index)
    source_path = os.path.join("shared_files", selected_file)
    try:
        os.remove(source_path)
        status_label.config(text=f"File '{selected_file}' deleted successfully.")
        update_list_box()
    except Exception as e:
        messagebox.showerror("Error", f"Error deleting file: {str(e)}")


def exit_app():
    db_connection.close()
    app.destroy()


def show_option_frame():
    login_frame.pack_forget()
    register_frame.pack_forget()
    dashboard_frame.pack_forget()
    option_frame.pack()


def show_login_frame():
    option_frame.pack_forget()
    login_frame.pack()


def show_register_frame():
    option_frame.pack_forget()
    register_frame.pack()


def register_user():
    name = name_entry.get()
    address = address_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if not name or not address or not username or not password:
        messagebox.showerror("Error", "All fields are required.")
        return

    password = hashlib.sha256(password.encode()).hexdigest()  # Securely hash the password

    try:
        db_cursor.execute("INSERT INTO users (name, address, username, password) VALUES (?, ?, ?, ?)",
                          (name, address, username, password))
        db_connection.commit()
        messagebox.showinfo("Success", "Registration successful. You can now log in.")
        register_frame.pack_forget()  # Hide the registration frame
        show_login_frame()  # Show the login frame
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists. Please choose a different username.")


def login_user():
    username = login_username_entry.get()
    password = login_password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return

    password = hashlib.sha256(password.encode()).hexdigest()  # Securely hash the password

    db_cursor.execute("SELECT id, username, password FROM users WHERE username = ? AND password = ?", (username, password))
    user_data = db_cursor.fetchone()

    if user_data:
        # Successfully logged in
        global current_user_id
        current_user_id = user_data[0]
        login_username_entry.delete(0, tk.END)
        login_password_entry.delete(0, tk.END)
        login_frame.pack_forget()  # Hide the login frame
        app.title(f"Distributed File System - Welcome, {username}!")
        show_dashboard_frame()  # Show the dashboard frame
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")


def show_dashboard_frame():
    dashboard_frame.pack()


def logout_user():
    global current_user_id
    current_user_id = None
    dashboard_frame.pack_forget()
    show_option_frame()
    app.title("Distributed File System")
    login_username_entry.delete(0, tk.END)
    login_password_entry.delete(0, tk.END)


def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_name = os.path.basename(file_path)
        destination_path = os.path.join("shared_files", file_name)
        try:
            with open(file_path, 'rb') as source_file:
                with open(destination_path, 'wb') as destination_file:
                    destination_file.write(source_file.read())
            status_label.config(text=f"File '{file_name}' uploaded successfully.")
            update_list_box()
        except Exception as e:
            status_label.config(text=f"Error uploading file: {str(e)}")


# Create the main application window
app = tk.Tk()
app.title("Distributed File System")
app.configure(bg='black')  # Set the background color to black

# Set the ttk style with 'clam' theme (dark color scheme)
style = ttk.Style()
style.theme_use("clam")

# Create a frame for the option
option_frame = ttk.Frame(app, padding=10, style="Red.TFrame")

# Load the logo image
logo_image = tk.PhotoImage(file="/home/kali/Documents/vscode/jk.jpg")  # Replace "logo.png" with your image file

# Create a label to display the logo
logo_label = ttk.Label(option_frame, image=logo_image)
logo_label.pack(pady=10)

# Create buttons for login and register options
login_button = ttk.Button(option_frame, text="Login", command=show_login_frame)
login_button.pack(pady=10)

register_button = ttk.Button(option_frame, text="Register", command=show_register_frame)
register_button.pack(pady=5)

# Create a frame for login
login_frame = ttk.Frame(app, padding=10, style="Red.TFrame")

# Create input fields for login
login_username_label = ttk.Label(login_frame, text="Username:")
login_username_label.pack(pady=5)
login_username_entry = ttk.Entry(login_frame)
login_username_entry.pack(pady=5)

login_password_label = ttk.Label(login_frame, text="Password:")
login_password_label.pack(pady=5)
login_password_entry = ttk.Entry(login_frame, show="*")
login_password_entry.pack(pady=5)

login_button = ttk.Button(login_frame, text="Login", command=login_user)
login_button.pack(pady=10)

# Create a button to go back to the option frame from login
back_to_option_button_login = ttk.Button(login_frame, text="Back", command=show_option_frame)
back_to_option_button_login.pack(pady=5)

# Create a frame for the register dashboard
register_frame = ttk.Frame(app, padding=10, style="Red.TFrame")

# Create input fields for registration
name_label = ttk.Label(register_frame, text="Name:")
name_label.pack(pady=5)
name_entry = ttk.Entry(register_frame)
name_entry.pack(pady=5)

address_label = ttk.Label(register_frame, text="Address:")
address_label.pack(pady=5)
address_entry = ttk.Entry(register_frame)
address_entry.pack(pady=5)

username_label = ttk.Label(register_frame, text="Username:")
username_label.pack(pady=5)
username_entry = ttk.Entry(register_frame)
username_entry.pack(pady=5)

password_label = ttk.Label(register_frame, text="Password:")
password_label.pack(pady=5)
password_entry = ttk.Entry(register_frame, show="*")
password_entry.pack(pady=5)

register_button = ttk.Button(register_frame, text="Register", command=register_user)
register_button.pack(pady=10)

# Create a button to go back to the option frame from register
back_to_option_button_register = ttk.Button(register_frame, text="Back", command=show_option_frame)
back_to_option_button_register.pack(pady=5)

# Create a frame for the dashboard
dashboard_frame = ttk.Frame(app, padding=10, style="Red.TFrame")

# Create a button to upload files
upload_button = ttk.Button(dashboard_frame, text="Upload File", command=upload_file)
upload_button.pack(pady=10)

# Create a button to list files
list_files_button = ttk.Button(dashboard_frame, text="List Files", command=update_list_box)
list_files_button.pack(pady=5)

# Create a button to download files
download_button = ttk.Button(dashboard_frame, text="Download File", command=download_file)
download_button.pack(pady=5)

# Create a button to delete files
delete_button = ttk.Button(dashboard_frame, text="Delete File", command=delete_file)
delete_button.pack(pady=5)

# Create a button to logout
logout_button = ttk.Button(dashboard_frame, text="Logout", command=logout_user)
logout_button.pack(pady=5)

# Create a button to exit the application
exit_button = ttk.Button(dashboard_frame, text="Exit", command=exit_app)
exit_button.pack(pady=5)

# Create a list box to display the uploaded files
list_box = tk.Listbox(dashboard_frame, width=50, bg='black', fg='white')  # Black background with white text
list_box.pack(pady=5)

# Create a label to show the status of the file upload
status_label = ttk.Label(dashboard_frame, text="", style="Red.TLabel", foreground='white')  # White text on red background
status_label.pack()

# Start with the option frame
show_option_frame()

# Start the tkinter event loop
app.mainloop()
