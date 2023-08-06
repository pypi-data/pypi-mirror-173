import cv2
import matplotlib.pyplot as plt
import os

class Read():
    def __init__(self) -> None:
        pass

    def read_image(self, path, filename):
        self.filename = filename
        self.path = path
        file_path = os.path.join(path, filename)
        self.img = cv2.imread(file_path)

        if self.img is None:
            raise Exception("Sorry, image not found")

        else:
            return self.img

    def write_image(self, filename, img, same_path=True, **kwargs):
        if same_path:
            file_path = os.path.join(self.path, filename)
        else:
            file_path = os.path.join(kwargs["path"], filename)

        cv2.imwrite(file_path, img)
        print(f"Image written in {file_path}")

    def show_image(self, img):
        plt.figure()
        if img.shape[-1] == 3:
            plt.imshow(img[:,:,::-1])
        else:
            plt.imshow(img, cmap="gray")
        plt.show()


    
