from tkinter import *
import tkinter.messagebox as tkm

root = Tk()
val = 0
val2 = 0

def op1():

    global e, l, root, val, e2, b, new
    try:
        val = int(e.get())
    except ValueError:
        tkm.showerror("Error", "Enter an int")
    else:
        new = Toplevel()
        e2 = Entry(new)
        e2.pack(side = LEFT)
        b2 = Button(new, text = "OK", command = op2)
        b2.pack(side = RIGHT)
        l2 = Label(new, text = "Enter new number to multiply %d by" %val)
        l2.pack()
        e2.focus_force()
        root.wait_window(new)
        for i in range(5):
            print (i + 1)



def op3():
    root.destroy()

def runLoop():
    global e2, new,l3,val
    new = Toplevel()
    e2 = Entry(new)
    e2.pack(side=LEFT)
    b2 = Button(new, text="OK", command=op2)
    b2.pack(side=RIGHT)
    l2 = Label(new, text="Enter new number ")
    l2.pack()
    l3 = Label(new)
    l3.pack()

    for i in range(5):
        print('running loop for count {}'.format(i))
        e2.focus_force()
        root.wait_window(new)
        print('entered val = {}'.format(val))

    new.destroy()

def op2():
    global val
    try:
        val = int(e2.get())
    except ValueError:
        tkm.showerror("Error", "Enter an int")
        e2.focus_force()
    else:
        #val = val * val2
        l3.config(text = "This is value - {}".format(val) )

        #b.config(command = op3)


e = Entry(root)
e.pack(side = LEFT)
#b = Button(root, text = "OK", command = op1)
b = Button(root, text = "OK", command = runLoop())
b.pack(side = RIGHT)
#l = Label(root, text = "Enter a number")
#l.pack()
root.mainloop()