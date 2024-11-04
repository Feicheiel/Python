# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 12:13:26 2023

@author: Eicheiel
"""

import time
import os.path
import winsound
import shutil
import secrets


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

def generateAllIDs(count: int=7, digitSum: int=7, allow_repetition: bool=False):
    printed = set()

    fln = f"ID{count:0>{2}}{digitSum:0>{2}}{'R' if allow_repetition else 'NR'}.txt"
    mode = 'a'
    if(os.path.exists(fln)):
        #read into print.
        with open(fln, 'r') as load:
            printed = set([_id for _id in load.read().strip(',').split(',')])
            print(f'Successfully loaded: {len(printed):,.0f} IDs into memory')
    else:
        with open(fln, 'w') as create:
            create.write("")
    
    blen = len(printed)
    times_counter = 0
    times = 1_000
    start_len = blen
    duration = 0
    rate = 0
    start = time.time()
    winsound.Beep(440, 500)
    print(f'{"-"*5*len(str(start))}\nStartTime: {time.ctime(start)}')

    while len(printed) < 26_000_000:
        _id = generateID(count, digitSum, allow_repetition)
        times_counter += 1
        if _id not in printed:
            with open(fln, mode) as add:
                add.write(f'{_id},')
            printed.add(_id)

        blen = len(printed)
        duration = time.time() - start
        rate = (blen - start_len)//duration

        # Get the total memory usage in bytes.
        # total_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

        # Convert the memory usage to megabytes.
        #total_memory_mb = total_memory / 1024 ** 2

        # Print the memory usage.
        #print("Total memory usage:", total_memory_mb, "MB")
        print(f"{blue}Start count: {start_len:,.0f} {green}Current Total: {blen:,.0f} {red}IDs added: {blen-start_len:,.0f} {mag}Time: {duration:,.0f}s {red}({rate} ID/s)", end=f'\x1B[0G{daf}')
        #print(gc.get_stats())

    end = time.time()
    print(f'{daf}{len(printed):,.0f} IDs found so far.\nEndTime: {time.ctime(end)}\n\tDuration: ({end - start})')
    winsound.Beep(440, 2000)


generateAllIDs(7, 7) 