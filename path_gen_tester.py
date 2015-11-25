import sys
import path_generator as PG
import Tkinter as tk

def main(argv=None):
    filename = str(raw_input("What image would you like to test? "))
    if (len(filename) == 0):
        filename = "demo2.png"
    array = PG.getPixelArrayForFilename(filename)
    # PG.printBlackEnoughArray(array)
    array = PG.getBoolArray(array)
    # PG.printPixelArray(array)
    paths = PG.getRawPaths(array)
    # mask = PG.getInversionMask(vec, array)
    # PG.printPixelArray(mask)
    # PG.invertForMask(array, mask)
    # PG.print01Array(array)

    gFrame = tk.Tk()
    gFrame.geometry('800x600')

    w = tk.Canvas(gFrame, width=800, height=600)
    w.pack()

    w.create_rectangle(0, 0, len(array[0])*20, len(array)*20,)

    scale = 400/len(array)

    for vec in paths:
        for edge in vec:
            w.create_line(edge[0][1]*scale, edge[0][0]*scale, edge[1][1]*scale, edge[1][0]*scale)


    gFrame.mainloop()

if __name__ == "__main__":
    sys.exit(main())
