from enum import Enum
import random
def log(message):
    print(message)

class AntState:
    GETFOOD = "GETFOOD"
    RETURNTOBASE = "RETURNTOBASE"
    EXPLORE = "EXPLORE"
    FIGHTANT = "FIGHTANT"
    FIGHTCOLONY = "FIGHTCOLONY"

class State(Enum):
    DIRT = 1
    EMPTY = 2
    FOOD = 3
    ANT = 4
    COLONY = 5

def getNewPosition(currentPos, move):
    newx = currentPos[0]
    newy = currentPos[1]
    if move == 'E':
        newx += 1
    elif move == 'W':
        newx -= 1
    elif move == 'N':
        newy += 1
    elif move == 'S':
        newy -= 1
    return [newx, newy]

def removeValuesFromList(theList, val):
   return [value for value in theList if value != val]


def getNeutralAntGenome():
    return {
        'startingHunger': 100,
        'startingHealth': 100
        # 'DesireForFood': 1,
        # 'ReturnWhenHungry:': 1,
        # 'DesireToFight': 1,
        # 'ReturnWhenHurt': 1,
        # 'Exploration': 1
    }

def randomName() :
    elements = "Hydrogen,Helium,Lithium,Beryllium,Boron,Carbon,Nitrogen,Oxygen,Fluorine,Neon,Sodium,Magnesium,Aluminum,Silicon,Phosphorus,Sulfur,Chlorine,Argon,Potassium,Calcium,Scandium,Titanium,Vanadium,Chromium,Manganese,Iron,Cobalt,Nickel,Copper,Zinc,Gallium,Germanium,Arsenic,Selenium,Bromine,Krypton,Rubidium,Strontium,Yttrium,Zirconium,Niobium,Molybdenum,Technetium,Ruthenium,Rhodium,Palladium,Silver,Cadmium,Indium,Tin,Antimony,Tellurium,Iodine,Xenon,Cesium,Barium,Lanthanum,Cerium,Praseodymium,Neodymium,Promethium,Samarium,Europium,Gadolinium,Terbium,Dysprosium,Holmium,Erbium,Thulium,Ytterbium,Lutetium,Hafnium,Tantalum,Tungsten,Rhenium,Osmium,Iridium,Platinum,Gold,Mercury,Thallium,Lead,Bismuth,Polonium,Astatine,Radon,Francium,Radium,Actinium,Thorium,Protactinium,Uranium,Neptunium,Plutonium,Americium,Curium,Berkelium,Californium,Einsteinium,Fermium,Mendelevium,Nobelium,Lawrencium,Rutherfordium,Dubnium,Seaborgium,Bohrium,Hassium,Meitnerium,Darmstadtium,Roentgenium,Copernicium,Nihonium,Flerovium,Moscovium,Livermorium,Tennessine,Oganesson"
    return random.choice(elements.split(','))