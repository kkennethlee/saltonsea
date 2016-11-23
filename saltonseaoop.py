import numpy as np
import math
import matplotlib.pyplot as pl

class SaltonSea:

    def __init__(self):

        print('Please enter the number of years from 2003 for proper projection: ', end="")

        numYearsInput = input()
        self.numYears = int(numYearsInput)

        self.evaporationMatrix = []

        self.year = 2003
        self.latitude = np.deg2rad(+33.3)

        self.temperature = [
            21.67, 24.44, 27.78,
            31.67, 35.56, 40.56,
            42.78, 41.67, 39.44,
            33.33, 26.11, 21.67
        ]

        #days in each month
        self.daysInMonth = [
            31, 28, 31,
            30, 31, 30,
            31, 31, 30,
            31, 30, 31
        ]

        #initial water level at elevation compared to the sea level
        self.waterLevel = -235 #(ft)

        #initial surface area of the lake at initial water level of -235 ft
        self.surfaceArea = 7.9104 * self.waterLevel + 2224.83

    def calculateEvaporation(self):
        for i in range(0, self.numYears):

            #evaporation row holds 12 elements of montly evaporation rate
            evaporationRow = []

            for j in range(0, 12):

                #Below calculates for julian day of first day of every month
                #http://www.cs.utsa.edu/~cs1063/projects/Spring2011/Project1/jdn-explanation.html
            
                #value of 'a' needs to be integer. value 1 for Jan, Feb. value 0 for Mar to Dec
                a = np.floor((14 - j + 1) / 12)
                y = self.year + i + 4800 - a
                m = j + 1 + 12*a - 3

                #calculates julian day of the first day of each month
                JDN = 1 + (153*m + 2)/5 + 365*y + y/4 - y/100 + y/400 -32045
                JD = JDN + (12 - 12)/24 + 0/1440 + 0/86400

                solarDeclination = 0.4093 * np.sin((2 * np.pi / 365) * JD - 1405)

                #Hargreave's Equation -> sunset hour angle [radians]
                sunsetHourAngle = np.arccos(-np.tan(self.latitude) * np.tan(solarDeclination))

                #Nt is the maximum number of daylight hours on day t
                Nt = (24*sunsetHourAngle)/np.pi


                #Penman's Equation.
                #vapor pressure (es), is a function of temperature
                es = 0.6108 * np.exp((17.27 * self.temperature[j]) / (237.3 + self.temperature[j]))

                evaporation = self.daysInMonth[j]*(2.1 * Nt**2 * es) / (self.temperature[j] + 273.2)

                evaporationRow.append(evaporation)

            self.evaporationMatrix.append(evaporationRow)

        self.evaporationMatrix = np.transpose(self.evaporationMatrix) #(mm/month)

        self.evaporationMatrix /= 304.8 #(ft/month)

        #sum the elements by column to get yearly evaporation
        self.evaporationMatrix = np.sum(self.evaporationMatrix, axis=0)

        print("evaporation matrix", self.evaporationMatrix)



class Scenario(SaltonSea):

    def __init__(self, SaltonSea, inflow):

        self.inflow = inflow # (mi^3/yr)
        self.lakeSalinity = 44000# (mg/L)

        """
               mg / yr           mi^3/yr  *   L / mi^3  *    mg / L
        """
        self.saltMassPerYear = self.inflow * 2.39913e+13 * self.lakeSalinity
        
        self.waterLevel_i = SaltonSea.waterLevel
        self.surfaceArea_i = SaltonSea.surfaceArea

        self.xAxisYear = []
        self.xAxisYear.append(0)

        self.yAxisWaterLevel = []
        self.yAxisWaterLevel.append(SaltonSea.waterLevel)

        self.yAxisSalinity = []
        self.yAxisSalinity.append(self.lakeSalinity)

        for i in range(1, SaltonSea.numYears + 1):
            self.xAxisYear.append(i)

            """
            Find new level of water level with inflow factored in
            f(x) = 2.8142x - 15.399 at residual of 0.9638
            waterLevel_i = 2.8142 * (volume + 0.3943) - 282.44
            """

            #(ft)      =     (ft)     -         (ft)            + (mi^3) /  mi^3      *     (ft)  
            waterLevel = self.waterLevel_i - SaltonSea.evaporationMatrix[i - 1] + (inflow / self.surfaceArea_i * 5380) #ft


            """
            Find surface area at the new water level using the calculated trend equation:
            f(x) = 7.9104x + 222.48 at residual of 0.9763
            """

            #(mi^2)     = 7.9104 *     ft     + 2224.83
            surfaceArea = 7.9104 * waterLevel + 2224.83

            self.surfaceArea_i = surfaceArea

            """
            Find volume at the new water level using the calculated trend equation:
            f(x) = 0.3425 x + 97.062 at residual of 0.9638
            """
            volume = 0.3425 * waterLevel + 97.062

            # update the next initial water level
            self.waterLevel_i = waterLevel

            #mg/L    =    mg/L    +  ((mg * yr /  * yr ) / ( mi^3   *  L/mi^3 )
            salinity = self.lakeSalinity + ((self.saltMassPerYear * i)/ (volume * 4.168e+12) ) #mg/L

            self.yAxisWaterLevel.append(waterLevel)
            self.yAxisSalinity.append(salinity)

    def changeFlowRate(self, flowRate):
        self.inflow = flowRate

    def plotChart(self):
        #print(xAxisYear)
        #print(yAxisWaterLevel)
        #print(yAxisSalinity)

        fig = pl.figure()
        yAxis1 = fig.add_subplot(111)
        yAxis1.plot(self.xAxisYear, self.yAxisWaterLevel)
        yAxis1.set_ylabel('Elevation (ft)')


        yAxis2 = yAxis1.twinx()
        pl.ylabel('Salinity (mg/L)')

        yAxis2.plot(self.xAxisYear, self.yAxisSalinity, 'r-')

        pl.xlabel('Years from 2003')

        pl.title('Salton Sea Water Level Elevation and Salinity (Scenario 1)')

        pl.show()





ss = SaltonSea()
ss.calculateEvaporation()

scenario1 = Scenario(ss, 0.3943)

scenario1.plotChart()