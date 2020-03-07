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
            self.block_list = []
            self.indirect_block_list = []
            if self.file_type is 'd' or self.file_type is 'f':
                for i in range(12):
                    self.block_list.append(int(info_list[12+i]))
                for i in range(12,15):
                    self.indirect_block_list.append(int(info_list[12+i]))
            
class Dirent:
    def __init__(self, info_list):
        if info_list is not None:
            self.parent_inode = int(info_list[1])
            self.offset = int(info_list[2])
            self.file_inode = int(info_list[3])
            self.entry_length = int(info_list[4])
            self.name_length = int(info_list[5])            
            self.name = info_list[6]

class Block:
     def __init__(self, info_list, block):
        if info_list is not None:
            self.status = 'ALLOCATED'
            self.inode = int(info_list[1])
            self.indirection = int(info_list[2])
            self.offset = int(info_list[3])
            self.block = block
            self.duplicate_list = []
        else:
            self.status = 'FREE'      # FREE / RESERVED / ALLOCATED / DUPLICATED 
            self.inode = 0
            self.block = block
            self.indirection = 0
            self.offset = 0
            self.duplicate_list = []


# helper function: convert int indirection level to string 
def ind_to_str(num):
    if num == 1 :
        return "INDIRECT"
    elif num == 2:
        return "DOUBLE INDIRECT"
    elif num == 3:
        return "TRIPLE INDIRECT"
    return ""

            
