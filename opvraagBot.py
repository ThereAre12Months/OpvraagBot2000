import json, os, random

# constants
WOORDSOORTEN = ["substantief", "adjectief", "voorzetsel"]

# opens the file with voc
def jsonLoader(file):
    with open(f"{file}", "r") as f:
        jsonFile = json.loads(f.read()) # turns the file into a dictionary
    naamvallen = jsonFile["naamvallen"]
    vocabulary = jsonFile["voc"]
    return vocabulary, naamvallen

# lists the available options
def listOptions(folder):
    return os.listdir(folder)

# gives a neat overview of all the vocabulary
def overview(vc):
    for key in vc.keys():
        word = vc[key]
        out = str(key)
        out += f": {word['type']}"
        if word["add"] != None: out += f": +{word['add']}"
        out += f": {', '.join(word['translate'])}"
        print(out)

# met deze functie kan je de voc opvragen
def vraagOp(vc, naamvl, times):
    correctCounter = 0
    for i in range(times):
        woordje = random.choice(list(vc.keys()))
        print(woordje)
        if stage("Welke woordsoort?", WOORDSOORTEN) == vc[woordje]["type"]:
            print("Correct!")
            if vc[woordje]["add"] != None:
                 if stage("Plus...", naamvl) == vc[woordje]["add"]:
                     print("Correct!")
                 else:
                    print("Fout! :-(")
                    continue
            # nu gaan we de vertalingen zelf opvragen
            if len(vc[woordje]["translate"]) > 1:
                sols = []
                wrong = False
                while not wrong:
                    for idx, translation in enumerate(vc[woordje]["translate"]):
                        if translation in sols:
                            print(f" [{idx}]: {translation}")
                        else:
                            print(f" [{idx}]: ...")
                    nextSol = input("De volgende vertaling? ")
                    if nextSol in vc[woordje]["translate"]:
                        if nextSol in sols:
                            print("Die oplossing heb je al gezegd.")
                        else:
                            sols.append(nextSol)
                            print("Dat is juist!")
                    else:
                        print("Fout! :-(")

                    if len(sols) == len(vc[woordje]["translate"]):
                        correctCounter += 1
                        break
        else:
            print("Fout! :-(")

    return correctCounter

# reusing the stage function
def stage(question, options):
    print(question)
    for idx, option in enumerate(options):
        print(f" [{idx}] {option}")
    return options[int(input("> "))] # returns the actual item instead of a number

# main loop
run = True
while run:
    language = stage("Welke taal wil je leren?", [*listOptions("Talen"), "exit"])
    if language == "exit": run = False; continue

    chapter = stage("Welk hoofdstuk wil je leren?", listOptions(f"Talen/{language}"))

    voc, nmvl = jsonLoader(f"Talen/{language}/{chapter}") # nmvl stands for naamvallen

    opvraagLoop = True
    while opvraagLoop:
        nextAction = stage("Volgende actie?", ["Geef een overzicht van de voc.", "Begin met oefenen.", "Ga terug."])
        if nextAction == "Geef een overzicht van de voc.":
            overview(voc)
        elif nextAction == "Begin met oefenen.":
            length = int(input("Hoeveel woordjes? "))
            juistCount = vraagOp(voc, nmvl, length)
            print(f"Je had {juistCount} woordje(s) juist, dat is {round(juistCount/length*100)}%!")
        else:
            opvraagLoop = False
