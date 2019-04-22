import face_recognition
import os 
import  shutil 
import sys


PHOTOS_PATH = sys.argv[1]+"/"
DESTINATION_PATH = sys.argv[2]+"/"

print(PHOTOS_PATH)
photos = os.listdir(PHOTOS_PATH)
raw_encodes = []


for index, image in enumerate(photos):
    path = PHOTOS_PATH+image

    image_file = face_recognition.load_image_file(path)
    print("Analisando imagem",image," ...")
    try:
        encodings = face_recognition.face_encodings(image_file)

        raw_encodes.append(encodings)
        
    except IndexError:
        print("Foto sem rostos:", image)
        


print("Separando pessoas...")
i = 0
known_people = []
people_final = []
for photo_encodes in raw_encodes:

    for encode in photo_encodes:
        encode_photos = []
        tmp_i = i
        known_people_scan = [False] if len(known_people) == 0 else face_recognition.compare_faces(encode, known_people)

        if(not True in known_people_scan):
            while(tmp_i < len(raw_encodes)):
                results = face_recognition.compare_faces(encode, raw_encodes[tmp_i])

                if(True in results):
                        encode_photos.append(tmp_i)
                tmp_i+= 1
            known_people.append(encode)
            people_final.append(encode_photos)
    i += 1


print("Separando fotos...")

os.mkdir(DESTINATION_PATH)
for i,people in enumerate(people_final):

    for photo_i in people: 
        shutil.copy(PHOTOS_PATH+photos[photo_i], DESTINATION_PATH+str(i))
print("Pronto")
    