# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 10:03:19 2020

@author: yux
"""
from astropy.io import fits
import numpy as np

pathic="//icnas2.cc.ic.ac.uk/ip1016/Desktop/LAB/A1/trimmed6.fits"
paththinkpad="C:/Users/User/Desktop/LAB A1/trimmed2.fits"
pathmac="//Users/apple/Desktop/trimmed10mean.fits"
hdu_list=fits.open(paththinkpad)
data=hdu_list[0].data
hdu_list.close()

slice=data[4345:4518,8:381]

#creating a mask full of 0
mask=np.ndarray(shape=(slice.shape[0],slice.shape[1]))
for i in range(slice.shape[1]):
    for j in range(slice.shape[0]):
        mask[j,i]=0


mean=3418.52
sigma=12.17
max=10000
r=6
r_back=3
R=r_back+r
galaxies=[]
while max>mean+4*sigma:
    
    #identifying the first max
    max=slice.max()
    max_arg=np.argmax(slice)+1
    max_row_y=max_arg//(slice.shape[1])+1-1
    max_col_x=max_arg%(slice.shape[1])-1
     
    #count the brightness in a aperture of 6 pixels

    brightness=0
    counter=0
    for x in range(max_col_x-r,max_col_x+r):
        for y in range(int(-np.sqrt(r**2-(x-max_col_x)**2)+max_row_y)-1,int(np.sqrt(r**2-(x-max_col_x)**2)+max_row_y)+1):
            brightness=brightness+slice[y,x]
            counter=counter+1
                
    print(brightness)

    #identify local background
    counter_R=0
    brightness_R=0
    for x in range(max_col_x-R,max_col_x+R):
        for y in range(int(-np.sqrt(R**2-(x-max_col_x)**2)+max_row_y)-1,int(np.sqrt(R**2-(x-max_col_x)**2)+max_row_y)+1):
            brightness_R=brightness_R+slice[y,x]
            counter_R=counter_R+1
            slice[y,x]=mean
    brightness_back=brightness_R-brightness
    counter_back=counter_R-counter
    brightness_back_average=brightness_back/counter_back
    brightness_final=brightness-brightness_back_average*counter
    list=[max_row_y+4346,max_col_x+9,max,brightness,brightness_back_average,brightness_final]
    galaxies.append(list)

print(galaxies)

import xlsxwriter

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('galaxies_slice.xlsx')
worksheet = workbook.add_worksheet()


# Start from the first cell. Rows and columns are zero indexed.
row = 0
col = 0

for i in ['y center','x center','value center','initial count','background count average','final count']:
    worksheet.write(row, col,i)
    col=col+1
    
row=1
col=0
# Iterate over the data and write it out row by row.
for i,j,k,l,m,n in galaxies:
    worksheet.write(row, col,i)
    worksheet.write(row, col+1,j)
    worksheet.write(row, col+2,k)
    worksheet.write(row, col+3,l)
    worksheet.write(row, col+4,m)
    worksheet.write(row, col+5,n)
    row += 1
    
workbook.close()