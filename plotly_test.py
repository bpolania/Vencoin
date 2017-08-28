import plotly.plotly as py
from plotly.graph_objs import *

trace0 = Scatter(
    x=[1, 2, 3, 4],
    y=[10, 15, 13, 17]
)
trace1 = Scatter(
    x=[1, 2, 3, 4],
    y=[16, 5, 11, 12]
)
data = Data([trace0, trace1])

print py.plot(data, filename = 'basic-line', fileopt = 'overwrite', auto_open = False)
