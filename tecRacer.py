# Rechner zur betrieblichen Altersvorsorge
# Autor:                    Andreas Bloch
# Erstellungsdatum:         17.03.2021
# letztes Aenderungsdatum:   18.03.2021
# Version 1.0

class Rules:
    def __init__(self):
        self.westBetragBBG = 7100
        self.ostBetragBBG = 6900
        self.agGrundbetrag = 0.014
        self.erhoeterAGBetrag = 0.058
        self.matchingProzent = 0.15
        self.prozentBrutto = 0.01
        self.schleifenIndex = 0
        self.ruleArrayNames = ["BBG-West in Euro [0]","BBG-Ost in Euro[1]", "AG-Grundbetrag in Prozent [2]",
                               "Erhoehter AG-Betrag in Prozent [3]", "Matching-Anteil in Prozent [4]",
                               "Anteil Bruttoeinkommen Matching in Prozent [5]"]
        self.ruleArrayValues = [self.westBetragBBG, self.ostBetragBBG,
                                self.agGrundbetrag, self.erhoeterAGBetrag,
                                self.matchingProzent, self.prozentBrutto]
    def showRules(self,ruleArray):
        self.schleifenIndex = 0
        self.ruleArrayValues = ruleArray
        print("--------------------------------------------------------------")
        for array_index in self.ruleArrayValues:
            print(self.ruleArrayNames[self.schleifenIndex],": ", array_index)
            self.schleifenIndex += 1
        print("--------------------------------------------------------------")

    def changeRules(self, ruleValue, changeValue):
        self.ruleArrayValues[ruleValue] = changeValue
        print("Der gewuenschte Wert wurde angepasst!")
        print("Angepasste Regeln.")
        self.showRules(self.ruleArrayValues)
        return self.ruleArrayValues

class Prompt(Rules):
    def __init__(self):
        super().__init__()
        self.bruttoEinkommen = 0
        self.wandlungsbetrag = 0
        self.wohnort = "ohne"
    # Eingabeaufforderung an den Nutzer, fuer notwendige Daten
    def userPrompt(self):
        while True:
            try:
                self.bruttoEinkommen = int(input("Bitte das Bruttogehalt pro Monat eingeben."))
                break
            except:
                print("Die Eingabe entsrpicht keiner Zahl. Eingabe wiederholen")
        while True:
            try:
                self.wandlungsbetrag = int(input("Bitte den Wandlungsbetrag eingeben."))
                break
            except:
                print("Die Eingabe entsrpicht keiner Zahl. Eingabe wiederholen")
        while True:
            self.wohnort = input("Bitte den Wohnort eingeben. (West / Ost)")
            if self.wohnort.upper() != "WEST" and self.wohnort.upper() != "OST":
                print("Die Wohnorteingabe war nicht korrekt, bitte wiederholen!")
            else:
                break

