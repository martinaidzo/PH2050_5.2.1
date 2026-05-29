#!/bin/bash

# Script to download and process ERA5 data as input for NEMO
# This script calls aa_downloadERA5_Tqpuv.py and ab_downloadERA5_radprecip.py
# You need cdsapi installed and a key in your .cdsapi file

# Select year(s) and month(s) in the for-loops

# Andrea Gierisch, 2020

cd DATA

# Activate conda environment that has cdsapi installed (via pip).
###########################################################
# The first line is necessary (on my laptop) to make the "conda activate" work.
#source /home/a21468/anaconda3/lib/python3.11/site-packages/conda/shell/etc/profile.d/conda.sh
#source /home/ang/bin/miniconda/bin/etc/profile.d/conda.sh
#conda init
##conda activate cdsapi

# Loop through years and months

for year in {1940..1978}
do
		echo Starting to process year $year
		date
		for month in {01..12}
		##for month in {09..09}
		do
				# Download grib files
				######################
				echo Starting to process year $year, month $month
				# Download Tqpuv_y????_m??.grb
				python3 ../aa_downloadERA5_Tqpuv.py $year $month
				# Download RadPrecip_y????_m??.grb
				python3 ../ab_downloadERA5_radprecip.py $year $month

				## Separate dew point and MSL
				# Note: Do not convert sea level pressure from Pa to hPa. NEMO needs Pa even though the documentation says hPa.
				# Save as netcdf 4
				######################
				cdo -f nc4 chname,10u,u10,10v,v10,2t,t2 -selname,10u,10v,2t,msl Tqpuv_y${year}_m${month}.grb     Tpuv_y${year}_m${month}.nc
				cdo -f nc4 chname,2d,d2m -selname,2d,msl     Tqpuv_y${year}_m${month}.grb     dew-slp_y${year}_m${month}.nc
				
				# Convert hourly-accumulated values to 3-hourly mean (adding 3 time steps and dividing by 3*3600)
				# Multiply precipitation/snow by 1000 to convert from m/s to mm/s (=kg/m^2/s )
				# Output as netcdf4
				############################
				cdo -f nc4 divc,10800 -timselsum,3    RadPrecip_y${year}_m${month}.grb RadPrecipRate_y${year}_m${month}.nc
				cdo mulc,1000 -selname,tp,sf      RadPrecipRate_y${year}_m${month}.nc Precip_y${year}_m${month}.nc
				cdo selname,ssrd,strd  RadPrecipRate_y${year}_m${month}.nc Rad_y${year}_m${month}.nc

				# Calculate specific humidity from dew point (use Tetens equation)
				#############################################
				cdo expr,'_epswarm=610.78*exp(17.27*(d2m-273.16)/(d2m-35.85)) ; _epscold=610.78*exp(21.875*(d2m-273.16)/(d2m-7.65)) ; _eps= ((d2m>273.15)) ? _epswarm : _epscold ; q2=((287./461.)*_eps)/(msl-(1-(287./461.))*_eps) ' dew-slp_y${year}_m${month}.nc q_y${year}_m${month}.nc

				# Combine variables
				####################
				cdo merge q_y${year}_m${month}.nc Tpuv_y${year}_m${month}.nc Rad_y${year}_m${month}.nc Precip_y${year}_m${month}.nc ERA5forcing_y${year}_m${month}.nc

			       
				# Clean up
				############
				rm *_y${year}_m${month}.grb
				rm dew-slp_y${year}_m${month}.nc
				rm RadPrecipRate_y${year}_m${month}.nc 
				rm q_y${year}_m${month}.nc Tpuv_y${year}_m${month}.nc Rad_y${year}_m${month}.nc Precip_y${year}_m${month}.nc 

		done
done

# ToDo:
# change units in output files: 
# - msl: hPa (not Pa)
# - rad: W/m**2
# - precip: mm/s

