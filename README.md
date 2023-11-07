# Documentation for Your Image Processing App

## Introduction
This document provides an overview of your Python image processing application, including its functions and usage. The application is designed to load an image, apply various image processing filters, and display the filtered images.

### Prerequisites
Before using this application, ensure that you have the following prerequisites:
- Python installed on your system.
- Required Python packages installed, including `cv2`, `PIL`, `numpy`, `tkinter`, and `matplotlib`.

## Application Structure

The application consists of the following key components:

1. **User Interface (UI)**: The main application window with a graphical user interface for selecting an image, choosing a filter, and applying it.
2. **Image Filters**: A collection of image processing functions that modify the loaded image according to user selections.
3. **Image Loading and Display**: The application allows users to browse their system for an image, which is then displayed in the UI. After applying a filter, the modified image is shown.

## Functions

### `add_constant(img, constant)`
```python
def add_constant(img, constant):
    """
    This function takes an image (in BGR format) and a constant as parameters. It adds the constant to each pixel in the image and returns the result. Pixel values are clipped to the range [0, 255] to ensure compatibility with 8-bit images.
    """
```

### `multiply_constant(img, constant)`
```python
def multiply_constant(img, constant):
    """
    This function takes an image (in BGR format) and a constant as parameters. It multiplies each pixel in the image by the specified constant and returns the result. Pixel values are clipped to the range [0, 255].
    """
```

### `power_transform(img, power)`
```python
def power_transform(img, power):
    """
    This function takes an image and a power value as parameters. It applies a power transformation to the pixel values by raising each value to the specified power. The result is scaled to the range [0, 255].
    """
```

### `logarithmic_transform(img)`
```python
def logarithmic_transform(img):
    """
    This function performs a logarithmic transformation on the pixel values of the input image. It is typically used to enhance contrast in dark or poorly lit images. The transformed image is scaled to the range [0, 255].
    """
```

### `negative(img)`
```python
def negative(img):
    """
    This function takes an image and generates its negative by subtracting each pixel value from 255. The result is a color-negative image.
    """
```

### `linear_contrast(img)`
```python
def linear_contrast(img):
    """
    This function performs linear contrast stretching on the input image. It scales the pixel values to cover the entire range [0, 255], improving contrast.
    """
```

### `build_hist(img)`
```python
def build_hist(img):
    """
    This function constructs a brightness histogram for the input image. It counts the number of pixels for each brightness intensity and normalizes the distribution based on the total number of pixels.
    """
```

### `equalize(result)`
```python
def equalize(result):
    """
    This function performs histogram equalization for a given image. It redistributes pixel intensities to create a uniform histogram, enhancing image contrast.
    """
```

### `histogram_equalization(img)`
```python
def histogram_equalization(img):
    """
    This function performs histogram equalization for the input image and returns the result.
    """
```

### `histogram_equalization_rgb(img)`
```python
def histogram_equalization_rgb(img):
    """
    This function performs histogram equalization for each channel (R, G, B) of the input image and returns the resulting image in RGB format.
    """
```

### `histogram_equalization_hsv(img)`
```python
def histogram_equalization_hsv(img):
    """
    This function performs histogram equalization for the brightness (V) channel in the HSV color model of the input image and returns the resulting image in RGB format.
    """
```

## User Interface

The user interface of the application consists of the following elements:

- **Browse Button**: Allows users to select an image from their system.
- **File Path Entry**: Displays the selected image file path.
- **Filter Listbox**: Provides a list of available image processing filters.
- **Apply Filter Button**: Applies the selected filter to the loaded image.

## Usage

1. Launch the application by running the Python script.
2. Click the "Browse" button to select an image from your system.
3. The selected image will be displayed in the application.
4. Choose a filter from the "Filter Listbox" to apply it to the image.
5. Depending on the selected filter, you may be prompted to enter additional parameters.
6. Click the "Apply Filter" button to see the filtered image in the application window.

Note that you can choose from a variety of filters, including basic arithmetic operations, power transformations, logarithmic transformations, and histogram equalization.

Enjoy experimenting with different image processing filters to enhance and manipulate your images using this application!
