"""
Author: Marine Remaud
22 of march 2023
Screen the differences between two restart files
"""

import xarray as xr
import pandas as pd
import numpy as np

begy=1870
endy=1873
pathsim="/home/scratch01/mremaud/IGCM_OUT/OL2/TEST/"
homedir="/home/users/mremaud/PYTHON/ORCHIDEE/DEBUG"
def_file="/home/users/mremaud/ORCHIDEE/modipsl/config/ORCHIDEE_OL/spinup_fm1/PARAM/orchidee_pft.def_39pft.4ac"
namesim1   ="test1d_scand"
namesim1bis="anspin1dscand"
namesim2   ="test4dScand"
namesim2bis="anspin3Dscand"
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
name_restart={"SRF":"sechiba"}
similar=1
yy=begy-1
while similar :
 yy+=1 
 for rr in name_restart.keys():
  file_restart1=pathsim+"/"+namesim1+"/"+namesim1bis+"/"+rr+"/Restart/"+namesim1bis+"_"+str(yy)+"1231_"+name_restart[rr]+"_rest.nc"
  file_restart2=pathsim+"/"+namesim2+"/"+namesim2bis+"/"+rr+"/Restart/"+namesim2bis+"_"+str(yy)+"1231_"+name_restart[rr]+"_rest.nc"
  restart1=xr.open_dataset(file_restart1,decode_times=False,decode_cf=False)
  restart2=xr.open_dataset(file_restart2,decode_times=False,decode_cf=False)
  #print("Dimensions of name_restart[rr]:", restart2.dims)
  for ipft in listpfts:
   restart1_pft=restart1.isel(l_e=ipft-1).isel(z_a=ipft-1)
   restart2_pft=restart2.isel(l_e=np.where(Table_PFT==ipft)[0]).isel(z_a=np.where(Table_PFT==ipft)[0])
   if len(restart2_pft.veget.values[restart2_pft.veget.values!=0]!=0):
      iac=np.where(np.squeeze(restart2_pft.veget.values)>0)[0]
      restart2_pft=restart2_pft.isel(z_a=iac).isel(l_e=iac)
   else:
      continue
   for var in restart2_pft.keys():
    #print(restart2_pft[var].dims,restart2_pft[var].shape)
    #print(restart1_pft[var].dims,restart1_pft[var].shape)
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
      line_new='%3s  %-2s  %-15s %4s %-2s %-5s %-7s   %12s %12s' % ("year: ",yy,var,"PFT: ","dimension: ","1",ipft,array1,array2)
      print(line_new)
     else:
      for  ii in range(len(array1)):
       if not np.array_equal(array1[ii],array2[ii]):
        line_new='%3s  %-2s  %-15s %4s %-2s %-5s %-7s %2s  %18s %18s' % ("year: ",yy,var,"PFT: ",ipft,"dimension: ",np.shape(array2),ii,array1[ii],array2[ii])
        print(line_new)
        line_new='%3s  %-2s  %-15s %4s %-2s %-5s %-7s %2s  %15s %20s' % ("year: ",yy,var,"PFT: ",ipft,"dimension: ",np.shape(array2),ii,"restart2-restart1",array2[ii]-array1[ii])
        print(line_new)

print("SBG: stomate")
name_restart={"SRF":"sechiba","SBG":"stomate"}
similar=1
yy=begy

while similar :
 yy+=1
 for rr in name_restart.keys():

  file_restart1=pathsim+"/"+namesim1+"/"+namesim1bis+"/SBG/Restart/"+namesim1bis+"_"+str(yy)+"1231_"+name_restart["SBG"]+"_rest.nc"
  file_restart2=pathsim+"/"+namesim2+"/"+namesim2bis+"/SBG/Restart/"+namesim2bis+"_"+str(yy)+"1231_"+name_restart["SBG"]+"_rest.nc"
  restart1=xr.open_dataset(file_restart1,decode_times=False,decode_cf=False)
  restart2=xr.open_dataset(file_restart2,decode_times=False,decode_cf=False)
  rr="SRF"
  file_sechiba1=pathsim+"/"+namesim1+"/"+namesim1bis+"/"+rr+"/Restart/"+namesim1bis+"_"+str(yy)+"1231_"+name_restart[rr]+"_rest.nc"
  file_sechiba2=pathsim+"/"+namesim2+"/"+namesim2bis+"/"+rr+"/Restart/"+namesim2bis+"_"+str(yy)+"1231_"+name_restart[rr]+"_rest.nc"
  sechiba1=xr.open_dataset(file_sechiba1,decode_times=False,decode_cf=False)
  sechiba2=xr.open_dataset(file_sechiba2,decode_times=False,decode_cf=False)

  for ipft in listpfts:
   restart1_pft=restart1.isel(l_e=ipft-1).isel(z_a=ipft-1)
   restart2_pft=restart2.isel(l_e=np.where(Table_PFT==ipft)[0]).isel(z_a=np.where(Table_PFT==ipft)[0])

   sechiba1_pft=sechiba1.isel(l_e=ipft-1).isel(z_a=ipft-1)
   sechiba2_pft=sechiba2.isel(l_e=np.where(Table_PFT==ipft)[0]).isel(z_a=np.where(Table_PFT==ipft)[0])  
   if len(sechiba2_pft.veget.values[sechiba2_pft.veget.values!=0]!=0):
      iac=np.where(np.squeeze(sechiba2_pft.veget.values)>0)[0]
      restart2_pft=restart2_pft.isel(z_a=iac).isel(l_e=iac)
   else:
      continue
   for var in restart2_pft.keys():
    array1=np.squeeze(restart1_pft[var].values)
    array2=np.squeeze(restart2_pft[var].values)
    if not np.array_equal(array1,array2):
     similar=0
     if len(array1.shape)==0:
      line_new='%3s  %-2s  %-15s %4s %-2s %-5s %-7s   %12s %12s' % ("year: ",yy,var,"PFT: ","dimension: ","1",ipft,array1,array2)
      print(line_new)
     else:
      for  ii in range(len(array1)):
       if not np.array_equal(array1[ii],array2[ii]):
        line_new='%3s  %-2s  %-15s %4s %-2s %-5s %-7s %2s  %18s %18s' % ("year: ",yy,var,"PFT: ",ipft,"dimension: ",np.shape(array2),ii,array1[ii],array2[ii])
        print(line_new)
        line_new='%3s  %-2s  %-15s %4s %-2s %-5s %-7s %2s  %15s %20s' % ("year: ",yy,var,"PFT: ",ipft,"dimension: ",np.shape(array2),ii,"restart2-restart1",array2[ii]-array1[ii])
        print(line_new)

