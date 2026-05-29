import xarray as xr
import subprocess

username = "yourlogin"
password = "passwd"

datnam_in=["dic"   ,"alk" ,"no3","po4","fe" ,"si" ,"o2" ]
datnam_ou=["dissic","talk","no3","po4","fe" ,"si" ,"o2" ]
datfac_ou=[1.e-3   ,1.e-3 ,1.e-3,1.e-3,1.e-3,1.e-3,1.e-3]
ndat=7



ny0=1992
ny1=2019
ny2=2025


for ny in range(ny1,ny2):

    for nd in range(0,ndat):

        varnam=datnam_in[nd]
        
        url = (
            f"https://{username}:{password}"
            "@tds.mercator-ocean.fr/thredds/dodsC/"
            "freebiorys2v4-monthly-"+varnam
        )

# Open dataset
        ds = xr.open_dataset(url, engine="pydap")

   
        nt0=(ny-ny0)*12
        nt1=nt0+12
    
# Select subset
        subset = ds[varnam].isel(
#    time_counter=slice(0,1),
                 time_counter=slice(nt0,nt1),
                 deptht=slice(0, 75),
                 y=slice(640, 790),
                 x=slice(0, 1441)
                                )
        subset = subset * datfac_ou[nd]
# Save locally
        subset.to_netcdf(varnam+"_freebiorys2v4_y"+str(ny)+".nc")

    lcom0='cdo merge '+'*_freebiorys2v4_y'+str(ny)+'.nc bgc_data_y'+str(ny)+'.nc'
    result = subprocess.run([lcom0], shell=True, capture_output=True, text=True)

    lcom1='rm -rf '+'*_freebiorys2v4_y'+str(ny)+'.nc'
    result = subprocess.run([lcom1], shell=True, capture_output=True, text=True)

    lcom2='ncrename -v dic,dissic -v alk,talk bgc_data_y'+str(ny)+'.nc'
    result = subprocess.run([lcom2], shell=True, capture_output=True, text=True)
    
    lcom3='cdo setmisstonn bgc_data_y'+str(ny)+'.nc dum.nc'
    result = subprocess.run([lcom3], shell=True, capture_output=True, text=True)

    lcom4='mv dum.nc GLORYS_BGC_FILES/bgc_data_y'+str(ny)+'.nc'
    result = subprocess.run([lcom4], shell=True, capture_output=True, text=True)
    
    lcom5='rm -rf bgc_data_y'+str(ny)+'.nc'
    result = subprocess.run([lcom5], shell=True, capture_output=True, text=True)
    
## 
