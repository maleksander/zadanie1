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
indeksyt =[]
indeksyf =[]
indeksyv =[]
track=[]
ktora = []
z=-1
kolejnetracki =[]
for i in range(0, len(linijki)):

    #znalezienie track line i definition line 
    if linijki[i].startswith("track"):
        z += 1
        t = i
        linijka = linijki[i]
        indeksyt.append(t)
        track.append(linijki[t])
        ktora.append(z)
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
#print indeksyt
#print ktora
liczba_setow = len(ktora)

#for i in range(0, liczba_setow):
#    n= ktora[i]
#    track_spl = track[n].split()
#    if track_spl[2] == "type=bedGraph":
#        track_spl[2] = track_spl[2].replace("type=bedGraph", "type=wiggle_0")
#    else:
#        track_spl[2] = track_spl[2].replace("type=wiggle_0", "type=bedGraph")
#    track_spl = " ".join(track_spl) + "\n"
#    kolejnetracki.append(track_spl)
#print kolejnetracki

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

        
       
elif jakiformat=='wig':
    a=-1
    b=a+1
    for j in range(0, len(indeksyt)-1):
        a+=1
        b+=1        
        sekcja = {}
        chromosom = None
        step = 0
        span = 0
        start = 0
        obecny_indeks = 0
        for i in range(indeksyt[a] +1, indeksyt[b]):
            linijka = linijki[i]
            if len(linijka.strip()) == 0:
                continue
            if linijka.startswith('fixedStep'):
                # dowiedz sie jaki to chromosom, jaki step, start i span
                chromosom = 'cos'
                step = 0
                start = 0
                obecny_indeks = start
                span = 0
                sekcja[chromosom] = []
            else:
                sekcja[chromosom].append([obecny_indeks, obecny_indeks + span, float(linijka)])
                obecny_indeks += step
            
        #print sekcja
        print kolejnetracki[j] #write
        index = start
        for chromosom in sekcja:
            for linijka in sekcja[chromosom]:
                print chromosom, linijka[0], linijka[1], linijka[2]
                index += step
                # upewnic sie, czy nie trzeba gdzies dodac albo odjac 1
            
        
          
    #declaration_line=[]
    #for i in range(0, len(indeksyt)-1):  
        #declaration_line = ["fixedStep", "chrom="+chrom[i], "start="+strt[i], "step="+srep[i], "span="+sran[i]]
        #deklaracja = " ".join(declaration_line) + "\n"
        
        
        
        
        
        

    
            
           
    
    
      

        


