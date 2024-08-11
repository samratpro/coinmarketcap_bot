from customtkinter import *
import sqlite3
import base64
import shutil
import os
import threading
import webbrowser
from tkinter import filedialog
from component import *

con = sqlite3.connect('database.db')
cur = con.cursor()
cur.execute('''
            CREATE TABLE IF NOT EXISTS Postdata (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                api_key CHAR(200),
                profile_id CHAR(200)
            )  
            ''')

data_check = cur.execute('''SELECT api_key FROM Postdata WHERE ID=1''').fetchone()
print(data_check)

if data_check == None:
    cur.execute('''
                    INSERT INTO Postdata(
                        api_key,
                        profile_id)
                    VALUES(
                        'api_key_xxxxxxxxxxxxxxxxxx',                          
                        'profile_id_xxxxxxxxxxxxxxx'                          
                    )
                    ''')
# TK part
window = CTk()
set_default_color_theme("green")
set_appearance_mode("light")
window.title("Coinmarketcap Bot")
window.geometry("600x600")
window.wm_iconbitmap()

# Create a Frame + Content Frame with scrollbar
frame = CTkFrame(window)
frame.pack(fill=BOTH, expand=True)
canvas = CTkCanvas(frame)
canvas.pack(side=LEFT, fill=BOTH, expand=True)
canvas.bind_all("<MouseWheel>", lambda event: on_mousewheel(event))  # Labda have to use when function is below
scrollbar = CTkScrollbar(frame, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
content_frame = CTkFrame(canvas)
canvas.create_window((0, 0), window=content_frame, anchor=NW)


# website info widgets
info_frame = CTkFrame(content_frame)
info_frame.grid(pady=10, padx=20)

# label section
api_key_labe = CTkLabel(info_frame, text="API Key")
api_key_labe.grid(row=0, column=0, padx=10, pady=3)
api_key = CTkEntry(info_frame, width=300, border_width=1)
api_key.insert(0,str(cur.execute('''SELECT api_key FROM Postdata WHERE ID=1''').fetchone()[0]))
api_key.grid(row=1, column=0, padx=10, pady=10)

profile_id_labe = CTkLabel(info_frame, text="Profile ID")
profile_id_labe.grid(row=0, column=1, padx=10, pady=3)
profile_id = CTkEntry(info_frame, width=200, border_width=1)
profile_id.insert(0, str(cur.execute('''SELECT profile_id FROM Postdata WHERE ID=1''').fetchone()[0]))
profile_id.grid(row=1, column=1, padx=10, pady=10)

file_frame = CTkFrame(content_frame)
file_frame.grid(pady=10, padx=20)
def select_file():
    file_path = filedialog.askopenfilename(title="Select CSV File",filetypes=[("CSV files", "*.csv")])
    if file_path:
        file_label.configure(text=f"Selected File : {os.path.basename(file_path)}")
        full_file_path.insert(0,str(file_path))

# Create a CTkLabel widget for displaying selected file path
file_label = CTkLabel(file_frame, text="No file selected", width=380)
file_label.grid(row=2, column=0, padx=10, pady=5)
full_file_path = CTkEntry(file_frame)

# Create a CTkButton to trigger file selection dialog
upload_button = CTkButton(file_frame, text="Select CSV File", command=lambda: select_file())
upload_button.grid(row=2, column=1)

# Switch
switch_frame = CTkFrame(content_frame)
switch_frame.grid(pady=10, padx=20)
Like_label = CTkLabel(switch_frame,text='Do Like?')
Like_label.grid(row=3,column=0)
Like = CTkComboBox(switch_frame, width=160, border_width=1, values=['Yes', 'No'], state='readonly')
Like.set('Yes')
Like.grid(row=4, column=0, pady=10, padx=10)

Follow_label = CTkLabel(switch_frame,text='Do Follow?')
Follow_label.grid(row=3,column=1)
Follow = CTkComboBox(switch_frame, width=160, border_width=1, values=['Yes', 'No'], state='readonly')
Follow.set('Yes')
Follow.grid(row=4, column=1, pady=10, padx=10)

Comment_label = CTkLabel(switch_frame,text='Do Comment?')
Comment_label.grid(row=3,column=2)
Comment = CTkComboBox(switch_frame, width=160, border_width=1, values=['Yes', 'No'], state='readonly')
Comment.set('Yes')
Comment.grid(row=4, column=2, pady=10, padx=10)

# Command
command_label = CTkFrame(content_frame)
command_label.grid(row=14, column=0, padx=10, pady=(30, 30))
start = CTkButton(command_label, text=" ▶ Run", fg_color=('#2AA26F'), command=lambda: operation_start())
start.grid(row=15, column=0, padx=10, pady=10, ipadx=10)
Update = CTkButton(command_label, text='✔ Save API', fg_color=("#2AA26F"), command=lambda: db_save())
Update.grid(row=15, column=1, padx=10, pady=10, ipadx=10)
Reset = CTkButton(command_label, text='↻ Reset API', fg_color=("#EB4C42"), command=lambda: reset_data())
Reset.grid(row=15, column=2, padx=10, pady=10, ipadx=10)


# Log
log_label = CTkLabel(content_frame, text="Logs", font=('', 20), fg_color=("red"))
log_label.grid(row=16, column=0, pady=0, ipadx=20)
log = CTkTextbox(content_frame, fg_color=('black', 'white'), text_color=('white', 'black'), width=550, height=200)
log.grid(row=17, column=0, padx=5, pady=(5, 10))
copyright = CTkLabel(content_frame, text="Need any help ?")
copyright.grid(row=18, column=0, padx=5, pady=(5, 0))
copy_button = CTkButton(content_frame, text="Contact With Developer", fg_color=('#2374E1'),command=lambda: webbrowser.open_new('https://www.facebook.com/samratprodev/'))
copy_button.grid(row=19, column=0, padx=5, pady=(5, 300))


def db_save():
    get_api_key = str(api_key.get())
    get_profile_id = str(profile_id.get())


    cur.execute('''
        UPDATE Postdata
        SET
            api_key = ?,
            profile_id = ?
        WHERE ID = 1
    ''', (
        get_api_key,
        get_profile_id
    ))


def reset_data():
    cur.execute('''
                    UPDATE Postdata
                    SET
                        api_key = 'api_key_xxxxxxxxxxxxxxxxxx',
                        profile_id = 'api_key_xxxxxxxxxxxxxxx'
                    WHERE ID = 1

                    ''')
    window.destroy()


def operation_start():
    thread = threading.Thread(target=operation_start_thread)
    thread.start()


def operation_start_thread():
    get_api_key = api_key.get()
    get_profile_id = profile_id.get()
    get_file_path = full_file_path.get()
    get_like = Like.get()
    get_follow = Follow.get()
    get_comment = Comment.get()
    content_generator_loop(get_api_key, get_profile_id, get_file_path, get_like, get_follow, get_comment, log)


def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


if __name__ == '__main__':
    window.mainloop()

con.commit()
cur.close()