import plotly.plotly as py
import plotly.graph_objs as go
from pymongo import MongoClient


def plot(name):
    client = MongoClient()
    results_db = client.analysis_database.results_database
    
    pre_data = results_db.find_one({"name": name},{"_id":0, "name" : 0})
    x = []
    y = []
    for k in pre_data.iterkeys():
        if (k != "_id" and k != "name"):
            x.append(k)
            y.append(pre_data[k])
    
    for i in range(0, len(y)):
        vmax = y[i]
        vpos = i
        for j in range(i,len(y)):
            if(y[j] > vmax):
                vmax = y[j]
                vpos = j
        tmp = y[i]
        y[i] = y[vpos]
        y[vpos] = tmp
        tmp = x[i]
        x[i] = x[vpos]
        x[vpos] = tmp

    data = [go.Bar(x=x, y=y)]
    client.close()

    return py.plot(data, filename=name)