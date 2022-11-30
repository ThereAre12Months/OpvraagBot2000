import json, os, random, sys, colorama
colorama.init()

# constants
WOORDSOORTEN = ["substantief", "adjectief", "voorzetsel", "voegwoord", "werkwoord", "bijwoord", "aanwijzend voornaamwoord", "persoonlijk voornaamwoord", "bezittelijk voornaamwoord", "vraagpartikel", "vraagwoord", "wederkerend voornaamwoord"]

# opens the file with voc
def jsonLoader(file):
    with open(f"{file}", "r") as f:
        jsonFile = json.loads(f.read()) # turns the file into a dictionary
    naamvallen = jsonFile["naamvallen"]
    vocabulary = jsonFile["voc"]
    naam       = jsonFile["title"]
    return vocabulary, naamvallen, naam

# lists the available options
def listOptions(folder):
    if ".json" in list(os.listdir(folder))[0]:
        if True: # True = new system, False = old system
            options = os.listdir(folder)
            file_list = []
            for opt in options:
                _,_,title_ = jsonLoader(folder + "/" + opt)
                file_list.append(title_)

            return file_list, os.listdir(folder)
        else:
            return os.listdir(folder), None
    else:
        return os.listdir(folder), None

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
            nextSol = input("De volgende vertaling? (Typ '?' of 'stop' als je het antwoord niet weet of wilt stoppen.) : ")
            if nextSol == "?":
                wrong = True
                allesJuist = False
                continue
            elif nextSol == 'stop':
                allesJuist = "stopping this sh*t"
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
        sluit_dit_ding_af = input("Wat is de vertaling? (Typ 'stop' om af te sluiten.) : ")
        if sluit_dit_ding_af == vertalingen[0]:
            pass
        elif sluit_dit_ding_af == "stop":
            allesJuist = "stoppping this sh*t"

        else:
            allesJuist = False
    return allesJuist

# gives a neat overview of all the vocabulary
def overview(vc):
    for key in vc.keys():
        out = "\033[1;3m" + "\033[94m"
        word = vc[key]
        out += str(key)
        out += "\033[0m" + "\033[93m"
        out += f": {word['type']}"
        if word["add"] != None: out += "\033[92m" f": +{word['add']}"
        new = "\033[95m"
        for translates in word["translate"]:
            if not len(new) == 0: new += ", "
            if type(translates) == str:
                new += translates
            else:
                new += f"({translates[0]}) {translates[1]}"
        out += f": {new}\n"
        sys.stdout.write(out + "\033[0m")

# met deze functie kan je de voc opvragen
def vraagOp(vc, naamvl, times, vraagWoordsoorten):
    correctCounter = 0
    for i in range(times):
        woordje = random.choice(list(vc.keys()))
        sys.stdout.write("\033[1;3m" + "\033[94m" + woordje + "\033[0m\n")
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
        sys.stdout.write("\033[1;3m" + "\033[94m" + foutWoordje + "\033[0m\n")
        trashcan = vertalingOpvragen(foutWoordje, vc[foutWoordje]["translate"])
        if trashcan == True:
            juisteWoordjes.append(foutWoordje)
            print("Dat was helemaal juist!")
        elif trashcan == "stoppping this sh*t":
            print("Oefenen voor toets sluit af.")
            break

        #los deze shit op Ruben
    return fouteWoordjes

# reusing the stage function
def stage(question, options, ids=None):
    print(question)
    for idx, option in enumerate(options):
        print(f" [{idx}] {option}")
    if ids == None:
        return options[int(input("> "))] # returns the actual item instead of a number
    else:
        return ids[int(input("> "))] # returns the .json variant instead of the actual name eg. Adspectus 1 -> adspectus1.json

# main loop
run = True
while run:
    language = stage("Welke taal wil je leren?", [*(listOptions("Talen")[0]), "Sluit woordentrainer af"])
    if language == "Sluit woordentrainer af": run = False; continue

    chapter_opts = listOptions(f"Talen/{language}")
    if chapter_opts[1] == None:
        chapter = stage("Welk hoofdstuk wil je leren?", chapter_opts[0])
    else:
        chapter = stage("Welk hoofdstuk wil je leren?", chapter_opts[0], chapter_opts[1])

    voc, nmvl, _ = jsonLoader(f"Talen/{language}/{chapter}") # nmvl stands for naamvallen

    opvraagLoop = True
    while opvraagLoop:
        nextAction = stage("Volgende actie?", ["Geef een overzicht van de voc.", "Begin met oefenen.", "Voorbereiden op toets.", "Ga terug."])
        if nextAction == "Geef een overzicht van de voc.":
            overview(voc)
        elif nextAction == "Voorbereiden op toets.":
            print("Zorg ervoor dat je genoeg tijd hebt,\n"
                  "deze modus blijft vragen tot je alles juist hebt gehad.")
            uitkomst = toetsModus(voc, nmvl)
            if uitkomst == []:
                print("Je hebt alle woordjes minstens 1 keer juist gehad!")

        elif nextAction == "Begin met oefenen.":
            length = int(input("Hoeveel woordjes? : "))
            vrgWrdsrt = (input("Woordsoorten opvragen? (y/n) : ").lower() == "y")
            juistCount = vraagOp(voc, nmvl, length, vrgWrdsrt)
            print(f"Je had {juistCount} woordje(s) juist, dat is {round(juistCount/length*100)}%!")
        else:
            opvraagLoop = False
