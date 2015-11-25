import sys
import path_generator as PG
import Tkinter as tk

def main(argv=None):
    filename = str(raw_input("What image would you like to test? "))
    if (len(filename) == 0):
        filename = "demo1.png"
    array = PG.getPixelArrayForFilename(filename)
    # PG.printBlackEnoughArray(array)
    array = PG.getBoolArray(array)
    # PG.printPixelArray(array)
    vec = PG.getRawPaths(array)

    gFrame = tk.Tk()
    gFrame.geometry('600x500')

    w = tk.Canvas(gFrame, width=200, height=100)
    w.pack()

    w.create_rectangle(0, 0, len(array[0])*20, len(array)*20,)

    for edge in vec:
        w.create_line(edge[0][1]*20, edge[0][0]*20, edge[1][1]*20, edge[1][0]*20)


    gFrame.mainloop()

if __name__ == "__main__":
    sys.exit(main())
