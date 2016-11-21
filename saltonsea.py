import numpy as np
import math
import matplotlib.pyplot as pl

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


        #Below calculates for julian day of first day of every month
        #http://www.cs.utsa.edu/~cs1063/projects/Spring2011/Project1/jdn-explanation.html
        
        #value of 'a' needs to be integer. value 1 for Jan, Feb. value 0 for Mar to Dec

        a = np.floor((14 - j + 1)/12)
        y = year + 4800 - a
        m = j + 1 + 12*a - 3

        #1 because first day of each month
        JDN = 1 + (153*m + 2)/5 + 365*y + y/4 - y/100 + y/400 -32045
        JD = JDN + (12 - 12)/24 + 0/1440 + 0/86400

        if j == 11:
            year += 1


        #julian day row
        julianDayRow.append(JD)
        
        
        #Penman's Equation. 
        #es, a function of temperature, is saturated vapor pressure in air at certain temperature
        es = 0.6108 * np.exp((17.27 * temperature[j]) / (237.3 + temperature[j]))
        
        #vapor pressure row
        vaporPressureRow.append(es)
        

    julianDayMatrix.append(julianDayRow)
    vaporPressureMatrix.append(vaporPressureRow)
    
#solar declination on day J
solarDeclination = 0.4093 *  np.sin((2 * np.pi * np.array(julianDayMatrix)/365) - 1.405)


sunsetHourAngle = np.arccos(-1 * np.tan(np.deg2rad(phi)) * np.tan(solarDeclination))

#Nt is the maximum number of daylight hours on day t
Nt = (24*sunsetHourAngle)/np.pi

#print(solarDeclination)
#print(sunsetHourAngle)
#print(Nt)

#reset year to 2003
year = 2003
for i in range(0, numYearsInt):

    evaporationRow = []

    for j in range(0, 12):

        #calculate average evporation per month. 
        evaporation = daysInMonth[j]*(2.1 * Nt[i][j]**2 * vaporPressureMatrix[i][j]) / (temperature[j] + 273.2)


        evaporationRow.append(evaporation)

    evaporationMatrix.append(evaporationRow)


#print(evaporationMatrix)
tEvaporationMatrix = np.transpose(evaporationMatrix) #(mm/month)

tEvaporationMatrix /= 304.8 #(ft/month)

#sum the elements by column to get yearly evaporation
tEvaporationMatrix = np.sum(tEvaporationMatrix, axis=0)

print(tEvaporationMatrix)

#SCENARIO 1##########

#ASSUME that inflow will be constant throughout the years
#ASSUME that the salinity of the lake will be well distributed over course of the year

##inflow = 1332500(ac-ft/yr), 1.643614549e+12(L/yr)

inflow = 0.3943 #inflow (mi^3/yr)
salinity_i = 44000 #initial salinity level of lake (mg/L)

#chosen salinity of the inflow 10343(mg/L)
##multiply salinity of inflow 10343(mg/L) to the water inflow rate 1.643614549e+12(L/yr) to find saltmassperyear

saltMassPerYear= 1.73e+16 #total amount of salt in inflow (mg/yr)

waterLevel_i = -235 #initial water level compared to sea level (ft)
volume_i = 15.93 #initial lake volume (mi^3)
volume = 15.93
surfaceArea_i = 357.67 # initial surface area (mi^2)

xAxisYear = []
xAxisYear2 = []
yAxisWaterLevel = []
yAxisSalinity = []


yAxisWaterLevel2 = []
yAxisSalinity2 = []


xAxisYear.append(0)
yAxisWaterLevel.append(waterLevel_i)
yAxisSalinity.append(salinity_i)

yAxisWaterLevel2.append(waterLevel_i)
yAxisSalinity2.append(salinity_i)


for i in range(1, numYearsInt + 1):
    #create x-axis
    xAxisYear.append(i)

    # find new level of water level with inflow factored in
    # f(x) = 2.8142x - 15.399 at residual of 0.9638
    #waterLevel_i = 2.8142 * (volume + 0.3943) - 282.44

    #(ft)      =     (ft)     -         (ft)            + (mi^3) /  mi^3      *     (ft)  
    waterLevel = waterLevel_i - tEvaporationMatrix[i - 1] + (inflow / surfaceArea_i * 5380) #ft

    # find surface area at the new water level using the calculated trend equation:
    # f(x) = 7.9104x + 222.48 at residual of 0.9763
    # (mi^2)    = 7.9104 *     ft     + 2224.83
    surfaceArea = 7.9104 * waterLevel + 2224.83

    surfaceArea_i = surfaceArea


    # find volume at the new water level using the calculated trend equation:
    # f(x) = 0.3425 x + 97.062 at residual of 0.9638
    # (mi^3) = 0.3425 * waterLevel + 97.062
    volume = 0.3425 * waterLevel + 97.062

    # update the next initial water level
    waterLevel_i = waterLevel

    #mg/L    =    mg/L    +  ((mg * yr /  * yr ) / ( mi^3   *  L/mi^3 )
    salinity = salinity_i + ((saltMassPerYear * i)/ (volume * 4.168e+12) ) #mg/L

    yAxisWaterLevel.append(waterLevel)
    yAxisSalinity.append(salinity)


print(xAxisYear)
#print(yAxisWaterLevel)
print(yAxisSalinity)

fig = pl.figure()
yAxis1 = fig.add_subplot(111)
yAxis1.plot(xAxisYear, yAxisWaterLevel)
yAxis1.set_ylabel('Elevation (ft)')


yAxis2 = yAxis1.twinx()
pl.ylabel('Salinity (mg/L)')

yAxis2.plot(xAxisYear, yAxisSalinity, 'r-')

pl.xlabel('Years from 2003')

pl.title('Salton Sea Water Level Elevation and Salinity (Scenario 1)')

pl.show()


### SCENARIO 2 ###

#In scenario 2 the inflow is at 0.2353 mi^3/yr
#

#Assume that total salinity of the inflow remains unchanged at 10343 mg/L
waterLevel_i = -235
saltMassPerYear2 = 1.014e+16 
inflow2 = 0.2353
for i in range(1, numYearsInt):
    #x axis is already created
    # xAxisYear
    xAxisYear.append(i)


    if i >= 15:
        inflow2 = 0.2122
        #due to decreased amount of inflow, inflow of salt mass is recalculated
        saltMassPerYear2 = 9.1474e+15



    waterLevel2 = waterLevel_i - tEvaporationMatrix[i - 1] + (inflow2 / surfaceArea_i * 5380)

    surfaceArea2 = 7.91 * waterLevel2 + 2224.83 # mi^2

    surfaceArea_i = surfaceArea2

    waterLevel_i = waterLevel2

    yAxisWaterLevel2.append(waterLevel_i)

    volume = 0.3425 * waterLevel2 + 97.062

    salinity = salinity_i + ((saltMassPerYear2 * i) / (volume * 4.168e+12) )

    yAxisSalinity2.append(salinity)


print('x axis year', xAxisYear)
print('y axis waterLevel2', yAxisWaterLevel2)
fig = pl.figure()
yAxis1 = fig.add_subplot(111)
yAxis1.plot(xAxisYear, yAxisWaterLevel2)
yAxis1.set_ylabel('Elevation (ft)')

yAxis2 = yAxis1.twinx()
pl.ylabel('Salinity (mg/L)')

yAxis2.plot(xAxisYear, yAxisSalinity2, 'r-')

pl.xlabel('Years from 2003')

pl.title('Salton Sea Water Level Elevation and Salinity (Scenario 2)')

pl.show()