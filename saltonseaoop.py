import numpy as np
import math
import matplotlib.pyplot as pl

class SaltonSea:

    def __init__(self):
        print('Please enter the number of years from 2003 for proper projection: ', end="")
        numYearsInput = input()
        self.numYears = int(numYearsInput)

        self.julianDayMatrix = []
        self.vaporPressureMatrix = []
        self.evaporationMatrix = []

        self.year = 2003
        self.latitude = np.deg2rad(+33.3)

        self.temperature = [
            21.67, 24.44, 27.78,
            31.67, 35.56, 40.56,
            42.78, 41.67, 39.44,
            33.33, 26.11, 21.67
        ]

        self.daysInMonth = [
            31, 28, 31,
            30, 31, 30,
            31, 31, 30,
            31, 30, 31
        ]

    def calculateSunHours(self):
        for i in range(0, self.numYears):

            julianDayRow = []
            vaporPressureRow = []

            for j in range(0, 12):

                #Below calculates for julian day of first day of every month
                #http://www.cs.utsa.edu/~cs1063/projects/Spring2011/Project1/jdn-explanation.html
            
                #value of 'a' needs to be integer. value 1 for Jan, Feb. value 0 for Mar to Dec
                a = np.floor((14 - j + 1) / 12)
                y = self.year + j + 4800 - a
                m = j + 1 + 12*a - 3

                #calculates julian day of the first day of each month
                JDN = 1 + (153*m + 2)/5 + 365*y + y/4 - y/100 + y/400 -32045
                JD = JDN + (12 - 12)/24 + 0/1440 + 0/86400

                #julianDayRow is an array of 12 Julian Day of the first day of each month (Gregorian Calendar)
                julianDayRow.append(JD)

                #Penman's Equation.
                #es, a function of temperature
                es = 0.6108 * np.exp((17.27 * self.temperature[j]) / (237.3 + self.temperature[j]))

                #vapor pressure row
                vaporPressureRow.append(es)

                self.julianDayMatrix.append(julianDayRow)
                self.vaporPressureMatrix.append(vaporPressureRow)


        #solar declination on day J
        solarDeclination = 0.4093 * np.sin((2 * np.pi / 365) * np.array(self.julianDayMatrix) - 1405)

        #Hargreave's Equation -> sunset hour angle [radians]
        #sunsetHourAngle = np.arccos(-1 * np.tan(np.rad2deg(self.latitude)) * np.tan(solarDeclination))
        sunsetHourAngle = np.arccos(-np.tan(self.latitude) * np.tan(solarDeclination))

        #Nt is the maximum number of daylight hours on day t
        Nt = (24*sunsetHourAngle)/np.pi

        print('Solar Declination', solarDeclination)
        print('Sunset Hour Angle', sunsetHourAngle)
        print('Maximum Number of Daylight Hours', Nt)

        for i in range(0, self.numYears):
            evaporationRow = []
            for j in range(0, 12):

                #calculate average evporation per month. 
                evaporation = self.daysInMonth[j]*(2.1 * Nt[i][j]**2 * self.vaporPressureMatrix[i][j]) / (self.temperature[j] + 273.2)


                evaporationRow.append(evaporation)

            self.evaporationMatrix.append(evaporationRow)


        #print(evaporationMatrix)
        tEvaporationMatrix = np.transpose(self.evaporationMatrix) #(mm/month)

        tEvaporationMatrix /= 304.8 #(ft/month)

        #sum the elements by column to get yearly evaporation
        tEvaporationMatrix = np.sum(tEvaporationMatrix, axis=0)

        print(tEvaporationMatrix)






ss = SaltonSea()
ss.calculateSunHours()
