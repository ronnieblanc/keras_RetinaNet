# keras_RetinaNet

python 01_selectImages.py -d n01440764

python 02_checkAnnotations.py -d 01_selectedImages

python 03_compressImages.py -d 01_selectedImages

python 04_xml2csv.py -d images_416x416

cd keras-retinanet-master  

pip install .

cd ..

retinanet-train --batch-size 4 --epochs 20 --steps 500 --workers=0 csv train.csv class.csv --val-annotation test.csv

retinanet-convert-model snapshots/resnet50_csv_20.h5 retinanet_inference.h5

jupyter notebook
05_retinanetTest.ipynb

