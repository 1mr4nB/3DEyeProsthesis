import cv2 as cv
import numpy as np
import math
"""
Dit bestand bevat alle nodige code voor de kleurherkenning/-detectie om de output van de oogfoto te bekomen.

Eerst vindt er een pupildetectie plaats, waarbij de pupil wordt ingekleurd. In de functie HoughCircles in pupildetection
mag met de parameters minDist, minRaduis en maxRadius gespeeld worden, naargelang de grootte van de cirkel die gezocht
wordt. 

Hierna volgt de iris (+sclera) extrapolatie. Hiervoor kunnen twee methodes uitgekozen worden:
• De cropimage en maskiris functie, vragen enkel de buitenrand van de iris aan te duiden.
• De cropimagepoly en maskirispoly functie, vragen meerdere punten rondom de iris, waarmee men ook een groot stuk van 
de sclera kan aanduiden voor in de finale afbeelding.

Een switch case met gebruikersinput voor een verkozen methode kan hier nog geïmplementeerd worden.
Voor nu moet men de onnodige functies in commentaar zetten, om tot het gewenste resultaat te komen.
"""
irisstraal = 0
pointlist = []


def pupildetection(img, dim):    # Pupildetection functie
    output = img.copy()
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = cv.medianBlur(gray, 3)

    # Zoek cirkels obv HoughCircles
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, dp=2, minDist=170, param1=199, param2=30, minRadius=30, maxRadius=50)
    # Als circles niet leeg: cirkels gevonden
    if circles is not None:
        # Zet (x,y)-coördinaten + straal om in gehele getallen
        #print(circles)  # [[[365. 255. 46.]]]
        circles = np.round(circles[0, :]).astype("int")
        print("[GEVONDEN CIRKELS]")
        print(circles)  # [[365 255 46]]
        print("---------------------------")
        # Loop over de (x,y)-coord en stralen van de cirkels
        for (x, y, r) in circles:
            # Teken de cirkel in de output image
            cv.circle(output, (x, y), r, (0, 255, 0), 1)
        #    cv.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        # Toon de output afbeelding
        cv.imshow("output", np.hstack([img, output]))
        # cv.imshow("Output", output)
        cv.waitKey(0)

    if len(circles) > 1:  # Meer dan 1 cirkel gevonden -- Behoud de meest centrale cirkel
        result = []
        for (x, y, r) in circles:   # Splits de afbeelding in 10 stukken, check of het in de middelste 4 stukken zit
            if x in range(int(dim[1]/10*3), int(dim[1]/10*7)):
                if y in range(int(dim[0]/10*3), int(dim[0]/10*7)):
                    result = [x, y, r]
        return result  # Geeft (x, y, r) terug

    if len(circles) == 1:
        return circles[0]
    else:
        return 0, 0, 0


def colorpupil(img, x, y, r):
    cv.circle(img, (x, y), r+3, (43, 42, 43), -1)
    return img


def cropimage(event, coordx, coordy, flags, params):
    global x1, y1, x2, y2
    # Gebruikersinput (linker)muisklik coördinaat op buitenrand iris
    if event == cv.EVENT_LBUTTONDOWN:
        print("Cirkelcentrum coördinaten: ", x, ' ', y)
        print("Klikcoördinaten: ", coordx, ' ', coordy)
        print("---------------------------")
        x1 = x
        y1 = y
        x2 = coordx
        y2 = coordy
        cv.waitKey(0)

        # Bereken afstand tot pupilcentrum
        print("Verschil volgens x: ", x2 - x1)
        print("Verschil volgens y: ", y2 - y1)

        afstand = math.dist([x1, y1], [x2, y2])
        print("Straal iris: ", afstand)

        # Teken cirkel met deze afstand als straal
        cv.circle(output, (x, y), int(afstand), (43, 42, 43), 2)
        cv.imshow("Iris Boundary", output)
        cv.waitKey(0)
        cv.destroyAllWindows()
        global irisstraal
        irisstraal = afstand
        print(f"Irisstraal: {irisstraal}")
        return irisstraal


