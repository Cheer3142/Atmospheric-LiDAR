import matplotlib.pyplot as plt
import numpy as np
from os.path import isfile, join
from os import listdir
import netCDF4
from datetime import datetime, timedelta
import json

# Cheer's add-on
from readtrc import Trc
import NCLoadMPL
import ALiNupdateSQL
import MongoInsert

'''
v = s/t 
s = vt/2 (ไป-กลับ)
'''

class ALiNPro():
    def __init__(self, timenow, timethai, MPL_path):
        self.trc = Trc()
        self.light_speed = 3e8
        
        # Next clound Load MPL
        com_path            = NCLoadMPL.get(path = MPL_path,
                                            dateandtime = timenow) # dateandtime = "202404031340"
        self.MPL_fulldata   = netCDF4.Dataset(com_path, 'r')

        self.SQLDateTime    = datetime.strptime(timethai, "%Y%m%d%H%M").strftime("%Y-%m-%d %H:%M:%S")
        self.SQLTime        = datetime.strptime(timethai, "%Y%m%d%H%M").strftime("%H:%M:%S")
        
    def OCread(self, path):
        ### Data from Oscilloscope
        C1_lst  = [self.trc.open(join(path, f))[1] for f in listdir(path) if isfile(join(path, f)) and 'C1' == f[:2]]
        C1      = np.mean(C1_lst, axis=0)
        self.C1      = (C1 * -1)

        ### Trig Data
        C2_file = [join(path, f)  for f in listdir(path) if isfile(join(path, f)) and 'C2' == f[:2]]
        C2_lst  = [self.trc.open(f)[1] for f in C2_file]

        # self.Trig    = np.mean(C2_lst, axis=0)
        fName   = C2_file[0]
        time    = self.trc.open(fName)[0]
        self.time    = time-10e-6

    def to32floatlst(self, arr):
        return np.array(arr, dtype=np.float32).tolist()
    
    def calpack(self):
        ### ALiN Data
        idx         = self.time > 0
        distance    = self.time * self.light_speed/2
        rs_C1       = self.C1 * distance * distance

        distance    = distance[idx]
        rs_C1       = rs_C1[idx]
        result_ALiN = [(float(x), float(y), self.SQLDateTime, self.SQLTime) for x, y in zip(distance, rs_C1)]

        ### MPL Data
        MPL_distance    = np.array(self.MPL_fulldata.variables["range_raw"])*1000
        MPL_signal      = self.MPL_fulldata.variables['copol_raw'][0] + \
                          self.MPL_fulldata.variables['crosspol_raw'][0]
        rsMPL_signal    = MPL_signal * MPL_distance * MPL_distance
        

        OC_json = {"dis"        : self.to32floatlst(distance),
                   "OC_cal"     : self.to32floatlst(rs_C1),
                   "MPL_dis"    : self.to32floatlst(MPL_distance),
                   "MPL_cal"    : self.to32floatlst(rsMPL_signal),}

        
        result_MPL = [(float(x), float(y), self.SQLDateTime, self.SQLTime) for x, y in zip(MPL_distance, rsMPL_signal)]
        
        return OC_json, result_ALiN, result_MPL

def delay10min(t):
    t       = t.replace(minute = t.minute//5*5) - timedelta(minutes=10)
    return t.strftime("%Y%m%d%H%M")

'''
    ALiN Function
'''
#-------------------------------------------------------------------------------
nowtime         = "202405141930" # delay10min(datetime.now())
utctime         = "202405101230" # delay10min(datetime.utcnow())

with open("pathcfg.json", "r") as openfile:
    path_json = json.load(openfile)
    
MPL_path    = path_json['MPL']
OC_path     = join(path_json['OSC'], "OSC_{}".format(nowtime))
# print(OC_path, '\nALiN_{}'.format(nowtime))   # OSC_202404161335
path        = path_json['OSC']                  # Kill this Line
OC_path     = path                              # Kill this Line
#-------------------------------------------------------------------------------

'''
    ALiN Function
'''
#-------------------------------------------------------------------------------
alin                                = ALiNPro(MPL_path = MPL_path,
                                      timenow = utctime,
                                      timethai = nowtime)      
alin.OCread(OC_path)                # path
MongoJson, ALiN_SQL, MPL_SQL        = alin.calpack()

'''
    SQL Insert
'''
#-------------------------------------------------------------------------------
'''
con, cur = ALiNupdateSQL.Connect()
ALiNupdateSQL.InsertMany('ALiN', ALiN_SQL, cur)
ALiNupdateSQL.InsertMany('MPL', MPL_SQL, cur)
ALiNupdateSQL.Commit(con, cur)
'''

'''
    Mongo Insert
'''
#-------------------------------------------------------------------------------
MongoInsert.insert_file(
    db_name     = 'ALiN',
    col_name    = 'ALiN_{}'.format(nowtime),
    json_file   = MongoJson)
#-------------------------------------------------------------------------------



















'''
with open("pathcfg.json", "w") as outfile:
    outfile.write(json_object)

#plot_name      = "1st On Sky Oscilloscope Captured Data"
#plot_name = "PMT in the front of the Laser"
#plot_name      = "31 Mar 2024 Oscilloscope 200 Stacks Data Beam Expander (21:10-21:12)"
'''

