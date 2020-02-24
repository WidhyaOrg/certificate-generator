from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from flask import send_file
from io import BytesIO

class Certificates():
    def __init__(self, name=None,filename=None, access='general'):
        self.filename = filename
        self.access = access
        self.name = name

    def serve_pil_image(self, pil_img):
        img_io = BytesIO()
        pil_img.save(img_io, 'JPEG', quality=70)
        img_io.seek(0)
        return send_file(img_io, mimetype='image/jpeg')

    def generate(self):
        if(self.access=='general'):
            print(self.filename)
            names = pd.read_excel(self.filename, headers=False, index=False)['Name']
        else:
            names = [self.name]

        for name in names:      #i in range(0,2): #name in names:
            name = name.upper()
            img = Image.open("modules/certificate.png")
            width, height = img.size
            font = ImageFont.truetype('modules/Open_Sans/Open Sans Bold.ttf', 70)
            draw = ImageDraw.Draw(img)
            w, h = draw.textsize(name)
            print(name,width, w, height, h)
            if(w>=30 and w<40):
                draw.text(xy=(900,570), text=name, fill=(225,81,175), font=font)    #fill=(250,209,890)

            elif(w>=40 and w<50):
                draw.text(xy=(860,570), text=name, fill=(225,81,175), font=font)    #fill=(250,209,890)

            elif(w>=50 and w<60):
                draw.text(xy=(820,570), text=name, fill=(225,81,175), font=font)    #fill=(250,209,890)

            elif(w>=60 and w<70):
                draw.text(xy=(780,570), text=name, fill=(225,81,175), font=font)    #fill=(250,209,890)

            elif(w>=70 and w<80):
                draw.text(xy=(740,570), text=name, fill=(225,81,175), font=font)

            elif(w>=80 and w<90):
                draw.text(xy=(700,570), text=name, fill=(225,81,175), font=font)

            elif(w>=90 and w<100):
                draw.text(xy=(660,570), text=name, fill=(225,81,175), font=font)

            elif(w>=100 and w<110):
                draw.text(xy=(620,570), text=name, fill=(225,81,175), font=font)

            elif(w>=110 and w<120):
                draw.text(xy=(580,570), text=name, fill=(225,81,175), font=font)

            elif(w>=120 and w<130):
                draw.text(xy=(540,570), text=name, fill=(225,81,175), font=font)

            elif(w>=130 and w<140):
                draw.text(xy=(500,570), text=name, fill=(225,81,175), font=font)

            elif(w>=140 and w<150):
                draw.text(xy=(460,570), text=name, fill=(225,81,175), font=font)

            elif(w>=150 and w<160):
                draw.text(xy=(420,570), text=name, fill=(225,81,175), font=font)

            else:
                draw.text(xy=(((width-w)/3.3),570), text=name, fill=(225,81,175), font=font)

            if(self.access=='general'):
                #img.show()
                img.save('Certificates/' + name + ' Certificate.png')
            else:
                img.save('modules/certificates/' + name + '.png')