class Calulate(Prompt):
    def __init__(self, changes):
        super().__init__()
        self.agGrundbeitrag = 0
        self.matchingDifferenz = 0
        self.matchingBeitrag = 0
        self.agZusatzBeitrag = 0
        self.changedArray = changes

    # Berechnung der Beitragsbemessungsgrenze(bbg)
    def bbg(self):
        # Arbeitnehmer zahlt mehr als 1 Prozent des Bruttoeinkommens in die bAv ein.
        if self.wandlungsbetrag >= self.changedArray[5] * self.bruttoEinkommen:
            # Berechnung des BBG mit Hilfe des Westwertes.
            if self.wohnort.upper() == "WEST":
                # Bruttoeinkommen liegt ueber dem BBG
                if self.bruttoEinkommen > self.changedArray[0]:
                    # Berechnung des AG-Betrages unter der BBG
                    self.agGrundbeitrag = self.changedArray[2] * self.westBetragBBG
                    # Berechnung des AG-Betrages ueber der BBG
                    self.agZusatzBeitrag = self.agGrundbeitrag + (self.bruttoEinkommen - self.changedArray[0]) * \
                                           self.changedArray[3]
                elif self.bruttoEinkommen <= self.changedArray[0]:
                    self.agGrundbeitrag = self.bruttoEinkommen * self.changedArray[2]
                    self.agZusatzBeitrag = 0
            elif self.wohnort.upper() == "OST":
                # Berechnung des BBG mit Hilfe des Ostwertes
                if self.bruttoEinkommen > self.changedArray[1]:
                    # Berechnung des AG-Betrages unter der BBG
                    self.agGrundbeitrag = self.changedArray[2] * self.changedArray[1]
                    # Berechnung des AG-Betrages ueber der BBG
                    self.agZusatzBeitrag = self.agGrundbeitrag + (self.bruttoEinkommen - self.changedArray[1]) * \
                                           self.changedArray[3]
                elif self.bruttoEinkommen <= self.changedArray[1]:
                    self.agGrundbeitrag = self.bruttoEinkommen * self.changedArray[2]
                    self.agZusatzBeitrag = 0
        else:
            #Der eingezahlte Wandlungsbetrag liegt unter einem Prozent des Bruttolohns des ANs.
            print("Zu geringer Wandlunsgbetrag!")
            self.agGrundbeitrag = 0
    # Berechnung des Matching Wertes
    def matchingWert(self):
        if self.wandlungsbetrag >= self.ruleArrayValues[5] * self.bruttoEinkommen:
            self.matchingDifferenz = self.wandlungsbetrag - (self.changedArray[5] * self.bruttoEinkommen)
            self.matchingBeitrag = self.matchingDifferenz * self.changedArray[4]
            #Ueberpruefung, ob der Matching Betrag groesser ist als die Haelfte des AG Anteils.
            if self.matchingBeitrag > (self.agGrundbeitrag / 2):
                self.matchingBeitrag = self.agGrundbeitrag / 2
        else:
            self.matchingBeitrag = 0
    def showCalc(self):
        print("-------------------------------------------------------------------------")
        print("AG-Grundbeitrag pro Monat in Euro: {:.2f}".format(self.agGrundbeitrag), "+",
              "AG-Zusatzbeitrag pro Monat in Euro: {:.2f}".format(self.agZusatzBeitrag))
        print("AG-Grundbeitrag pro Jahr in Euro: {:.2f}".format(12 * self.agGrundbeitrag), "+",
              "AG-Zusatzbeitrag pro Jahr in Euro: {:.2f}".format(12 * self.agZusatzBeitrag))
        print("Matching Beitrag pro Monat in Euro: {:.2f}".format(self.matchingBeitrag))
        print("Matching Beitrag pro Jahr in Euro: {:.2f}".format(12 * self.matchingBeitrag))
        print("-------------------------------------------------------------------------")

def main():
    berechnung = True
    aenderung = Rules()
    ruleArray = aenderung.ruleArrayValues

    print("Willkommen zum Rechner fuer die betriebliche Altersvorsorge.")
    #Schleife zur Veraenderung des Regelwerkes
    while berechnung == True:
        # Aufruf nach Regelaenderung oder Berechnung mit den bisherigen Werten.
        # While Schleife nutzen für weitere Berechnungen
        regelAbfrage = input("Soll das Regelwerk geaendert werden?(J/N)")
        if regelAbfrage.upper() != "J" and regelAbfrage.upper() != "N":
            print("Moechten Sie das Programm beenden?")
            endabfrage = input("Eingabe beenden?(J/N)")
            if endabfrage.upper() == "J":
                break
            elif endabfrage.upper() == "N":
                print("Regelaenderung wird von vorne gestartet.")
        elif regelAbfrage.upper() == "J":
            print("Ausgabe der aktuellen Werte")
            aenderung = Rules()
            #Ausgabe der aktuellen Werte
            aenderung.showRules(ruleArray)
            ruleValue = int(input("Welcher Wert soll geaendert werden? [0-5]"))
            if ruleValue >= 0 and ruleValue < 6:
                changeValue = float(input("Bitte neuen Wert eingeben."))
                ruleArray = aenderung.changeRules(ruleValue, changeValue)
            else:
                print("Die Eingabe war nicht korrekt! Vorgang abgebrochen.")
        elif regelAbfrage.upper() == "N":
            print("Die bAv-Berechnung wird fortgesetzt.")
            bAvBerechnung = Calulate(ruleArray)
            bAvBerechnung.userPrompt()
            bAvBerechnung.bbg()
            bAvBerechnung.matchingWert()
            bAvBerechnung.showCalc()
            calcContinue = input("Soll eine weitere Berechnung durchgeführt werden?(J/N)")
            if calcContinue.upper() != "J":
                print("Die Berechnung wird beendet. Vielen Dank fuer die Nutzung.")
                berechnung = False


if __name__ == "__main__":
    main()
