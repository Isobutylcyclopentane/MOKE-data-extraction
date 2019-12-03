#MOKE_data analysis
import math
import csv
from scipy import optimize
import statistics

def read_MOKE_data(fileName):

    result = dict()
    result[1] = []
    result[2] = []
    result[3] = []
    result[4] = []

    with open(fileName, 'r',encoding="UTF-8-sig") as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            x, y = line
            x, y = float(x), float(y)
            if x>=0 and y>=0:
                result[1].append((x,y))
            elif x<=0 and y>=0:
                result[2].append((x,y))
            elif x<=0 and y<=0:
                result[3].append((x,y))
            elif x>=0 and y<=0:
                result[4].append((x,y))

    for index in result:
        result[index].sort()

    return result

def find_Mr(data):
    # get the data for residual magnetization and uncertainty
    # 1in: dict; 2out: float, float

    upperMr = find_intersection(data[2],data[1],0)
    lowerMr = find_intersection(data[2],data[1],0)

    # minimizing experimental error by centering the data
    # and find uncertainty by the uncentered value
    uncentered = abs(upperMr) - abs(lowerMr)
    Mr = abs(upperMr - uncentered)

    uncertainty = abs(uncentered) / 2

    return Mr,uncertainty

def find_Hc(data):
    leftHc = find_intersection(data[2],data[3], 1)
    rightHc = find_intersection(data[1],data[4], 1)

    uncentered = rightHc - leftHc
    Hc = rightHc - uncentered

    uncertantity = abs(uncentered)/2

    return Hc,uncertantity


def find_intersection(quadrum1, quadrum2, mode, numPtsAna = 1,):
    quadrum1.sort(key= lambda x: abs(x[mode]))
    quadrum2.sort(key= lambda x: abs(x[mode]))

    point_data = quadrum1[0:numPtsAna] + quadrum2[0:numPtsAna]
    point_data.sort()

    dataX = list(map(lambda x: x[0],point_data))
    dataY = list(map(lambda x: x[1],point_data))

    popt,pcov = list(optimize.curve_fit(liner, dataX, dataY))
    a,b = popt
    if mode == 1:
        return (b/a)
    elif mode == 0:
        return b


def find_Ms (data):

    Quad1Result = find_saturation(data[1])
    Quad3Result = find_saturation(data[3])

    uncent = Quad1Result[0] + Quad3Result[0]

    Ms = Quad1Result[0] - uncent
    uncertantity = Quad1Result[1] + abs(uncent)
    result = Ms, uncertantity

    return result


def find_saturation(quadrum):

    temp_y = []
    temp = []
    for i in range(6):
        tmp_val = quadrum[-(i+1)]
        temp_y.append(tmp_val[1])
        temp.append(tmp_val)

    for index in range((len(quadrum)-7),-1,-1):
        tmp_val = quadrum[index]

        stdv = statistics.stdev(temp_y)
        avg = statistics.mean(temp_y)
        upper_bound = avg + stdv
        lower_bound = avg - stdv

        if not (lower_bound < tmp_val[1] < upper_bound):
            break
        temp.append(tmp_val)
        temp_y.append(tmp_val[1])
    avg = statistics.mean(temp_y)
    stdv = statistics.stdev(temp_y)
    result = (avg,stdv)
    return result


def liner(x,a,b):
    return a * x + b


def MOKE_analysis(data):
    # complete analysis with a set of MOKE data
    # include find coercivity(Hc), residual magnetization(Mr), and saturation(Ms)
    # 1in: dict; 1out: dict

    result = dict()

    result["Hc_result"] = find_Hc(data)
    result["Mr_result"] = find_Mr(data)
    result["Ms_result"] = find_Ms(data)

    return result


def moke_main(fileName = None):
    if fileName == None:
        fileName = input("please enter the name of the data file (.csv required) => ")
    fileName += ".csv"
    data = read_MOKE_data(fileName)

    result = MOKE_analysis(data)
    Hc_result = result["Hc_result"]
    Mr_result = result["Mr_result"]
    Ms_result = result["Ms_result"]

    print("The coercivity strength (Hc) of the material is %.5f , with an uncertainty of %.5f" % Hc_result)
    print("The residual magnetization (Mr) of the material is %.5f, with an uncertainty of %.5f" % Mr_result)
    print("The magnetic saturation (Ms) of the material is %.5f, with an uncertainty of %.5f" % Ms_result)

    command = input("\nmore accurate data? (y/n) => ")
    if command.strip().lower() == 'y':
        print()
        print("Hc:",Hc_result[0],'±',Hc_result[1])
        print("Mr:",Mr_result[0],'±',Mr_result[1])
        print("Ms:",Ms_result[0],'±',Ms_result[1])
    elif command.strip().lower() =='n':
        return
    else:
        print("Invalid command")

if __name__ == "__main__":
    fileName = input("please type in the name of the data file => ")
    moke_main(fileName)


