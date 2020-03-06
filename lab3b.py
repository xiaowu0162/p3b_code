#!/usr/bin/python
# NAME: Di Wu,Jingnong Qu
# EMAIL: xiaowu200031@gmail.com,andrewqu2000@g.ucla.edu
# ID: 205117980,805126509

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
