from ultralytics import YOLO
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
# Load a model

model = YOLO("runs/detect/train45/weights/best.pt")
# Train the model
train_results = model.train(
    data="datasets/mydata.yaml",  # path to dataset YAML
    epochs=55,  # number of training epochs
    imgsz=640,  # training image size
    device= '0' ,  # device to run on, i.e. device=0 or device=0,1,2,3 or device=cpu
)

