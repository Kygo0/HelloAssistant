from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.messagebox import askokcancel, WARNING
import sqlite3
from PIL import ImageTk, Image
from datetime import datetime
import win32ui
import win32gui
import win32con
import win32api
import pywintypes

mycursor = sqlite3.connect('Apps.db')

mycursor.execute(
    "CREATE TABLE IF NOT EXISTS filepaths (id INT AUTO_INCREMENT PRIMARY KEY, path VARCHAR(255), name VARCHAR(255))")
cur = mycursor.cursor()

saveList = []
setPathList = []
nameIconList = []


def on_destroy(event):
    global deletion
    if event.widget != deletion:
        return
    root.deiconify()


# Deletes all the apps that are set up for the voice assistant.
def confirmDeleteAll():
    global deletion
    answer = askokcancel(
        title='DELETION',
        message='Delete and exit?',
        icon=WARNING)

    if answer:
        exe = mycursor.execute('SELECT COUNT(*) FROM filepaths')
        for q in exe:
            strTuple = str(q)
        if strTuple == '(0,)':
            msg = 'No content available for deletion'
        else:
            msg = 'Everything was successfully deleted'
        messagebox.showinfo(
            title='DELETION',
            message=msg)
        mycursor.execute("DELETE FROM filepaths;")
        mycursor.commit()
    else:
        pass
    deletion.destroy()


# Lets the user choose what app to delete from the voice assistant.
def deletionMode():
    global deletion
    root.iconify()
    deletion = Toplevel()
    deletion.iconphoto(False, PhotoImage(file='backgrounds/settings.ico'))
    deletion.state('zoomed')
    deletion.resizable(False, False)
    deletion.grab_set()
    deletion.configure(bg='#3E45A1')
    deletion.bind("<Destroy>", on_destroy)
    app_width3 = 600
    app_height3 = 500
    screen_width3 = root.winfo_screenwidth()
    screen_height3 = root.winfo_screenheight()
    x3 = (screen_width3 / 2) - (app_width3 / 2)
    y3 = (screen_height3 / 2) - (app_height3 / 2)
    deletion.geometry(f'{app_width3}x{app_height3}+{int(x3)}+{int(y3)}')
    deletion.title("Delete configured apps")
    # Saves the icons of every app.
    ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
    ico_y = win32api.GetSystemMetrics(win32con.SM_CYICON)

    # Lets the user choose what app to delete from the voice assistant.
    def deletePressed():
        answer = askokcancel(
            title='DELETION',
            message='Are you sure?\nTHIS IS AN IRREVERSIBLE ACTION',
            icon=WARNING)
        if answer:
            stripString1 = str(name).lstrip("(").rstrip(")")
            stripString2 = str(stripString1).rstrip(",")
            stripString3 = str(stripString2).lstrip('"').rstrip('"')
            stripString4 = str(stripString3).lstrip("'").rstrip("'")
            sql = "DELETE FROM filepaths WHERE name = ?"
            adr = (str(stripString4),)
            mycursor.execute(sql, adr)
            mycursor.commit()
            deletion.destroy()

    # Display icons of apps that are already setup.
    conn = mycursor.execute("SELECT path FROM filepaths;")

    for setPath in conn:
        stripString1 = str(setPath).lstrip("(").rstrip(")")
        stripString2 = str(stripString1).rstrip(",")
        stripString3 = str(stripString2).lstrip('"').rstrip('"')
        stripString4 = str(stripString3).lstrip("'").rstrip("'")
        setPathList.append(stripString4)
    setPathList_no_duplicates = list(dict.fromkeys(setPathList))
    mycursor.commit()

    conn = mycursor.execute("SELECT name FROM filepaths;")

    for nameIcon in conn:
        stripString1 = str(nameIcon).lstrip("(").rstrip(")")
        stripString2 = str(stripString1).rstrip(",")
        stripString3 = str(stripString2).lstrip('"').rstrip('"')
        stripString4 = str(stripString3).lstrip("'").rstrip("'")
        nameIconList.append(stripString4)
    nameIconList_no_duplicates = list(dict.fromkeys(nameIconList))
    mycursor.commit()
    adding = 0
    for creatingIcon in setPathList_no_duplicates:
        try:
            try:
                large, small = win32gui.ExtractIconEx(str(creatingIcon), 0)
                win32gui.DestroyIcon(large[0])
                hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
                hbmp = win32ui.CreateBitmap()
                hbmp.CreateCompatibleBitmap(hdc, ico_x, ico_y)
                hdc = hdc.CreateCompatibleDC()

                hdc.SelectObject(hbmp)
                hdc.DrawIcon((0, 0), small[0])
                hbmp.SaveBitmapFile(hdc, 'icons/' + str(nameIconList_no_duplicates[adding]) + '.bmp')
                adding += 1
            except pywintypes:
                pass
        except IndexError:
            pass

    conn = mycursor.execute("SELECT name FROM filepaths;")

    nameList = []
    for name in conn:
        stripString1 = str(name).lstrip("(").rstrip(")")
        stripString2 = str(stripString1).rstrip(",")
        stripString3 = str(stripString2).lstrip('"').rstrip('"')
        stripString4 = str(stripString3).lstrip("'").rstrip("'")
        if stripString4 == "":
            pass
        else:
            nameList.append(stripString4)
    nameList_no_duplicates = list(dict.fromkeys(nameList))

    add_y_coordinate = 0
    add_y_coordinate2 = 0
    addIcon = 0

    if not nameList_no_duplicates:
        emptyDel = Label(deletion,
                         text="There are no apps available to be deleted.\nYou can add some by clicking Create New Apps on the main window",
                         bg='#3E45A1', padx=25, pady=50, font=30)
        emptyDel.place(relx=0.5, rely=0.5, anchor=CENTER)
    else:
        for execute in nameList_no_duplicates:
            Button(deletion, text=execute.upper(), command=deletePressed, padx=30, pady=30, bg='pink').place(x=0,
                                                                                                             y=add_y_coordinate)
            try:
                image = Image.open('icons\\' + str(nameList_no_duplicates[addIcon]) + '.bmp')
                img = image.resize((15, 15))
                my_img = ImageTk.PhotoImage(img)
                lbl = Label(deletion, image=my_img, padx=5, pady=5)
                lbl.place(x=0, y=add_y_coordinate2)
                lbl.image = my_img
            except FileNotFoundError:
                pass
            add_y_coordinate += 90
            add_y_coordinate2 += 90
            addIcon += 1

            # Button that deletes every app that is set up for the voice assistant.
            deleteEverything = Button(deletion, text="Delete All Apps", command=confirmDeleteAll, bg='pink',
                                      font="bold", )
            deleteEverything.place(relx=0.97, rely=0.01, anchor=NE)
    mycursor.commit()


