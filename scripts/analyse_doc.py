#Detects text in a document stored in an S3 bucket. Display polygon box around text and angled text 
import os
import boto3
import io
import glob
from PIL import Image, ImageDraw
import json

def process_text_detection(client, image_path):
    with open(image_path, 'rb') as img_file:
        ### To display image using PIL ###
       image = Image.open(image_path)
        ## Read bytes ###
       img_bytes = img_file.read()
       response = client.detect_document_text(Document={'Bytes': img_bytes})
    print ('Detected Document Text')
    # Create image showing bounding box/polygon the detected lines/text
    with open(os.path.join("Chatty_llm_personal_assistant/datasets/txt", os.path.basename(image_path).replace(".jpg", ".json")), "w") as f:
        json.dump(response, f)
    blocks=response['Blocks']
    width, height =image.size    
    print ('Detected Document Text')

    # Create image showing bounding box/polygon the detected lines/text
    for block in blocks:
        # Display information about a block returned by text detection
        print('Type: ' + block['BlockType'])
        if block['BlockType'] != 'PAGE':
            print('Detected: ' + block['Text'])
            print('Confidence: ' + "{:.2f}".format(block['Confidence']) + "%")

        print('Id: {}'.format(block['Id']))
        if 'Relationships' in block:
            print('Relationships: {}'.format(block['Relationships']))
        print('Bounding Box: {}'.format(block['Geometry']['BoundingBox']))
        print('Polygon: {}'.format(block['Geometry']['Polygon']))
        print()
        draw=ImageDraw.Draw(image)
        # Draw WORD - Green -  start of word, red - end of word
        if block['BlockType'] == "WORD":
            draw.line([(width * block['Geometry']['Polygon'][0]['X'],
            height * block['Geometry']['Polygon'][0]['Y']),
            (width * block['Geometry']['Polygon'][3]['X'],
            height * block['Geometry']['Polygon'][3]['Y'])],fill='green',
            width=2)
        
            draw.line([(width * block['Geometry']['Polygon'][1]['X'],
            height * block['Geometry']['Polygon'][1]['Y']),
            (width * block['Geometry']['Polygon'][2]['X'],
            height * block['Geometry']['Polygon'][2]['Y'])],
            fill='red',
            width=2)    
                
        # Draw box around entire LINE  
        if block['BlockType'] == "LINE":
            points=[]
            for polygon in block['Geometry']['Polygon']:
                points.append((width * polygon['X'], height * polygon['Y']))
            draw.polygon((points), outline='black')    
    # Display the image
    image.show()

    return len(blocks)

def main():
    session = boto3.Session(profile_name='default')
    client = session.client('textract')
    images = glob.glob("../datasets/images/*.jpg")
    for image_path in images:
        block_count=process_text_detection(client, image_path)
        # print("Blocks detected: " + str(block_count))
    
if __name__ == "__main__":
    main()
