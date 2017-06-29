
import os
import re
import numpy as np
from datetime import datetime as dt


class Dataset:
    
#     poseModeGps = 1
#     poseModeIns = 2
#     poseModeVO  = 3
    
    def __init__ (self, datadir):
        if (not os.path.isdir(datadir)):
            raise IOError 
        self.path = datadir

    def getTimestamp (self, name, raw=False):
        abspath = self.path + '/' + name + '.timestamps'
        fd = open(abspath)
        tslist = []
        for l in fd:
            tokens = l.split()
            if raw==True:
                tslist.append(tokens[0])
            else:
                datetime = dt.utcfromtimestamp(int(tokens[0])/1000000)
                tslist.append(datetime)
        return tslist
    
    # Returns file names
    def getStereo (self):
        timestamps = self.getTimestamp('stereo', raw=True)
        fileList = []
        ctrname = self.path + '/stereo/centre'
        lftname = self.path + '/stereo/left'
        rhtname = self.path + '/stereo/right'
        for ts in timestamps :
            rcatch = {
                    'timestamp' : float(ts) / 1000000.0,    # in seconds
                    'center' : ctrname + '/' + ts + '.png',
                    'left'   : lftname + '/' + ts + '.png',
                    'right'  : rhtname + '/' + ts + '.png'
                }
            fileList.append(rcatch)
        return fileList
    
    def getMainLidar (self):
        timestamps = self.getTimestamp('ldmrs', raw=True)
        filelist = []
        for ts in timestamps:
            filelist.append (self.path + '/ldmrs/' + ts + '.bin')
        return filelist
    
    def getGps (self):
        gpsTbl = np.loadtxt(self.path+'/gps/gps.csv',
            skiprows=1,
            delimiter=',',
            usecols=[0,9,8,4])
        gpsTbl[:,0] /= 1000000.0
        gpsTbl[:,1] -= 620248.53
        gpsTbl[:,2] -= 5734882.47
        return gpsTbl
    
    def getIns (self):
        # Get timestamp, easting, northing, altitude, roll, pitch, yaw
        insTbl = np.loadtxt(self.path+'/gps/ins.csv', 
            skiprows=1, 
            delimiter=',', 
            usecols=[0,6,5,4,12,13,14])
        insTbl[:,0] /= 1000000
        insTbl[:,1] -= 620248.53
        insTbl[:,2] -= 5734882.47
        return insTbl