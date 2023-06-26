date=$(date '+%y.%m.%d')
image_name=cri-o.tpos.dev/tmt-crawlers/$1:$date.$2
echo $image_name
docker build -t $image_name $3
docker push $image_name