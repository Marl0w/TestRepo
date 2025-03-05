# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 15:24:33 2025

@author: m-wei
"""



import zipfile
import random

# Path to the ZIP file
zip_file_path = './mechfiles/mechs.zip'

"""
# Code for when you want to choose what mech.
mechSource = input('Enter Mech Source (ex. "3039u"): ')
mechName = input('Enter Mech Name (ex. "Atlas AS7-D"): ')
"""
def readBasics(content):
    """
    Extracts the basics of the mech (Chassis, Model, Armor Type, Internal Type) 
    and returns them as a string variables (ex. v = f"Chassis: {chassis}")
    """  
    # Initialize variables
    chassis = None
    model = None
    armor = None
    structure = None
    mass = None

    # Decode the byte content if necessary (assuming UTF-8 encoded)
    decoded_content = content.decode('utf-8')

    # Read the file content line by line
    for line in decoded_content.splitlines():
        # Check if the line contains a colon
        if ':' in line:
            key, value = line.strip().split(':', 1)  # Split only on the first colon

            # Assign values to variables based on the key
            if key.lower() == "chassis":
                chassis = value
            elif key.lower() == "model":
                model = value
            elif key.lower() == "armor":
                armor = value
            elif key.lower() == "structure":
                structure = value
            elif key.lower() == "mass":
                mass = value
                
    # Return the assigned variables
    return chassis, model, armor, structure, mass

def readArmor(content):
    """
    Reads armor values for the mech and converts into a dictionary with format
    '{Location: Armor Value}'
    """
    # Initialize variables (armor dictionary)
    armorDict = {}

    # Decode the byte content if necessary (assuming UTF-8 encoded) 
    decoded_content = content.decode('utf-8')
    for line in decoded_content.splitlines():
        # Check if the line contains a colon
        if ':' in line:
            key, value = line.strip().split(':', 1)  # Split only on the first colon

            # Assign values to variables based on the key
            if key.lower() == "la armor":
                armorDict["LA"] = int(value)
            elif key.lower() == "ra armor":
                armorDict["RA"] = int(value)
            elif key.lower() == "lt armor":
                armorDict["LT"] = int(value)
            elif key.lower() == "rt armor":
                armorDict["RT"] = int(value)
            if key.lower() == "ct armor":
                armorDict["CT"] = int(value)
            elif key.lower() == "hd armor":
                armorDict["HD"] = int(value)
            elif key.lower() == "ll armor":
                armorDict["LL"] = int(value)
            elif key.lower() == "rl armor":
                armorDict["RL"] = int(value)                
            if key.lower() == "rtl armor":
                armorDict["RTL"] = int(value)
            elif key.lower() == "rtr armor":
                armorDict["RTR"] = int(value)
            elif key.lower() == "rtc armor":
                armorDict["RTC"] = int(value)

    return armorDict

def readInternal(content):
    """
    Function contains dictionary of dictionaries, and pulls correct one based
    on mech tonnage for later use.
    """
    internalDict = {
        '20' : {'LA': 3, 'RA': 3, 'LT': 5, 'RT': 5, 'CT': 6, 'HD': 3, 'LL': 4, 'RL': 4},
        '25' : {'LA': 4, 'RA': 4, 'LT': 6, 'RT': 6, 'CT': 8, 'HD': 3, 'LL': 6, 'RL': 6},
        '30' : {'LA': 5, 'RA': 5, 'LT': 7, 'RT': 7, 'CT': 10, 'HD': 3, 'LL': 7, 'RL': 7},
        '35' : {'LA': 6, 'RA': 6, 'LT': 8, 'RT': 8, 'CT': 11, 'HD': 3, 'LL': 8, 'RL': 8},
        '40' : {'LA': 6, 'RA': 6, 'LT': 10, 'RT': 10, 'CT': 12, 'HD': 3, 'LL': 10, 'RL': 10},
        '45' : {'LA': 7, 'RA': 7, 'LT': 11, 'RT': 11, 'CT': 14, 'HD': 3, 'LL': 11, 'RL': 11},
        '50' : {'LA': 8, 'RA': 8, 'LT': 12, 'RT': 12, 'CT': 16, 'HD': 3, 'LL': 12, 'RL': 12},
        '55' : {'LA': 9, 'RA': 9, 'LT': 13, 'RT': 13, 'CT': 18, 'HD': 3, 'LL': 13, 'RL': 13},       
        '60' : {'LA': 10, 'RA': 10, 'LT': 14, 'RT': 14, 'CT': 20, 'HD': 3, 'LL': 15, 'RL': 15},
        '65' : {'LA': 10, 'RA': 10, 'LT': 14, 'RT': 14, 'CT': 21, 'HD': 3, 'LL': 15, 'RL': 15},
        '70' : {'LA': 11, 'RA': 11, 'LT': 15, 'RT': 15, 'CT': 22, 'HD': 3, 'LL': 15, 'RL': 15},
        '75' : {'LA': 12, 'RA': 12, 'LT': 16, 'RT': 16, 'CT': 23, 'HD': 3, 'LL': 16, 'RL': 16},
        '80' : {'LA': 13, 'RA': 13, 'LT': 17, 'RT': 17, 'CT': 25, 'HD': 3, 'LL': 17, 'RL': 17},
        '85' : {'LA': 14, 'RA': 14, 'LT': 18, 'RT': 18, 'CT': 27, 'HD': 3, 'LL': 18, 'RL': 18},
        '90' : {'LA': 15, 'RA': 15, 'LT': 19, 'RT': 19, 'CT': 29, 'HD': 3, 'LL': 19, 'RL': 19},
        '95' : {'LA': 16, 'RA': 16, 'LT': 20, 'RT': 20, 'CT': 30, 'HD': 3, 'LL': 20, 'RL': 20},
        '100': {'LA': 17, 'RA': 17, 'LT': 21, 'RT': 21, 'CT': 31, 'HD': 3, 'LL': 21, 'RL': 21}
        }
    chassis, model, armor, structure, mass = readBasics(content)
    internal = internalDict[f'{mass}']
    return internal

def readCrits(content):
    """
    Reads the crititcal slots assigned to each limb and generates a list for each limb
    """  
    
    # Initialize variables
    critLA = []
    critRA = []
    critLT = []
    critRT = []
    critCT = []
    critHD = []
    critLL = []
    critRL = []
    critDict = {}
    critCurrent = None

    
    # Decode the byte content if necessary (assuming UTF-8 encoded)
    decoded_content = content.decode('utf-8')

    # Read the file content line by line
    for line in decoded_content.splitlines():
        line = line.strip()
        # Determine which slot to add to: "Left Arm:", "Right Arm:", etc.
        if line == "Left Arm:":
            critCurrent = critLA
        elif line == "Right Arm:":
            critCurrent = critRA
        elif line == "Left Torso:":
            critCurrent = critLT
        elif line == "Right Torso:":
            critCurrent = critRT
        elif line == "Center Torso:":
            critCurrent = critCT
        elif line == "Head:":
            critCurrent = critHD
        elif line == "Left Leg:":
            critCurrent = critLL
        elif line == "Right Leg:":
            critCurrent = critRL
        # Add non-empty crit slots to currently open list
        elif critCurrent is not None and line and line != "-Empty-":
            critCurrent.append(line)
        # Reset current crit list if encounters empty line
        elif not line:
            critCurrent = None
                    
    # Move all the crit lists into the dictionary
    for var_name, var_value in locals().items():
        if var_name.startswith('crit') and isinstance(var_value, list):
            critDict[var_name] = var_value            
                
                
                
    # Return the assigned variables
    return critLA, critRA, critLT, critRT, critCT, critHD, critLL, critRL, critDict
    
def assignDamage(content):
    """
    Takes an integer input and randomly assigns it in groups of 'n' (decided by user)
    """
    
    # Pull armor and internal from respective functions
    damageDict = readArmor(content) #dictionary ({'Limb': Integer})
    internal = readInternal(content) #dictionary ({'Limb': Integer})
    
    # Damage Table, to refer random number to
    facingDict = {
        'front': {2: 'CT', 3: 'RA', 4: 'RA', 5: 'RL', 6: 'RT', 7: 'CT', 8: 'LT', 9: 'LL', 10: 'LA', 11: 'LA', 12: 'HD'},
        'rear': {2: 'RTC', 3: 'RA', 4: 'RA', 5: 'RL', 6: 'RTR', 7: 'RTC', 8: 'RTL', 9: 'LL', 10: 'LA', 11: 'LA', 12: 'HD'},
        'left': {2: 'LT', 3: 'LL', 4: 'LA', 5: 'LA', 6: 'LL', 7: 'LT', 8: 'CT', 9: 'RT', 10: 'RA', 11: 'RL', 12: 'HD'},
        'right': {2: 'RT', 3: 'RL', 4: 'RA', 5: 'RA', 6: 'RL', 7: 'RT', 8: 'CT', 9: 'LT', 10: 'LA', 11: 'LL', 12: 'HD'},
        }
   
    # Preset input for testing
    facing = 'front'
    damage = 16
    grouping = 5
    
    """
    # User input
    facing = input("Unit Facing (Front, Rear, Left, or Right): ").lower()
    damage = int(input("Amount of Damage: "))
    grouping = int(input("Grouping Number: "))
    """
    
    # determine the total number of groups of damage, as well as any remainder group    
    fullGroups = damage // grouping
    remainderGroup = damage % grouping
    
    #assign damage groups to armor based on results of 2d6 roll
    facingDict = facingDict[facing]
    # full groupings
    for i in range(fullGroups):
        rollLocation = (random.randint(1,6) + random.randint(1,6))
        location = facingDict[rollLocation]
        damageDict[location] -= grouping
    # remainder grouping
    rollLocation = (random.randint(1,6) + random.randint(1,6))
    location = facingDict[rollLocation]
    damageDict[location] -= remainderGroup
    
    return damageDict


    
    
    
# Open the ZIP file and extract the specific file content
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    """
    # List the files in the ZIP to check the exact path
    zip_ref.printdir()
    """
    
    # Specify the file name inside the ZIP
    # For Testing, remove next line when you want input
    file_name = '3039u/Atlas AS7-D.mtf'
    
    
    """
    # Code for when you want to input mech name
    file_name = f'{mechSource}/{mechName}.mtf'
    """
    
    # Open the specific file inside the ZIP and read the content
    with zip_ref.open(file_name) as file:
        content = file.read()  # Read the content of the file

    # Call readBasics function with the content read from the file
    chassis, model, armor, structure, mass = readBasics(content)
    armorDict = readArmor(content)
    internalHP = readInternal(content)
    damagedHull = assignDamage(content)
    
    # Print the extracted data
    print(f"Chassis: {chassis}")
    print(f"Model: {model}")
    print(f"Armor: {armor}")
    print(f"Structure: {structure}")
    print(f"Mass: {mass}")
    print("")
    print("Armor:")
    for key, value in armorDict.items():
        print (f"{key}: {value}")
    print("")
    print("Internal")
    for key, value in internalHP.items():
        print (f"{key}: {value}")
        
