import csv

def GetData(instance):
    #Input: instancia
    #Output: n: número de trabajos, m: número de máquinas, data[]: matriz con el tiempo pij que tarda cada máquina i para procesar cada trabajo j.
    ct=0
    n=0
    m=0
    data=[]
    with open(instance, newline='') as File:
        reader = csv.reader(File)
        ct=0
        for row in reader:
            #print("ct: ", ct)
            if ct > 1:
                vec=[]
                for x in range(0, (m*2)+1):
                  if(x!=0 and x%2==0):
                    vec.append(int(row[x]))
                    #print("elementos: ", vec)
                    data.append(vec)
            else:
                #print(row[0])
                if ct == 0:
                    try:
                        n=int(row[0].partition(" ")[0])
                        #print("n:", n)
                    except ValueError:
                        print(" ")
                if ct ==1:
                    try:
                        #m=int(row[0].partition(" ")[2])
                        m=int(row[0])
                        #print("m:", m)
                    except ValueError:
                        print(" ")
                ct+=1

    return (data, n, m)