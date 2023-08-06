import setuptools

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()


long_description = '''
    window
    imshow          WIP, passing in on image variable name in string type, variable name will be displayed as title. Resizable window as default.
    utility
    converge        use eitehr mean or gaussian kernel to make a high pass filter, low frequency signal will be merged into average color. 
                (https://github.com/JiayouQin/Python-projects/tree/master/17%20Image%20Balancing)
    list_images     return all image files in the directory including sub directories in a list
    imread          identical to openCV imread but supports UTF-8 formatted string path
    imwrite         identical to openCV imwrite but supports UTF-8 formatted string path
    open_morph      perform open operation with given kernel
    open_circle     perform open operation with circular kernel
    open_rect       perform open operation with rectangular kernel
    close_morph     perform close operation with given kernel
    close_circle    perform close operation with circular kernel
    close_rect      perform close operation with rectangular kernel
    bgr_to_hsv      convert a bgr image to hsv image, if parameter 2 is true then returned image will be split into 3 channels
    add_noise       add noise of given type to image (0:gaussian, 1:s&p), accepts both string and integer number

'''

setuptools.setup(
    name="cvsimpleton",
    version="0.0.9",
    author="JiayouQin",
    author_email="JiayouQinCN@gmail.com",
    description="Write less boilerplate code in OpenCV",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JiayouQin/cvSimlepton",
    project_urls={
        "Bug Tracker": "https://github.com/JiayouQin/Python-projects/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "C:\\Users\\11110024\\Anaconda3\\Lib\\site-packages"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)