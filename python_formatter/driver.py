import filecmp
import glob
import difflib
from basicformatter import Formatter

def main():
    
    testinputs = glob.glob('tests/in*')
    testinputs.sort()
    testoutputs = glob.glob('tests/out*')
    testoutputs.sort()
    
    for counter, file in enumerate(testinputs):
        formatter = Formatter(file)
        formattedlines = formatter.format()
        with open('tests/output.txt', "w") as f:
            for line in formattedlines:
                f.write(line)
        print("Test %d: " % counter,
                filecmp.cmp('tests/output.txt', testoutputs[counter]))
        if not filecmp.cmp('tests/output.txt', testoutputs[counter]):
            print("Failed on test", testoutputs[counter])
            text1 = open('tests/output.txt').readlines()
            text2 = open(testoutputs[counter]).readlines()
            for line in difflib.unified_diff(text1, text2):
                print(line) 
            break

if __name__=="__main__":
    main()
