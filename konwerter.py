import sys

#sprawdzenie czy wprowadzono sciezke pliku
if len(sys.argv) <2:
    print "podaj sciezke pliku"
    sys.exit(1)

#sprawdzenie czy wskazany plik ma wlasciwy format
nazwa = sys.argv[1].split('.')
if nazwa[1] != "bedGraph" and nazwa[1] != "wig":
    print "niewlasciwy format pliku"
    sys.exit(1)

#otwarcie wskazanego pliku
plik = open(sys.argv[1], "r")

#plik do zapisu - zmiana nazwy zgodnie z konwersja
if nazwa[1] == "bedGraph":
    nazwa[1] = "wig"
    jakiformat = "bedGraph"    
elif nazwa[1] == "wig":
    jakiformat = "wig"
    nazwa[1] = "bedGraph"
nowanazwa = ".".join(nazwa)
print jakiformat
plikzapis= open(nowanazwa, 'w')

#czytanie linijka po linijce
linijki =[]
linijki = plik.readlines()
for i in range(0, len(linijki)):
    #print linijki[i]
    
#znalezienie track line
    if linijki[i].startswith("track"):
        track = linijki[i]         
        x = i + 1
    if linijki[i].startswith("fixedStep"):
        jakiformat = "fixedStep"
        

# zamaiana typu w track line
track_line = track.split()  #['track', 'type=bedGraph', 'name="BedGraph', 'Format"', 'description="BedGraph', 'format"']
if track_line[1] == "type=bedGraph":
    track_line[1] = track_line[1].replace("type=bedGraph", "type=wiggle_0")
else:
    track_line[1] = track_line[1].replace("type=wiggle_0", "type=bedGraph")
#print track_line
track_line_def = " ".join(track_line) + "\n"
plikzapis.write(track_line_def)



#czytanie wartosci danych  z bedgraph
if jakiformat == "bedGraph":
    chromosomy=[]
    pozstart=[]
    pozstop =[]
    value=[]

    for a in range (x, len(linijki)-1):
        wartosci = (linijki[a].split())
        chromosom = wartosci[0]
        chromosomy.append(wartosci[0])
        start = int(wartosci[1]) + 1
        pozstart.append(start)
        stop = int(wartosci[2]) + 1
        pozstop.append(stop)
        wartosc = float(wartosci[3])
        value.append(wartosc)

#tworzenie declaration line

    span = pozstop[1] - pozstart[1]
    step = pozstop[1] - pozstop[0]
    declaration_line=[]
    declaration_line = ["fixedStep", "chrom="+str(chromosomy[1]),"start="+str(pozstart[0]), "step="+str(step), "span="+str(span)]
    deklaracja = " ".join(declaration_line) + "\n"
    #print deklaracja
    plikzapis.write(deklaracja)


#drukowanie wartosci w formacie fixedStep
    for d in range(0,len(linijki)-(x+1)):
        #a = str(pozstart[d])
        b = str(value[d]) + "\n"
        #c = a +" " + b + "\n"
        plikzapis.write(b)
    plikzapis.close()
    
