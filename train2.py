from fastai.vision.all import *
import time
import cv2

from windowcapture import WindowCapture


def label_func(x): return x.parent.name


def main():
    path = Path("I:/ia/")

    fnames = get_image_files(path)
    print(f"Total Images:{len(fnames)}")

    dls = ImageDataLoaders.from_path_func(path, fnames, label_func, bs=40, num_workers=0)

    learn = cnn_learner(dls, resnet18, metrics=error_rate)
    print("Loaded")
    learn.fine_tune(4, base_lr=1.0e-02)



    learn.export()

    # start_time = time.time()
    # test = learn.predict('g1-j5.png')
    # print("--- %s seconds ---" % (time.time() - start_time))
    # print(test)
    start_time = time.time()
    wincap = WindowCapture("ArcheAge")
    image = wincap.getScreenshot(region={
        "x": 278,
        "y": 10,
        "w": 1437,
        "h": 775
    })
    image = cv2.resize(image, (368, 193))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    test = learn.predict(image)
    print("--- %s seconds ---" % (time.time() - start_time))
    print(test)


if __name__ == '__main__':
    main()
