import sys
import copy
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


if __name__ == "__main__":
    meta_path, num_split = sys.argv[1], sys.argv[2]
    
    num_split = int(num_split)
    with open(meta_path, "r") as f:
        metas = json.loads(f.readlines()[0])
        new_metas = copy.deepcopy(metas)
        # images, annotations
        images = metas["images"]
        annotations = metas["annotations"]
    print("Loading meta file done.")
    id2img, id2anno = _convert(images, annotations)
    print("Converting format done.")

    new_images, new_annos = [], []
    img_ids = list(id2img.keys())
    for idx in range(num_split):
        img_id = img_ids[idx]
        print(f"Processing {img_id} done.")
        if img_id not in id2anno:
            continue
        new_images.append(id2img[img_id])
        new_annos.extend(id2anno[img_id])
    new_metas["images"] = new_images
    new_metas["annotations"] = new_annos

    sv_path = meta_path.split(".")[0] + f"_{num_split}s.json"
    with open(sv_path, "w") as f:
        new_metas_json = json.dumps(new_metas)
        f.write(new_metas_json + "\n")
    print(f"Saving {sv_path} done.")
