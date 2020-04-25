from PIL import Image
import numpy as np


org = Image.open('test_images/0003.jpg')                                                                                  
mask = Image.open('test_results/0003.png').convert('L')                                                                     org.putalpha(mask)                                                                                                                 
org_arr = np.array(org)

alpha_mask = org_arr[:,:,3]
print((alpha_mask[alpha_mask == 0].shape[0]) / (alpha_mask.shape[0] * alpha_mask.shape[1]))