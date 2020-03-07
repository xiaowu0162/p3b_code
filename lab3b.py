#!/usr/bin/python
# NAME: Di Wu,Jingnong Qu
# EMAIL: xiaowu200031@gmail.com,andrewqu2000@g.ucla.edu
# ID: 205117980,805126509

import sys

class Superblock:
    def __init__(self, info_list):
        if info_list is not None:
            self.total_blocks = int(info_list[1])
            self.total_inodes = int(info_list[2])
            self.block_size = int(info_list[3])
            self.inode_size = int(info_list[4])
            self.b_per_group = int(info_list[5])
            self.i_per_group = int(info_list[6])
            self.first_inode = int(info_list[7])
        
class Group:
    def __init__(self, info_list):
        if info_list is not None:
            self.total_blocks = int(info_list[2])
            self.total_inodes = int(info_list[3])
            self.free_blocks = int(info_list[4])
            self.free_inodes = int(info_list[5])
            self.b_bmap = int(info_list[6])
            self.i_bmap = int(info_list[7])
            self.i_table = int(info_list[8])


class Inode:
    def __init__(self, info_list):
        if info_list is not None:
            self.i_number = int(info_list[1])
            self.file_type = info_list[2]
            self.link_count = int(info_list[6])
            self.file_size = int(info_list[10])
            self.n_blocks = int(info_list[11])

class Dirent:
    def __init__(self, info_list):
        if info_list is not None:
            self.parent_inode = int(info_list[1])
            self.offset = int(info_list[2])
            self.file_inode = int(info_list[3])
            self.entry_length = int(info_list[4])
            self.name_length = int(info_list[5])            
            self.name = info_list[6]


def main():
    # parse arguments
    args = sys.argv
    if len(args) is not 2:
        print('Error: wrong number of arguments.')
        print('Usage: lab3b some_file.csv')
        exit(1)

    # open file and read lines 
    try:
        fs_data = [line.rstrip('\n').split(',') for line in open(args[1], 'r')]
    except:
        print("Error: specified file does not exist.")
        exit(1)

    # generate basic data structures 
    sb = Superblock(None)
    group = Group(None)
    inodes = {}           # allocated inodes
    dirents = []           # directory entries
    
    for line in fs_data:
        if line[0] == 'SUPERBLOCK':
            sb = Superblock(line)
        if line[0] == 'GROUP':
            group = Group(line)

    i_freelist = [0 for i in range(group.total_inodes)]     # inode bitmap
    b_freelist = [0 for i in range(group.total_blocks)]     # block bitmap
    
    for line in fs_data:
        if line[0] == 'IFREE':
            i_freelist[int(line[1]) - 1] = 1
        if line[0] == 'BFREE':
            b_freelist[int(line[1])] = 1            # ????????
        if line[0] == 'INODE':
            inodes[int(line[1])] = Inode(line)
        if line[0] == 'DIRENT':
            dirents.append(Dirent(line))



    # TO-DO: determine exit code 


    
if __name__ == '__main__':
    main()
