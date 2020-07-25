url = 'https://media.nature.com/w300/magazine-assets/d41586-018-07881-1/d41586-018-07881-1_16369438.jpg'                             
url = 'https://firebasestorage.googleapis.com/v0/b/fitted-image-upload.appspot.com/o/1A945B16-1486-40B8-B171-52274DB15F5E.jpg?alt=media&token=11c7e900-067a-4bab-8556-4d8cf7bb18e1'
url = 'https://firebase.google.com/docs/dynamic-links/images/desktop-to-app.png'
url = 'https://uc7ab4a57690d025b91b88ce7026.previews.dropboxusercontent.com/p/thumb/AA2IXgGY2zbQYErvQnuRcs1ehsh5cKc6NVHuaVua2Cygp9C0HLDqgf7S_zk-c85O4t5ZQmrX8WLqEzoEMnZY3_zrOP1G2obKtusrDnC_kl5u5-mJ_hjHJPuzLOGqs0IebOdJ-IRuWuD6myjADpsAkT-qqIT2JN7p4UPp7DzbxrpMR93Q2dq73MxfY75U8xmq93Z6K13MO_V7eJjnKSgqCKCg8bkjsChhou-AHFUmWaF6bTQ94f0qPIiBu7nfSEkxYv0JUBnNU2eCNVU-T30T_jkNske4A229U-msCQxGuwBLK-SOC1TK1DxCQeoBT-8APvFGN2QvWDtfJgEAtELn2fib4fPWDXwtwRAcSKV3o5PVAp-DOGsoIXFEvjCiynWZWLfX8D-KtTwouY5lhPg-ZTHn/p.png?size=2048x1536&size_mode=3'
url = 'https://www.dropbox.com/s/w3wx3nadtv2any8/Screenshot%202020-07-23%2002.45.24.png?dl=0'
url = 'https://demo-res.cloudinary.com/image/upload/sample.jpg'
url = 'https://res.cloudinary.com/demo/image/instagram_name/angelinajolieofficial.jpg'
url = 'https://upload.wikimedia.org/wikipedia/commons/1/13/Benedict_Cumberbatch_2011.png'
url = 'https://www.dropbox.com/s/w3wx3nadtv2any8/Screenshot%202020-07-23%2002.45.24.png?dl=0'
url = 'https://hello-world23.s3.amazonaws.com/01-04-2019_13-28-33+(1).jpg'
url = 'https://drive.google.com/uc?id=1Mhj841jYyjZXsKv-2CbTRl5fDMH0aEEs'

import requests 
from PIL import Image 
from io import BytesIO         
import os
from urllib.parse import urlparse
import gdown                     
from PIL import Image                                                                              


def download_image(url):
	''' download image file

	Input : url link
	Output : Pillow image object

	'''

	if 'drive.google' in url:
		output = gdown.download(url, quiet=True)
		im = Image.open(output)

		
	else:
		if 'dropbox' in url:
			url = url.replace("dl=0", "dl=1")

		a = urlparse(url)
		img_data = requests.get(url).content                                                                                                 
		im = Image.open(BytesIO(img_data))                                                                                                                                                                                  
		im.save(os.path.basename(a.path))
	

	return im


image_data = download_image(url)