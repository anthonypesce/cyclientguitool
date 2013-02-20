#!/usr/bin/env python
#
# cyclientgui.py - GUI to work with cyclient
#
# Copyright (C) 2013  Anthony Pesce
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
import subprocess

from Tkinter import *
import tkMessageBox

#Tool tip class for the tool tips use throughout the program
class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        try:
            # For Mac OS
            tw.tk.call("::tk::unsupported::MacWindowStyle",
                       "style", tw._w,
                       "help", "noActivates")
        except TclError:
            pass
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

#Creates tool tip, requires the widget you wish to have the tool tip show
#and takes in the text to display
def createToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


#Exits the gui pannel
def exitfunction():
    root.destroy()

#A help popup
def printhelp():
    tkMessageBox.showinfo("Help","Type in the various fields \n"
                          "to pass information to cyclient. An \n"
                          "empty field is considered a default\n"
                          "or type \"./cyphesis --help\" for help")

#prints the version of cyclient by calling ./cylient --version
def printversion():
    ver = subprocess.check_output(["./cyclient","--version"])
    newver=  ver.replace("./cyclient","")
    tkMessageBox.showinfo("Version",newver)

def about():
    tkMessageBox.showinfo("About","Cyclient GUI Frontend \n"
                          "By Anthony Pesce \n"
                          "2013")

root = Tk()
root.wm_title("Cyclient gui tool")

menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Exit", command=exitfunction)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="Help",command=printhelp)
helpmenu.add_command(label="Version",command=printversion)
helpmenu.add_command(label="About...", command=about)

#A grid view to create the gui, the first
#column is the labels and the second column is
#the text fields
#Both the labels and text field have a tooltip
instancelabel = Label(root,text="Instance: ")
instancelabel.grid(row=0,column=0)
instancetext = Entry(root)
instancetext.grid(row=0,column=1)
createToolTip(instancelabel,"Unique short name for the server instance")
createToolTip(instancetext,"Unique short name for the server instance")

accountlabel = Label(root,text="Account: ")
accountlabel.grid(row=1,column=0)
accounttext = Entry(root)
accounttext.grid(row=1,column=1)
createToolTip(accountlabel,"Account name to use to authenticate to the server")
createToolTip(accounttext,"Account name to use to authenticate to the server")

functionlabel= Label(root,text="Function: ")
functionlabel.grid(row=2,column=0)
functiontext = Entry(root)
functiontext.grid(row=2,column=1)
createToolTip(functionlabel,"Python function to initialise the world")
createToolTip(functiontext,"Python function to initialise the world")

packagelabel = Label(root,text="Package: ")
packagelabel.grid(row=3,column=0)
packagetext = Entry(root)
packagetext.grid(row=3,column=1)
createToolTip(packagelabel,"Python package which contains the world "
              "initialisation code")
createToolTip(packagetext,"Python package which contains the world "
              "initialisation code")

passwordlabel = Label(root,text="Password: ")
passwordlabel.grid(row=4,column=0)
passwordtext = Entry(root)
passwordtext.grid(row=4,column=1)
createToolTip(passwordlabel,"Password to use to authenticate to the server")
createToolTip(passwordtext,"Password to use to authenticate to the server")

hostlabel = Label(root,text="Server host: ")
hostlabel.grid(row=5,column=0)
hosttext = Entry(root)
hosttext.grid(row=5,column=1)
createToolTip(hostlabel,"Hostname of the server to connect to")
createToolTip(hosttext,"Hostname of the server to connect to")

pythonportlabel = Label(root,text="Python port: ")
pythonportlabel.grid(row=6,column=0)
pythonporttext = Entry(root)
pythonporttext.grid(row=6,column=1)
createToolTip(pythonportlabel,"Local listen socket for python connections")
createToolTip(pythonporttext,"Local listen socket for python connections")

unixportlabel = Label(root,text="Unix Port: ")
unixportlabel.grid(row=7,column=0)
unixporttext = Entry(root)
unixporttext.grid(row=7,column=1)
createToolTip(unixportlabel,"Local listen socket for admin connections")
createToolTip(unixporttext,"Local listen socket for admin connections")

slaveportlabel = Label(root,text="Slave Unix Port: ")
slaveportlabel.grid(row=8,column=0)
slaveporttext = Entry(root)
slaveporttext.grid(row=8,column=1)
createToolTip(slaveportlabel,"Local listen socket for admin connections to"
              " the slave server")
createToolTip(slaveporttext,"Local listen socket for admin connections to"
              " the slave server")

#A function that is called from the bottom button
#It checks the text to see if anything has been entered
#if it is empty, than it is not used as an argument
def runfunction():
    instance = instancetext.get()
    account = accounttext.get()
    function = functiontext.get()
    package = packagetext.get()
    password = passwordtext.get()
    host = hosttext.get()
    pythonport = pythonporttext.get()
    unixport = unixporttext.get()
    slaveport = slaveporttext.get()

    commandlist=[]
    commandlist.append("./cyclient")

    if(instance != ""):
        commandlist.append("--instance="+instance)
    if(account != ""):
        commandlist.append("--client:account="+account)
    if(function != ""):
        commandlist.append("--client:function="+function)
    if(package != ""):
        commandlist.append("--client:package="+package)
    if(password != ""):
        commandlist.append("--client:password="+password)
    if(host != ""):
        commandlist.append("--client:serverhost="+host)
    if(pythonport != ""):
        commandlist.append("--cyphesis:pythonport="+pythonport)
    if(unixport != ""):
        commandlist.append("--cyphesis:unixport="+unixport)
    if(slaveport != ""):
        commandlist.append("--slave:unixport="+slaveport)

    subprocess.Popen(commandlist)  
        
runbutton = Button(root, text="Run cyclient", command=runfunction)
runbutton.grid(row=9,column=0)
#tool tip for runbutton
createToolTip(runbutton,"Runs cyclient with current arguments")
root.mainloop()
