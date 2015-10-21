import sys
print sys.argv
if len(sys.argv) <2:
    print "podaj sciezke do pliku"
    sys.exit(1) #1 jesli cos poszlo nie tak  0 jesli ok
    
x = sys.argv[1].split(".")
if x[1] != "bedGraph" and x[1] != "wig":
    print "niewlasciwy plik"
    sys.exit(1) 

plik = open(sys.argv[1], "r")
if x[-1] == "bedGraph":
    x[-1]= "wig"
else:
    x[-1] = "bedGraph"
string = "."
nowanazwa = string.join(x)
plik1 = open(nowanazwa, 'w')
linie = plik.readlines()
for i in linie:
    print i
    



# konwerter.py C:\Users\Maciek\plik.wig
# sys.argv => [..., 'C:\Users\Maciek\plik.wig']
# sys.argv[1].split('.') => ['C:\Users\Maciek\plik', 'wig']
# ['...', 'bedGraph']
# '.'.join([...]) => 'C:\Users\Maciek\plik.bedGraph'
