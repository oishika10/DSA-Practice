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
                    # Long flag: starts with '--'
                    # Example input: --output=json
                    if "=" in splitCommanddsList[i]:
                        # Flag has an inline value separated by '='
                        # e.g. "--output=json" → split into ["--output", "json"]
                        #      flagName = "output", flagValue = "json"
                        values = splitCommanddsList[i].split("=", 1)
                        flagName = values[0][2:]  # Strip leading '--'
                        flagValue = values[1]
                        longFlags[flagName] = flagValue
                    else:
                        # Flag is a boolean toggle with no value
                        # e.g. "--verbose" → flagName = "verbose", stored as None (presence = True)
                        flagName = splitCommanddsList[i][2:]  # Strip leading '--'
                        longFlags[flagName] = None
                    i += 1
                elif splitCommanddsList[i].startswith("-"):
                    # Short flag: starts with a single '-'
                    # Short flags can be grouped together as a single token
                    # e.g. "-vp" means both -v and -p are set

                    # 1. Slice off the '-' and get individual flag characters
                    # e.g. "-vp" → chars = "vp" → ['v', 'p']
                    chars = splitCommanddsList[i][1:]

                    # 2. Check if the NEXT token is a value (not another flag)
                    # e.g. "-p 8080" → next_val = "8080"
                    # e.g. "-p -v"  → next_val = None (next token is a flag, skip)
                    next_val = None
                    if i + 1 < len(splitCommanddsList) and not splitCommanddsList[i+1].startswith("-"):
                        next_val = splitCommanddsList[i+1]

                    # 3. Set all flags in the group to True initially
                    # e.g. "-vp" → shortFlags = {'v': True, 'p': True}
                    for c in chars:
                        shortFlags[c] = True

                    # 4. If a value token was found, assign it to the LAST flag in the group
                    # e.g. "-vp 8080" → shortFlags = {'v': True, 'p': '8080'}
                    # The value is consumed (i incremented) so it isn't treated as an argument
                    if next_val:
                        shortFlags[chars[-1]] = next_val
                        i += 1  # Consume the value token
                else:
                    # Positional argument: not a flag, just a plain value
                    # e.g. "run server.py file.txt" → arguments = ["server.py", "file.txt"]
                    arguments.append(splitCommanddsList[i])
                    i += 1

            commandObject = Command(mainCommand, shortFlags, longFlags, arguments)
            print("Main Command: " + commandObject.mainCommand)
            print("Short Flags: " + str(commandObject.shortFlags))
            print("Long Flags: " + str(commandObject.longFlags))
            print("Arguments: " + str(commandObject.arguments))
        except:
            print("Something went wrong.")
