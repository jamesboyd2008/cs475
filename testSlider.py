# This script visualizes soil vapor concentrations over time.

import datetime
import numpy as np
import pandas as pandas
import plotly.graph_objects as go

dataFrame = pandas.read_excel(
    "soil-vapor_complete-data-set_11_25_20_modified.xlsx",
    engine = 'openpyxl',
    index_col = "Date")

# printing the spreadsheet to confirm import
# print("dataFrame:")
# print(dataFrame)

# print the names of the columns
# print("columns:\n", dataFrame.columns)
# print column type (it's <class 'pandas.core.indexes.base.Index'>)
# print("columns type:\n", type(dataFrame.columns))
# print("second col:\n", dataFrame.columns[1])

# getting rid of NaN... didn't work
# dataFrame.interpolate(method = "linear")

# must replace NaNs in index before using this
# dataFrame.interpolate(method = "cubicspline")

# dataFrame.replace(0) # fail

# dataFrame.fillna(0)

# first row of column
colName = dataFrame.columns[1]

print("keys:\n", dataFrame.keys())
# print("colName:", colName)

specialColumn = dataFrame[colName]
specialColumn.fillna(0)

dateCol = dataFrame[dataFrame.columns[0]]
dateCol.fillna(method = 'backfill')

# print("specialColumn:\n", specialColumn)
print("dateCol:\n", dateCol)

# values = specialColumn.values.fillna(0) # fail
# values = specialColumn.values
# cleanValues = values[np.logical_not(np.isnan(values))]

# print(cleanValues)

# print("specialColumn values:\n", specialColumn.values)
vapes = specialColumn.values.tolist()
dates = dateCol.values.tolist()

# Clean up the vapes.
for i in range(len(vapes)):
    # print(vapes[i], type(vapes[i]), str(vapes[i]) == 'nan')
    if str(vapes[i]) == 'nan':
        vapes[i] = 0

# Clean up the dates.
now = datetime.datetime.now()

# Drop empty rows.
# for i in range(len(dates)):
i = 0
length = len(dates)
while(i < length):
    # print(i, dates[i], vapes[i])
    # if ((dates[i] == 0 and vapes[i] == 0) or \
    #    (type(dates[i]) != type(now)) or \
    #    vapes[i] == 0):
    if (dates[i] == 0 or vapes[i] == 0 or \
       (type(dates[i]) != type(now))):
        # remove the row
        dates.pop(i)
        vapes.pop(i)
        length -= 1
    i += 1

i = 0
length = len(dates)
while(i < length):
    if vapes[i] == 0:
        # remove the row
        dates.pop(i)
        vapes.pop(i)
        length -= 1
    i += 1


i = 0
length = len(dates)
while(i < length):
    if vapes[i] == 0:
        # remove the row
        dates.pop(i)
        vapes.pop(i)
        length -= 1
    i += 1

i = 0
length = len(dates)
while(i < length):
    if vapes[i] == 0:
        # remove the row
        dates.pop(i)
        vapes.pop(i)
        length -= 1
    i += 1

i = 0
length = len(dates)
while(i < length):
    if vapes[i] == 0 or vapes[i] == " NC  ":
        # remove the row
        dates.pop(i)
        vapes.pop(i)
        length -= 1
    i += 1



# vapes.pop(0) # pop the NC value
# dates.pop(0) # even out for getting the same quantity of dates

# for i in range(len(dates)):
#     print(i, dates[i], vapes[i])
#     if vapes[i] == 0:
#         print('zero vape date:', i)


# print("list version:\n", vapes)
# print("len(vapes):\n", len(vapes))
# print("len(dates):\n", len(dates))
# print("dates:", dates)




# Create figure
fig = go.Figure()

# Add traces, one for each slider step
for step in np.arange(0, 5, 0.1):
    fig.add_trace(
        go.Scatter(
            visible=False,
            line=dict(color="#00CED1", width=6),
            name="𝜈 = " + str(step),
            # x=np.arange(0, 10, 0.01),
            # y=np.sin(step * np.arange(0, 10, 0.01))))

            # len(vapes) is 185.
            # With 0.01 steps, we get a 1.85 length of axis
            # give it a custom length
            # match the x with the dates

            # x=np.arange(0, len(vapes), 1),
            x=dates,
            y=vapes))

# Make 10th trace visible
fig.data[10].visible = True

# TODO: add standard deviations and means to visualization

# Create and add slider
steps = []
for i in range(len(fig.data)):
    # pickup here: make the slider behave properly.
    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig.data)},
              # {"title": "Slider switched to step: " + str(i)}],  # layout attribute
              {"title": "Slider switched to step: " + str(i)}],  # layout attribute
    )
    step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
    steps.append(step)

sliders = [dict(
    active=10,
    currentvalue={"prefix": "Frequency: "},
    pad={"t": 50},
    steps=steps
)]

fig.update_layout(
    sliders=sliders
)

fig.show()




