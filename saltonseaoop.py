import numpy as np
import matplotlib.pyplot as pl
from matplotlib.patches import Polygon

class SaltonSea:

    def __init__(self):

        self.evaporationMatrix = []

        self.year = 2003
        self.latitude = np.deg2rad(33.3)

        #celsius
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

        #average annual precipitation
        #http://www.areavibes.com/salton+sea+beach-ca/weather/
        self.precipitation = 4.3/12 #(ft)

        #initial water level at elevation compared to the sea level
        self.waterLevel = -235 #(ft)

        #initial lake volume
        self.volume = 15.93 #(mi^3)

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

                #print ('JD', JD)

                solarDeclination = 0.4093 * np.sin((2 * np.pi  * JD / 365) - 1405)

                #Hargreave's Equation -> sunset hour angle [radians]
                sunsetHourAngle = np.arccos(-1 *np.tan(self.latitude) * np.tan(solarDeclination))

                #print('sun angle', sunsetHourAngle)

                #Nt is the maximum number of daylight hours on day t
                Nt = (24*sunsetHourAngle)/np.pi


                #Penman's Equation.
                #vapor pressure (es), is a function of temperature
                es = 0.6108 * np.exp((17.27 * self.temperature[j]) / (237.3 + self.temperature[j]))

                #print('es', es)


                evaporation = self.daysInMonth[j]*(2.1 * Nt**2 * es) / (self.temperature[j] + 273.2) #mm/day

                evaporationRow.append(evaporation)

            self.evaporationMatrix.append(evaporationRow)

        self.evaporationMatrix = np.transpose(self.evaporationMatrix) #(mm/month)

        self.evaporationMatrix /= 304.8 #(ft/month)

        #sum the elements by column to get yearly evaporation
        self.evaporationMatrix = np.sum(self.evaporationMatrix, axis=0)

    def contourMap(self):
        x = np.random.normal(3., 1., (0,0))  # generate a random map
        exten = np.array([0, 23, 0, 23])

        ax = pl.figure().add_subplot(111)

        im = pl.imshow(x,  origin='lower',extent=exten)

        hx = "1.59 2 2.5 3.21 3.52 4.16 4.57 4.74 5.97 6.59 7.01 7.09 7.47 7.78 7.86 8.16 8.16 8.37 8.3 8.89 9.42 9.77 10.17 10.34 10.44 10.44 11.18 11.99 12.51 13.43 14.25 14.53 15.09 15.66 16.69 17.06 17.74 18.2 18.74 18.92 19.17 19.73 19.85 20.16 20.39 20.38 20.7 20.92 21.17 21.25 21.44 21.45 21.54 21.47 21.61 21.63 21.43 20.37 20.1 19.99 19.84 19.33 19.11 19.12 19.03 19.14 18.87 18.94 18.04 17.54 17.29 16.58 15.88 15.58 15.28 14.71 14.55 14.13 14.09 13.93 13.35 12.98 12.54 12.31 12.28 12.09 11.69 11.39 11.21 11.24 11.01 10.91 10.43 10.42 10.14 10.21 10.4 10.3 10.3 10.11 10.22 10.21 10.22 10.04 10.02 9.84 9.77 9.71 9.54 9.45 9.2 9 8.95 8.54 7.76 7.75 7.22 7.26 7.11 7.11 6.11 6.34 5.49 5.22 3.72 3.47 3.06 2.93 3.13 3.07 2.87 2.62 2.43 1.76 1.41 1.26 1.02 .98 .88 .92 .71 .64 .61 .8 1.26 1.43"
        hy = "22.35 22.37 22.1 21.46 21.25 21.01 20.99 21.06 20.93 20.92 20.53 20.36 20.07 19.97 19.74 19.52 19.3 19.17 18.98 18.32 17.92 17.71 17.32 17.3 17.2 16.98 15.8 14.89 14.1 13.39 13.22 13.32 13.86 14.1 13.59 13.16 12.97 12.64 11.91 11.49 11.25 10.32 10.07 9.69 9.14 8.96 8.63 8.07 7.58 7.03 6.53 6.09 5.97 5.8 5.24 4.77 4.14 3.42 3.35 3.43 3.1 3.08 2.75 2.36 2.19 2.1 1.59 1.26 1.09 1.12 1.02 .93 .28 .18 .28 .78 .95 1.2 1.33 1.31 1.66 1.82 1.98 2.13 2.26 2.29 2.21 2.25 2.36 2.54 2.63 2.87 3.02 3.46 3.83 4.42 4.96 5.14 5.47 5.63 5.84 6.34 6.37 6.57 6.77 7.01 7.21 7.5 7.68 7.93 7.97 8.21 8.55 8.53 9.29 9.62 9.89 10.25 10.5 10.85 11.45 11.91 12.72 12.89 14.26 14.48 14.66 14.93 15.51 16.02 16.27 17.11 17.43 17.9 18.12 18.39 18.81 19.44 19.7 20.06 20.36 20.74 21.37 21.72 21.95 22.25"

        h = self.parseCoordinates(hx, hy)

        ax.add_patch(Polygon(h, fill=False))


        gx = "1.61 1.8 2.26 3.05 3.7 4.21 4.97 5.87 6.35 6.87 7.1 7.7 8 8.38 8.6 9.05 9.68 10.22 10.37 10.45 11.14 12.05 12.75 13.45 14.23 14.77 14.97 15.02 15.24 15.44 15.62 15.8 16.05 16.52 16.90 17.09 17.27 17.37 17.59 17.91 18.34 18.45 18.84 18.98 19.18 19.23 19.57 19.73 19.94 20.37 20.41 20.37 20.05 19.61 18.97 18.67 18.62 17.71 17.71 16.99 16.79 15.86 15.59 15.2 14.91 14.53 14.22 14.15 13.95 13.48 12.94 12.78 12.64 12.49 12.38 12.14 11.95 11.98 11.74 11.05 10.9 10.94 10.68 10.57 10.6 10.51 10.49 10.2 9.92 9.45 8.83 8.49 7.24 6.83 6.63 5.64 5.3 4.62 4.12 3.66 3.42 3.21 3.28 3.07 2.85 2.23 1.69 1.32 1.28 1.41"
        gy = "20.81 21.07 21.26 21.07 20.76 20.68 20.67 20.74 20.74 20.48 20.19 19.84 19.51 18.91 18.53 18.04 17.63 17.22 16.99 16.6 15.46 14.58 13.73 13.22 13.09 13.31 13.31 13.42 13.44 13.51 13.42 13.42 13.23 13.09 12.59 12.61 12.69 12.57 12.56 12.29 11.87 11.56 11.09 10.69 10.57 10.31 9.74 8.85 8.58 7.21 6.41 5.83 5.39 5.19 5.01 4.61 4.37 3.65 3.47 2.89 1.94 1.53 1.19 1.05 1.07 1.33 1.4 1.71 1.81 1.81 2.13 2.22 2.48 2.46 2.58 2.58 2.89 3.21 3.53 3.83 4.09 4.4 4.54 4.97 5.47 5.69 6.11 6.62 7.36 8.27 8.8 9.58 10.95 11.57 12.01 12.89 13.23 13.61 14.24 14.63 14.71 15.03 15.45 16.33 17.23 17.94 18.27 19 19.76 20.53"

        g = self.parseCoordinates(gx, gy)

        ax.add_patch(Polygon(g, fill=False))


        fx = "2.28 2.74 3.74 4.1 4.99 5.29 6.08 6.69 7.26 7.95 8.8 9.63 10.2 10.37 10.9 11.24 11.34 12.28 13.01 13.39 14.04 14.63 14.79 15.7 15.73 16.27 16.62 17.06 17.52 17.93 18.25 18.53 18.76 18.72 18.84 18.93 18.94 19.06 19.1 19 18.94 18.64 18.7 18.54 18.38 18.02 17.07 16.65 16.57 16.36 16.26 15.77 15.42 15.3 15.31 15.05 14.78 14.22 13.56 13.41 13.09 12.99 13.08 13.03 12.78 12.78 12.59 12.11 11.78 11.08 10.8 10.74 10.58 10.29 9.97 9.92 9.7 9.45 9.42 8.9 8.23 8.01 7.88 7.62 7.34 7.15 7.06 6.62 6.06 5.56 5.02 4.8 4.6 4.34 4 3.54 3.34 3.26 3.08 2.9 2.89 2.42 2.19 2.07 2.13 2.3"
        fy = "19.74 20.03 20.16 20.26 20.34 20.46 20.39 20.36 19.93 19.33 18.14 17.43 17.02 16.35 15.5 15.11 14.85 13.95 13.24 13.12 12.76 12.71 12.63 12.72 12.83 12.58 12.29 12.17 11.82 11.11 10.68 10.05 10.02 9.58 8.95 8.82 8.43 8.37 7.86 7.04 6.83 6.73 6.61 6.62 6.34 5.99 5.55 4.89 4.16 3.88 3.47 3.12 2.89 2.48 2.05 1.95 2.02 2.5 2.68 2.81 2.82 2.92 3.26 3.43 3.49 3.76 4.21 4.79 4.96 5.02 5.17 5.79 6.42 6.94 7.57 8.18 8.89 9.36 9.69 10.43 10.97 10.97 11.09 11.11 11.31 11.56 11.91 12.41 13.06 13.5 13.85 13.9 14.1 14.41 14.62 15.09 16 16.69 17.37 17.59 17.78 18.38 18.69 19.03 19.36 19.73"

        f = self.parseCoordinates(fx, fy)

        ax.add_patch(Polygon(f, fill=False))


        ex = "2.74 3.74 4.26 4.75 5.17 6.24 6.69 7.66 8 8.93 9.98 10.9 11.62 12.7 13.56 13.92 14.56 15.38 16.19 17.17 17.36 17.63 18.05 18.3 18.29 17.97 17.43 16.76 16 15.78 15.18 14.39 14.11 13.9 13.81 13.36 13.1 13.09 12.62 12.49 11.32 11.23 11.05 10.62 10.42 10.23 10.22 9.98 9.98 9.3 9.05 8.56 8.11 7.9 7.49 7.33 7.03 6.36 5.76 5.13 4.76 4.03 3.62 3.41 3.41 3.19 3.1 2.79"
        ey = "18.84 19.76 19.87 19.92 20.13 20.23 20.24 19.49 19.19 17.93 16.92 15.29 14.39 13.35 12.85 12.69 12.62 12.32 12.16 11.36 10.91 10.68 10.01 9.04 7.93 7.56 7.42 6.62 5.56 5.12 4.6 4.54 4.15 4.14 4.27 4.25 4.49 4.67 5.01 5.48 5.5 5.4 5.47 6.59 6.9 7.7 8.21 8.55 9.83 10.64 10.87 11.16 11.23 11.31 11.3 11.54 12.26 12.92 13.49 13.9 14.11 14.85 15.24 15.91 17.1 17.7 18.04 18.46"

        e = self.parseCoordinates(fx, fy)

        ax.add_patch(Polygon(e, fill=False))


        dx = "3.67 3.63 4.14 5.14 5.83 6.37 7.03 7.8 8.8 9.27 9.25 10.21 10.81 12.28 13.16 13.83 14.52 15.9 16.58 17.33 17.82 17.8 17.44 17.16 16.9 16.49 15.68 15.43 15.2 14.33 13.66 13.38 13.01 12.64 12.36 12.02 11.36 11.25 10.85 10.43 10.48 10.63 10.34 10.03 9.7 8.97 8.33 8.09 7.29 6.13 4.61 3.97 3.59"
        dy = "16.97 18.17 18.93 19.64 19.74 19.96 19.86 19.21 17.93 17.41 17.22 16.03 15 13.49 12.83 12.52 12.37 11.54 10.94 9.92 8.89 8.44 8.44 8.16 7.69 7.29 6.88 6.56 6.04 5.27 5.27 5.42 5.94 6.15 6.19 6.36 6.28 6 6.75 7.38 8.54 9.36 10.17 10.44 10.88 11.41 11.7 11.71 12.25 13.44 14.52 15.23 15.96"

        d = self.parseCoordinates(dx, dy)

        ax.add_patch(Polygon(d, fill=False))


        cx = "4.02 4.32 4.64 5.55 6.74 7.43 8.07 8.36 8.94 10.17 10.8 12.44 13.64 14.31 15.49 16.06 16.51 16.69 16.59 16.13 14.64 14.16 13.69 13.22 12.42 11.92 11.55 11.3 10.71 10.25 9.63 8.37 7.9 7.15 6.53 5.19 4.33"
        cy = "16.12 17.96 18.41 18.96 19.29 19.07 18.51 18.09 17.44 15.48 14.26 12.62 11.87 11.82 11.21 10.68 9.75 9.25 8.81 8.29 6.68 6.48 6.6 7.04 7.71 8.15 8.69 10.15 11.01 11.61 11.94 12.1 12.41 13.77 14.17 14.5 15.18"

        c = self.parseCoordinates(cx, cy)

        ax.add_patch(Polygon(c, fill=False))


        bx = "4.33 4.36 4.55 5.43 6.11 7.42 8.49 9.14 9.54 9.81 10.09 10.28 10.7 12.08 13.17 14.61 15.17 15.8 16.04 16.04 15.26 14.55 13.89 12.55 12.07 11.97 11.47 10.75 10.18 9.47 8.98 8.27 7.69 7.08 5.69 4.89"
        by = "15.59 16.67 17.23 18.22 18.52 18.64 17.7 16.42 15.9 15.38 14.92 14.22 14.01 12.04 11.28 10.94 10.74 10.12 9.58 8.96 7.94 7.5 7.48 8.44 9.11 10.09 11.4 11.95 12.38 12.54 12.54 12.96 13.88 14.51 14.79 14.92"

        b = self.parseCoordinates(bx, by)

        ax.add_patch(Polygon(b, fill=False))


        a2x = "12.77 12.83 12.78 13.19 13.9 14.55 14.77 14.75 14.33 13.81 13.16"
        a2y = "10.65 10.37 9.74 9.21 8.83 8.97 9.23 9.63 10.07 10.3 10.41"

        a2 = self.parseCoordinates(a2x, a2y)

        ax.add_patch(Polygon(a2, fill=False))


        a1x = "5.33 5.79 6.35 7.2 7.93 8.93 9.42 9.44 9.81 9.81 9.62 9.2 8.61 8.2 7.96 7.23 5.9 5.31"
        a1y = "16 17 17.39 17.39 17 16.09 15 14.46 13.7 13.32 13.19 13.22 13.7 14.55 14.63 15.05 15.17 15.71"

        a1 = self.parseCoordinates(a1x, a1y)

        ax.add_patch(Polygon(a1, fill=False))


        pl.show()

    def parseCoordinates(self, x, y):
        x = x.split()
        y = y.split()

        arr = []

        for i in range(0, len(x)):
            subArr = []
            subArr.append(float(x[i]))
            subArr.append(float(y[i]))
            arr.append(subArr)

        return arr
        




