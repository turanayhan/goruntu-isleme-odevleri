import cv2
import numpy as np
import json
import os


def nothing(x):
    pass


def main():

    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)


    cap = cv2.VideoCapture(0)
    with open(path + '\\settings' + '\\' + 'ayar2.json', ) as f:
        lower_colors_sett = json.load(f)
    with open(path + '\\settings' + '\\' + 'up_ayar.json') as f:
        upper_colors_sett = json.load(f)



    window_name = 'Renk Parametreleri Ayarlama'
    cv2.namedWindow(window_name)

    cv2.createTrackbar('a1', window_name, lower_colors_sett['a1'], 255, nothing)
    cv2.createTrackbar('a2', window_name, lower_colors_sett['a2'], 255, nothing)
    cv2.createTrackbar('a3', window_name, lower_colors_sett['a3'], 255, nothing)

    cv2.createTrackbar('b1', window_name, upper_colors_sett['b1'], 255, nothing)
    cv2.createTrackbar('b2', window_name, upper_colors_sett['b2'], 255, nothing)
    cv2.createTrackbar('b3', window_name, upper_colors_sett['b3'], 255, nothing)

    while True:

        ret, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_colors_sett['a1'] = cv2.getTrackbarPos('a1', window_name)
        lower_colors_sett['a2'] = cv2.getTrackbarPos('a2', window_name)
        lower_colors_sett['a3'] = cv2.getTrackbarPos('a3', window_name)

        upper_colors_sett['b1'] = cv2.getTrackbarPos('b1', window_name)
        upper_colors_sett['b2'] = cv2.getTrackbarPos('b2', window_name)
        upper_colors_sett['b3'] = cv2.getTrackbarPos('b3', window_name)


        lower_color = np.array([lower_colors_sett['a1'], lower_colors_sett['a2'], lower_colors_sett['a3']])
        upper_color = np.array([upper_colors_sett['b1'], upper_colors_sett['b2'], upper_colors_sett['b3']])
        mask = cv2.inRange(hsv, lower_color, upper_color)
        res = cv2.bitwise_and(frame, frame, mask=mask)


        cv2.imshow('mask', mask)
        cv2.imshow('res', res)

        cv2.putText(frame, 'Cikmak icin "ESC", Ayarlari ve ekran goruntusunu kaydedip cikmak icin "S" tusuna basin.',
                    (0, 20), 3, 0.4, (255, 255, 255))
        cv2.imshow(window_name, frame)


        k = cv2.waitKey(1) & 0xFF
        if k == 27:  # Çıkış için 'ESC' girişi beklemesi
            break
        elif k == ord('s'):

            cv2.imwrite(path + '\\screen_shots' + '\\' + 'Img_screen_mask.jpg', mask)
            cv2.imwrite(path + '\\screen_shots' + '\\' + 'Img_screen_res.jpg', res)

            # JSON'a ayrı ayrı kaydetme

            with open(path + '\\settings' + '\\' + 'ayar1.json', 'w') as json_dosya:
                json.dump(lower_colors_sett, json_dosya)
            with open(path + '\\settings' + '\\' + 'ayar2', 'w') as json_dosya:
                json.dump(upper_colors_sett, json_dosya)
            break


    cap.release()

    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()
