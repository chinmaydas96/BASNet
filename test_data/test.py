from PIL import Image
import numpy as np
org  = Image.open('junk_images/J-1560.jpg')
mask = Image.open('junk_mask/J-1560.png').convert('L')
org.putalpha(mask)
org_arr = np.array(org)
alpha_mask = org_arr[:,:,3]
print((alpha_mask[alpha_mask == 0].shape[0]) / (alpha_mask.shape[0] * alpha_mask.shape[1]))
print(np.amax(alpha_mask))
org.save('out.png')