import numpy as np
import math

#ignore settings
np.seterr(over='ignore')

#initial year of 2003
year = 2003


#latitude (degree) of Salton Sea
phi = 33.3

#temperature is in celsius
temperature = [
    21.67, 24.44, 27.78,
    31.67, 35.56, 40.56,
    42.78, 41.67, 39.44,
    33.33, 26.11, 21.67
]

daysInMonth = [
    31, 28, 31,
    30, 31, 30,
    31, 31, 30,
    31, 30, 31
]

print('Please enter the number of years from 2003 for proper projection')
numYears = input()

numYearsInt = int(numYears)

#trouble shoot if the input is not a number

#endYear = year + numYearsInt

julianDayMatrix = []
vaporPressureMatrix = []
evaporationMatrix = []


#tallymarks year
for i in range(0, numYearsInt):

    julianDayRow = []
    vaporPressureRow = []
    

    #tallymarks month
    for j in range(0, 12):

        a = (14 - j + 1)/12
        y = year + 4800 - a
        m = j + 1 + 12*a - 3

        JDN = 1 + (153*m + 2)/5 + 265*y + y/4 - y/100 + y/400 -32045
        JD = JDN + (12 - 12)/24 + 0/1440 + 0/86400

        if j == 11:
            year += 1


        #julian day row
        julianDayRow.append(JD)
        
        
        #vapor pressure equation
        es = 0.6108 * np.exp((17.27 * temperature[j]) / (237.3 + temperature[j]))
        
        #vapor pressure row
        vaporPressureRow.append(es)
        

    julianDayMatrix.append(julianDayRow)
    vaporPressureMatrix.append(vaporPressureRow)
    

solarDecline = 0.4093 *  np.sin((2 * np.pi * np.array(julianDayMatrix)/365) - 1405)
sunAngle = np.arccos(-1 * np.tan(np.radians(solarDecline)))
Nt = (24*sunAngle)/np.pi

#print(solarDecline)
#print(sunAngle)
#print(Nt)

#reset year to 2003
year = 2003
for i in range(0, numYearsInt):

    evaporationRow = []

    for j in range(0, 12):

        #calculate average evporation per day. Multiply by 

        evaporation = 31*(2.1 * Nt[i][j]**2 * vaporPressureMatrix[i][j]) / (temperature[j] + 273.2)


        evaporationRow.append(evaporation)

    evaporationMatrix.append(evaporationRow)


#print(evaporationMatrix)
tEvaporationMatrix = np.transpose(evaporationMatrix) #(mm/year)
tEvaporationMatrix /= 304.8 #(ft/year)

#print(tEvaporationMatrix)


#SCENARIO 1##########

#ASSUME that inflow will be constant throughout the years
#ASSUME that the salinity of the lake will be well distributed over course of the year

##inflow = 1332500(ac-ft/yr), 1.643614549e+12(L/yr)

inflow = 0.3943 #inflow (mi^3/yr)
salinity_i = 44000 #initial salinity level of lake (mg/L)

#chosen salinity of the inflow 10343(mg/L)
##multiply salinity of inflow 10343(mg/L) to the water inflow rate 1.643614549e+12(L/yr) to find saltmassperyear

saltMassPerYear= 1.1173e+18 #total amount of salt in inflow (mg/yr)

waterLevel_i = -235 #initial water level compared to sea level (ft)
volume_i = 15.93 #initial lake volume (mi^3)
surfaceArea_i = 357.67 # initial surface area (mi^2)

xAxisYear = []
yAxisWaterLevel = []
yAxisSalinity = []
for i in range(0, numYearsInt):
    #create x-axis
    xAxisYear.append(i)

    #current water level = initial water level - evaporation + inflow
    waterLevel = waterLevel_i - evaporation + (inflow/surfaceArea_i) * 5280 #ft

    #surface area = 7.91 * water level + 2224.83
    surfaceArea = 7.91 * waterLevel + 2224.83 #mi^2

    surfaceArea_i = surfaceArea

    yAxisWaterLevel.append(waterLevel)

    volume = 0.34 * waterLevel * + 97.06 #mi^3

    waterLevel_i = waterLevel

    #mg/L + mg/yr * yr / mi^3
    salinity = salinity_i + ((saltMassPerYear * (i + 1))/volume) #mg/L

    yAxisSalinity.append(salinity)



print(yAxisWaterLevel)
print(yAxisSalinity)