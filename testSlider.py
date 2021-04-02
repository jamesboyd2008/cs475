import pandas as pandas
import plotly.graph_objects as go
import numpy as np

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
colName = dataFrame.columns[1]
# print("keys:\n", dataFrame.keys())


specialColumn = dataFrame[colName]
specialColumn.fillna(0)

# print("specialColumn:\n", specialColumn)

# values = specialColumn.values.fillna(0) # fail
# values = specialColumn.values
# cleanValues = values[np.logical_not(np.isnan(values))]

# print(cleanValues)

# print("specialColumn values:\n", specialColumn.values)
vapes = specialColumn.values.tolist()

for i in range(len(vapes)):
    vape = vapes[i]
    # print(vapes[i], type(vapes[i]), str(vapes[i]) == 'nan')
    if str(vapes[i]) == 'nan':
        vapes[i] = 0

vapes.pop(0)
# print("list version:\n", vapes)



# Create figure
fig = go.Figure()

# Add traces, one for each slider step
for step in np.arange(0, 5, 0.1):
    fig.add_trace(
        go.Scatter(
            visible=False,
            line=dict(color="#00CED1", width=6),
            name="𝜈 = " + str(step),
            # pickup here: update these xy pairs
            # x=np.arange(0, 10, 0.01),
            # y=np.sin(step * np.arange(0, 10, 0.01))))
            x=np.arange(0, len(vapes), 0.01),
            y=vapes))

# Make 10th trace visible
fig.data[10].visible = True

# Create and add slider
steps = []
for i in range(len(fig.data)):
    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig.data)},
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