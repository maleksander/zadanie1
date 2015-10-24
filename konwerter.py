import sys

#sprawdzenie czy wprowadzono sciezke pliku
if len(sys.argv) <2:
    print "podaj sciezke pliku"
    sys.exit(1)

#sprawdzenie czy wskazany plik ma wlasciwy format
nazwa = sys.argv[1].split('.')
if nazwa[-1] != "bedGraph" and nazwa[1] != "wig":
    print "niewlasciwy format pliku"
    sys.exit(1)

#otwarcie wskazanego pliku
plik = open(sys.argv[1], "r")

#plik do zapisu - zmiana nazwy zgodnie z konwersja
if nazwa[1] == "bedGraph":
    nazwa[1] = "wig"
    jakiformat = "bedGraph"    
elif nazwa[1] == "wig":
    nazwa[1] = "bedGraph"
nowanazwa = ".".join(nazwa)
plikzapis= open(nowanazwa, 'w')


#czytanie linijka po linijce
linijki =[]
linijki = plik.readlines()
track=[]
indeksyt =[]
indeksyf =[]
indeksyv =[]
kolejnetracki =[]
for i in range(0, len(linijki)):

    #znalezienie track line i definition line 
    if linijki[i].startswith("track"):
        t = i
        linijka = linijki[i]
        indeksyt.append(t)
        track.append(linijki[t])
        track_spl = linijka.split()
        if track_spl[2] == "type=bedGraph":
            track_spl[2] = track_spl[2].replace("type=bedGraph", "type=wiggle_0")
        else:
            track_spl[2] = track_spl[2].replace("type=wiggle_0", "type=bedGraph")
        track_spl = " ".join(track_spl) + "\n"
        kolejnetracki.append(track_spl)
        
    elif linijki[i].startswith("fixedStep"):
        jakiformat = "fixedStep"
        f = i
        indeksyf.append(f)
    elif linijki[i].startswith("variableStep"):
        jakiformat = "variableStep"
        v = i
        indeksyv.append(v)
        
indeksyt.append(len(linijki))

#czytanie z bedGraph
if jakiformat == "bedGraph":
    a=-1
    b=a+1
    for j in range(0, len(indeksyt)-1):
        a+=1
        b+=1        
        sekcja = {}
        for i in range(indeksyt[a] +1, indeksyt[b]): 
            wartosci = (linijki[i].split())
            chromosom = wartosci[0]
            start = int(wartosci[1]) + 1
            stop = int(wartosci[2]) + 1
            wartosc = float(wartosci[3])
            if not chromosom in sekcja:
                sekcja[chromosom] = []
            sekcja[chromosom].append([start, stop, wartosc])
            
        
        plikzapis.write(kolejnetracki[j]) 
        for chromosom in sekcja:
            s=sekcja[chromosom][0][0]
            st=int(sekcja[chromosom][1][0]) - int(sekcja[chromosom][0][0])
            sp = int(sekcja[chromosom][0][1]) - int(sekcja[chromosom][0][0])
            
            declaration_line = ["fixedStep", "chrom="+chromosom, "start="+str(s), "step="+str(st), "span="+str(sp)]
            deklaracja = " ".join(declaration_line) + "\n"
            plikzapis.write(deklaracja)
            for linijka in sekcja[chromosom]:
                wiersz = str(linijka[2])+"\n"
                plikzapis.write(wiersz)
    plikzapis.close()

        

        
        
        
        
        
        

    
            
           
    
    
      

        


