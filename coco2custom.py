import os
import sys
import json


def _convert(images, annotations):
    id2img, id2anno = {}, {}
    for image in images:
        if image["id"] not in id2img:
            id2img[image["id"]] = image
    for annotation in annotations:
        if annotation["image_id"] not in id2anno:
            id2anno[annotation["image_id"]] = []
        id2anno[annotation["image_id"]].append(annotation)
    return id2img, id2anno


def _coco2custom(id2img, id2anno):
    custom_meta = []
    for img_id in id2img:
        tmp, instances = {}, []
        file_name = os.path.basename(id2img[img_id]["file_name"])
        image_height = id2img[img_id]["height"]
        image_width = id2img[img_id]["width"]
        annos = id2anno[img_id]
        tmp["filename"] = file_name
        tmp["image_height"] = image_height
        tmp["image_width"] = image_width
        for anno in annos:
            bbox, cat_id = anno["bbox"], anno["category_id"]
            x1, y1, w, h = bbox
            x2, y2 = x1 + w, y1 + h
            instances.append({
                "is_ignored": False,
                "bbox": [x1, y1, x2, y2],
                "label": cat_id
            })
        tmp["instances"] = instances
        custom_meta.append(tmp)
    return custom_meta


if __name__ == "__main__":
    coco_meta = sys.argv[1]

    with open(coco_meta, "r") as f:
        coco_metas = json.loads(f.readlines()[0])
        # image: file_name, height, width
        # annotation: bbox, category_id
        images, annotations = coco_metas["images"], coco_metas["annotations"]
    print("Loading coco meta done.")
    id2img, id2anno = _convert(images, annotations)
    custom_meta = _coco2custom(id2img, id2anno)
    print("Converting format done.")

    sv_path = coco_meta.split(".")[0] + "_custom.json"
    with open(sv_path, "w") as f:
        for cus_meta in custom_meta:
            print(f"Saving {cus_meta['filename']} done.")
            f.write(json.dumps(cus_meta) + "\n")
