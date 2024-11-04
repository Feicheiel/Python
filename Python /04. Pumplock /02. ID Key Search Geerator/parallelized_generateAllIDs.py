# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 12:13:26 2023

@author: Eicheiel
"""

from itertools import count
import time
import os.path
import winsound
import shutil
import secrets
import multiprocessing 
#from pathos import multiprocessing


red   = "\x1b[1;31m"
green = "\x1b[1;32m"
blue  = "\x1b[1;34m"
daf   = "\x1b[1;39m"
mag   = "\x1b[1;35m"

literals = (
        '5', '6', '7', '1', '2', '4', '9', '3', '0', '8',
        'I', 'O', 'E', 'H', 'L', 'Z', 'F', 'G', 'J'
    )

characters = ''.join(literals)

def generateID(count: int=7, digitSum: int=7, allow_repetition:bool=False) -> str:
    random_id = ''
    while True :
        # generate a random ID
        random_id = ''.join(secrets.choice(characters) for _ in range(count))
        if not allow_repetition:
            random_id = ''.join(set(random_id))
        
        if len(random_id) == count and sum((literals.index(literal) for literal in random_id))%9 == digitSum:
            break
    
    yield random_id

def worker(count: int):
    return generateID(count, 7, False)

if __name__ == "__main__":
    
    printed = set()
    allow_repetition = False
    count = 7
    digitSum = 7
    counts = [7,7,7,7]
    num_processes = multiprocessing.cpu_count()//2

    fln = f"ID{count:0>{2}}{digitSum:0>{2}}{'R' if allow_repetition else 'NR'}.txt"
    mode = 'a'
    if(os.path.exists(fln)):
        #read into printed.
        with open(fln, 'r') as load:
            printed = set([_id for _id in load.read().strip(',').split(',')])
            print(f'Successfully loaded: {len(printed):,.0f} IDs into memory')
    else:
        with open(fln, 'w') as create:
            create.write("")
    
    blen = len(printed)
    start_len = blen
    duration = 0
    rate = 0
    start = time.time()
    winsound.Beep(440, 500)
    print(f'{"-"*5*len(str(start))}\nStartTime: {time.ctime(start)}')

    while len(printed) < 26_000_000:

        #with multiprocessing.ProcessPool(processes=num_processes) as pool:
        with multiprocessing.Pool(processes=num_processes) as pool:
            ids = set(pool.map(worker, counts))
        
        print(ids)
        if not ids <= printed:    #checks if ids is a subset of printed.
            with open(fln, mode) as add:
                for _id in ids:
                    add.write(f'{_id},')

            printed.union(ids)
        
        print(f'ids <= printed: {ids <= printed}') #diagnostic

        blen = len(printed)
        duration = time.time() - start
        rate = (blen - start_len)

        print(f"{blue}Start count: {start_len:,.0f} {green}Current Total: {blen:,.0f} {red}IDs added: {blen-start_len:,.0f} {mag}Time: {duration:,.0f}s {red}({rate} ID/s)", end=f'\x1B[0G{daf}')
        #print(f"Start count: {start_len:,.0f} Current Total: {blen:,.0f} IDs added: {blen-start_len:,.0f} Time: {duration:,.0f}s ({rate} ID/s)")

    end = time.time()
    print(f'{daf}{len(printed):,.0f} IDs found so far.\nEndTime: {time.ctime(end)}\n\tDuration: ({end - start})')
    winsound.Beep(440, 2000)
