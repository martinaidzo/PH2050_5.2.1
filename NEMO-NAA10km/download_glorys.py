
import subprocess
import copernicusmarine

monlist_sta=['01','02','03','04','05','06','07','08','09','10','11','12']
monlist_end=['02','03','04','05','06','07','08','09','10','11','12','01']


for ny in range(2004,2025):
    
    for nmon in range(0,12):

        
        year_sta=str(ny)
        year_end=str(ny)

        if nmon == 11:
            year_end=str(ny+1)

        sta_date_k=year_sta+'-'+monlist_sta[nmon]+'-01'
        end_date_k=year_end+'-'+monlist_end[nmon]+'-01'

        sta_date=sta_date_k+'T00:00:00'
        end_date=end_date_k+'T00:00:00'
        copernicusmarine.subset(
         dataset_id="cmems_mod_glo_phy-all_my_0.25deg_P1M-m",
         ##variables=["chl", "phyc"],
         variables=["so_glor","thetao_glor","zos_glor","uo_glor","vo_glor"],
         minimum_longitude=-180,
         maximum_longitude=179.75,
         minimum_latitude=35.,
         maximum_latitude=54.,
         start_datetime=sta_date,
         end_datetime=end_date,
         minimum_depth=0.49402499198913574,
         maximum_depth=5000., 
          )
       

        filename='cmems_mod_glo_phy-all_my_0.25deg_P1M-m_*'+sta_date_k+'-'+end_date_k+'.nc'

        lcom0='ncks --mk_rec_dmn time '+filename+' '+'data_'+sta_date_k+'.nc'
        result = subprocess.run([lcom0], shell=True, capture_output=True, text=True)

        lcom1='ncra data_'+sta_date_k+'.nc dum.nc'
        result = subprocess.run([lcom1], shell=True, capture_output=True, text=True)

        outfilename='data_'+year_sta+'-'+monlist_sta[nmon]+'.nc'

        lcom1b='nccopy -d 3 dum.nc '+outfilename
        result = subprocess.run([lcom1b], shell=True, capture_output=True, text=True)

        lcom2='rm -rf cmems*.nc'+' dum.nc data_'+sta_date_k+'.nc'
        result = subprocess.run([lcom2], shell=True, capture_output=True, text=True)


    lcom3='ncrcat data_*.nc '+'glorys_'+year_sta+'.nc'
    result = subprocess.run([lcom3], shell=True, capture_output=True, text=True)

    lcom4='rm -rf data_*.nc'
    result = subprocess.run([lcom4], shell=True, capture_output=True, text=True)

    lcom5='ncrename -v so_glor,so -v thetao_glor,thetao -v zos_glor,zos -v uo_glor,uo -v vo_glor,vo '+'glorys_'+year_sta+'.nc'
    result = subprocess.run([lcom5], shell=True, capture_output=True, text=True)

    
