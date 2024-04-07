# PA1 Surya Raghavendran, Vedant Grover, Shrey Patel
from collections import Counter
import math
import sys

#Example Command python PA1Final.py /filespace/s/suryar/ece556/ece556/PA1/input_pa1/input_5.dat /filespace/s/suryar/ece556/ece556/PA1/input_pa1/output5.dat

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        balance_factor = float(file.readline().strip())  # Read the balance factor from the first line

        nets = []  
        uniqueCells = set()  
        totalCells = []  

        current_line = ""  

       
        for line in file:
            # Check if the current line is part of a net description
            if "NET" in line or ";" not in current_line:
                current_line += " " + line.strip()  # Accumulate the line

            # Check if the end of a net description is reached
            if ";" in current_line:
               
                current_line = current_line.replace("NET", "").strip()  
                parts = current_line.split(";")[0].strip().split()  
                net_name = parts[0] 
                cells = parts[1:] 

                for cell in cells:
                    uniqueCells.add(cell)  
                    totalCells.append(cell)  

                nets.append({"net_name": net_name, "cells": cells})  

                current_line = ""  

    return balance_factor, nets, uniqueCells, totalCells

#Main Function
def FMPartioner(input_file_path, output_filepath):
    balance_factor, nets, uniqueCells, totalCells = read_input_file(input_file_path)

    #Net Calculations
    sizeG1 = math.ceil((len(uniqueCells)*(1-balance_factor))/2)
    sizeG2 = math.floor((len(uniqueCells)*(1+balance_factor))/2)

    # Ordering the Cells based on frequency
    orderedcells  = list(dict(Counter(totalCells).most_common()).keys())
    G1CellVals = orderedcells[-sizeG1:]
    G2CellVals = orderedcells[:-sizeG1]
    
    #Output Data
    Cutsize = 0
    
    #Preallocation
    G1CellVals_set = set(G1CellVals)
    G2CellVals_set = set(G2CellVals)
    for i in range(len(nets)):
        cell_val = set(nets[i]['cells'])
        if not((cell_val <= G1CellVals_set) or (cell_val <= G2CellVals_set)):
            Cutsize = Cutsize + 1

    #Write Output File
    with open(output_filepath, 'w') as file:

        # Write the Cutsize and group sizes
        file.write("Cutsize = " + str(Cutsize) + "\n")
        file.write("G1 " + str(sizeG1) + "\n")
        
        # Join G1CellVals and G2CellVals into a string and append a semicolon, then write to file
        g1_cells = " ".join(G1CellVals) + " ;"
        file.write(g1_cells + "\n")
        file.write("G2 " + str(sizeG2) + "\n")
        g2_cells = " ".join(G2CellVals) + " ;"
        file.write(g2_cells + "\n")

#Call Function from Terminal
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py input_file_path output_file_path")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    
    FMPartioner(input_file_path, output_file_path)