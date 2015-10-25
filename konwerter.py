import sys
import re

#sprawdzenie czy wprowadzono sciezke pliku
if len(sys.argv) <2:
    print "podaj sciezke pliku"
    sys.exit(1)

#sprawdzenie czy wskazany plik ma wlasciwy format
nazwa = sys.argv[1].split('.')
if nazwa[-1] != "bedGraph" and nazwa[-1] != "wig":
    print "niewlasciwy format pliku"
    sys.exit(1)

#otwarcie wskazanego pliku
plik = open(sys.argv[1], "r")

#plik do zapisu - zmiana nazwy zgodnie z konwersja
if nazwa[-1] == "bedGraph":
    nazwa[-1] = "wig"
    jakiformat = "bedGraph"    
elif nazwa[-1] == "wig":
    nazwa[-1] = "bedGraph"
nowanazwa = ".".join(nazwa)
plikzapis= open(nowanazwa, 'w')


#czytanie linijka po linijce
linijki =[]
linijki = plik.readlines()
track=[]
indeksyt =[]
kolejnetracki =[]
for i in range(0, len(linijki)):

#znalezienie track line i definition line 
    if linijki[i].startswith("track"):
        t = i
        linijka = linijki[i]
        indeksyt.append(t)
        track.append(linijki[t])
        track_spl = linijka.split()
        if track_spl[1] == "type=bedGraph":
            track_spl[1] = track_spl[1].replace("type=bedGraph", "type=wiggle_0")
        else:
            track_spl[1] = track_spl[1].replace("type=wiggle_0", "type=bedGraph")
        track_spl = " ".join(track_spl) + "\n"
        kolejnetracki.append(track_spl)
        
    elif linijki[i].startswith("fixedStep"):
        jakiformat = "fixedStep"
    elif linijki[i].startswith("variableStep"):
        jakiformat = "variableStep"

        
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

elif jakiformat== 'fixedStep':
    a=-1
    b=a+1
    for j in range(0, len(indeksyt)-1):
        a+=1
        b+=1        
        sekcja = {}
        for i in range(indeksyt[a] +1, indeksyt[b]):
            linijka = linijki[i]
            if len(linijka.strip()) == 0:
                continue
            if linijka.startswith('fixedStep'):
                DATA = linijka
                linijka_split = re.findall(r"[\w']+", DATA)
                chrom= linijka_split[2]
                pocz= int(linijka_split[4]) - 1
                krok= int(linijka_split[6])
                spn=  int(linijka_split[8])
                sekcja[chrom] = []
            else:
                sekcja[chrom].append([pocz, pocz + spn, float(linijka)])
                pocz += krok

        plikzapis.write(kolejnetracki[j]) 
        for chrom in sekcja:
            for linijka in sekcja[chrom]:
                wiersz = [chrom, str(linijka[0]), str(linijka[1]), str(linijka[2])]
                wiersz_str = " ".join(wiersz) +"\n"
                plikzapis.write(wiersz_str)
    plikzapis.close()

elif jakiformat=='variableStep':
    a=-1
    b=a+1
    for j in range(0, len(indeksyt)-1):
        a+=1
        b+=1        
        sekcja = {}
        for i in range(indeksyt[a] +1, indeksyt[b]):
            linijka = linijki[i]
            if len(linijka.strip()) == 0:
                continue
            if linijka.startswith('variableStep'):
                DATA = linijka
                linijka_split = re.findall(r"[\w']+", DATA)
                chrom= linijka_split[2]
                spn=  int(linijka_split[4])
                sekcja[chrom] = []
            else:
                wiersze = linijka.split()
                pocz = int(wiersze[0]) -1
                warto = float(wiersze[1])
                sekcja[chrom].append([pocz, pocz + spn, warto])
        

        plikzapis.write(kolejnetracki[j])
        for chrom in sekcja:
            for linijka in sekcja[chrom]:
                wiersz = [chrom, str(linijka[0]), str(linijka[1]), str(linijka[2])]
                wiersz_str = " ".join(wiersz) + "\n"                
                plikzapis.write(wiersz_str)
    plikzapis.close()

        

        
        
        
        
        
        

    
            
           
    
    
      

        


