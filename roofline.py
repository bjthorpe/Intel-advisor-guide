'''
Python script to read in data from Intel advisor and plot a roofline diagram. Usage: roofline.py --survey path/to/survey.csv --roofs path/to/roofs.csv.
'''
from argparse import ArgumentParser, FileType
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
###############################################################
#Parse argumants to get paths for survey data and compute/memory roofs
###############################################################
parser = ArgumentParser()
parser.add_argument('--survey', type=str, required=True)
parser.add_argument('--roofs', type=str, required=True)
args = parser.parse_args()
survey=args.survey
###############################################################
#read in in survey data
##############################################################
df = pd.read_csv(survey,usecols=[2,7,8,11,48,50,53,55],header=0,skiprows=5)
#rename first column
df.columns.values[0]='Line'
#remove junk from first column so it only contains line numbers
df['Line']=df['Line'].str.replace('^.+?in','')
df['Line']=df['Line'].str.replace('at DLMUSN.f90','')
df['Line']=df['Line'].str.replace(']','')
# Remove trailing s and less than/greater than signs from second column and convert to floating point
df['Self Time']=df['Self Time'].str.replace('[s<>]','')
df['Self Time']=pd.to_numeric(df['Self Time'])
# Fill NANs with zeros
df=df.fillna(0)
# Sort results by self time
df.sort_values(by=['Self Time'], inplace=True,ascending=False)
# Seperate out into vectories and scalar loops
Vectorized=df[df['Type'].str.contains("Vectorized")]
Scalar=df[~df['Type'].str.contains("Vectorized")]
#############################################################
# Seperate roof data into single and multi-treaded roofs, then futher seperate # single thread roofs into vector and scalar.
#############################################################################
full_roofs = pd.read_csv(args.roofs,header=0,skiprows=1)
mt_roofs=full_roofs[~full_roofs['Name'].str.contains("single-threaded")]
st_roofs=full_roofs[full_roofs['Name'].str.contains("single-threaded")]
#############################################################
# Extract  Vectorized roofline data
#############################################################
vec_roofs=st_roofs[~st_roofs['Name'].str.contains("Scalar")]
vec_roofs['Bandwidth']=vec_roofs['Bandwidth']/1E9
vec_memory=vec_roofs.loc[vec_roofs['Type'] == "memory"]
vec_compute=vec_roofs.loc[vec_roofs['Type'] == "compute"]
stop=vec_compute['Bandwidth'].max()/vec_memory['Bandwidth']
vec_x_mem=np.linspace(0,stop)
vec_x_compute=np.linspace(0,100)
#convert pdatframes to np arrays
vec_mem_gradient=vec_memory['Bandwidth'].to_numpy()
vec_com_gradient=vec_compute['Bandwidth'].to_numpy()
vec_mem_roofs=np.zeros(vec_x_mem.shape)
vec_y_compute=np.ones((vec_x_compute.shape[0],vec_com_gradient.shape[0]))
#calculate memory roofs
for A in range(0,vec_x_mem.shape[0]):
    vec_mem_roofs[A,:]=vec_x_mem[A,:]*vec_mem_gradient
#calculate compute roofs
for B in range(0,vec_y_compute.shape[0]):
    vec_y_compute[B,:]=vec_y_compute[B,:]*vec_com_gradient
############################################################
# Extract Scalar roofline data
############################################################
roofs=st_roofs[st_roofs['Name'].str.contains("Scalar")]
roofs['Bandwidth']=roofs['Bandwidth']/1E9
# Add back in the DRAM line since it is the same for both vector and scalar
roofs = roofs.append(vec_roofs.loc[vec_roofs['Name'] == "DRAM Bandwidth (single-threaded)"], ignore_index=True)
memory=roofs.loc[roofs['Type'] == "memory"]
compute=roofs.loc[roofs['Type'] == "compute"]
stop=compute['Bandwidth'].max()/memory['Bandwidth']
x_mem=np.linspace(0,stop)
x_compute=np.linspace(0,100)
#convert dataframes to np arrays
mem_gradient=memory['Bandwidth'].to_numpy()
com_gradient=compute['Bandwidth'].to_numpy()
mem_roofs=np.zeros(x_mem.shape)
y_compute=np.ones((x_compute.shape[0],com_gradient.shape[0]))
#calculate memory roofs
for A in range(0,x_mem.shape[0]):
    mem_roofs[A,:]=x_mem[A,:]*mem_gradient
#calculate compute roofs
for B in range(0,y_compute.shape[0]):
    y_compute[B,:]=y_compute[B,:]*com_gradient
##########################################################    
#colourmap for scatter plots
##########################################################
colourmap_vec = Vectorized['Self Time']
colourmap_scalar = Scalar['Self Time']
##########################################################
# Vectroized roofline plot
##########################################################
plt.figure()
plt.scatter(Vectorized['Self AI'],Vectorized['Self GFLOPS'],c=colourmap_vec,cmap='rainbow')
cbar = plt.colorbar()
cbar.set_label('Self Time')
plt.loglog(vec_x_mem,vec_mem_roofs,ls='-',color='black')
plt.loglog(vec_x_compute,vec_y_compute[:,:],ls='--',color='black',lw=0.6)
axes = plt.gca()
axes.annotate('DRAM', xy=(0.004, 0.03),  xycoords='data')
axes.annotate('L1', xy=(0.004, 0.08),  xycoords='data')
axes.annotate('L2', xy=(0.004, 0.6),  xycoords='data')
axes.annotate('L3', xy=(0.004, 1.4),  xycoords='data')
axes.annotate('DP Vector Add', xy=(0.004, 60.0),  xycoords='data')
axes.annotate('DP Vector FMA', xy=(0.004, 110.0),  xycoords='data')
axes.annotate('SP Vector FMA', xy=(0.004, 210.0),  xycoords='data')
axes.set_xlim([1E-3,50])
axes.set_ylim([0.015,300])    
plt.xlabel('Arithmetic Intensity (FLOPS/Byte)')
plt.ylabel('Performance (GFLOPS)')
plt.title('Roofline for Vectorized loops')
###########################################################
# Scalar roofline plot
##########################################################
plt.figure()
plt.scatter(Scalar['Self AI'],Scalar['Self GFLOPS'],c=colourmap_scalar,cmap='rainbow')
cbar = plt.colorbar()
cbar.set_label('Self Time')
plt.loglog(x_mem,mem_roofs,ls='-',color='black')
plt.loglog(x_compute,y_compute[:,:],ls='--',color='black',lw=0.6)
axes = plt.gca()
axes.annotate('DRAM', xy=(0.009, 0.1),  xycoords='data')
axes.annotate('L1', xy=(0.010, 0.2),  xycoords='data')
axes.annotate('L2', xy=(0.008, 0.3),  xycoords='data')
axes.annotate('L3', xy=(0.009, 1.0),  xycoords='data')
axes.annotate('Integer Scalar Add Peak', xy=(0.004, 8.9),  xycoords='data')
axes.annotate('Scalar Add Peak', xy=(0.004, 7.3),  xycoords='data')
axes.set_xlim([1E-3,1])
axes.set_ylim([0.07,10])
plt.xlabel('Arithmetic Intensity (FLOPS/Byte)')
plt.ylabel('Performance (GFLOPS)')
plt.title('Roofline for Scalar loops')
###########################################################
plt.show()
