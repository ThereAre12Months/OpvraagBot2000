import json, os, random

# constants
WOORDSOORTEN = ["substantief", "adjectief", "voorzetsel", "voegwoord", "werkwoord", "bijwoord", "aanwijzend voornaamwoord", "persoonlijk voornaamwoord", "bezittelijk voornaamwoord"]

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

# dit vraagt de vertaling op
def vertalingOpvragen(origWoordje, vertalingen):
    allesJuist = True
    if len(vertalingen) > 1:
        sols = []
        wrong = False
        while not wrong:
            for idx, translation in enumerate(vertalingen):
                if translation in sols:
                    if type(translation) == str:
                        print(f" [{idx}]: {translation}")
                    else:
                        print(f" [{idx}] ({translation[0]}): {translation}")
                else:
                    if type(translation) == str:
                        print(f" [{idx}]: ...")
                    else:
                        print(f" [{idx}] ({translation[0]}): ...")
            nextSol = input("De volgende vertaling? (Typ '?' als je het antwoord niet weet.) ")
            if nextSol == "?":
                wrong = True
                allesJuist = False
                continue
            if nextSol in vertalingen:
                if nextSol in sols:
                    print("Die oplossing heb je al gezegd.")
                else:
                    sols.append(nextSol)
                    print("Dat is juist!")
            else:
                allesJuist = False

            if len(sols) == len(vertalingen):
                break
    else:
        if input("Wat is de vertaling? ") == vertalingen[0]:
            pass
        else:
            allesJuist = False
    return allesJuist

# gives a neat overview of all the vocabulary
def overview(vc):
    for key in vc.keys():
        word = vc[key]
        out = str(key)
        out += f": {word['type']}"
        if word["add"] != None: out += f": +{word['add']}"
        new = ""
        for translates in word["translate"]:
            if not len(new) == 0: new += ", "
            if type(translates) == str:
                new += translates
            else:
                new += f"({translates[0]}) {translates[1]}"
        out += f": {new}"
        print(out)

# met deze functie kan je de voc opvragen
def vraagOp(vc, naamvl, times, vraagWoordsoorten):
    correctCounter = 0
    for i in range(times):
        woordje = random.choice(list(vc.keys()))
        print(woordje)
        if vraagWoordsoorten:
            if stage("Welke woordsoort?", WOORDSOORTEN) == vc[woordje]["type"]:
                print("Correct!")
            else:
                print("Fout! :-(")
                continue
        if vc[woordje]["add"] != None:
            if stage("Plus...", naamvl) == vc[woordje]["add"]:
                 print("Correct!")
            else:
                print("Fout! :-(")
                continue
        # nu gaan we de vertalingen zelf opvragen
        if vertalingOpvragen(vc[woordje], vc[woordje]["translate"]):
            correctCounter += 1
            print("Alles juist!!!")
        else:
            print("Je maakte een fout. :-(")

    return correctCounter

def toetsModus(vc, naamvl):
    juisteWoordjes = []
    while len(juisteWoordjes) < len(list(vc.keys())):
        fouteWoordjes = list(set(juisteWoordjes).symmetric_difference(list(vc.keys())))
        foutWoordje = random.choice(fouteWoordjes)
        print(foutWoordje)
        if vertalingOpvragen(foutWoordje, vc[foutWoordje]["translate"]):
            juisteWoordjes.append(foutWoordje)
            print("Dat was helemaal juist!")
        else:
            print(f"Je maakte een fout door {foutWoordje} te typen. :-(")
        #los deze shit op Ruben

# reusing the stage function
def stage(question, options):
    print(question)
    for idx, option in enumerate(options):
        print(f" [{idx}] {option}")
    return options[int(input("> "))] # returns the actual item instead of a number

# main loop
run = True
while run:
    language = stage("Welke taal wil je leren?", [*listOptions("Talen"), "Sluit woordentrainer af"])
    if language == "Sluit woordentrainer af": run = False; continue

    chapter = stage("Welk hoofdstuk wil je leren?", listOptions(f"Talen/{language}"))

    voc, nmvl = jsonLoader(f"Talen/{language}/{chapter}") # nmvl stands for naamvallen

    opvraagLoop = True
    while opvraagLoop:
        nextAction = stage("Volgende actie?", ["Geef een overzicht van de voc.", "Begin met oefenen.", "Toetsmodus.", "Ga terug."])
        if nextAction == "Geef een overzicht van de voc.":
            overview(voc)
        elif nextAction == "Toetsmodus.":
            toetsModus(voc, nmvl)
            print("Je hebt alle woordjes minstens 1 keer juist gehad!")
        elif nextAction == "Begin met oefenen.":
            length = int(input("Hoeveel woordjes? "))
            vrgWrdsrt = (input("Woordsoorten opvragen? (y/n) ").lower() == "y")
            juistCount = vraagOp(voc, nmvl, length, vrgWrdsrt)
            print(f"Je had {juistCount} woordje(s) juist, dat is {round(juistCount/length*100)}%!")
        else:
            opvraagLoop = False
