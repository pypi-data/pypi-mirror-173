import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
    
class Methods():

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
    
    def resize(self, img, output_size):
        new_x = output_size[0]
        new_y = output_size[1]
        x = len(img)     
        y = len(img[0])  
        new = [[ img[int(x * r / new_x)][int(y * c / new_y)] for c in range(new_y)] for r in range(new_x)]
        return np.array(new)

    def grayscale(self, img):
        shapes = img.shape[:-1]
        small = self.resize(img, (256, 256))
        gray = np.zeros((len(small), len(small[0])))
        for i in range(len(small)):
            for j in range(len(small[0])):
                gray[i][j] = int(0.21 * small[i][j][0] + 0.72 * small[i][j][1] + 0.007 * small[i][j][2])
        return self.resize(gray, shapes)
    
    def blur(self, img, kernel_size):
        blurred = cv2.blur(img, (kernel_size, kernel_size))
        return blurred
    
    def sharpen(self, img, kernel_size):
        blurred = self.blur(img, kernel_size)
        sharpened = float(1 + 1) * img - float(1) * blurred
        sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
        sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
        sharpened = sharpened.round().astype(np.uint8)
        return sharpened

    def histogram(self, img):
        if img.shape[-1] == 3:
            img = self.grayscale(img)
        else: pass

        x,y = np.histogram(img)
        plt.bar(y[0:-1], x, width=3)
        plt.xticks(y, rotation=45);
        plt.title("Histogram of the grayscale image");
        plt.show();

    def threshold(self, img, hist=False, **kwargs):
        img = self.grayscale(img)

        if len(kwargs["threshold"]) ==  1:
            threshold = kwargs["threshold"]
            img = np.where(img > threshold, 0, img)

        elif len(kwargs["threshold"]) == 2:
            lbound = kwargs["threshold"][0]
            ubound = kwargs["threshold"][1]
            img = np.where(((img < lbound) | (img > ubound)), 0, img)

        if hist==True:
            self.histogram(img)
        return img
    
    def inverse(self, img, gray=False):
        if gray:
            if img.shape[-1] == 3:
                img = self.grayscale(img)
        img = 255 - img
        return img


