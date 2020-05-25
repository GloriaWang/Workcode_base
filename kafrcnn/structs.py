import os


class ObjectDetection:
    def __init__(self, cls, left, top, right, bottom, score):
        self.cls = cls
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.score = score


class FrameDetections:
    def __init__(self, img_path, dets):
        self.img_path = img_path
        self.img_dir, img_name = os.path.split(img_path)
        self.dets = dets

        # If no extension is given in the file, assume jpg
        fname, fext = os.path.splitext(img_name)
        if fext is '':
            img_name = img_name + '.jpg'

        self.img_name = img_name
