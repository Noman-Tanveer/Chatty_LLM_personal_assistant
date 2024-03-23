
import os
import json
import glob

json_dir = "../datasets/jsons"
output_dir = "../datasets/txt"
jss = glob.glob(os.path.join(json_dir, "*.json"))
print(len(jss))

def post_process(text):
    text = text.replace("9", "I")
    return text

for js in jss:
    with open(js) as f:
        dat = json.load(f)
    out_txt = ""
    blocks = dat["Blocks"]
    for blk in blocks:
        if blk["BlockType"]=="LINE":
            out_txt += " " + blk["Text"]
    
    with open(os.path.join(output_dir, os.path.basename(js).replace(".json", ".txt")), "w") as f:
        f.write(post_process(out_txt))
