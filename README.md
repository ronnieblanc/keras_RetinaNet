# keras_RetinaNet


python 02_checkAnnotations.py -d 01_selectedImages
python 03_compressImages.py -d 01_selectedImages
python 04_xml2csv.py -d images_416x416
cd ./keras-retinanet-master/  pip install .
retinanet-convert-model snapshots/resnet50_csv_20.h5 retinanet_inference.h5
