"""
Author: Marine Remaud
22 of march 2023
Screen the differences between two outputs files
"""

import xarray as xr
import pandas as pd
import numpy as np

begy=1872
pathsim="/home/scratch01/mremaud/IGCM_OUT/OL2/TEST/"
homedir="/home/users/mremaud/PYTHON/ORCHIDEE/DEBUG"
def_file="/home/users/mremaud/ORCHIDEE/modipsl/config/ORCHIDEE_OL/spinup_fm1/PARAM/orchidee_pft.def_39pft.4ac"
namesim1   ="spinup_1ac_do3"
namesim1bis="anspin"
namesim2   ="test_4ac_do3"
namesim2bis="anspin"
listpfts=[2,3,4,5,6,7,8,9]
#--------------------------------------------------------------------------------------------------------

#1 - Read the def files
with open(def_file) as f:
    for line in f:
     if "NAGEC" in line:
      nb_ac=int(line[6:7])
     if "NVMAP" in line:
      n_veget=int(line[6:8])
     if "NVM" in line:
      npft=int(line[6:8])

#Table_PFT= correspondance between metaclass and pft
#Table_AGE= correspondance between metaclass and age
Table_PFT=np.zeros(npft)
Table_AGE=np.zeros(npft)
with open(def_file) as f:
    for line in f:
      if "AGEC_GROUP" in line:
       i_mc=int(line[12:14])
       Table_PFT[i_mc-1]=int(line[15:17])
      if ("PFT_NAME" in line )&("age" in line):
       i_mc=int(line[10:12])
       Table_AGE[i_mc-1]=int(line[-2:])

print("File 2: Number of meta-class",npft)
print("File 2: Number of age class",nb_ac)
print("File 2: Number of PFTs",n_veget)

#2 - Screen the difference
name_restart={"SRF":"sechiba","SBG":"stomate"}
name_veget  ={"SRF":"maxvegetfrac","SBG":"VEGET_MAX"}
dd=0
similar=1
while similar:
 dd+=1 
 for rr in name_restart.keys():
  file_restart1=pathsim+"/"+namesim1+"/"+namesim1bis+"/"+rr+"/Output/YE/"+namesim1bis+"_"+str(begy)+"0101_"+str(begy)+"1231_1Y_"+name_restart[rr]+"_history.nc"
  file_restart2=pathsim+"/"+namesim2+"/"+namesim2bis+"/"+rr+"/Output/YE/"+namesim2bis+"_"+str(begy)+"0101_"+str(begy)+"1231_1Y_"+name_restart[rr]+"_history.nc"
  restart1=xr.open_dataset(file_restart1,decode_times=False,decode_cf=False)
  restart2=xr.open_dataset(file_restart2,decode_times=False,decode_cf=False)
  print("Dimensions of name_restart[rr]:", restart2.dims)
  restart2=restart2.isel(time_counter=(dd-1))
  restart1=restart1.isel(time_counter=(dd-1))
  for ipft in listpfts:
   restart1_pft=restart1.isel(veget=ipft-1).copy(deep=True)
   restart2_pft=restart2.isel(veget=np.where(Table_PFT==ipft)[0]).copy(deep=True)
   if len(restart2_pft[name_veget[rr]].values[restart2_pft[name_veget[rr]].values!=0]!=0):
      iac=np.where(np.squeeze(restart2_pft[name_veget[rr]].values)>0)[0]
      print(restart2_pft.veget.values)
      restart2_pft=restart2_pft.isel(veget=iac)
   else:
      continue
   for var in restart2_pft.keys():
    array1=np.squeeze(restart1_pft[var].values)
    array2=np.squeeze(restart2_pft[var].values)
    #Debug
    try:
      array1 + array2
    except ValueError:
      print("Different dimensions",np.shape(array1),np.shape(array2))
    if not np.array_equal(array1,array2):
     similar=0
     if len(array1.shape)==0:
      line_new='%3s  %-2s  %-15s %4s %-2s %-5s %-7s   %12s %12s' % ("day: ",dd,var,"PFT: ",ipft,"dimension: ","1",array1,array2)
      print(line_new)
     else:
      for  ii in range(len(array1)):
       if not np.array_equal(array1[ii],array2[ii]):
        line_new='%3s  %-2s  %-15s %4s %-2s %-5s %-7s %2s  %18s %18s' % ("day: ",dd,var,"PFT: ",ipft,"dimension: ",np.shape(array2),ii,array1[ii],array2[ii])
        print(line_new)
#        line_new='%3s  %-2s  %-15s %4s %-2s %-5s %-7s %2s  %15s %20s' % ("day: ",dd,var,"PFT: ",ipft,"dimension: ",np.shape(array2),ii,"restart2-restart1",array2[ii]-array1[ii])
#        print(line_new)


