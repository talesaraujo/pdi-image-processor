import os, sys
import argparse
import cv2 as cv    
import intensity
import output


DEFAULT_IMGPATH = os.path.join(os.getcwd(), "imgs")
print(os.getcwd())
print(DEFAULT_IMGPATH)

def run(folder_path):
    # ufc_img = os.path.join(DEFAULT_IMGPATH, 'ufc.jpg')

    if not os.path.isfile(folder_path):
        raise FileNotFoundError("No such file.")

    img = cv.imread(folder_path, cv.IMREAD_GRAYSCALE)

    img = intensity.normalize(img)

    output.display_image(img, label="UFC Original")
    output.display_image(intensity.negative(img), label="UFC Inverted")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', metavar="", help="The folder directory in which the image is located on")
    args = parser.parse_args()

    # If no argument is provided
    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    if args.input:
        run(args.input)
