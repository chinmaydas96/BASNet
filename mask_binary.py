import numpy as np
from PIL import Image

mask = Image.open('jeffery-erhunse-rvV3wOuxNWs-unsplash (1).png').convert('L')
arr = np.array(mask)
new_arr = (arr > 100).astype(int)
new_mask = Image.fromarray((new_arr * 255).astype(np.uint8))
new_mask.save('mask_3.png')