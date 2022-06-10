from Manager import *
 
def test():
    manager = Manager()
    # requestes
    id = 0
    # fill up the 4KB and show a split
    for i in range(10):
        request = MemRequest(id,4,"A")
        manager.addRequest(request)
        id += 1
    # add a request that already exists
    request = MemRequest(2,4,"A")
    manager.addRequest(request)
    # fill up the 8KB Blocks
    for i in range(15):
        request = MemRequest(id,8,"A")
        manager.addRequest(request)
        id += 1
    # show the splitting for a bigger block and the allocation of a request below the minAllocation
    for i in range(2):
        request = MemRequest(id, 2, "A")
        manager.addRequest(request)
        id += 1
    #s show allocation of rounding up to the nearest power
    request = MemRequest(id, 6, "A")
    manager.addRequest(request)
    id += 1
    # split entire layer of 64KB for 32KB this will be used to show deallocation warning later with replacement
    for i in range(48):
        request = MemRequest(id,32,"A")
        manager.addRequest(request)
        id += 1
    # remove the layer of 128KB
    for i in range(16):
        request = MemRequest(id,128,"A")
        manager.addRequest(request)
        id += 1
    # if all blocks above are filled the management issues replacement rather than allocation
    request = MemRequest(id, 24, "A")
    manager.addRequest(request)
    id += 1
    # get rid of all 16KB
    for i in range(15):
        request = MemRequest(id,16,"A")
        manager.addRequest(request)
        id += 1
    # replacement example full mememory
    request = MemRequest(id,32,"A")
    manager.addRequest(request)
    id += 1
    #normal write twice
    did = 9
    for i in range(4):
        request = MemRequest(did,4,"W")
        manager.addRequest(request)
        did += -1
    # deallocation with save
    request = MemRequest(9,4,"D")
    manager.addRequest(request)
    # replacemwnt with a save
    for i in range(2):
        request = MemRequest(id,4,"A")
        manager.addRequest(request)
        id += 1
    # example of allocation where no block of that size exists # change to W to showcase that
    request = MemRequest(id,56,"A")
    manager.addRequest(request)
    id += 1
    # normal deallocation example
    request = MemRequest(74,32,"D")
    manager.addRequest(request)
    # pairing example previous delayed block should be available for above allocation
    request = MemRequest(75,32,"D")
    manager.addRequest(request)
    # set up deallocation
    did = 73
    for i in range(2):
        request = MemRequest(did,32,"D")
        manager.addRequest(request)
        did += -1
    # write to something not in memory
    request = MemRequest(id, 64, "W")
    manager.addRequest(request)
 
    request = MemRequest(200, 64, "D")
    manager.addRequest(request)
    # start
    manager.run()
 
if __name__ == "__main__":
    test()
 
