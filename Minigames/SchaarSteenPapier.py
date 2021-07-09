import random


class bcolors:
    ENDC='\033[0m'
    BOLD='\033[01m' #Maakt vet
    DISABLE='\033[02m' #Maakt lichter
    UNDERLINE='\033[04m' #Onderlijnt
    REVERSE='\033[07m' #Witte achtergrond
    STRIKETHROUGH='\033[09m'
    INVISIBLE='\033[08m'#Maakt onzichtbaar, duhhh
class letters:   
    BLACK='\033[30m'
    RED='\033[31m'
    GREEN='\033[32m'
    ORANGE='\033[33m'
    BLUE='\033[34m'
    PURPLE='\033[35m'
    CYAN='\033[36m'
    LIGHTGREY='\033[37m'
    DARKGREY='\033[90m'
    LIGHTRED='\033[91m'
    LIGHTGREEN='\033[92m'
    YELLOW='\033[93m'
    LIGHTBLUE='\033[94m'
    PINK='\033[95m'
    LIGHTCYAN='\033[96m'
class background:    
    BLACK='\033[40m'
    RED='\033[41m'
    GREEN='\033[42m'
    ORANGE='\033[43m'
    BLUE='\033[44m'
    PURPLE='\033[45m'
    CYAN='\033[46m'
    LIGHTGREY='\033[47m'


keuzes = ["schaar","steen","papier"] #Dit is een lijst
def speler_input(): #Dit is een functie
    keuze_speler = (input("Uw keuze:")).lower()
    while (keuze_speler not in keuzes):
        keuze_speler= (input("Dit was geen optie lolbroek. Opnieuw!\U0001F913:")).lower()#De functie '.lower() maakt alles met kleine letter
    return keuze_speler #Die return zorgt ervoor dat keuze_speler de output v/d functie wordt

def computer_input():
    computer_keuze = keuzes[random.randint(0,2)]#Kiest element uit lijst; 0, 1 of 2
    return computer_keuze

def who_wins():
    winnaar = 0
    while (winnaar == 0): #While zorgt ervoor dat het blijft verder gaan als winnaar = 0
        computer = computer_input()
        speler = speler_input()
        if speler == computer:
            winnaar = 0
            print("De computer had ook", computer,", opnieuw!")
            continue
        winnaar = 1 #De volgende if/elif zorgt ervoor dat als jij zou winnen winnaar = 2, anders blijft winnaar 1
        if speler == "papier" and computer == "steen":
            winnaar = 2
        elif speler == "schaar" and computer =="papier":
            winnaar = 2
        elif speler == "steen" and computer == "schaar":
            winnaar = 2
    return(winnaar, speler, computer) #Zorgen dat de if/elif statemets in de loop staan
#Geen [] bij return als dat niet ndg is. [] duid een lijst aan; () of niets een tupel. 
#Lijst = kan aangepast worden; tupel = kan niet aangepast worden

keuze_ec=["e", "c"]
def prompt_continue():
    print("What to do next?\n"
          "<c(ontinue)?>\n"
          "<e(xit)?>\n")
    check=input()
    if check == "e":
        return False
    elif check == "c":
        return True
    while(check not in keuze_ec):
        check = input("Dit was geen keuze lolbroek!:")
        if check == "e":
            return False
        elif check == "c":
            return True

#Werking: Dictionary = {"key":value
#                       "key":value
#                        etc.}
#dictionary[key]=value

#emojis["papier"] geeft \U...
emojis ={ "schaar": "\U0001F596",
         "steen": "\U0001F44A",
         "papier": "\U0001F91A"}
#avatar["Kakje"] geeft \U...
avatar ={"kakje":"\U0001F4A9",
          "raket":"\U0001F680",
          "smiley":"\U0001F600"}
#cavatar["Kakje"] geeft text.
cavatar ={"kakje": letters.ORANGE,
          "raket": letters.CYAN,
          "smiley": letters.YELLOW}

avatar_keuze = ["kakje", "raket", "smiley"]

