import face_recognition
import os 
import  shutil 
from PIL import Image 
import PIL



class PhotoSeparator:
    def __init__(self, pf, dp):
        self.PHOTOS_PATH = pf + '/'
        self.DESTINATION_PATH = dp + '/'
        self.REDUCED_PATH = self.DESTINATION_PATH+'reduced/'

        self.LOW_PATH = self.DESTINATION_PATH+'low/'        
        self.NOMAL_PATH = self.DESTINATION_PATH+'normal/'
        self.photos = os.listdir(self.PHOTOS_PATH)
        self.raw_encodes = []
        self.known_people = []
        self.people_final = []


    def reduceQuality(self):
        os.mkdir(self.DESTINATION_PATH)
        os.mkdir(self.REDUCED_PATH)

        for index,image in enumerate(self.photos):
            path = self.PHOTOS_PATH+image
            im = Image.open(path) 
            wpercent = (600 / float(im.size[0]))
            hsize = int((float(im.size[1]) * float(wpercent)))

            im = im.resize((600, hsize), PIL.Image.ANTIALIAS)
            im.save(self.REDUCED_PATH +image, quality = 70)

         


    def separateEncodes(self):
        
        for index, image in enumerate(self.photos):
                print(index+1," de ",len(self.photos)," fotos")
            
                path =  self.REDUCED_PATH+ image
                image_file = face_recognition.load_image_file(path)
            
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
                    
                    
                
    
    def analyseEncodes(self):
        print("Comparando rostos...")
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
        
        os.mkdir(self.NOMAL_PATH)
        os.mkdir(self.LOW_PATH)
        for i,people in enumerate(self.people_final):
            
            os.mkdir(self.NOMAL_PATH+str(i))
            os.mkdir(self.LOW_PATH+str(i))

            for photo_i in people: 
                shutil.copy(self.PHOTOS_PATH+self.photos[photo_i], self.NOMAL_PATH+str(i)+'/')
                shutil.copy(self.REDUCED_PATH+self.photos[photo_i], self.LOW_PATH+str(i)+'/')
        

    def clear(self):
        self.raw_encodes = []
        self.known_people = []
        self.people_final = []
    
    def start(self):
        self.reduceQuality()
        self.separateEncodes()
        self.analyseEncodes()
        self.separatePhotos()
        self.clear() 
                
    
    




















    