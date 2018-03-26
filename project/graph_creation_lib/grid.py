import os, sys
#import ogr
import math
from math import ceil
import matplotlib.pyplot as plt


def remove_short_trajectories(data, thres=50):
        for key, value in data.items()[:]:
            #print '\n short_trajectories key', key
            value = [f for f in value if len(f)>thres]
        return data

def check_range_latlon(data, minlat=-90, maxlat=90, minlon=-180, maxlon=180):
        for key, value in data.iteritems():
            #print key  
            #print (value['lat']>minlat) & (value['lat']<maxlat) & (value['lon']>minlon) & (value['lon']<maxlon)
            if not  value.shape==value[(value['lat']>minlat) & (value['lat']<maxlat) & (value['lon']>minlon) & (value['lon']<maxlon)].shape:
                print('invalid latlon :', key)
            data[key]=value[(value['lat']>minlat) & (value['lat']<maxlat) & (value['lon']>minlon) & (value['lon']<maxlon)]
        return data 


def square_grids(data,R=6.371*10**6, gridWidth=500, gridHeight=500):
    for key, value in data.items()[:]:
        #print '\n\n key : ', key

        #######################################################################
        # lat lon to xy

        th0=min(value['lat'])
        th1=max(value['lat'])
        ph0=min(value['lon'])
        ph1=max(value['lon'])
        d1 = 2*math.pi*R*((ph1-ph0)*2*math.pi/360)/(2*math.pi)
        d2 = 2*math.pi*(R*math.sin(math.pi/2-ph1*2*math.pi/360))*((th1-th0)*2*math.pi/360)/(2*math.pi)
        d3 = 2*math.pi*(R*math.sin(math.pi/2-ph0*2*math.pi/360))*((th1-th0)*2*math.pi/360)/(2*math.pi)
        x_v = [0]*len(value['lat'])
        y_v = [0]*len(value['lon'])
        w1=(value['lat']-ph0)/(ph1-ph0)
        w2=(value['lon']-th0)/(th1-th0)
        y_v=w1*math.fabs(d3-d2)/2+w2*(d3*(1-w1)+d2*w1)
        #print math.fabs((d3-d2)/(2*d1)), th0, th1, ph0, ph1 

        x_v=w1*d1*math.sin(math.acos(math.fabs((d3-d2)/(2*d1))))
        value['y_v']=w1*math.fabs(d3-d2)/2+w2*(d3*(1-w1)+d2*w1)
        value['x_v']=w1*d1*math.sin(math.acos(math.fabs((d3-d2)/(2*d1))))

        '''
        plt.scatter(value['lat'], value['lon'])
        plt.show() 
        plt.scatter(x_v, y_v)
        plt.show()
        '''
        #########################################################################

        xmin=min(x_v)
        xmax=max(x_v)
        ymin=min(y_v)
        ymax=max(y_v)

        gridWidth = float(gridWidth)
        gridHeight = float(gridHeight)

        #print 'before printing rows'
        #print ymax, ymin, xmax, xmin

        # get rows
        rows = ceil((ymax-ymin)/gridHeight)
        # get columns
        cols = ceil((xmax-xmin)/gridWidth)

        value['x_id']=(value['x_v']-xmin)//gridWidth
        value['y_id']=(value['y_v']-ymin)//gridWidth
        value['labels']= list(zip(value.x_id, value.y_id))

        #print value.head(n=100), len(set(value['x_id'])), len(set(value['y_id'])), #
    return data


