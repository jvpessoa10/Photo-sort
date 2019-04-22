import face_recognition
import os 
import  shutil 
from PIL import Image 
import PIL



class PhotoSeparator:
    def __init__(self, pf, dp):
        self.PHOTOS_PATH = pf + '/'
        self.DESTINATION_PATH = dp + '/'
        self.photos = os.listdir(self.PHOTOS_PATH)
        self.raw_encodes = []
        self.known_people = []
        self.people_final = []

    def separateEncodes(self):
        for index, image in enumerate(self.photos):
            
                image_not_pass = False
                while True:
                    
                    path = self.PHOTOS_PATH+image


                    if(image_not_pass):
                        im = Image.open(path) 
                        wpercent = (300 / float(im.size[0]))
                        hsize = int((float(im.size[1]) * float(wpercent)))
                        im = im.resize((300, hsize), PIL.Image.ANTIALIAS)
                        im.save(path, quality = 10)

                    
                    

                    image_file = face_recognition.load_image_file(path)
                    print("Analisando imagem",image," ...")
                    try:
                        encodings = face_recognition.face_encodings(image_file)

                        self.raw_encodes.append(encodings)
                        
                    except IndexError:
                        print("Foto sem rostos:", image)
                    except MemoryError:
                        print("Foto muito pesada, reduzindo...")
                        image_not_pass = True
                    else:
                        print("Pronto")
                        break
                    
                
    
    def analyseEncodes(self):
        i = 0
        for photo_encodes in self.raw_encodes:

            for encode in photo_encodes:
                encode_photos = []
                tmp_i = i
                known_people_scan = [False] if len(self.known_people) == 0 else face_recognition.compare_faces(encode, self.known_people)

                if(not True in known_people_scan):
                    while(tmp_i < len(self.raw_encodes)):
                        try:
                            results = face_recognition.compare_faces(encode, self.raw_encodes[tmp_i])

                            if(True in results):
                                    encode_photos.append(tmp_i)
                            
                        except:
                            tmp_i+= 1
                            continue
                        else:
                            tmp_i +=1

                    self.known_people.append(encode)
                    self.people_final.append(encode_photos)
            i += 1
    def separatePhotos(self):
        os.mkdir(self.DESTINATION_PATH)
        for i,people in enumerate(self.people_final):
            
            os.mkdir(self.DESTINATION_PATH+str(i))
            for photo_i in people: 
                shutil.copy(self.PHOTOS_PATH+self.photos[photo_i], self.DESTINATION_PATH+str(i)+'/')
        print("Pronto")

    def clear(self):
        self.raw_encodes = []
        self.known_people = []
        self.people_final = []
    
    def start(self):
        self.separateEncodes()
        self.analyseEncodes()
        self.separatePhotos()
        self.clear()
                
    
    

















    