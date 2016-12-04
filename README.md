# Salton Sea Project

### What is this Project?

Salton Sea is a saline lake located in Riverside County, created accidentally when millions of gallons of water from Colorado River were diverted into a dried lakebed 200 feet below sea level. Although unintentionally created, Salton Sea because essential as it was a refugee to many wild life species and an attractive tourist attraction during its prime. Today’s Salton Sea tells a different story as rising salinity and decreasing lakebed have caused ecosystem decline in migrating birds and fishes in lake.

Facing such critical environmental issue, in 2003 California was asked to come with a plan to save Salton Sea.

The goal of this project is to create a projection of Salton Sea’s water level and its salinity depending on various water inflow within defined scenarios.

**First scenario** estimates total inflow of 0.3943 cubic mile per year with inflow salinity of 44000 mg/L.

**Second scenario** estimates total inflow of 0.233 cubic mile of water per year with inflow salinity of 44000 mg/L. In the year 2017, the inflow decreases to 0.212 cubic mile per year.

User inputs the number of years from 2003. The project will then give a yearly projection of Salton Sea’s water level.

### Background Story
I first started learning Python through my job. After playing with its interactive shell, I couldn’t help but think how similar its functions were to that of Matlab. Without a second thought, I decided to revive my Salton Sea Projection code I have written few years back.

Transitioning from Matlab to Python allows means for my Salton Sea to be more readily available. Thanks to Python (and its Matplotlib and Numpy library), my Salton Sea project lives again once more after years of being locked away in a proprietary file for a program with expired license.

After refamiliarizing with the logic of this programming, I have rewritten the code for efficiency and calibrated the calculation to project what I believe to be more accurate.

### (Brief) Summary of Process

The initial water level was recorded at -235 ft in year 2003. To find the lake volume in year 2003, the surface area of [each contour level](http://cdn.calisphere.org/data/13030/qs/kt5f59n7qs/figures/caljsiol_sio1ca175_113_073.gif) was first calculated using the [Simpsons Rule](http://mathworld.wolfram.com/SimpsonsRule.html). Knowing the depth of the lake at each surface area that is calculated, initial volume of water was estimated.

Trending Equation below was formed to establish relationship between the lake's water level and the remaining lake volume.
```
Water Level = 0.0728 * Lake Volume^2 + 1.4607 * Lake Volume - 282.44
    Regression of 0.9738, 1 being 100% accurate
```
```
Lake Volume = 0.3425 * water level + 97.062
    Regression of 0.96, 1 being 100% accurate
```

**Evaporation** is the only means of outflow for the Salton Sea. Thus, evaporation rate was carefuly calculated using the following information

* Latitude of Salton Sea: 33 degrees North
* Calculate [Julian Day](http://www.cs.utsa.edu/~cs1063/projects/Spring2011/Project1/jdn-explanation.html) from Gregorian Day
* The Following [Equations](http://nest.su.se/mnode/Methods/penman.htm) Below:
    * Penman's Equation which factors in average monthly temperature to calculate vapor pressure. (Note: This project assumes that the temperature will stay constant throughout the years and does not take climate change into a factor)
    * Hargreaves Equation to calculate Sunset Hour Angle 
    * Hamon's Equation to calculate daily evaporation rate

After yearly evaporation rate is calculated, water balance is formed below:

```
Lake Volume = inflow + precipitation - evaporation + initial lake volume
```

With Lake Volume calculated, Salinity Level is calculated:
```
Lake Salinity = (Mass of Lake Salt + Mass of Inflow Salt) / Lake Volume
```