def cropimagepoly(event, coordx, coordy, flags, params):
    # Gebruikersinput (linker)muisklik coördinaat op buitenrand iris
    global pointlist
    if event == cv.EVENT_LBUTTONDOWN:
        print("Cirkelcentrum coördinaten: ", x, ' ', y)
        print("Klikcoördinaten: ", coordx, ' ', coordy)
        print("---------------------------")
        x2 = coordx
        y2 = coordy
        cv.waitKey(0)

        # font = cv.FONT_HERSHEY_SIMPLEX
        # cv.putText(output, '.', (x2, y2), font,
        #             1, (255, 0, 0), 2)
        # cv.imshow("Coord", output)
        #cv.waitKey(0)

        pointlist.append((x2,y2))
        # print(pointlist)
        # Teken polygon met deze afstand als straal

        return pointlist


def maskiris(img, x, y, r):
    mask = np.zeros(img.shape[:2], dtype = "uint8")
    cv.circle(mask, (x, y), int(r), 255, -1)
    masked = cv.bitwise_and(img, img, mask = mask)
    return masked


def maskirispoly(img, pointlist):
    polypoints = []
    for coord in pointlist:
        polypoints.append([coord[0], coord[1]])
    polypoints = np.array(polypoints, np.int32)
    mask = np.zeros(img.shape[:2], dtype = "uint8")
    # cv.polylines(mask, [polypoints], isClosed=True, color=(255, 255, 255), thickness=1)
    cv.fillPoly(mask, [polypoints], 255)
    masked = cv.bitwise_and(img, img, mask = mask)
    return masked


if __name__ == "__main__":

    # Absoluut pad naar afbeelding
    path = r'D:\Skorro\P&O Biomed\Oogfotos\Yannick Resize 25%.JPG'
    #path = r'D:\Skorro\P&O Biomed\Oogfotos\IMG_022721.JPG'      # Testfoto
    path = r'D:\Skorro\P&O Biomed\Oogfotos\Job 2.JPG'


    image = cv.imread(path)  # Lees image

    # Resize image voor output
    image = cv.resize(image, (750, 500), interpolation=cv.INTER_CUBIC)  # Herschaal naar 750x500 pixels
    dimensions = image.shape        # (height, width, n. channels)

    (x, y, r) = pupildetection(image, dimensions)
    print("[PUPILDETECTIE OUTPUT]")
    print(f"Coördinaten cirkelcentrum: {x, y}, straal: {r}")
    print("-------------------------------------------")

    # Originele image nog intact
    output = colorpupil(image, x, y, r)
    cv.imshow("Colored pupil", output)
    cv.waitKey(0)

    # # Coordinaten voor crop circle
    # cv.imshow("Cropping: Duid een punt aan", output)
    # cv.setMouseCallback("Cropping: Duid een punt aan", cropimage)
    # cv.waitKey(0)

    # Coordinaten voor crop polygon
    cv.imshow("Cropping (polygon): Duid een aantal punten aan", output)
    cv.setMouseCallback("Cropping (polygon): Duid een aantal punten aan", cropimagepoly)
    cv.waitKey(0)

    print("Input irisstraal voor mask: ", irisstraal)
    print("Lijst van punten: ", pointlist)

    # masked = maskiris(output, x, y, irisstraal)
    # cv.imshow("Finaal", masked)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    masked = maskirispoly(output, pointlist)
    cv.imshow("Finaal", masked)
    cv.waitKey(0)
    cv.destroyAllWindows()

    # Afbeelding opslaan
    split = path.split("\\")
    path = "\\".join(split[0:-1])
    print(path)
    filenaam = split[-1]
    cv.imwrite(f"{path}\{filenaam[0:-4]}Crop.JPG", masked)
    print(f"Afbeelding opgeslagen in {path} onder {filenaam}!")
