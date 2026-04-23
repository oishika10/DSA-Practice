import re

class Command:
    def __init__(self, mainCommand: str, shortFlags: dict, longFlags: dict, arguments: list):
        self.mainCommand = mainCommand
        self.shortFlags = shortFlags
        self.longFlags = longFlags
        self.arguments = arguments

SCHEMA = {
    "short_flags": {
        "v": {"type": "bool"},
        "p": {"type": "int", "required": True}, # Needs a value
        "f": {"type": "string"}
    },
    "long_flags": {
        "verbose": {"type": "bool"},
        "output": {"type": "string", "choices": ["json", "text"]}
    }
}

def getUserInput():
    while (True):
        try:
            command = input(">> ")
            splitCommanddsList = [arg for arg in command.split(" ") if arg.strip()]
            mainCommand = splitCommanddsList[0]
            shortFlags: list = {}
            longFlags: dict = {}
            arguments: list = []

            i: int = 1
            while i < len(splitCommanddsList):
                if splitCommanddsList[i].startswith("--"):
                    if "=" in splitCommanddsList[i]:
                        values = splitCommanddsList[i].split("=", 1)
                        flagName = values[0][2:]
                        flagValue = values[1]
                        longFlags[flagName] = flagValue
                    else:
                        flagName = splitCommanddsList[i][2:]
                        longFlags[flagName] = None
                    i += 1
                elif splitCommanddsList[i].startswith("-"):
                    # 1. Slice off the '-' and get individual flag characters
                    chars = splitCommanddsList[i][1:] 

                    # 2. Check for a value in the NEXT argument
                    next_val = None
                    if i + 1 < len(splitCommanddsList) and not splitCommanddsList[i+1].startswith("-"):
                        next_val = splitCommanddsList[i+1]

                    # 3. Apply boolean 'True' to all flags in the group
                    for c in chars:
                        shortFlags[c] = True
                        
                    # 4. If a value was found, assign it ONLY to the last flag in the group
                    if next_val:
                        shortFlags[chars[-1]] = next_val
                        i += 1 # Consume the value argument
                else:
                    arguments.append(splitCommanddsList[i])
                    i += 1

            commandObject = Command(mainCommand, shortFlags, longFlags, arguments)
            print("Main Command: " + commandObject.mainCommand)
            print("Short Flags: " + str(commandObject.shortFlags))
            print("Long Flags: " + str(commandObject.longFlags))
            print("Arguments: " + str(commandObject.arguments))
        except:
            print("Something went wrong.")