# Lets the user set up a new app for the voice assistant.
def newCreate():
    global save, saveList
    new = Toplevel()
    new.iconphoto(False, PhotoImage(file=r'backgrounds/settings.ico'))
    new.geometry("600x200")
    new.configure(bg='#3E45A1')
    new.resizable(False, False)
    new.grab_set()
    app_width2 = 400
    app_height2 = 300
    screen_width2 = root.winfo_screenwidth()
    screen_height2 = root.winfo_screenheight()
    x2 = (screen_width2 / 2) - (app_width2 / 2)
    y2 = (screen_height2 / 2) - (app_height2 / 2)
    new.geometry(f'{app_width2}x{app_height2}+{int(x2)}+{int(y2)}')
    new.title("Setup a new app")

    def inCreate():
        save = e.get().lower()
        if str(save) == "" or save.isspace():
            messagebox.showerror('Error', 'First, insert the name of the app')
        else:
            saveList.append(save)
            file_path = filedialog.askopenfilename(filetypes=(("Executable files", "*.exe"), ("All files", "*.*")))
            path.set(file_path)
            pathFile = path.get()
        try:
            mycursor.execute("INSERT INTO filepaths (path, name) VALUES (?,?)", (pathFile, save))
            mycursor.commit()
        except NameError:
            pass
        new.destroy()

    newLabel = Label(new, text='Setup an app', font=('Calibri', 20, "bold"), pady=50, padx=200, fg='pink', bg='#3E45A1')
    newLabel.pack()

    LabelSmall = Label(new, text='App Name                   ', pady=4, padx=4, bg='pink',
                       font=('Calibri', 13, 'bold'))
    LabelSmall.place(x=60, y=165)

    saveName = Button(new, text='Apply & find file', command=inCreate, padx=4, pady=4, font=('Calibri', 13, 'bold'),
                      bg='pink')
    saveName.place(x=230, y=190)

    e = Entry(new, width=27, bg='white')
    e.place(x=60, y=200)


root = Tk()
root.title('Assistant Setup')
root.resizable(False, False)
canv = Canvas(root, width=700, height=600, bg='white')
canv.grid(row=2, column=3)

# In case user deletes `FinalBackground.png` from files.
try:
    img = ImageTk.PhotoImage(Image.open("backgrounds/FinalBackground.png"))
    canv.create_image(0, 0, anchor=NW, image=img)
except FileNotFoundError:
    errorBackground = Label(root, text='Background image has been deleted or its file destination has been changed.',
                            font='Calibri 10')
    errorBackground.place(x=160, y=565)

# Making window to open in the exact center of the screen.
app_width = 697
app_height = 596
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height / 2)
root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

# In case user deletes `settings.ico` from files.
try:
    photo = PhotoImage(file="backgrounds/settings.ico")
    root.iconphoto(False, photo)
except TclError:
    pass  # Uses the default logo tkinter provides.

path = StringVar()

createNew = Button(root, text='Create App', command=newCreate, bg='pink', font="bold")
createNew.place(x=10, y=170)

deleteMode = Button(root, text="Delete App", command=deletionMode, bg='pink', font='bold')
deleteMode.place(x=10, y=240)

# Greet the user.
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
timeInt = int(current_time[0:2])

if 12 > timeInt > 5:
    try:
        bg1 = PhotoImage(file="backgrounds/GoodMorning.png")
        GreetLabel = Label(root, image=bg1, bg='blue')
        GreetLabel.place(x=20, y=80)
    except TclError:
        GreetLabel = Label(root, text='Good Morning', font='bold 20', bg='pink')
        GreetLabel.place(x=20, y=80)
elif 12 < timeInt < 17:
    try:
        bg1 = PhotoImage(
            file="backgrounds/GoodAfternoon.png")  # Inserting "try/exception" statement in case user
        GreetLabel = Label(root, image=bg1, bg='blue')  # deletes .png images from files.
        GreetLabel.place(x=20, y=80)
    except TclError:
        GreetLabel = Label(root, text='Good Afternoon', font='bold 20', bg='pink')
        GreetLabel.place(x=20, y=80)
else:
    try:
        bg1 = PhotoImage(file="backgrounds/GoodEvening.png")
        GreetLabel = Label(root, image=bg1, bg='blue')
        GreetLabel.place(x=20, y=80)
    except TclError:
        GreetLabel = Label(root, text='Good Evening', font='bold 20', bg='pink')
        GreetLabel.place(x=20, y=80)

root.mainloop()
mycursor.close()
