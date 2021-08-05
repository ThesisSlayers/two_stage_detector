import xml.etree.ElementTree as ET
import cv2

def read_xml_content(xml_file: str):                                                                                                                                                                                                                                      
    tree = ET.parse(xml_file)                                                                                                                                                                                                                                                   
    root = tree.getroot()                                                                                                                                                                                                                                                       
    list_with_all_boxes = []                                                                                                                                                                                                                                                    
    for boxes in root.iter('object'):

        class_name = boxes.find("name").text                                                                                                                                                                                                                                         

        ymin, xmin, ymax, xmax = None, None, None, None                                                                                                                                                                                                                         
        ymin = int(float(boxes.find("bndbox/ymin").text))                                                                                                                                                                                                                       
        xmin = int(float(boxes.find("bndbox/xmin").text))                                                                                                                                                                                                                       
        ymax = int(float(boxes.find("bndbox/ymax").text))                                                                                                                                                                                                                       
        xmax = int(float(boxes.find("bndbox/xmax").text))        
        list_with_all_boxes.append([class_name, xmin, ymin, xmax, ymax])
        
    return list_with_all_boxes

def bb_in_realtive_coords(bb): 
    y1, x1, y2, x2 = bb
    return 0 <= x1 <= 1 and 0 <= y1 <= 1 and 0 <= x2 <= 1 and 0 <= y2 <= 1

def draw_bbs(img, bbs, color=[0,0,255], bb_format='array_coords'):
##### DA FARE FORSE
#     for bb in bbs:
#         if    bb_format=='array_coords': bb = bb
#         elif: bb_format=='coco':
#             x, y, w, h = bb
#             bb = [y, x, w, h]
#####
    h, w, _ = img.shape
    for bb in bbs:
        y1, x1, y2, x2 = bb
        y1, x1, y2, x2 = (int(h*y1), int(w*x1), int(h*y2), int(w*x2)) if bb_in_realtive_coords(bb) else (int(y1), int(x1), int(y2), int(x2))
        cv2.rectangle( img, (x1, y1), (x2, y2), color, 10)

        def area(b): return b[2]*b[3]
