"""Fine-tune YOLOv8n on the bundled COCO128 set. Outputs go to runs/detect/train."""
from pathlib import Path

import yaml
from ultralytics import YOLO
from ultralytics.utils import ROOT

HERE = Path(__file__).resolve().parent
DATA_YAML = HERE / "datasets" / "coco128.yaml"


def write_data_yaml():
	# Reuse Ultralytics' class names but point at the local copy of the dataset
	data = yaml.safe_load((ROOT / "cfg/datasets/coco128.yaml").read_text(encoding="utf-8"))
	data.pop("download", None)
	data["path"] = str(HERE / "datasets" / "coco128")
	DATA_YAML.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


if __name__ == "__main__":
	write_data_yaml()
	YOLO("yolov8n.pt").train(
		data=str(DATA_YAML),
		epochs=100,
		imgsz=640,
		batch=16,
		device=0,
		workers=2,  # each Windows worker loads the CUDA DLLs; the default 8 exhausts the paging file
		project=str(HERE / "runs" / "detect"),
		name="train",
		exist_ok=True,
		seed=0,
	)
