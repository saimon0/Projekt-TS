import re
import socket
import time
from time import sleep
from _datetime import datetime
from re import split

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # utworzenie gniazda


def connectingg():
    global iddod, idode, idmno, iddzi, idpot, idlog
    global id
    IPw = input("Podaj IP serwera: ")
    iddod = 0
    idode = 0
    idmno = 0
    global decodeID
    iddzi = 0
    idpot = 0
    idlog = 0
    connected = False
    print("Czekam na polaczenie...")
    while not connected:
        try:
            serversocket.connect((IPw, 1234))  # nawiazanie polaczenia
            connected = True
            id = serversocket.recv(1024)
            idstr = str(id, 'utf8')  # konwertowanie id sesji do formatu utf-8
            id = str(idstr)
            id = id.split("$", 10)
            decodeID = id[0]
            decodeID = decodeID[3:]
            czas = id[3]
            czas = czas[3:]
            print("\nPolaczono z serwerem. Twoj identyfikator sesji to: ", decodeID, sep="")
            print("Znacznik czasu: ", czas)
            # gwiazdka i ten sep musi byc, bo regex po wyciagnieciu danej wartosci wrzuca ja do listy
            # i wtedy wyswietla z nawiasami kwadratowymi i rownoscia, dzieki temu wyswietla tylko sama wartosc
        except Exception as e:
            pass


z1 = 0
z2 = 0
connectingg()


def switchOperation():
    print("\n0. Zakonczenie dzialania programu.")
    print("1. Historia obliczen przez podanie ID sesji.")
    print("2. Historia obliczen przez podanie ID obliczen.")
    print("3. Wykonywanie operacji matematycznych.")
    print("4. Zmien uzytkownika (zmiana id sesji).")
    choice = input("\nWybierz operacje do wykonania (podaj numer): ")

    return {
        '0': "FN",  # zakonczenie dzialania programu
        '1': "HS",  # wyswietlenie historii obliczen przez ID sesji
        '2': "HO",  # odejmowanie historii obliczen przez ID obliczen
        '3': "OB",  # wykonywanie obliczen
        '4': "RE",  # relog bo pewnie potrzebny na rzecz sprawdzania
    }.get(choice, "Podano nieprawidlowy numer operacji.")


def listenIncoming():
    receivedOperationCode = serversocket.recv(1024)
    operationCode = str(receivedOperationCode, 'utf-8')
    decodeOperationCode(operationCode)


def decodeOperationCodeHSIO(operationCode):
    global IS
    global IO
    global OP
    global OD
    global Z1
    global Z2
    splitedOperationCode = operationCode.split("$", 5)
    ID = splitedOperationCode[0]
    ID = ID[3:]
    print("\nID sesji: " + ID)

    ST = splitedOperationCode[1]
    ST = ST[3:]
    print("Status: " + ST)

    OP = splitedOperationCode[2]
    OP = OP[3:]
    NR = 1

    print("Operacja: " + OP)
    if ST != "ER":
        ZC = splitedOperationCode[3]
        if OP == "HS":
            NRS = splitedOperationCode[4]
            NRS = NRS[3:]
            NR = int(NRS)
    else:
        ZC = splitedOperationCode[4]
    ZC = ZC[3:]
    print("ZC: " + ZC)

    if ST != "ER":
        print("\nWyszukane dzialania: ")
        for x in range(int(NR)):
            receivedOperationCode = serversocket.recv(1024)

            operationCode = str(receivedOperationCode, 'utf-8')
            second = operationCode

            splitedOperationCode = operationCode.split("$", 30)

            ID = splitedOperationCode[0]
            ID = ID[3:]
            print("\nID sesji: " + ID)

            ST = splitedOperationCode[1]
            ST = ST[3:]
            print("Status: " + ST)

            IO = splitedOperationCode[2]
            IO = IO[3:]
            print("ID operacji: " + IO)

            ZC = splitedOperationCode[3]
            ZC = ZC[3:]
            print("ZC: " + ZC)


            ID = splitedOperationCode[4]
            ID = ID[3:]
            print("\nID sesji: " + ID)

            ST = splitedOperationCode[5]
            ST = ST[3:]
            print("Status: " + ST)

            IO = splitedOperationCode[6]
            IO = IO[3:]
            print("ID operacji: " + IO)

            OP  = splitedOperationCode[7]
            OP = OP[3:]
            print("Operacja: " + OP)

            ZC1 = splitedOperationCode[8]
            ZC1 = ZC1[3:]
            print("Zmienna 1: " + ZC1)

            ZC2 = splitedOperationCode[9]
            ZC2 = ZC2[3:]
            print("Zmienna 2: " + ZC2)

            WY = splitedOperationCode[10]
            WY = WY[3:]
            print("Wynik: " + WY)
            ZC = splitedOperationCode[11]
            ZC = ZC[3:-1]
            print("ZC: " + ZC)





    else:
        print("Wystapil blad - nie znaleziono operacji o podanym ID w historii")


