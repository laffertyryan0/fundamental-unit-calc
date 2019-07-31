##Created by Ryan Lafferty

from math import sqrt
import tkinter as tk

##Return a function representing the norm in R of u = a + b(1+sqrt{d})/2
def norm_R(d):
    def N(a,b):
        return int(a**2 + a*b - (b**2) *(d-1)/4)
    return N

##Find the fundamental solution to the Pell equation x^2 - d y^2 = 1
def fs_pell(d):
    b = 1
    a = 0
    loop = True
    while(loop):
        c = 1 + d * b**2
        if(sqrt(c) == int(sqrt(c))):
            a = int(sqrt(c))
            loop = False
        else:
            b = b+1
    return (a,b)

##Find the fundamental unit of Z[sqrt(d)]. Return a tuple (a,b) representing
## a + b sqrt(d) 
def fu_pell(d):
    fs = fs_pell(d)
    a = fs[0]
    b = fs[1]
    has_sqrt = False
    fu_a = a
    fu_b = b
    for e in range(-a,a):
        fbound = int(a/sqrt(d))+1
        for f in range(-fbound,fbound):
            if((e+f * sqrt(d))**2 == a + b *sqrt(d)):
                fu_a = e
                fu_b = f
    return (fu_a,fu_b)

##Find the fundamental unit of R. That is, the smallest unit u such that u>1.
##Recall that such u = a + b(1+sqrt{d})/2 must have positive b, non-negative a.
##Also note that u must be at least as small as the fundamental unit
##for Z[sqrt(d)]
def fu_R(d):
    dd = (1 + sqrt(d))/2
    b = 1
    a = 0
    fp = fu_pell(d)
    umax = fp[0] + fp[1]*sqrt(d)
    N = norm_R(d)
    fu_a = fp[0]
    fu_b = fp[1]
    while(a < umax):
        b = 1
        while(b<=umax):
            if(a + b * dd < fu_a + fu_b * dd and N(a,b)**2 == 1):
                fu_a = a
                fu_b = b
            b = b + 1
        a = a + 1
    return (fu_a,fu_b)

##A user interface
def prompt():
    print("Welcome to the Fundamental Unit Calculator!")
    again = "Y"
    while(again == "Y"):
        print("Type 1 to find the fundamental solution to the Pell Equation x^2 - d y^2 = 1\n"+
              "Type 2 to find the fundamental unit in Z[sqrt(d)], or\n"+
              "Type 3 to find the fundamental unit in Z[(1+sqrt(d)/2]")
        task = int(input("Select a task (1,2 or 3): "))
        if(task >3 or task < 0):
            print("Invalid response. Please try again.")
        else:
            d = int(input("Enter a positive squarefree value for d: "))
            if(task == 1):
                sol = fs_pell(d)
                print("The fundamental solution to x^2 - "+str(d)+"y^2 = 1 is:\nx=" + str(sol[0])+"\ny="+str(sol[1]))
            if(task == 2):
                sol = fu_pell(d)
                print("The fundamental unit in Z[sqrt(d)] is:\nu="+str(sol[0])+"+"+str(sol[1])+"*sqrt("+str(d)+")")
            if(task == 3):
                sol = fu_R(d)
                print("The fundamental unit in Z[(1+sqrt(d))/2] is:\nu="+str(sol[0])+"+"+str(sol[1])+"*(1+sqrt("+str(d)+"))/2")
            again = input("Press Y to start over or N to exit the program: ")
            
class GUI:
    def __init__(self,master):

        master.title("Fundamental Unit Calculator")

        self.outstr = tk.StringVar()
        
        frame = tk.Frame(master)
        frame.pack()

        welcome = tk.Label(frame,
                           text = "Welcome to the Fundamental Unit Calculator!\n\n\n"
                                   +"Select a task below:")
        welcome.pack(side = tk.TOP)
        
        buttonlabels = ["Find the fundamental solution to a Pell Equation",
                        "Find the fundamental unit in Z[sqrt(d)]",
                        "Find the fundamental unit in Z[(1+sqrt(d))/2]"]

        self.compute_what = tk.IntVar()
        self.compute_what.set(0)

        buttons = []
        
        for i in range(3):
            buttons.append(tk.Radiobutton(frame,
                                       text = buttonlabels[i],
                                       variable = self.compute_what,
                                       value = i))
            buttons[i].pack(anchor = tk.W)

        entrylabel = tk.Label(frame,
                              text = "\n\nEnter a positive squarefree value for d:\n")
        entrylabel.pack()

        self.entrytext = tk.StringVar()
        entry = tk.Entry(frame,
                         textvariable = self.entrytext)
        entry.pack()
        
        enterbutton = tk.Button(frame,
                                text = "Compute",
                                command = self.compute)
        enterbutton.pack()

        out_message = tk.Label(frame,
                            textvariable = self.outstr)
        out_message.pack()
        
    def compute(self):
        try:
            d = int(self.entrytext.get())
            task = self.compute_what.get()
            output = ""
            
            if(task == 0):
                sol = fs_pell(d)
                output = "The fundamental solution to x^2 - "+str(d)+"y^2 = 1 is:\nx=" + str(sol[0])+"\ny="+str(sol[1])
            if(task == 1):
                sol = fu_pell(d)
                output = "The fundamental unit in Z[sqrt(d)] is:\nu="+str(sol[0])+"+"+str(sol[1])+"*sqrt("+str(d)+")"
            if(task == 2):
                sol = fu_R(d)
                output = "The fundamental unit in Z[(1+sqrt(d))/2] is:\nu="+str(sol[0])+"+"+str(sol[1])+"*(1+sqrt("+str(d)+"))/2"

            self.outstr.set("\n\n"+output+"\n\n")
        except:
            pass
        


##Main function
def main():
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
