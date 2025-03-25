from ultralytics import YOLO

def get_model(mode=""):
    # pass mode="-seg" if using Segment model
    # pass mode="-pose" if using Pose model
    model = YOLO(f'yolo11n{mode}.pt')
    return model