def listenIncomingHSIO():
    receivedOperationCode = serversocket.recv(1024)
    operationCode = str(receivedOperationCode, 'utf-8')
    decodeOperationCodeHSIO(operationCode)


def decodeOperationCode(operationCode):
    global IS
    global IO
    global OP
    global OD
    global Z1
    global Z2

    if len(
            operationCode) >= 20:  # sprawdzanie czy kod dotyczy dzialan matematycznych, jak jest mniejszy niz 50 to chodzi o historie

        splitedOperationCode = operationCode.split("$", 5)
        ID = splitedOperationCode[0]
        ID = ID[3:]
        print("\nid sesji: " + ID)

        ST = splitedOperationCode[1]
        ST = ST[3:]
        print("status: " + ST)

        IO = splitedOperationCode[2]
        IO = IO[3:]
        print("ID operacji: " + IO)

        OP = splitedOperationCode[3]
        OP = OP[3:]
        print("operacja mat: " + OP)
        if ST != "ER":
            WY = splitedOperationCode[4]
            WY = WY[3:]
            print("Odpowiedz: " + WY)
        if ST == "ER":
            print("Wystapil blad, Podano niewlasciwa wartosc")

        ZC = splitedOperationCode[5]
        ZC = ZC[3:-1]
        print("Data, godzina wykonania operacji: " + ZC + "s")


    else:
        print("Wystapil nieoczekiwany blad :(")


def InputLiczby():
    global z1
    global z2
    z1 = input("Wprowadz pierwsza liczbe:")
    z2 = input("Wprowadz druga liczbe:")
    while z1.isalpha() or z2.isalpha():
        print("Zmienne musza byc liczba!")
        z1 = input("Wprowadz pierwsza liczbe:")
        z2 = input("Wprowadz druga liczbe:")
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    while True:
        if regex.search(z1) == None and regex.search(z2) == None:
            break
        else:
            print("Zmienne musza byc liczba!")
            z1 = input("Wprowadz pierwsza liczbe:")
            z2 = input("Wprowadz druga liczbe:")

    z1 = int(float(z1))
    z2 = int(float(z2))


def switchMathOperation():
    global z1
    global z2

    global iddod, idode, idmno, iddzi, idpot, idlog
    print("1. Dodawanie\n 2. Odejmowanie\n 3. Mnozenie\n 4. Dzielenie\n 5. Potegowanie\n 6. Logarytmowanie\n")
    choice = input("\nWybierz operacje matematyczna, ktora chcesz wykonac (podaj numer): ")
    if choice == "1":
        print("\nWybrano dodawanie:")
        InputLiczby()
        iddod = iddod + 1
    if choice == "2":
        print("\nWybrano odejmowanie:")
        InputLiczby()
        idode = idode + 1
    if choice == "3":
        print("\nWybrano mnozenie:")
        InputLiczby()
        idmno = idmno + 1
    if choice == "4":
        print("\nWybrano dzielenie:")
        InputLiczby()
        iddzi = iddzi + 1
    if choice == "5":
        print("\nWybrano potegowanie:")
        InputLiczby()
        idpot = idpot + 1
    if choice == "6":
        print("\nWybrano logarytmowanie:")
        InputLiczby()
        idlog = idlog + 1

    return {
        '1': "dodawaj",  # dodawanie
        '2': "odejmuj",  # odejmowanie
        '3': "mnoz",  # mnozenie
        '4': "dziel",  # dzielenie
        '5': "poteguj",  # potegowanie
        '6': "logarytmuj",  # logarytmowanie
    }.get(choice, "Podano nieprawidlowy numer operacji.")


def IDO(Operacja):
    global iddod, idode, idmno, iddzi, idpot, idlog
    if Operacja == "dodawaj":
        return iddod
    if Operacja == "odejmuj":
        return idode
    if Operacja == "mnoz":
        return idmno
    if Operacja == "dziel":
        return iddzi
    if Operacja == "poteguj":
        return idpot
    if Operacja == "logarytmuj":
        return idlog


def CreateAndSendMessage(Operacja):
    if not Operacja == "Podano nieprawidlowy numer operacji.":
        global z1
        global z2
        global id
        global decodeID
        nowTime = datetime.now()
        year = nowTime.strftime("%Y")
        month = nowTime.strftime("%m")
        day = nowTime.strftime("%d")
        time = nowTime.strftime("%H:%M:%S")
        ZC = nowTime.strftime("%d/%m/%Y,%H:%M:%S")
        wiadomosc = "ID=" + str(decodeID) + "$ST=" + "null" + "$IO=" + Operacja + str(
            IDO(Operacja)) + "$OP=" + Operacja + "$Z1=" + str(z1) + "$Z2=" + str(z2) + "$ZC=" + str(ZC) + "$"
        serversocket.send(bytes(wiadomosc, 'utf-8'))
    else:
        return "0"


