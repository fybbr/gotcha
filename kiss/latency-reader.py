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

def process(fix_hash, no, ou_no, am, ou_am, ca, ou_ca, time):
    if "35" in fix_hash.keys():
        if fix_hash["35"] == "D": #NewOrder
            fix_hash["52"] = time;
            no[fix_hash["11"]] = fix_hash
        elif fix_hash["35"] == "G": #Amend
            fix_hash["52"] = time;
            am[fix_hash["11"]] = fix_hash
        elif fix_hash["35"] == "F": #Cancel
            fix_hash["52"] = time;
            ca[fix_hash["11"]] = fix_hash
            
    if "35" in fix_hash.keys() and "150" in fix_hash.keys():
        if fix_hash["35"] == "8" and fix_hash["150"] == "0": #NewOrder -> NEW
            fix_hash["52"] = time;
            ou_no[fix_hash["11"]] = fix_hash
        elif fix_hash["35"] == "8" and fix_hash["150"] == "5": #Amend -> Replaced
            fix_hash["52"] = time;
            ou_am[fix_hash["11"]] = fix_hash
        elif fix_hash["35"] == "8" and fix_hash["150"] == "4": #Cancel -> Cancelled
            fix_hash["52"] = time;
            ou_ca[fix_hash["11"]] = fix_hash
            
def calculate_time_delta(no, ou, count):
    lists = []
    for idx in no:
        time_no = no[idx]["52"]
        time_no = datetime.strptime(time_no.split("-")[1], '%H:%M:%S.%f')
        
        if idx in ou:
            time_ou = ou[idx]["52"]
            time_ou = datetime.strptime(time_ou.split("-")[1], '%H:%M:%S.%f')
            
            diff = time_ou-time_no
            delta_t = diff.total_seconds() * 1000
            
            if delta_t < 1800.0:
                lists.append(delta_t)
            #else:
             #   print(str(time_no).split(" ")[1] + " - " +str(idx) + " = "+str(delta_t) + "ms")
            
            if delta_t > 1800.0:
                count = count + 1
        
    
    print("Max: "+str(max(lists)))
    print("Min: "+str(min(lists)))
    print("Mean: "+str(statistics.mean(lists)))
    print("STDEV: "+str(statistics.stdev(lists)))
    print("Num: "+str(len(lists)))
    print(">1800ms: "+str(count))
    
    
def main():
    no = {} #NewOrder
    am = {} #Amend
    ca = {} #Cancel
    
    ou_no = {} #OrderUpdate New
    ou_am = {} #OrderUpdate Amend
    ou_ca = {} #OrderUpdate Cancel
    
    count_no = 0 #NewOrder outlier counter
    count_am = 0 #Amend outlier counter
    count_ca = 0 #Cancel outlier counter
    
    with open('C:/Users/u004449/Documents/projetcs/gotcha/logs/FIX.4.4-CXPIA818-OE059.messages.current.log') as f:
        for line in f:                
            try:            
                time = line.split(" ")[0]
                values = line.split(" ")[2].rstrip("\n")
                values = values.replace("\x01", "=").split("=")
                fix_hash = create_fix_hash(values)
                process(fix_hash, no, ou_no, am, ou_am, ca, ou_ca, time)
            
            except Exception as ex:
                print(ex)
                print(line)
                pass
    
    print("#NewOrder")
    calculate_time_delta(no, ou_no, count_no)
    print("")
    print("#Amend")
    calculate_time_delta(am, ou_am, count_am)
    print("")
    print("#Cancel")
    calculate_time_delta(ca, ou_ca, count_ca)
        
if __name__ == "__main__":
    print("Start grep orders v1.7.2...")
    try:
        main()
    except KeyboardInterrupt:
        print("Ctrl+C pressed. Stopping...")