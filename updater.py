import os, sys, json

try:
    path = sys.argv[1]
except:
    print("Kopiëer het het bestands-pad van je .update bestand.")
    path = input("> ")

path = str(path)
path = path.replace('"', "")

try:
    with open(path, "r") as f:
        try:
            jFile = json.loads(f.read())
            file = f.read()
        except:
            print("Corrupted or incorrect file")
            exit()
except:
    print("Sorry, dit bestand bestaat niet :-(")
    print("Valideer of je bestands-pad correct is en probeer opnieuw.")
    exit()

try:
    locatie = jFile["location"]
except:
    print("Sorry, uw bestand heeft niet alle nodige headers.")
    exit()

actual = "Talen/"+locatie
if not os.path.exists(actual):
    os.mkdir(actual)

if not os.path.exists(f"{actual}/{jFile['fileName']}"):
    empty = open(f"{actual}/{jFile['fileName']}", "x")
with open(f"{actual}/{jFile['fileName']}", "w") as f:
    f.write(json.dumps(jFile))
