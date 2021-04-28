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

triplet['Month'] = month

# Build year column.
year = []
for index, row in triplet.iterrows():
    year.append(row['DATE'].year)

triplet['Year'] = year

print(triplet)

fig = plotXpress.line(
                        data_frame = triplet,
                        x = 'Month',
                        # x = 'DATE',
                        y = [col1, col2, col3],
                        animation_frame = 'Year',
                        title = "Soil Vapor Concentrations",
                        # text = "Here Be Text"
                     )

fig["layout"].pop("updatemenus")
fig.show()

# pickup here: change y axis label to hydrocarbon ppm
# "variable" is the label for tank triplets. Try "Sampling Sites"
# try facetting tank triplets, or tank triplet aggregates
# update y_range to fit via autoscale by default
# clean up labels.
# try to make lines a little wider
# try to make lines a little less opaque - try ~75% opacity
# fix monthwise granularity via "reset axes" by default

# Select 1-[18-20] of triplets

# TODO: optional: implement additional visualization as range slider
#                 .. and allow toggling between the two.

#




