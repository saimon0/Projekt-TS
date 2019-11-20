import math
import re
import socket
import datetime

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # utworzenie gniazda
serversocket.bind((socket.gethostname(), 1234))  # dowiazanie do portu 1234
serversocket.listen(5)


def setID(): #funkcja tworzaca 6 cyfrowy identyfikator sesji, jest to godzina minuta sekunda polaczenia z uzupelnieniem zerem
    nowTime = datetime.datetime.now()
    idHour = str(nowTime.hour)
    idMinute = str(nowTime.minute)
    idSecond = str(nowTime.second)

    if len(idHour) == 1:
        idHour = str(0) + idHour
    if len(idMinute) == 1:
        idMinute = str(0) + idMinute
    if len(idSecond) == 1:
        idSecond = str(0) + idSecond

    id = int(idHour + idMinute + idSecond)
    operationID = "ID=" + str(id) + "$"
    return operationID


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    return a / b


def log(a, b):
    return math.log(a, b)


def power(a, b):
    return math.pow(a, b)


def switchOperations():
    print("\n0. Zakonczenie dzialania programu.")
    print("1. Historia obliczen przez podanie ID sesji.")
    print("2. Historia obliczen przez podanie ID obliczen.")
    print("3. Wyswietlenie wszystkich wykonanych obliczen.")
    choice = input("\nWybierz operacje do wykonania (podaj numer): ")

    return {
        '0': "FN",  #zakonczenie dzialania programu
        '1': "HS",  # wyswietlenie historii obliczen przez ID sesji
        '2': "HO",  # odejmowanie historii obliczen przez ID obliczen
        '3': "HA",  # wykonywanie wszystkich wykonanych obliczen
    }.get(choice, "Podano nieprawidlowy numer operacji.")


class operation:
    ID = "123456"
    ST = "AB"
    IO = "AB"
    OP = "AB"
    OD = "AB"
    Z1 = "1"
    Z2 = "2"
    WY = "3"

operationHistory = [] #lista zawierajca wpisy wykonanych dzialan mat


def displayMathOperationsHistorySession():
    if len(operationHistory) == 0:
        print("Historia operacji jest pusta.\n")
    else:
        print("\nWykonane dzialania matematyczne w obecnej sesji: \n")
        print("\n".join(operationHistory))
        print("\n")


def displayMathOperationsHistoryOperationID():
    operation = input("Podaj ID operacji do wyswietlenia: \n")
    matcher = str(operation)
    findOperation = [s for s in operationHistory if any(xs in s for xs in matcher)]
    if len(findOperation) != 0:
        print(findOperation)
    else:
        print("\nNie znaleziono wskazanej opracji.\n")

def  displayAllMathOperations():
    if len(operationHistory) == 0:
        print("Historia operacji jest pusta.\n")
    else:
        print("\nWykonane do tej pory dzialania matematyczne: \n")
        print("\n".join(operationHistory))
        print("\n")


DOcounter = 1
ODcounter = 1
MNcounter = 1
DZcounter = 1
POcounter = 1
LOcounter = 1

ID = 0
ST = 0
IO = 0
OP = 0
OD = 0
WY = 0
Z1 = 0
Z2 = 0

def decodeOperationCode(operationCode):
    global ID
    global ST
    global IO
    global OP
    global OD
    global Z1
    global Z2
    global WY
    if len(operationCode) >= 40:  # sprawdzanie czy kod dotyczy dzialan matematycznych, jak jest mniejszy niz 50 to chodzi o historie
        splitedOperationCode = operationCode.split("$", 6)
        ID = splitedOperationCode[0]
        ID = ID[3:]
        #print("ID: " + ID)

        ST = splitedOperationCode[1]
        ST = ST[3:]
        #print("ST: " + ST)

        IO = splitedOperationCode[2]
        IO = IO[3:]
        #print("IO: " + IO)

        OP = splitedOperationCode[3]
        OP = OP[3:]
        #print("OP: " + OP)

        OD = splitedOperationCode[4]
        OD = OD[3:]
        #print("OD: " + OD)

        Z1 = splitedOperationCode[5]
        Z1 = Z1[3:]
        #print("Z1: " + Z1)
        Z1 = int(Z1)

        Z2 = splitedOperationCode[6]
        Z2 = Z2[3:-1]
        #print("Z2: " + Z2)
        Z2 = int(Z2)
    else:
        print("tutaj bedzie dekodowanie zapytania o historie sesji/konkretengo dzialnia")


