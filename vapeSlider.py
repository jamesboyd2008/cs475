# This script visualizes soil vapor concentrations over time.

import datetime
import plotly.graph_objects as go
import pandas as pandas

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

# collection of all triplets
triplets = []

# Establish date column
col0 = dataFrame.columns[triCount    ]

# There must be a package that does this, but it's quicker to just DIY it.
monthsOfYear =  [
                    "zerothMonth", # datetime module associates 1 w/ January
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

# TODO: generate ~20 line charts in below FOR statement
# for i in range(1): # change 1 to 20?

# pair columns into 3's of shallow, medium, and deep depths.
col1 = dataFrame.columns[triCount + 1]
col2 = dataFrame.columns[triCount + 2]
col3 = dataFrame.columns[triCount + 3]
three = [col1, col2, col3]
triplets.append(three)
# Skip ahead to next triplet (ignoring redundant date columns)
triCount += 5

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


# Build rows to be appended to the front of the dataset for normalcy of
#   axis display between the first year and following years.

oldYear, newYear, oldMonth, newMonth = None, None, None, None

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


revFront = padFront[::-1]
# Prepend built rows for x axis normalcy.
for row in revFront:
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

# Build figure skeleton as per plotly graph_object specifications.
fig_dict =  {
                'data': [],
                'layout': {},
                'frames': []
            }

# Configure layout for visualization.
fig_dict['layout']['xaxis'] =   {
                                    'range': monthsOfYear,
                                    'title': 'Month',
                                    'type': 'category'
                                }
fig_dict['layout']['yaxis'] =   {
                                    'title': 'Hydrocarbon ppm',
                                    'type': 'linear' # considered log
                                }
fig_dict['layout']['hovermode'] = 'closest'
fig_dict['layout']['updatemenus'] = [
    # Enable animation and add buttons
    {
        'buttons': [
            # Add play button
            {
                'args': [
                    None,
                    {
                        'frame': {
                            'duration': 400,
                            'redraw': False
                        },
                        'fromcurrent': True,
                        'transistion': {
                            'duration': 350,
                            'easing': 'quadratic-in-out'
                        }
                    }
                ],
                'label': 'Play Years',
                'method': 'animate' # Enable slider functionality
            },
            # Add pause button
            {
                'args': [
                    [None],
                    {
                        'frame': {
                            'duration': 0,
                            'redraw': False
                        },
                        'mode': 'immediate',
                        'transition': {
                            'duration': 0
                        }
                    }
                ],
                'label': 'Pause Years',
                'method': 'animate'
            }
        ],
        'direction': 'left',
        'pad': {
            'r': 15,
            't': 80
        },
        'showactive': False,
        'type': 'buttons',
        'x': 0,
        'xanchor': 'right',
        'y': 0,
        'yanchor': 'top'
    }
]

sliders_dict = {
    'active': 0,
    'yanchor': 'top',
    'xanchor': 'left',
    'currentvalue': {
        'font': {
            'size': 20
        },
        'prefix': 'Year is ',
        'visible': True,
        'xanchor': 'right'
    },
    'transition': {
        'duration': 350,
        'easing': 'cubic-in-out'
    },
    'pad': {
        'b': 10,
        't': 50
    },
    'len': 0.9,
    'x': 0,
    'y': 0,
    'steps': [] # Filled in below
}

# Convert pandas dataframe into dict of lists for graph_object


















