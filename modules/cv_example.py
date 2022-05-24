crop_img = printscreen_gray[
    pt[1]:pt[1] + 30,
    pt[0] + 5:pt[0] + w]
ocr_text = self.tesseract_img_to_text(crop_img).lower()

if 'trade' in ocr_text.lower():
    print(f'- TRADE INVITE: {ocr_text}')
    obj += ('trade', ocr_text)
elif 'party' in ocr_text.lower():
    print(f'- PARTY INVITE: {ocr_text}')
    obj += ('party', ocr_text)
else:
    print(f'- UNKNOWN INVITE: {ocr_text}')
    obj += ('unknown', ocr_text)


    def screen_record(self):
        last_time = time.time()
        hwnd = win32gui.FindWindow(None, r'%s' % self.app_title)
        win32gui.SetForegroundWindow(hwnd)
        dimensions = win32gui.GetWindowRect(hwnd)

        template = cv2.imread('assets/ui/hpbar2.png', 0)
        w, h = template.shape[::-1]

        while True:
            printscreen = np.array(ImageGrab.grab(dimensions))

            printscreen_gray = cv2.cvtColor(printscreen, cv2.COLOR_BGR2GRAY)
            res = cv2.matchTemplate(printscreen_gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.80
            loc = np.where(res >= threshold)
            detectedObjects = []

            for pt in zip(*loc[::-1]):
                detectedObjects.append(pt)
                cv2.rectangle(printscreen, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
            screen = cv2.resize(printscreen, (960, 540))
            print('loop took {} seconds'.format(time.time() - last_time))
            last_time = time.time()
            cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

    def template_matching(self):
        dimensions = self.get_app_rect()
        template = cv2.imread('assets/ui/trade_invite.png', 0)
        w, h = template.shape[::-1]

        while True:
            detected_objects = set()
            printscreen = np.array(ImageGrab.grab(dimensions))
            printscreen_gray = cv2.cvtColor(printscreen, cv2.COLOR_BGR2GRAY)

            res = cv2.matchTemplate(
                printscreen_gray,
                template,
                cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= 0.66)

            for pt in zip(*loc[::-1]):
                detected_objects.add(pt)
                crop_img = printscreen_gray[pt[1]:pt[1] + 30, pt[0] + 5:pt[0] + w]
                ocr_text = self.tesseract_img_to_text(crop_img)
                # cv2.imshow("cropped", crop_img)
                # cv2.waitKey(0)
                # x_mp = int((pt[0] + pt[0] + w) / 2)  # obj middle point
                # y_mp = int((pt[1] + pt[1] + h) / 2)  # obj middle point
                # x_btn_c = int(((w * 80) / 100) + pt[0])  # x btn % calc
                # y_btn_c = int(((h * 85) / 100) + pt[1])  # y btn % calc

                if 'trade' in ocr_text.lower():
                    print(f'- TRADE INVITE: {ocr_text}')
                    x_btn_a = int(((w * 25) / 100) + pt[0])  # x btn % calc
                    y_btn_a = int(((h * 85) / 100) + pt[1])  # y btn % calc
                    self.mouse_move_click(x_btn_a, y_btn_a)
                    time.sleep(1)
                    break
                elif 'party' in ocr_text.lower():
                    print(f'- PARTY INVITE: {ocr_text}')
                else:
                    print(f'- UNKNOWN INVITE: {ocr_text}')

                # cv2.rectangle(printscreen, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 1)
                # cv2.line(printscreen, (x_mp, y_mp), (x_mp, y_mp), (255, 0, 0), 5)
                # cv2.line(
                #     printscreen,
                #     (x_btn_a, y_btn_a),
                #     (x_btn_a, y_btn_a),
                #     (255, 0, 0), 5)
                # cv2.line(
                #     printscreen,
                #     (x_btn_c, y_btn_c),
                #     (x_btn_c, y_btn_c),
                #     (255, 0, 0), 5)

                # self.mouse_move_click(x_btn_c, y_btn_c)
            # print(detected_objects)

            screen = cv2.resize(printscreen, (960, 540))
            cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
