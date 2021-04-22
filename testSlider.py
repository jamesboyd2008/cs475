# # This script visualizes soil vapor concentrations over time.
#
# import datetime
# import numpy as np
# import pandas as pandas
# import plotly.graph_objects as go
#
# dataFrame = pandas.read_excel(
#     "soil-vapor_complete-data-set_11_25_20_modified.xlsx",
#     engine = 'openpyxl',
#     index_col = "Date")
#
# # first row of column
# colName = dataFrame.columns[1]
#
# print("keys:\n", dataFrame.keys())
# # print("colName:", colName)
#
# specialColumn = dataFrame[colName]
# specialColumn.fillna(0)
#
# dateCol = dataFrame[dataFrame.columns[0]]
# dateCol.fillna(method = 'backfill')
#
# print("dateCol:\n", dateCol)
#
# vapes = specialColumn.values.tolist()
# dates = dateCol.values.tolist()
#
# # Clean up the vapes.
# for i in range(len(vapes)):
#     if str(vapes[i]) == 'nan':
#         vapes[i] = 0
#
# # Clean up the dates.
# now = datetime.datetime.now()
#
# # TODO: DRY up the loops
#
# # Drop empty rows.
# i = 0
# length = len(dates)
# while(i < length):
#     if (dates[i] == 0 or vapes[i] == 0 or \
#        (type(dates[i]) != type(now))):
#         # remove the row
#         dates.pop(i)
#         vapes.pop(i)
#         length -= 1
#     i += 1
#
# i = 0
# length = len(dates)
# while(i < length):
#     if vapes[i] == 0:
#         # remove the row
#         dates.pop(i)
#         vapes.pop(i)
#         length -= 1
#     i += 1
#
#
# i = 0
# length = len(dates)
# while(i < length):
#     if vapes[i] == 0:
#         # remove the row
#         dates.pop(i)
#         vapes.pop(i)
#         length -= 1
#     i += 1
#
# i = 0
# length = len(dates)
# while(i < length):
#     if vapes[i] == 0:
#         # remove the row
#         dates.pop(i)
#         vapes.pop(i)
#         length -= 1
#     i += 1
#
# i = 0
# length = len(dates)
# while(i < length):
#     if vapes[i] == 0 or vapes[i] == " NC  ":
#         # remove the row
#         dates.pop(i)
#         vapes.pop(i)
#         length -= 1
#     i += 1
#
#
#
#
# # Create figure
# fig = go.Figure()
#
# # Add traces, one for each slider step
# for step in np.arange(0, 5, 0.1):
#     fig.add_trace(
#         go.Scatter(
#             visible=False,
#             line=dict(color="#00CED1", width=6),
#             name="date = " + str(step),
#             # x=np.arange(0, 10, 0.01),
#             # y=np.sin(step * np.arange(0, 10, 0.01))))
#
#             # len(vapes) is 185.
#             # With 0.01 steps, we get a 1.85 length of axis
#             # give it a custom length
#             # match the x with the dates
#
#             # x=np.arange(0, len(vapes), 1),
#             x=dates,
#             y=vapes))
#
# # Make 10th trace visible
# fig.data[10].visible = True
#
# # TODO: add standard deviations and means to visualization
#
# # Create and add slider
# steps = []
# for i in range(len(fig.data)):
#     step = dict(
#         method="update",
#         args=[{"visible": [False] * len(fig.data)},
#               # {"title": "Slider switched to step: " + str(i)}],  # layout attribute
#               {"title": "Slider switched to step: " + str(i)}],  # layout attribute
#     )
#     step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
#     steps.append(step)
#
# sliders = [dict(
#     active=10,
#     currentvalue={"prefix": "Frequency: "},
#     pad={"t": 50},
#     steps=steps
# )]
#
# fig.update_layout(
#     sliders=sliders
# )
#
# fig.show()
#
#
#
#

import datetime
import numpy as np
import pandas as pandas
import plotly.express as plotXpress

dataFrame = pandas.read_excel(
    "soil-vapor_complete-data-set_11_25_20_modified.xlsx",
    engine = 'openpyxl',
    index_col = "DATE")

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
col2 = dataFrame.columns[triCount    ]
col3 = dataFrame.columns[triCount + 1]
col4 = dataFrame.columns[triCount + 2]

# establish working dataframe of 3 depths
triplet = dataFrame[[col2, col3, col4]]
# print(triplet)

# Remove ugly rows
triplet.dropna()


# Remove NC ("Not Collected") row(s)
# ID ugly rows
uglyRows = []


for i in triplet.index:
    # pickup here: fix key error
    print(triplet[' SV02S  '][i])

# TODO: optional: implement additional visualization as range slider
#                 .. and allow toggling between the two.

#




