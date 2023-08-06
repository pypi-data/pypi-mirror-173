# pyimage

The **pyimage** package is a Python library that provides simple and expressive manual image processing techniques. It aims to provide an easy toolkit for begginer users in order to develop their image treatment projects. It is already well on its way towards this goal.


## Main Features

Here are some of the implemented features: 

- Easy way to read, write and display images
- Image resizing to any dimension
- RGB to grayscale conversion
- Image blurring and sharpening methods
- Image filtering by thresholding
- Visualization of the histogram of the image
- Inverse image obtention

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pyimage.

```bash
pip install pyimage
```

## Usage

```python
import pyimage

# loads 'image' from 'path'
img = pyimage.Methods.read_image('path','image')

# converts img to grayscale
gray = pyimage.Methods.grayscale(img)

# sharpen img with a 100x100 kernel
sharp = pyimage.Methods.sharpen(img, 100)

# displays both images
pyimage.Methods.show_image(img)
pyimage.Methods.show_image(gray)
pyimage.Methods.show_image(sharp)
```
![Original image](/examples/cat_resized.png "Original image")
![Image on grayscale](/examples/cat_grayscale.png "Image on grayscale")
![Image sharpened](/examples/cat_sharpened.png "Image sharpened")

## Dependencies
- [NumPy](https://numpy.org/) - Adds support for large, multi-dimensional arrays, matrices and high-level mathematical functions to operate on these arrays
- [Matplotlib](https://matplotlib.org) - Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python. Matplotlib makes easy things easy and hard things possible.
- [OpenCV](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html) - OpenCV provides a real-time optimized Computer Vision library, tools, and hardware.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
