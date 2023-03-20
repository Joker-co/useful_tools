import os
import sys
import json

if __name__ == "__main__":
    img_dir, meta_file = sys.argv[1], sys.argv[2]

    # input.txt
    input_txt, img_names = "input.txt", None
    with open(input_txt, "w") as f:
        for root, dirs, files in os.walk(img_dir, topdown=False):
            img_names = files
            for name in files:
                img_item = {
                    "image": {
                        "image_path": "images/{}".format(name),
                        "#keson_code": "FRM"
                    }
                }
                f.write(json.dumps(img_item) + "\n")

    # ground_truth.txt
    name2id, id2img, id2annos = {}, {}, {}
    with open(meta_file, "r") as f:
        metas = f.readlines()[0]
        # 'info', 'licenses', 'images', 'annotations', 'categories'
        # category start from 1
        metas = json.loads(metas)
        images, annotations, categories = metas["images"], metas["annotations"], metas["categories"]
    for image in images:
        image_id, file_name = image["id"], image["file_name"]
        if file_name not in name2id:
            name2id[file_name] = image_id
        if image_id not in id2img:
            id2img[image_id] = image
    for annotation in annotations:
        image_id = annotation["image_id"]
        if image_id not in id2annos:
            id2annos[image_id] = []
        id2annos[image_id].append(annotation)
    # generate ground_truth.txt
    with open("ground_truth.txt", "w") as f:
        for img_name in img_names:
            image_id = name2id[img_name]
            image_path = "images/{}".format(img_name)
            img_annos = id2annos[image_id]
            for img_anno in img_annos:
                x1, y1, w, h = img_anno["bbox"]
                x1, y1, x2, y2 = int(x1), int(y1), int(x1 + w), int(y1 + h)
                label = img_anno["category_id"] - 1
                gt_item = {
                    "image_path": image_path,
                    "roi": {
                        "left": x1,
                        "top": y1,
                        "width": w,
                        "height": h,
                        "#keson_code": "RCT"
                    },
                    "is_ignored": False,
                    "label": label
                }
                f.write(json.dumps(gt_item) + "\n")
    import pdb;pdb.set_trace()
