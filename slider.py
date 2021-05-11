# This script visualizes soil vapor concentrations over time.

import datetime
import numpy as np
import pandas as pandas
import plotly.express as plotXpress

dataFrame = pandas.read_excel(
    "soil-vapor_complete-data-set_11_25_20_modified.xlsx",
    engine = 'openpyxl',
    index_col = None)

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

# # Build a dict of y axis ranges per year for keeping all data in the view.
# yMinMax = {}
# # temporary placeholders for tracking min/max of y values per year
# curYear, prevYear, curMin, curMax = None, None, None, None
# minContender, maxContender = None, None
#
# # Determine min/max per year
# for index, row in triplet.iterrows():
#     curYear = row['Year']
#     if prevYear is None:
#         prevYear = curYear
#
#     yVals = [row[col1], row[col2], row[col3]]
#     minContender = min(yVals)
#     maxContender = max(yVals)
#
#     # Determine whether to reset min/max trackers.
#     if prevYear is not curYear:
#         # We've seen the highs and lows (vice versa). Record them.
#         yMinMax[prevYear] = [curMin, curMax]
#         prevYear = curYear
#         curMin = minContender
#         curMax = maxContender
#
#     # Determine whether there's a new min/max.
#     if curMin is None or minContender < curMin:
#         curMin = minContender
#     if curMax is None or maxContender > curMax:
#         curMax = maxContender
#
# # Make a list of min/max to add as a column to the dataframe.
# yMins, yMaxs = [], []
# for index, row in triplet.iterrows():
#     yMins.append(yMinMax[row['Year']][0])
#     yMaxs.append(yMinMax[row['Year']][1])
#
# triplet['Min'] = yMins
# triplet['Max'] = yMaxs

# Build rows to be appended to the front of the dataset for normalcy of
#   axis display between the first year and following years.

# Find out which months need filling
# Check whether a year has a record for each of 12 months
oldYear, newYear, oldMonth, newMonth = None, None, None, None
monthsOfYear =  [
                    "zerothMonth",
                    "January",
                    "Februay",
                    "March",
                    "April",
                    "May",
                    "June",
                    "July",
                    "August",
                    "September",
                    "October",
                    "November",
                    "December"
                ]

padFront = []
for index, row in triplet.iterrows():
    if oldMonth is None:
        oldYear = row['Year']
        oldMonth = row['Month']
    # newYear = row['Year']
    if oldMonth != 'January':
        newMonth = 1
        # create new montly rows of 0's until we hit oldMonth
        while monthsOfYear[newMonth] != oldMonth:
            newRow = []
            fillerDatetime = datetime.datetime(oldYear, newMonth, 1, 1, 1, 1, 1)
            newRow.append(fillerDatetime)
            # col1
            newRow.append(0)
            # col2
            newRow.append(0)
            # col3
            newRow.append(0)
            # Month
            newRow.append(fillerDatetime.strftime("%B"))
            # Year
            newRow.append(fillerDatetime.year)
            # Add the new row to the list of rows to be prepended to dataframe.
            padFront.append(newRow)
            # Increment empty month tracker.
            newMonth += 1
        break

# Prepend built rows for x axis normalcy.
for row in padFront:
    newRow =    pandas.DataFrame(
                                    {
                                        'DATE': row[0],
                                        col1: row[1],
                                        col2: row[2],
                                        col3: row[3],
                                        'Month': row[4],
                                        'Year': row[5]
                                    },
                                    index = [0]
                                )
    triplet = pandas.concat([newRow, triplet]).reset_index(drop = True)

# Determine y axis range
yMin = None
yMax = None
for index, row in triplet.iterrows():
    yVals = [row[col1], row[col2], row[col3]]
    minContender = min(yVals)
    maxContender = max(yVals)
    # Determine whether there's a new min/max.
    if yMin is None or minContender < yMin:
        yMin = minContender
    if yMax is None or maxContender > yMax:
        yMax = maxContender

print(triplet)

fig = plotXpress.line(
                        data_frame = triplet,
                        x = 'Month',
                        y = [col1, col2, col3],
                        range_y = [yMin, yMax],
                        animation_frame = 'Year',
                        title = "Soil Vapor Concentrations",
                        labels =    {
                                        'Month': "Month",
                                        'value': "Hydrocarbon ppm",
                                        'variable': "Sampling Site"
                                    }
                     )

fig.layout.pop("updatemenus")


# Add dropdown
fig.update_layout(
    updatemenus=[
        dict(
            buttons=list([
                dict(
                    args=["type", "surface"],
                    label="SVO2",
                    method="restyle"
                ),
                dict(
                    args=["type", "surface"],
                    label="SVO3",
                    method="restyle"
                ),
                dict(
                    args=["type", "surface"],
                    label="SVO4",
                    method="restyle"
                ),
                dict(
                    args=["type", "surface"],
                    label="SVO5",
                    method="restyle"
                ),
                dict(
                    args=["type", "surface"],
                    label="SVO6",
                    method="restyle"
                ),
                dict(
                    args=["type", "surface"],
                    label="SVO7",
                    method="restyle"
                ),
                dict(
                    args=["type", "heatmap"],
                    label="SVO8",
                    method="restyle"
                )
            ]),
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.1,
            yanchor="top"
        ),
    ]
)

# Add annotation
fig.update_layout(
    annotations=[
        dict(text="Choos sampling site:", showarrow=False,
        x=0, y=1.085, yref="paper", align="left")
    ]
)


fig.show()
# Persit the page (then sftp it onto serve at Manoa)
# fig.write_html("hydrocarbon_slider.html")

# https://plotly.com/python/reference/layout/yaxis/
# consider log y axis.
# "variable" is the label for tank triplets. Try "Sampling Sites"
# update y_range to fit via autoscale by default
# clean up labels.
# Implement the red, green, yellow square dashboard scenario
# try to make lines a little wider
# try to make lines a little less opaque - try ~75% opacity
# for the sake of visibility of overlapping lines
# fix monthwise granularity via "reset axes" by default
# clarify the meaning of svo2s, svo2m, svo2d
# consider a dashboard of all 20 tanks visible, some red, some yellow, some red.
#   then, the dashboard operator can zoom in on individual tanks
#       and view a facet grid of tank triplets, if they chose multiple,
#       or just the one. https://plotly.com/python/facet-plots/
# consider adding the red line for problematic

# Dr. Don is open to bar graphs: three bars for each site. Twenty total.

# Select 1-[18-20] of triplets

# TODO: optional: implement additional visualization as range slider
#                 .. and allow toggling between the two.

#




