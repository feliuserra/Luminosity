cd data/downloads/Version_4_DMSP-OLS_Nighttime_Lights_Time_Series
  # F101992\
  # F101993\
  # F101994\
  # F121994\
  # F121995\
  # F121996\
  # F121997\
  # F121998\
  # F121999\
  # F141997\
  # F141998\
  # F141999\
  # F142000\
  # F142001\
  # F142002\
  # F142003\
  # F152000\
  # F152001\
  # F152002\
  # F152003\
  # F152004\
  # F152005\
  # F152006\
  # F152007\
  # F162004\
  # F162005\
  # F162006\
  # F162007\
  # F162008\
  # F162009\
  # F182010\
  # F182011\
  # F182012\
for IMAGE in \
  F101993\
  F182013
do
  echo "Getting image $IMAGE"
  if [ ! -f $IMAGE.v4b_web.stable_lights.avg_vis.tif ] && [ ! -f $IMAGE.v4c_web.stable_lights.avg_vis.tif ]; then
    wget https://www.ngdc.noaa.gov/eog/data/web_data/v4composites/$IMAGE.v4.tar
    mkdir $IMAGE && tar -xvf $IMAGE.v4.tar -C $IMAGE
    cd $IMAGE
    if [ -f $IMAGE.v4b_web.stable_lights.avg_vis.tif.gz ]; then
      IMAGE_FNAME=$IMAGE.v4b_web.stable_lights.avg_vis.tif
      mv $IMAGE_FNAME.gz ../
    else
      IMAGE_FNAME=$IMAGE.v4c_web.stable_lights.avg_vis.tif
      mv $IMAGE_FNAME.gz ../
    fi
    cd ..
    gunzip $IMAGE_FNAME
    rm -r $IMAGE
    rm $IMAGE.v4.tar
  else
    echo "Image $IMAGE was already created"
  fi
done