class Scenario(SaltonSea):

    def __init__(self, SaltonSea, inflow):

        self.inflow = inflow #(mi^3/yr)
        self.inflowSalinity = 10343 #mg/L
        """
               mg / yr            mi^3/yr  *   L / mi^3  *    mg / L
        """
        self.saltMassPerYear = self.inflow * 2.39913e+13 * self.inflowSalinity

        self.lakeSalinity = 44000 #(mg/L)
        self.volume = SaltonSea.volume # mi^3
        """
                   mg             mi^3  *   L / mi^3  *    mg / L
        """
        self.saltMassLake = self.volume * 2.39913e+13 * self.lakeSalinity



        self.waterLevel_i = SaltonSea.waterLevel # ft
        self.surfaceArea_i = SaltonSea.surfaceArea # mi^2

        self.xAxisYear = []
        self.xAxisYear.append(0)

        self.yAxisWaterLevel = []
        self.yAxisWaterLevel.append(self.waterLevel_i)

        self.yAxisSalinity = []
        self.yAxisSalinity.append(self.lakeSalinity)

        for i in range(1, SaltonSea.numYears + 1):
            self.xAxisYear.append(i)

            #if the water volume of lake is less than 0, then there is nothing left for evaporation
            #set the lake volume to 0
            if self.volume < 0:
                SaltonSea.evaporationMatrix[i - 1] = 0
                self.volume = 0

            #inflow adds to the volume
            self.volume += self.inflow


            """
            Find new level of water level with inflow factored in
            f(x) = 2.8142x - 282.44 at residual of 0.9638
            """
            waterLevel = 2.8142 * self.volume - 282.44 - SaltonSea.evaporationMatrix[i - 1] + SaltonSea.precipitation

            """
            Find volume at the new water level using the calculated trend equation:
            f(x) = 0.3425 x + 97.062 at residual of 0.9638
            """
            self.volume = 0.3425 * waterLevel + 97.062

            # update the next initial water level
            #self.waterLevel_i = waterLevel

            #mg/L    =    mg/L    +  ((mg * yr /  * yr ) / ( mi^3   *  L/mi^3 )
            self.lakeSalinity = (self.saltMassLake + self.saltMassPerYear * i)/ (self.volume * 4.168e+12) #mg/L

            self.yAxisWaterLevel.append(waterLevel)
            self.yAxisSalinity.append(self.lakeSalinity)

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


def main():
    ss = SaltonSea()

    while True:
        try:
            print('Please enter the number of years from 2003 for proper projection: ', end="")
            ss.numYears = int(input())
            ss.calculateEvaporation()
            break
        except ValueError:
            print("That is not a valid number. Please try again\n")

    while True:
        try:
            print('\n1. Contour Map')
            print('2. Scenario 1')
            print('3. Scenario 2')
            print('Please select the following (1 - 3): ', end="")
            option = int(input())
            if(option >= 1 and option <= 3):
                if(option == 1):
                    ss.contourMap()
                if(option == 2):
                    scenario1 = Scenario(ss, 0.3943)
                    scenario1.plotChart()
                if(option == 3):
                    print('3 is pressed')
                break
        except ValueError:
            print("That is not a valid option. Please try again.")


if __name__ == "__main__":
    main()