def AskForRelog():
    global decodeID
    nowTime = datetime.now()
    year = nowTime.strftime("%Y")
    month = nowTime.strftime("%m")
    day = nowTime.strftime("%d")
    time = nowTime.strftime("%H:%M:%S")
    ZC = nowTime.strftime("%d/%m/%Y,%H:%M:%S")
    wiadomosc = "ID=" + str(decodeID) + "$ST=" + "null" + "$OP=" + "RE$ZC=" + str(ZC) + "$"
    serversocket.send(bytes(wiadomosc, 'utf-8'))


def ReceiveID():
    global decodeID
    id = serversocket.recv(1024)
    idstr = str(id, 'utf8')  # konwertowanie id sesji do formatu utf-8
    id = str(idstr)
    id = id.split("$", 10)
    decodeID = id[0]
    decodeID = decodeID[3:]
    czas = id[3]
    czas = czas[3:]
    print("\nPolaczono z serwerem. Twoj nowy identyfikator sesji to: ", decodeID, sep="")
    print("Znacznik czasu: ", czas)


def AskForHistoryByID():
    global decodeID
    nowTime = datetime.now()
    year = nowTime.strftime("%Y")
    month = nowTime.strftime("%m")
    day = nowTime.strftime("%d")
    time = nowTime.strftime("%H:%M:%S")
    ZC = nowTime.strftime("%d/%m/%Y,%H:%M:%S")
    IDS = input("Podaj ID sesji do wyswietlenia historii:")
    while len(IDS) != 6:
        IDS = input(
            "ID sesji jest niewlasciwy, sprobuj ponownie: \n")  # tutaj ma do skutku prosic o conajmniej 6 cyfrowy id sesji
    wiadomosc = "ID=" + str(
        decodeID) + "$ST=" + "null" + "$OP=" + "HS" + "$HS=" + IDS + "$ZC=" + ZC + "$"  # w kazdej wiadomosci ma byc wysylane id biezacej sesji dltego id = id sesji
    serversocket.send(bytes(wiadomosc, 'utf-8'))


def EndSession():
    nowTime = datetime.now()
    year = nowTime.strftime("%Y")
    month = nowTime.strftime("%m")
    day = nowTime.strftime("%d")
    time = nowTime.strftime("%H:%M:%S")
    ZC = nowTime.strftime("%d/%m/%Y,%H:%M:%S")

    wiadomosc = "ID=" + str(
        decodeID) + "$ST=" + "null" + "$OP=" + "FN" + "$ZC=" + ZC + "$"  # w kazdej wiadomosci ma byc wysylane id biezacej sesji dltego id = id sesji
    serversocket.send(bytes(wiadomosc, 'utf-8'))


def AskForHistoryByIO():
    IDOP = input("Podaj indentyfikator operacji:")
    nowTime = datetime.now()
    year = nowTime.strftime("%Y")
    month = nowTime.strftime("%m")
    day = nowTime.strftime("%d")
    time = nowTime.strftime("%H:%M:%S")
    ZC = nowTime.strftime("%d/%m/%Y,%H:%M:%S")
    while len(IDOP) < 3:
        IDOP = input(
            "ID operacji matematycznej jest niewlasciwy, sprobuj ponownie: \n")  # tutaj ma do skutku prosic o conajmniej 3 znakowy id
    wiadomosc = "ID=" + str(decodeID) + "$ST=" + "null" + "$OP=" + "HI" + "$IO=" + IDOP + "$ZC=" + str(ZC) + "$"
    serversocket.send(bytes(wiadomosc, 'utf-8'))


while 1:
    operation = switchOperation()
    # dziala
    if operation == "FN":
        print("Zakonczono dzialanie programu, rozlaczono z serwerem.")
        EndSession()
        serversocket.close()
        break
    elif operation == "HS":
        print("Wyswietlenie historii obliczen przez ID sesji.")
        AskForHistoryByID()
        listenIncomingHSIO()
    elif operation == "HO":
        print("Wyswietlenie historii obliczens przez ID obliczen.")
        AskForHistoryByIO()
        listenIncomingHSIO()
    elif operation == "OB":
        print("Wykonywanie operacji matematycznych.")
        sprawdzanko = CreateAndSendMessage(switchMathOperation())
        if sprawdzanko != "0":
            listenIncoming()
    elif operation == "RE":
        AskForRelog()
        ReceiveID()
    else:
        print("\nPodano nieprawidlowy numer operacji, sprobuj jeszcze raz...")