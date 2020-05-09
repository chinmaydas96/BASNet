from glob import glob
path = './'
list_im = glob(path + '*.jpg')
list_im

from PIL import Image
rm_img = []

for img in list_im:

    try:
        org = Image.open(img)
    except:
        rm_img.append(img)
        
for i in rm_img:
    try:
        os.remove(i)
    except:
        print(i)
print("File Removed!")     