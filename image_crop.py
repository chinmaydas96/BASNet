from PIL import Image

def trim(im, crop = True, border = 0 , border_type = 'single'):
	'''
	parameters : im - Pillow image file
				 crop = [True, False]
	             border - border value (default : 0)
	             border_type - ['single', 'lurl', 'percentage']


	'''
	
	width,height = im.size
	bbox = im.getbbox()



	# Code for single value border line
	if border_type == 'single':
		if bbox:
			left, upper, right, lower = bbox

			if crop == True:	
				bbox = (max((left - border),0), max((upper - border),0), min((right + border),width), min((lower + border),height))
			
			return im.crop(bbox)

		else:
		 	# found no content
			raise ValueError("cannot trim; image was empty")

	# Code for left, upper, right, lower value border

	if border_type == 'lurl':
		if bbox:
			left, upper, right, lower = bbox
			if crop == True : 
				bbox = (max((left - border[0]),0), max((upper - border[1]),0), min((right + border[2]),width), min((lower + border[3]),height))
			
			return im.crop(bbox)
		else:
		 	# found no content
			raise ValueError("cannot trim; image was empty")

	if border_type == 'percentage':

		border = round(width * border / 100)

		if bbox:
			left, upper, right, lower = bbox
			if crop == True : 
				bbox = (max((left - border),0), max((upper - border),0), min((right + border),width), min((lower + border),height))
			
			return im.crop(bbox)
		else:
		 	# found no content
			raise ValueError("cannot trim; image was empty")



def main():
	image=Image.open('img1.png')
	new_img = trim(image, crop = True, border = 0, border_type = 'single')
	print(new_img.size)
	new_img.save('output.png')



if __name__ == "__main__":
    main()