def main():
    error_count = 0
    # parse arguments
    args = sys.argv
    if len(args) != 2:
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
    blocks = {}           # allocated blocks
    dirents = []           # directory entries
    
    for line in fs_data:
        if line[0] == 'SUPERBLOCK':
            sb = Superblock(line)
        if line[0] == 'GROUP':
            group = Group(line)

    i_freelist = []     # inode bitmap (a list of IFREE inode numbers)
    b_freelist = []     # block bitmap (a list of BFREE block numbers)

    for i in range(group.total_blocks):
        blocks[i] = Block(None, i)

    for i in range(group.i_table + (group.total_inodes * sb.inode_size / sb.block_size)):
        blocks[i].status = 'RESERVED'
        
    for line in fs_data:
        if line[0] == 'IFREE':
            i_freelist.append(int(line[1]))
        if line[0] == 'BFREE':
            b_freelist.append(int(line[1]))
        if line[0] == 'INODE':
            inodes[int(line[1])] = Inode(line)
        if line[0] == 'DIRENT':
            dirents.append(Dirent(line))
        if line[0] == 'INDIRECT':
            blocks[int(line[5])] = Block(line, int(line[5]))
            inodes[int(line[1])].indirect_block_list.append(int(line[5]))

    # check blocks
    for i in range(1,group.total_inodes+1):
        if i not in inodes or inodes[i].file_type == '0':
            continue
        offset = 0

        for b in (inodes[i].block_list + inodes[i].indirect_block_list):
            if b == 0:
                offset += 1
                continue
            # check invalid blocks 
            if b < 0 or b >= group.total_blocks:
                if b in inodes[i].block_list:
                    print("INVALID BLOCK %d IN INODE %d AT OFFSET %d" % (b, i, offset))
                    error_count += 1
                elif offset == 12:
                    print("INVALID %s BLOCK %d IN INODE %d AT OFFSET %d" % (ind_to_str(offset-11), b, i, offset))
                    error_count += 1
                elif offset == 13:
                    print("INVALID %s BLOCK %d IN INODE %d AT OFFSET %d" % (ind_to_str(offset-11), b, i, 268))
                    error_count += 1
                elif offset == 14:
                    print("INVALID %s BLOCK %d IN INODE %d AT OFFSET %d" % (ind_to_str(offset-11), b, i, 65804))
                    error_count += 1
                else:  # deeper indirect blocks
                    print("INVALID %s BLOCK %d IN INODE %d AT OFFSET %d" % (ind_to_str(blocks[b].indirection), b, i, blocks[b].offset))
                    error_count += 1
                offset += 1
                continue

            # check reserved blocks
            if b < group.i_table + (group.total_inodes * sb.inode_size / sb.block_size):
                if b in inodes[i].block_list:
                    print("RESERVED BLOCK %d IN INODE %d AT OFFSET %d" % (b, i, offset))
                    error_count += 1
                elif offset == 12:
                    print("RESERVED %s BLOCK %d IN INODE %d AT OFFSET %d" % (ind_to_str(offset-11), b, i, offset))
                    error_count += 1
                elif offset == 13:
                    print("RESERVED %s BLOCK %d IN INODE %d AT OFFSET %d" % (ind_to_str(offset-11), b, i, 268))
                    error_count += 1
                elif offset == 14:
                    print("RESERVED %s BLOCK %d IN INODE %d AT OFFSET %d" % (ind_to_str(offset-11), b, i, 65804))
                    error_count += 1
                else:  # deeper indirect blocks
                    print("RESERVED %s BLOCK %d IN INODE %d AT OFFSET %d" % (ind_to_str(blocks[b].indirection), b, i, blocks[b].offset))
                    error_count += 1
                offset += 1
                continue
            
            # register block status
            if blocks[b].status == "FREE":    # only possible for blocks referenced inside inode
                blocks[b].status = "ALLOCATED"
                blocks[b].inode = i
                blocks[b].block = b
                if offset in range(0,12):
                    blocks[b].indirection = 0
                    blocks[b].offset = offset
                elif offset == 12:
                    blocks[b].indirection = 1
                    blocks[b].offset = offset
                elif offset == 13:
                    blocks[b].indirection = 2
                    blocks[b].offset = 268
                elif offset == 14:
                    blocks[b].indirection = 3
                    blocks[b].offset = 65804
                
                blocks[b].duplicate_list = []
                
            #elif blocks[b].status == "RESERVED":     # already checked
            #    pass
            elif (blocks[b].status == "ALLOCATED" or blocks[b].status == "DUPLICATED") and blocks[b].inode != i:
                new_block = Block(None, b)
                new_block.status = "ALLOCATED"
                new_block.inode = i
                new_block.block = b
                if offset in range(0,12):
                    new_block.indirection = 0
                    new_block.offset = offset
                elif offset == 12:
                    new_block.indirection = 1
                    new_block.offset = offset
                elif offset == 13:
                    new_block.indirection = 2
                    new_block.offset = 268
                elif offset == 14:
                    new_block.indirection = 3
                    new_block.offset = 65804
                blocks[b].status = "DUPLICATED"
                blocks[b].duplicate_list.append(new_block)

            offset += 1

    # check duplicates:
    for b in blocks.values():
        if b.status == "DUPLICATED":
            if b.indirection == 0:
                print("DUPLICATE BLOCK %d IN INODE %d AT OFFSET %d" % (b.block, b.inode, b.offset))
                error_count += 1
            else:
                print("DUPLICATE %s BLOCK %d IN INODE %d AT OFFSET %d" % (ind_to_str(b.indirection), b.block, b.inode, b.offset))
                error_count += 1
            for d in b.duplicate_list:
                if d.indirection == 0:
                    print("DUPLICATE BLOCK %d IN INODE %d AT OFFSET %d" % (d.block, d.inode, d.offset))
                    error_count += 1
                else:
                    print("DUPLICATE %s BLOCK %d IN INODE %d AT OFFSET %d" % (ind_to_str(d.indirection), d.block, d.inode, d.offset))
                    error_count += 1

    # check unreferenced blocks and allocated blocks on freelist
    for i in range(len(blocks)):
        if blocks[i].status == "ALLOCATED" or blocks[i].status == "DUPLICATED":
            if i in b_freelist:
                print("ALLOCATED BLOCK %d ON FREELIST" % i)
                error_count += 1
        elif blocks[i].status == "FREE":
            if i not in b_freelist:
                print("UNREFERENCED BLOCK %d" % i)
                error_count += 1

    # check inodes
    for i in range(1,group.total_inodes+1):
        if i not in inodes or inodes[i].file_type == '0':
            if(i >= sb.first_inode and (i not in i_freelist)):
                print("UNALLOCATED INODE %d NOT ON FREELIST" % i)
                error_count += 1
        else:
            if(i in i_freelist):
                print("ALLOCATED INODE %d ON FREELIST" % i)
                error_count += 1
    
    if error_count:
        exit(2)
    exit(0)

    
if __name__ == '__main__':
    main()
