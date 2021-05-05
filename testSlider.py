# This script visualizes soil vapor concentrations over time.

import datetime
import numpy as np
import pandas as pandas
import plotly.express as plotXpress

dataFrame = pandas.read_excel(
    "soil-vapor_complete-data-set_11_25_20_modified.xlsx",
    engine = 'openpyxl',
    index_col = None)

"""
Clean dataFrame:
1. Removing junk columns.
2. Fixing column names by removing whitespace
3. removing bad rows, such as rows with
    a. partial data
    b. wierd values, such as NC
   Maybe just delete the row from that column,
   that is, just give it a zero, or see what NaN does.
   Specify that the row is just for the three sampling depths
   (or just one?)
"""

# print(dataFrame)
# print(dataFrame.columns)


# Clean dataFrame.

# Drop bad date column
dataFrame.drop(dataFrame.iloc[:, 0:1], inplace = True, axis = 1)
# print(dataFrame)

# Remove whitespace from column names.


# track which triplett is being graphed
triCount = 0

# pair columns into 3's of shallow, medium, and deep depths.
col0 = dataFrame.columns[triCount    ]
col1 = dataFrame.columns[triCount + 1]
col2 = dataFrame.columns[triCount + 2]
col3 = dataFrame.columns[triCount + 3]

# establish working dataframe of 3 depths
triplet = dataFrame[[col0, col1, col2, col3]]

# Remove ugly rows
# triplet.dropna()

# print(triplet)

# Rows to be marked for deletion due to ugliness.
uglyRows = []

now = datetime.datetime.now()
nowType = type(now)
strCls = type('s')

for index, row in triplet.iterrows():
    if type(row['DATE']) != nowType or \
       type(row[col1]) == strCls:
        # drop the row
        triplet = triplet.drop([index])

# Build month column.
month = []
for index, row in triplet.iterrows():
    month.append(row['DATE'].strftime("%B"))

# Add the month list to the dataframe.
triplet['Month'] = month

# Build year column.
year = []
for index, row in triplet.iterrows():
    year.append(row['DATE'].year)

# Add the year list to the dataframe.
triplet['Year'] = year

# Build a dict of y axis ranges per year for keeping all data in the view.
yMinMax = {}
# temporary placeholders for tracking min/max of y values per year
curYear, prevYear, curMin, curMax = None, None, None, None
minContender, maxContender = None, None

# Determine min/max per year
for index, row in triplet.iterrows():
    curYear = row['Year']
    if prevYear is None:
        prevYear = curYear

    yVals = [row[col1], row[col2], row[col3]]
    minContender = min(yVals)
    maxContender = max(yVals)

    # Determine whether to reset min/max trackers.
    if prevYear is not curYear:
        # We've seen the highs and lows (vice versa). Record them.
        yMinMax[prevYear] = [curMin, curMax]
        prevYear = curYear
        curMin = minContender
        curMax = maxContender

    # Determine whether there's a new min/max.
    if curMin is None or minContender < curMin:
        curMin = minContender
    if curMax is None or maxContender > curMax:
        curMax = maxContender

# Make a list of min/max to add as a column to the dataframe.
yMins, yMaxs = [], []
for index, row in triplet.iterrows():
    yMins.append(yMinMax[row['Year']][0])
    yMaxs.append(yMinMax[row['Year']][1])

triplet['Min'] = yMins
triplet['Max'] = yMaxs

print(triplet)


fig = plotXpress.line(
                        data_frame = triplet,
                        x = 'Month',
                        y = [col1, col2, col3],
                        # range_y (list of two numbers) – If provided, overrides auto-scaling on the y-axis in cartesian coordinates.
                        # range_y = []# this line
                        # pickup here: make it autoscale per year
                        animation_frame = 'Year',
                        title = "Soil Vapor Concentrations",
                        labels =    {
                                        'Month': "Month",
                                        'value': "Hydrocarbon ppm",
                                        'variable': "Sampling Site"
                                    }
                     )

# fig.update_yaxes(autorange = True) # doesn't work
# fig["layout"].pop("updatemenus")
fig.layout.pop("updatemenus")
# fig.layout.pop("update_yaxes") # doesn't work
# fig["layout"].pop("update_yaxes")

# find the range of the lines.
# ymin, ymax = fig['layout']['yaxis']['range']


fig.show()
# Persit the page (then sftp it onto serve at Manoa)
# fig.write_html("hydrocarbon_slider.html")

# https://plotly.com/python/reference/layout/yaxis/
# consider log y axis.
# "variable" is the label for tank triplets. Try "Sampling Sites"
# update y_range to fit via autoscale by default
# clean up labels.
# try to make lines a little wider
# try to make lines a little less opaque - try ~75% opacity
# fix monthwise granularity via "reset axes" by default
# clarify the meaning of svo2s, svo2m, svo2d
# consider a dashboard of all 20 tanks visible, some red, some yellow, some red.
#   then, the dashboard operator can zoom in on individual tanks
#       and view a facet grid of tank triplets, if they chose multiple,
#       or just the one. https://plotly.com/python/facet-plots/

# Dr. Don is open to bar graphs: three bars for each site. Twenty total.

# Select 1-[18-20] of triplets

# TODO: optional: implement additional visualization as range slider
#                 .. and allow toggling between the two.

#




