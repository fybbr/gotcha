# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 15:40:16 2020

@author: U004456
"""
from datetime import datetime
import statistics

def create_fix_hash(values_list):
    i = 0
    fix_hash = {}
    while i < (len(values_list)-1):
        fix_hash[values_list[i]] = values_list[i+1]          
        i = i + 2
    
    return fix_hash

def process(fix_hash, no, ou, time):
    if "35" in fix_hash.keys():
        if fix_hash["35"] == "D":
            fix_hash["52"] = time;
            no[fix_hash["11"]] = fix_hash
    
    if "35" in fix_hash.keys() and "150" in fix_hash.keys():
        if fix_hash["35"] == "8" and fix_hash["150"] == "0":
            fix_hash["52"] = time;
            ou[fix_hash["11"]] = fix_hash

def calculate_time_delta(no, ou, count):
    lists = []
    for idx in no:
        
        time_no = no[idx]["52"]
        time_no = datetime.strptime(time_no.split("-")[1], '%H:%M:%S.%f')
        
        #print(time_no)
        
        if idx in ou:
            time_ou = ou[idx]["52"]
            time_ou = datetime.strptime(time_ou.split("-")[1], '%H:%M:%S.%f')
            
            diff = time_ou-time_no
            
            #delta_t = (diff.microseconds / 1000)
            delta_t = diff.total_seconds() * 1000
            
            if delta_t < 1800.0:
                lists.append(delta_t)
            else:
                print(idx)
            
            #if delta_t < 100.0:
                #print(diff.total_seconds() * 1000)
                
            if delta_t > 1800.0:
                #print(time_ou)
                #print(idx)
                #print(delta_t)
                count = count + 1
        
    
    print("Max: "+str(max(lists)))
    print("Min: "+str(min(lists)))
    print("Mean: "+str(statistics.mean(lists)))
    print("STDEV: "+str(statistics.stdev(lists)))
    print("Num orders: "+str(len(lists)))
    print(">1800ms: "+str(count))
    
    
def main():
    no = {}
    ou = {}
    count = 0 
    #with open('C:/Codes/Apama/txt3') as f:
    with open('C:/Users/u004449/Documents/projetcs/gotcha/logs/FIX.4.4-CXPIA818-OE059.messages.current.log') as f:
        for line in f:                
            try:            
                time = line.split(" ")[0]
                values = line.split(" ")[2].rstrip("\n")
                values = values.replace("\x01", "=").split("=")
                fix_hash = create_fix_hash(values)
                process(fix_hash, no, ou, time)
            
            except Exception as ex:
                print(ex)
                print(line)
                pass
    
    calculate_time_delta(no, ou, count)
        
if __name__ == "__main__":
    print("Start grep orders v1.0...")
    try:
        main()
    except KeyboardInterrupt:
        print("Ctrl+C pressed. Stopping...")