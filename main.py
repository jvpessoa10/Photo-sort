import PhotoSeparator
import sys

def main():
    pf = sys.argv[1]
    des = sys.argv[2]
    p1 = PhotoSeparator.PhotoSeparator(pf,des)
    
    p1.start()
    
    


if __name__ == "__main__":
    main()