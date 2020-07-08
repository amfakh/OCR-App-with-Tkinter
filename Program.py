from tkinter import (
    Tk,
    Menu,
    filedialog,
    messagebox,
    PhotoImage,
    Label,
    Button,
    Frame,
    Scrollbar,
    Text,
    END,
)
from PIL import ImageTk, Image
import os
import pytesseract


def newProcess():
    imgPanel = Label(root, image="")
    imgPanel.pack()
    content_text.delete(1.0, END)


def openFile():
    filename = filedialog.askopenfilename(
        defaultextension=".jpg",
        title="Buka Gambar",
        filetypes=[("All Files", "*.*"), ("Images", "*.jpg, *.png")],
    )
    if filename:
        global file_name
        file_name = filename
        root.title("{} - {}".format(os.path.basename(file_name), Program_Title))

    pytesseract.pytesseract.tesseract_cmd = r"tesseract"
    ocr = pytesseract.image_to_string(filename)
    content_text.delete(1.0, END)
    content_text.insert(END, ocr)
    return filename


def openImage(event=None):
    x = openFile()
    img = Image.open(x)
    img = img.resize((250, 250), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    imgPanel.config(image=img)
    imgPanel.image = img
    imgPanel.pack()


def saveFileAs(event=None):
    global content_text
    t = content_text.get("1.0", "end-1c")
    saveName = filedialog.asksaveasfilename(
        defaultextension=".txt",
        title="Simpan Hasil OCR",
        initialfile="Hasil OCR",
        filetypes=[("Text Document", "*.txt"), ("All Files", "*.*")],
    )
    file1 = open(saveName, "w+")
    file1.write(t)


def aboutInfo(event=None):
    messagebox.showinfo(
        "Tentang Saya",
        "{}{}".format(Program_Title, "\nNama: Muhammad Ammar Fakhri\nNIM: 41516010027"),
    )


def helpInfo(event=None):
    messagebox.showinfo(
        "Klik di sini", "Saya mengerjakan program ini sendiri tanpa bantuan orang lain"
    )


def exitProgram(event=None):
    if messagebox.askokcancel("Keluar?", "Yakin ingin keluar?"):
        root.destroy()


# # # #
# Root configuration
Program_Title = "OCR Viewer"
file_name = None

root = Tk()
root.geometry("800x600")
root.title(Program_Title)

menu_bar = Menu(root)  # Menampilkan menu bar

# Menu bar icon
new_icon = PhotoImage(file="icons/new.png")
open_icon = PhotoImage(file="icons/open.png")
save_icon = PhotoImage(file="icons/save.png")
exit_icon = PhotoImage(file="icons/exit.png")
about_icon = PhotoImage(file="icons/about.png")
help_icon = PhotoImage(file="icons/help.png")

# Function untuk mengonstruksi menu bar
def menuBarConstruct():
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(
        label="Baru",
        compound="left",
        image=new_icon,
        command=newProcess,
    )
    file_menu.add_command(
        label="Buka Gambar",
        compound="left",
        image=open_icon,
        command=openImage,
    )

    file_menu.add_command(
        label="Simpan Hasil OCR",
        compound="left",
        image=save_icon,
        command=saveFileAs,
    )
    file_menu.add_separator()
    file_menu.add_command(
        label="Keluar",
        compound="left",
        image=exit_icon,
        command=exitProgram,
    )
    menu_bar.add_cascade(label="File", menu=file_menu)

    about_menu = Menu(menu_bar, tearoff=0)
    about_menu.add_command(
        label="Tentang saya", 
        compound="left", 
        image=about_icon,
        command=aboutInfo
    )
    about_menu.add_command(
        label="Klik di sini", 
        compound="left",
        image=help_icon, 
        command=helpInfo
    )
    menu_bar.add_cascade(label="Tentang", menu=about_menu)


menuBarConstruct()  # Untuk menampilkan menu bar
root.config(menu=menu_bar)


lbl_welcome = Label(root, text="Selamat datang di program pembaca teks dari gambar")
btn_input = Button(root, text="Masukkan gambar", command=openImage)


lbl_welcome.config(font=("Arial", 20))
lbl_welcome.pack()

btn_input.config(font=("Arial", 12))
btn_input.pack()

imgPanel = Label(root, image="")
imgPanel.pack()

lbl_OCR = Label(root, text="")
lbl_OCR.pack()

content_text = Text(root, wrap="word", undo=1)
content_text.pack(expand="yes", fill="both")
scroll_bar = Scrollbar(content_text)
content_text.configure(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=content_text.yview)
scroll_bar.pack(side="right", fill="y")

root.mainloop()
