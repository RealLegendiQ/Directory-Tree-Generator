""" Made by N Purushotam Kumar (COMP A - AIT Pune) | github link : https://github.com/RealLegendiQ """
""" Directory Tree Generator :  A program to generate a directory tree which allows users to see relationship between all of the files/directories in that tree 
and to search for a file in a given directory"""

from tkinter import *
from tkinter import filedialog as tfd
from tkinter import messagebox as tmb
from PIL import ImageTk, Image, ImageDraw, ImageFont
import os

# COLORS
bgColor = "orange"
btnBgColor = "forest green"
DefaultTextColor = "#b3b3b3"


# TKINTER SETUP
class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Directory Tree Generator")
        self.geometry("800x500")
        self.minsize(800, 500)
        self.configure(bg=bgColor)
        self.iconbitmap('DirTree.ico')


root = Root()

# STATIC STUFF

DirEntryDefault = "Enter path of directory"
FileEntryDefault = "Enter file name"
PathEmptyMsg = "No directory has given.\nPlease enter path of directory."
FileEmptyMsg = "No file has given.\nPlease Enter file name to search in the given directory."
WinCOLOR = ["black", "white"]
COLORS = ["red", "RoyalBlue1", "dark orange", "goldenrod1", "SpringGreen3", "purple3", "CadetBlue1", "deep pink",
          "cyan3"]

# VARIABLES

DirPath = StringVar()
DirPath.set(DirEntryDefault)
FileName = StringVar()
FileName.set(FileEntryDefault)
Mode = 0


# FUNCTIONS

def browseDirectory():
    dir_selected = tfd.askdirectory()
    dir_entry.config(fg="black")
    DirPath.set(dir_selected.replace('/', '\\'))


def isEmpty():
    if DirPath.get() == "" or DirPath.get() == DirEntryDefault:
        OutputWindow.config(state="normal")
        OutputWindow.delete("1.0", END)
        OutputWindow.config(state="disabled")
        tmb.showerror("Directory Tree Generator", PathEmptyMsg)
        return True
    else:
        return False


def clearDirDefaultEntry(event):
    if DirPath.get() == DirEntryDefault:
        dir_entry.config(fg="black")
        DirPath.set("")


def clearFileDefaultEntry(event):
    if FileName.get() == FileEntryDefault:
        file_entry.config(fg="black")
        FileName.set("")


def browseIconEnter(event):
    generateTree()


def searchEnter(event):
    searchFile()


'''
-> The generateTree() function is core of this program in this os.walk() function recursively visits all the directories present
   in a given directory in top-down manner that is root is visited first. 
-> Level of a any directory is obtained by counting the number of separators.
-> Total line in the output window is counted while inserting lines in it.
-> To represent different levels in different color we added tag on the current line and configured its font color to 
   represent level color.
'''


def generateTree():
    if not isEmpty():
        OutputWindow.config(state="normal")

        path = DirPath.get()

        OutputWindow.delete("1.0", END)
        OutputWindow.insert(END, path)
        line, mx = 1, "10000"
        for root, dirs, files in os.walk(path):
            root = root.replace(path, "")
            # counting the separators
            level = root.count(os.sep)
            pt, i = 0, 0
            while i < len(root):
                if root[i] == os.sep:
                    pt = i
                i += 1
            if level == 0:

                currentLine = root + "\n"
                OutputWindow.insert(END, currentLine)
                start, end = str(line) + '.' + '0', str(line) + '.' + mx
                OutputWindow.tag_add(str(line), start, end)
                OutputWindow.tag_config(
                    str(line), foreground=COLORS[level % 9])
                line += 1

                for file in files:
                    currentLine = "  " * level + "|--" + file + "\n"
                    OutputWindow.insert(END, currentLine)
                    start, end = str(line) + '.' + '0', str(line) + '.' + mx
                    OutputWindow.tag_add(str(line), start, end)
                    OutputWindow.tag_config(
                        str(line), foreground=COLORS[(level + 1) % 9])
                    line += 1

            else:

                currentLine = "|" + "--" * level + root[pt + 1:] + "\n"
                OutputWindow.insert(END, currentLine)
                start, end = str(line) + '.' + '0', str(line) + '.' + mx
                OutputWindow.tag_add(str(line), start, end)
                OutputWindow.tag_config(
                    str(line), foreground=COLORS[level % 9])
                line += 1

                for file in files:
                    currentLine = "|" + "  " * level + "|--" + file + "\n"
                    OutputWindow.insert(END, currentLine)
                    start, end = str(line) + '.' + '0', str(line) + '.' + mx
                    OutputWindow.tag_add(str(line), start, end)
                    OutputWindow.tag_config(
                        str(line), foreground=COLORS[(level + 1) % 9])
                    line += 1

            OutputWindow.insert(END, "|\n")
            line += 1
    OutputWindow.config(state="disabled")


def searchFile():
    if not isEmpty():
        file_name = FileName.get()
        flag = 0
        if file_name == "" or file_name == FileEntryDefault:
            tmb.showerror("Directory Tree Generator", FileEmptyMsg)
        else:
            OutputWindow.config(state="normal")
            OutputWindow.delete("1.0", END)
            for root, dirs, files in os.walk(DirPath.get()):
                for file in files:
                    if file_name in file:
                        OutputWindow.insert(
                            END, os.path.join(root, file) + "\n")
                        flag = 1
            OutputWindow.config(state="disabled")
            if flag == 0:
                tmb.showerror("Directory Tree Generator", "File not found")


