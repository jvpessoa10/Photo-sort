import face_recognition
import os 
import  shutil 
from PIL import Image 
import PIL






class PhotoSeparator:
    def __init__(self, pf, dp):
        self.PHOTOS_PATH = pf + '/'
        self.DESTINATION_PATH = dp + '/'
       
  
        self.NOMAL_PATH = self.DESTINATION_PATH+'normal/'
        self.photos = os.listdir(self.PHOTOS_PATH)
        self.raw_encodes = []
        self.known_people = []
        self.people_final = []


    def separateEncodes(self):
        
        for index, image in enumerate(self.photos):
                print(index+1," de ",len(self.photos)," fotos")
            
                path =  self.PHOTOS_PATH+ image 
                image_file = face_recognition.load_image_file(path)
                encodings = face_recognition.face_encodings(image_file)

                
                self.raw_encodes.append(encodings)
                    
                
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
       
        for i,people in enumerate(self.people_final):
            
            os.mkdir(self.NOMAL_PATH+str(i))
           

            for photo_i in people: 
                shutil.copy(self.PHOTOS_PATH+self.photos[photo_i], self.NOMAL_PATH+str(i)+'/')
               
        

    def clear(self):
        self.raw_encodes = []
        self.known_people = []
        self.people_final = []
    
    def start(self):
        
        os.mkdir(self.DESTINATION_PATH)
        self.separateEncodes()
        self.analyseEncodes()
        self.separatePhotos()
        self.clear() 
                
    
    




















    