def executeRequest():
    global DOcounter, ODcounter, MNcounter, DZcounter, POcounter, LOcounter, OD
    if OP == 'DO':
        WY = add(Z1, Z2)
        IO = "DO" + str(DOcounter)
    if OP == 'OD':
        WY = subtract(Z1, Z2)
        IO = "OD" + str(ODcounter)
    if OP == 'MN':
        WY = multiply(Z1, Z2)
        IO = "MN" + str(MNcounter)
    if OP == 'DZ':
        WY = divide(Z1, Z2)
        IO = "DZ" + str(DZcounter)
    if OP == 'PO':
        WY = power(Z1, Z2)
        IO = "PO" + str(POcounter)
    if OP == 'LO':
        WY = log(Z1, Z2)
        IO = "LO" + str(LOcounter)

    ST="OB" #tak narazie
    OD="OK" #tez narazie okej, potem bede sprawdzac czy nie wyszlo poza zasieg inta
    putToList()
    answerCode = "ID=" + str(ID) + "$ST=" + str(ST) + "$IO=" + str(IO) + "$OP=" + str(OP) + "$OD=" + str(OD) + "$WY=" + str(WY)
    print("\nUtworzona odpowiedz: " + answerCode + "\n")
    return answerCode


def listenIncomingRequest():
    receivedOperationCode = clientsocket.recv(1024)
    operationCode = str(receivedOperationCode, 'utf-8')
    return operationCode


def sendIDsessionToClient():
    clientsocket.send(bytes(str(setID()), 'utf8'))

def sendAnswerForRequest():
    clientsocket.send(bytes(str(executeRequest()), 'utf8'))  # wysylanie id sesji do klienta



def putToList():
    operation = "0"
    if OP == "DO":
        operation = "Dodawanie"
    if OP == "OD":
        operation = "Odejmowanie"
    if OP == "MN":
        operation = "Mnozenie"
    if OP == "DZ":
        operation = "Dzielenie"
    if OP == "PO":
        operation = "Potegowanie"
    if OP == "LO":
        operation = "Logarytmowanie"

    operationCodeToList = "ID operacji: " + str(IO) + " | Dzialanie: " + str(operation) + " | Wynik dzialania: " + str(OD) + " | Wartosc 1 liczby: " + str(Z1) + " | Wartosc 2 liczby: " + str(Z2)
    operationHistory.append(operationCodeToList)


#*** Uruchomienie serwera ***


while 1:

    clientsocket, address = serversocket.accept()  # odebranie polaczenia od klienta i akceptacja
    print(f'Polaczono z: ', address)
    sendIDsessionToClient()  # wysylanie id sesji do klienta

    while 1:
        print("1. Nasluchuj klienta 2. Wybierz operacje")
        choice = input("Wybierz operacje do wykonania: ")
        if choice == "1":
                operationCode = listenIncomingRequest()  # nasluchiwanie na przyjscie zapytania
                decodeOperationCode(operationCode)
                sendAnswerForRequest()
        if choice == "2":
            operation = switchOperations()

            if operation == "FN":
                print("Zakonczono dzialanie programu.")
                clientsocket.close()
                break
            elif operation == "HS":
                print("Wyswietlenie historii obliczen przez ID sesji.\n")
                displayMathOperationsHistorySession()
            elif operation == "HO":
                print("Wyswietlenie historii obliczens przez ID obliczen.\n")
                displayMathOperationsHistoryOperationID()
            elif operation == "HA":
                print("Wyswietlenie wszystkich wykonanych dotychczas operacji matematycznych.\n")
                displayAllMathOperations()
            else:
                print("\nPodano nieprawidlowy numer operacji, sprobuj jeszcze raz...")