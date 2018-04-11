import numpy as np
import cv2
def main():
    conn=cv2.VideoCapture(0)
    conn.set(3,700)
    conn.set(4,500)
    if conn.isOpened():
        ret,fr=conn.read()
    else:
        ret=False
    ret,fr1=conn.read()
    ret,fr2=conn.read()
    if (np.allclose(fr1,fr2)):
        print "clear"

    x=0 
    while ret:
        
        b=cv2.absdiff(fr1,fr2) 
        frcon=cv2.cvtColor(b,cv2.COLOR_BGR2GRAY)
        blur=cv2.GaussianBlur(frcon,(5,5),0)# frame 
        ret,thresold=cv2.threshold(blur,20,255,cv2.THRESH_BINARY)#gaussian threshold
        dil=cv2.dilate(thresold,np.ones((3,3),np.uint8),iterations=2) #accuracy
        er=cv2.erode(dil,np.ones((3,3),np.uint8),iterations=2)
        con,h=cv2.findContours(er,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(fr1,con,-1,(15,150,255),2)# color
        

        if(b==cv2.absdiff(fr1,fr2)).all():
            x=x+1
        if(x%3000==0):  #sample rate for accuracy
            print "movement detected"  
        else:
            x=0
            print "no movement"  
        cv2.imshow("Camera Frame", np.fliplr(fr1))
        if cv2.waitKey(1)==27:
            break
        fr1=fr2
        ret,fr2=conn.read()
    cv2.destroyAllWindows()
    conn.release()

if __name__=="__main__":
    main()
