#!/usr/bin/python

import sys

def main():
    # parse arguments
    args = sys.argv
    if len(args) is not 2:
        print('Error: wrong number of arguments.')
        print('Usage: lab3b some_file.csv')
        exit(1)

    # open file and read lines 
    try:
        fs_data = [line.rstrip('\n') for line in open(args[1], 'r')]
    except:
        print("Error: specified file does not exist.")
        exit(1)


    #print(fs_data)

    
    # TO-DO: determine exit code 


    
if __name__ == '__main__':
    main()