def ImageWidth():
    max_width = 0
    no_of_char = 0
    for ch in OutputWindow.get("1.0", END):
        if ch == "\n":
            if no_of_char > max_width:
                max_width = no_of_char
            no_of_char = 0
        else:
            no_of_char += 1
    return max_width * 9


def ImageHeight():
    lines = 0
    for ch in OutputWindow.get("1.0", END):
        if ch == "\n":
            lines += 1
    return lines * 19


def save():
    if (OutputWindow.get("1.0", END)) == "\n":
        tmb.showerror("Output Window Empty!",
                      "Generate a tree first or search for a file. ")
        return

    font = ImageFont.truetype('bahnschrift.ttf', 18)

    NewImage = Image.new('RGB', (ImageWidth(), ImageHeight()), color='white')
    draw = ImageDraw.Draw(NewImage)
    draw.text((0, 0), OutputWindow.get("1.0", END), fill="black", font=font)

    SaveLocation = tfd.asksaveasfilename(initialfile="Untitled.jpg", defaultextension=".jpg",
                                         filetypes=[('JPG file', '.jpg'), ('JPEG file', '.jpeg'), ('all files', '*.*')])
    if SaveLocation is None:
        return
    else:
        NewImage.save(SaveLocation)
        tmb.showinfo('SAVED', 'File has been saved successfully!')


def clear():
    OutputWindow.config(state="normal")
    OutputWindow.delete("1.0", END)
    OutputWindow.config(state="disabled")
    dir_entry.config(fg=DefaultTextColor)
    file_entry.config(fg=DefaultTextColor)
    DirPath.set(DirEntryDefault)
    FileName.set(FileEntryDefault)


def setColor():
    global Mode
    Mode = (Mode + 1) % 2
    OutputWindow.config(bg=WinCOLOR[Mode], fg=WinCOLOR[(Mode + 1) % 2])


'''
INTERFACE part of the code includes every widgets present in the program including Output window, Entry bar for path
and Entry bar for file name to be searched. 
'''
# INTERFACE
# FRAME-1
browse_frame = Frame(root, width=600, height=50, bg=bgColor)
browse_frame.pack(padx=5, pady=5)

generate_btn = Button(browse_frame, width=10, text="GENERATE",
                      command=generateTree, bg=btnBgColor, fg="white")
generate_btn.pack(side=RIGHT, padx=5, pady=5)

image = Image.open('Folder-Explorer-icon.png')
image = image.resize((30, 20), Image.ANTIALIAS)
iconImage = ImageTk.PhotoImage(image)
browse_icon = Button(browse_frame, image=iconImage,
                     command=browseDirectory, padx=5)
browse_icon.pack(side=RIGHT, padx=5, pady=5)

dir_entry = Entry(browse_frame, width=200, bd=1,
                  font="consolas 12", textvariable=DirPath, fg=DefaultTextColor)
dir_entry.pack(side=RIGHT, padx=5, pady=5)
dir_entry.bind('<Button-1>', clearDirDefaultEntry)
dir_entry.bind('<Return>', browseIconEnter)

# FRAME-2
file_frame = Frame(root, width=600, height=50, bg=bgColor)
file_frame.pack(padx=5, pady=5)

file_btn = Button(file_frame, width=10, text="SEARCH",
                  command=searchFile, bg=btnBgColor, fg="white")
file_btn.pack(side=RIGHT, padx=5, pady=5)

file_entry = Entry(file_frame, width=200, bd=1,
                   font="consolas 12", textvariable=FileName, fg="#b3b3b3")
file_entry.pack(side=RIGHT, padx=5, pady=5)
file_entry.bind('<Button-1>', clearFileDefaultEntry)
file_entry.bind('<Return>', searchEnter)

# FRAME-3
buttons_frame = Frame(root, width=600, height=50, bg=bgColor)
buttons_frame.pack(padx=5, pady=5, fill=BOTH)

save_btn = Button(buttons_frame, width=10, text="SAVE",
                  command=save, bg=btnBgColor, fg="white")
save_btn.pack(side=RIGHT, padx=5, pady=5)

clear_btn = Button(buttons_frame, width=10, text="CLEAR",
                   command=clear, bg=btnBgColor, fg="white")
clear_btn.pack(side=LEFT, padx=5, pady=5)

colChange_btn = Button(buttons_frame, width=10, text="THEME",
                       command=setColor, bg=btnBgColor, fg="white")
colChange_btn.pack(side=LEFT, padx=5, pady=5)

# OUTPUT WINDOW

scrollBarYaxis = Scrollbar(root, orient=VERTICAL)
scrollBarYaxis.pack(side=RIGHT, fill=Y)

scrollBarXaxis = Scrollbar(root, orient=HORIZONTAL)
scrollBarXaxis.pack(side=BOTTOM, fill=X)

OutputWindow = Text(root, wrap=NONE, state="disabled", yscrollcommand=scrollBarYaxis.set,
                    xscrollcommand=scrollBarXaxis.set, font="consolas 11", bg=WinCOLOR[Mode],
                    fg=WinCOLOR[(Mode + 1) % 2])

OutputWindow.pack(side=LEFT, fill=BOTH, expand=1)

scrollBarYaxis.config(command=OutputWindow.yview)
scrollBarXaxis.config(command=OutputWindow.xview)

if __name__ == "__main__":
    root.mainloop()