print("Welkom bij schaar, steen, papier tegen de \U0001F63A \n"
      "Je kan je figuur kiezen uit: \n"
      ,letters.ORANGE,avatar["kakje"],bcolors.ENDC,"Kakje \n"
      ,letters.CYAN,avatar["raket"],bcolors.ENDC,"Raket \n"
      ,letters.YELLOW,avatar["smiley"],bcolors.ENDC,"Smiley")

avatar_speler = (input("Maak uw keuze:")).lower()
while (avatar_speler not in avatar_keuze):
    avatar_speler = (input("Dit is geen optie lolbroek:")).lower()
    

print("Nu kunnen we beginnen.\n"
      "Je kan kiezen tussen: \n"
      "\U0001F596 Schaar\n"
      "\U0001F44A Steen\n"
      "\U0001F91A Papier")


score_speler = 0
score_computer = 0

while(1):#While(x) herhaalt enkel als uw x niet gelijk is aan 0
    winnaar, speler, computer = who_wins() #Volgorde is belangrijk! Hier heb je who_wins() die [winnaar, speler, computer] bevat. 
    if winnaar == 1:                       #Daarna stel ik dat winnaar=winnnaar, speler=speler, computer=computer; als volgorde verschillend is stel ik bv. computer=speler
        print(emojis[speler],"verliest tegen", emojis[computer])
        score_computer += 1
    elif winnaar == 2:
        print(emojis[speler], "wint tegen", emojis[computer])
        score_speler += 1
    if score_computer<score_speler:
        print(cavatar[avatar_speler]+avatar[avatar_speler]+bcolors.ENDC, letters.GREEN, score_speler, bcolors.ENDC,"-", letters.RED,score_computer,bcolors.ENDC, letters.DARKGREY+"\U0001F63A"+bcolors.ENDC)
    elif score_computer>score_speler:
        print(cavatar[avatar_speler]+avatar[avatar_speler]+bcolors.ENDC, letters.RED,score_speler, bcolors.ENDC,"-", letters.GREEN,score_computer,bcolors.ENDC, letters.DARKGREY+"\U0001F63A"+bcolors.ENDC )
    else:
        print(cavatar[avatar_speler] + avatar[avatar_speler], bcolors.ENDC, letters.PURPLE, score_speler, bcolors.ENDC,"-", letters.PURPLE, score_computer, bcolors.ENDC, letters.DARKGREY+"\U0001F63A"+bcolors.ENDC)
    if prompt_continue()==True: #True moet niet aangezien if al checkt of het true is
        continue
    else:
        print("Dit is de eindscore!")
        if score_computer<score_speler:
            print(cavatar[avatar_speler]+avatar[avatar_speler]+bcolors.ENDC, letters.GREEN, score_speler, bcolors.ENDC,"-", letters.RED,score_computer,bcolors.ENDC, letters.DARKGREY+"\U0001F63A"+bcolors.ENDC,"\n"
                  "Proficiat! Je hebt gewonnen!\U0001F973")
        elif score_computer>score_speler:
            print(cavatar[avatar_speler]+avatar[avatar_speler]+bcolors.ENDC, letters.RED,score_speler, bcolors.ENDC,"-", letters.GREEN,score_computer,bcolors.ENDC, letters.DARKGREY+"\U0001F63A"+bcolors.ENDC,"\n"
                  "Jammer... Volgende keer beter!\U0001F9D0")
        else:
            print(cavatar[avatar_speler] + avatar[avatar_speler], bcolors.ENDC, letters.PURPLE, score_speler, bcolors.ENDC,"-", letters.PURPLE, score_computer, bcolors.ENDC, letters.DARKGREY+"\U0001F63A"+bcolors.ENDC,"\n"
                  "Goed gespeeld! Volgende keer winnen eh.\U0001F92A")
        break

#Schaar verliest tegen steen
#Steen verliest tegen papier
#Papier verliest tegen schaar

#gelijk = 0
#computer gewonnen = 1
#speler gewonnen = 2
