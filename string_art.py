import sys
import numpy as np
from PIL import Image, ImageDraw

def run():
    try:
        filename = sys.argv[1]
        # L is for convert to grayscale
        img_file = Image.open(filename).convert("L")
        img = square_image(np.array(img_file))
        img_input = circular_image(img)
        # For debug purpose
        Image.fromarray(img_input).save('result.png')

    except IOError:
        print('Not an image', file=sys.stderr)
    
    
def circular_image(img: np.ndarray) -> np.ndarray:
    '''
    Crops the image into a RGBA circular image    
    '''

    (width, height) = img.shape

    # Create circle mask to crop 
    alpha = Image.new('L', (height, width), 0)
    draw = ImageDraw.Draw(alpha)
    bounding_box = [(0, 0), (width, width)]
    white = 255
    draw.pieslice(bounding_box, 0, 360, fill = white)
    
    np_alpha = np.array(alpha)
    result = np.dstack((img, np_alpha))
    
    return result 

def square_image(img: np.ndarray) -> np.ndarray:
    '''
    Makes the image into a square, which is centered.
    To perform this action, it takes the min size
    of the image.
    '''

    (width, height) = img.shape  
    min_size = min(height, width)
    max_size = max(height, width)
    
    slice_x = slice(0, min_size)
    slice_y = slice(0, min_size)
    start = (max_size - min_size) // 2    

    if (height < width):
        slice_x = slice(start, min_size + start)
    elif (width < height):
        slice_y = slice(start, min_size + start)
    
    return img[slice_x, slice_y]

if __name__ == '__main__':
    run()
