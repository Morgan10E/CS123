import sys
import path_generator as PG

def main(argv=None):
    filename = str(raw_input("What image would you like to test? "))
    array = PG.getPixelArrayForFilename(filename)
    PG.printBlackEnoughArray(array)
    array = PG.getBoolArray(array)
    PG.printPixelArray(array)

if __name__ == "__main__":
    sys.exit(main())
