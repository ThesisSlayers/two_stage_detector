import tensorflow as tf

def load_image(img_path):
    img = tf.io.read_file(str(img_path))
    img = tf.image.decode_jpeg(img, channels=3)
    return img

def get_bbs(img, model, threshold=0.7):
    out = model(img[None])
    scrs, bbs = out['detection_scores'].numpy(), out['detection_boxes'].numpy()
    return bbs[scrs > threshold]

def get_bb_crop(img, bb):
    height, width, _ = img.shape
    y1, x1, y2, x2 = bb
    return img[int(height*y1):int(height*y2), int(width*x1):int(width*x2)]

def get_bb_crops(img, bbs): 
    return [get_bb_crop(img, bb) for bb in bbs]

def get_foods_and_recipes(img, det1, det2, multi_piatto_dim=700):
    bbs = get_bbs(img, det1)
    foods = get_bb_crops(img, bbs)
    foods_rcps = []
    for food in foods:
        h, w, _ = food.shape
        if h > multi_piatto_dim and w > multi_piatto_dim: 
            rcp_bbs = get_bbs(food, det2)
            rcps = get_bb_crops(food, rcp_bbs)
            foods_rcps.append((food, rcps))
        else:
            foods_rcps.append((food,))           
    return foods_rcps