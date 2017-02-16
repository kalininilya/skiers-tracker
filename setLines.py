import cv2

def run(im, multi = False):
    im_disp = im.copy()
    im_draw = im.copy()
    window = "Select start and finish lines."
    cv2.namedWindow(window, cv2.WINDOW_NORMAL)
    cv2.imshow(window, im_draw)

    pts_1 = []
    pts_2 = []

    rects = []
    run.mouse_down = False

    def on_mouse(event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
    	    if multi == False and len(pts_2) == 1:
		print "WARN: Cannot select another object in SINGLE OBJECT TRACKING MODE."
		print "Press d to delete"
		return
            run.mouse_down = True
            pts_1.append((x, y))
        elif event == cv2.EVENT_LBUTTONUP and run.mouse_down == True:
            run.mouse_down = False
            pts_2.append((x, y))
            print "Object selected at [{}, {}]".format(pts_1[-1], pts_2[-1])
        elif event == cv2.EVENT_MOUSEMOVE and run.mouse_down == True:
            im_draw = im.copy()
            cv2.rectangle(im_draw, pts_1[-1], (x, y), (255,255,255), 1)
            cv2.imshow(window, im_draw)
    
    cv2.setMouseCallback(window, on_mouse)
    
    while True:
        # Draw the rectangular boxes on the image
        window_2 = "Objects to be tracked."
        for pt1, pt2 in zip(pts_1, pts_2):
            rects.append([pt1[0],pt2[0], pt1[1], pt2[1]])
            cv2.rectangle(im_disp, pt1, pt2, (255, 255, 255), 1)
        # Display the cropped images
        
        key = cv2.waitKey(30)
        if key == ord('s'):
            # Press key `s` to return the selected pnts
            cv2.destroyAllWindows()
            pnt= [(tl + br) for tl, br in zip(pts_1, pts_2)]
            new_pnt=pnt
            return new_pnt
        elif key == ord('d'):
            # Press ket `d` to delete the last rectangular region
            if run.mouse_down == False and pts_1:
                print "Object deleted at  [{}, {}]".format(pts_1[-1], pts_2[-1])
                pts_1.pop()
                pts_2.pop()
                im_disp = im.copy()
            else:
                print "No object to delete."
    cv2.destroyAllWindows()
    pnt= [(tl + br) for tl, br in zip(pts_1, pts_2)]
    new_pnt=pnt
    return new_pnt