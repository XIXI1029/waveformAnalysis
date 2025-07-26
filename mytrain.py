from ultralytics import YOLO
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

def main():
    # 加载模型
    model = YOLO('yolov8n.pt')

    # 训练模型
    results = model.train(
        data='datasets/waveform.yaml',
        epochs=75,
        imgsz=640
    )


if __name__ == '__main__':
    main()
