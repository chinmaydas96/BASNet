import torch
import torchvision
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F

from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
import torch.optim as optim

import torchvision.transforms as standard_transforms

import numpy as np
import glob

from data_loader import Rescale
from data_loader import RescaleT
from data_loader import RandomCrop
from data_loader import CenterCrop
from data_loader import ToTensor
from data_loader import ToTensorLab
from data_loader import SalObjDataset

from model import BASNet

import pytorch_ssim
import pytorch_iou


# ------- 1. define loss function --------

bce_loss = nn.BCELoss(size_average=True)
ssim_loss = pytorch_ssim.SSIM(window_size=11,size_average=True)
iou_loss = pytorch_iou.IOU(size_average=True)


reduction='mean'

def bce_ssim_loss(pred,target):

	bce_out = bce_loss(pred,target)
	ssim_out = 1 - ssim_loss(pred,target)
	iou_out = iou_loss(pred,target)

	loss = bce_out + ssim_out + iou_out

	return loss

def muti_bce_loss_fusion(d0, d1, d2, d3, d4, d5, d6, d7, labels_v):

	loss0 = bce_ssim_loss(d0,labels_v)
	loss1 = bce_ssim_loss(d1,labels_v)
	loss2 = bce_ssim_loss(d2,labels_v)
	loss3 = bce_ssim_loss(d3,labels_v)
	loss4 = bce_ssim_loss(d4,labels_v)
	loss5 = bce_ssim_loss(d5,labels_v)
	loss6 = bce_ssim_loss(d6,labels_v)
	loss7 = bce_ssim_loss(d7,labels_v)
	#ssim0 = 1 - ssim_loss(d0,labels_v)

	# iou0 = iou_loss(d0,labels_v)
	#loss = torch.pow(torch.mean(torch.abs(labels_v-d0)),2)*(5.0*loss0 + loss1 + loss2 + loss3 + loss4 + loss5) #+ 5.0*lossa
	loss = loss0 + loss1 + loss2 + loss3 + loss4 + loss5 + loss6 + loss7#+ 5.0*lossa
	#print("l0: %3f, l1: %3f, l2: %3f, l3: %3f, l4: %3f, l5: %3f, l6: %3f\n"%(loss0.item(),loss1.item(),loss2.item(),loss3.item(),loss4.item(),loss5.item(),loss6.item()))	# print("BCE: l1:%3f, l2:%3f, l3:%3f, l4:%3f, l5:%3f, la:%3f, all:%3f\n"%(loss1.data[0],loss2.data[0],loss3.data[0],loss4.data[0],loss5.data[0],lossa.data[0],loss.data[0]))

	return loss0, loss
    
# ------- 2. set the directory of training dataset --------

data_dir = './train_data/'
#tra_image_dir = 'DUTS/DUTS-TR/DUTS-TR/im_aug/'
#tra_image_dir = 'DUTS/image/'
tra_image_dir = 'Archive/train/image/'
valid_image_dir = 'Archive/validation/image/'

#tra_label_dir = 'DUTS/DUTS-TR/DUTS-TR/gt_aug/'
#tra_label_dir = 'DUTS/mask/'
tra_label_dir = 'Archive/train/mask/'
valid_label_dir = 'Archive/validation/mask/'

image_ext = '.jpg'
label_ext = '.png'

model_dir = "./saved_models/"

#PATH = "./saved_models/basnet.pth"
PATH = "./saved_models/optimized_model_0.346057.pth"
#PATH = "./saved_models/optimized_model_0.334364.pth"

epoch_num = 200
batch_size_train = 32 
batch_size_val = 1
train_num = 0
val_num = 0



tra_img_name_list = glob.glob(data_dir + tra_image_dir + '*' + image_ext)

tra_lbl_name_list = []
for img_path in tra_img_name_list:
	img_name = img_path.split("/")[-1]

	aaa = img_name.split(".")
	bbb = aaa[0:-1]
	imidx = bbb[0]
	for i in range(1,len(bbb)):
		imidx = imidx + "." + bbb[i]

	tra_lbl_name_list.append(data_dir + tra_label_dir + imidx + label_ext)


valid_img_name_list = glob.glob(data_dir + valid_image_dir + '*' + image_ext)

valid_lbl_name_list = []
for img_path in valid_img_name_list:
	img_name = img_path.split("/")[-1]

	aaa = img_name.split(".")
	bbb = aaa[0:-1]
	imidx = bbb[0]
	for i in range(1,len(bbb)):
		imidx = imidx + "." + bbb[i]

	valid_lbl_name_list.append(data_dir + valid_label_dir + imidx + label_ext)    
    
    

print("---")
print("train images: ", len(tra_img_name_list))
print("train labels: ", len(tra_lbl_name_list))
print("---")


print("---")
print("valid images: ", len(valid_img_name_list))
print("valid labels: ", len(valid_lbl_name_list))
print("---")



#valid_size = round(len(tra_img_name_list) * 0.2)
valid_size = len(valid_img_name_list)
#train_size = len(tra_img_name_list) - valid_size
train_size = len(tra_img_name_list)
#print([train_size, valid_size])


#train_num = len(tra_img_name_list)

train_data = SalObjDataset(
    img_name_list=tra_img_name_list,
    lbl_name_list=tra_lbl_name_list,
    transform=transforms.Compose([
        RescaleT(256),
        RandomCrop(224),
        ToTensorLab(flag=0)]))


val_data = SalObjDataset(
    img_name_list=valid_img_name_list,
    lbl_name_list=valid_lbl_name_list,
    transform=transforms.Compose([
        RescaleT(256),
        RandomCrop(224),
        ToTensorLab(flag=0)]))



#train_data, val_data = torch.utils.data.random_split(salobj_dataset, [train_size, valid_size])

train_loader = DataLoader(train_data, batch_size=batch_size_train, shuffle=True, num_workers=0)
valid_loader = DataLoader(val_data, batch_size=batch_size_train, shuffle=True, num_workers=0)



# ------- 3. define model --------
# define the net
net = BASNet(3, 1)
net.load_state_dict(torch.load(PATH))


#device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
if torch.cuda.device_count() > 1:
    print("Let's use", torch.cuda.device_count(), "GPUs!")
    net = nn.DataParallel(net)

#net.to(device)


if torch.cuda.is_available():
    net.cuda()
    

# ------- 4. define optimizer --------

print("---define optimizer...")

################ New Code ################
### optimizer with step LR decrease
optimizer = optim.Adam(net.parameters(), lr=0.001, betas=(0.9, 0.999), eps=1e-08, weight_decay=0)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)

##########################################

#from torch.utils.tensorboard import SummaryWriter

# default `log_dir` is "runs" - we'll be more specific here
#writer = SummaryWriter('runs/basnet')


# ------- 5. training process --------
print("---start training...")
ite_num = 0
running_loss = 0.0
running_tar_loss = 0.0
ite_num4val = 0


ite_num_valid = 0
running_loss_valid = 0.0

running_tar_loss_valid = 0.0
ite_num4val_valid = 0

valid_loss_min = np.Inf


for epoch in range(0, epoch_num):

    net.train()
    for i, data in enumerate(train_loader):
        ite_num = ite_num + 1
        ite_num4val = ite_num4val + 1

        inputs, labels = data['image'], data['label']

        inputs = inputs.type(torch.FloatTensor)
        labels = labels.type(torch.FloatTensor)

        # wrap them in Variable
        if torch.cuda.is_available():
            inputs_v, labels_v = Variable(inputs.cuda(), requires_grad=False), Variable(labels.cuda(),
                                                                                        requires_grad=False)
        else:
            inputs_v, labels_v = Variable(inputs, requires_grad=False), Variable(labels, requires_grad=False)

        # y zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        d0, d1, d2, d3, d4, d5, d6, d7 = net(inputs_v)
        loss2, loss = muti_bce_loss_fusion(d0, d1, d2, d3, d4, d5, d6, d7, labels_v)

        loss.backward()
        optimizer.step()

        # # print statistics
        running_loss += loss.item()
        running_tar_loss += loss2.item()

        # del temporary outputs and loss
        del d0, d1, d2, d3, d4, d5, d6, d7, loss2, loss
        training_loss = running_tar_loss / ite_num4val
        print("[epoch: %3d/%3d, batch: %5d/%5d, ite: %d] train loss: %3f, tar: %3f ]" % (
        epoch + 1, epoch_num, (i + 1) * batch_size_train, train_size, ite_num, running_loss / ite_num4val, running_tar_loss / ite_num4val))
        
        ################## new code ###################
        ############ implement validation #############
        
        net.eval()
        for i, data in enumerate(valid_loader):
            
            ite_num_valid = ite_num_valid + 1
            ite_num4val_valid = ite_num4val_valid + 1

            inputs, labels = data['image'], data['label']
        
            inputs = inputs.type(torch.FloatTensor)
            labels = labels.type(torch.FloatTensor)

            # wrap them in Variable
            if torch.cuda.is_available():
                inputs_v, labels_v = Variable(inputs.cuda(), requires_grad=False), Variable(labels.cuda(),
                                                                                            requires_grad=False)
            else:
                inputs_v, labels_v = Variable(inputs, requires_grad=False), Variable(labels, requires_grad=False)

            # forward + backward + optimize
            d0, d1, d2, d3, d4, d5, d6, d7 = net(inputs_v)
            loss2_val, loss_val = muti_bce_loss_fusion(d0, d1, d2, d3, d4, d5, d6, d7, labels_v)
            
            
            # # print statistics
            running_loss_valid += loss_val.item()
            running_tar_loss_valid += loss2_val.item()


        
        # del temporary outputs and loss
        del d0, d1, d2, d3, d4, d5, d6, d7, loss2_val, loss_val
        
        valid_loss = running_tar_loss_valid / ite_num4val_valid
      
        

        
        print("[Valid loss: %3f, tar: %3f ]" % (running_loss_valid / ite_num4val_valid,
                                               valid_loss))

        ############# Save the model if tar loss decrease #################
        ###################################################################
        # save model if validation loss has decreased
        if valid_loss <= valid_loss_min:
            print('Validation loss decreased ({:.6f} --> {:.6f}).  Saving model ...'.format(
            valid_loss_min,
            valid_loss))
            torch.save(net.module.state_dict(), model_dir + 'optimized_model_%3f.pth' %(valid_loss))
            #torch.save(net.state_dict(), model_dir + "basnet_bsi_itr_%d_train_%3f_tar_%3f.pth" % (ite_num, running_loss / ite_num4val, running_tar_loss / ite_num4val))
            valid_loss_min = valid_loss
            
            running_loss = 0.0
            running_tar_loss = 0.0
            net.train()  # resume train
            ite_num4val = 0
            print('##########')
            
            
        ite_num_valid = 0
        ite_num4val_valid = 0
        
        running_loss_valid = 0.0

        running_tar_loss_valid = 0.0
        scheduler.step()
        
        ############### Tensorboard #################

        # ...log the running loss
        #writer.add_scalar('training loss',
        #                    training_loss,
        #                    ite_num + 1)
        
        # ...log the running loss
        #writer.add_scalar('validation loss',
        #                    valid_loss,
        #                    ite_num + 1)  
        
        #if ite_num % 2000 == 0:  # save model every 2000 iterations

         #   torch.save(net.state_dict(), model_dir + "basnet_bsi_itr_%d_train_%3f_tar_%3f.pth" % (ite_num, running_loss / ite_num4val, running_tar_loss / ite_num4val))
         #   running_loss = 0.0
         #   running_tar_loss = 0.0
         #   net.train()  # resume train
         #   ite_num4val = 0
        
        
        #if ite_num % 2000 == 0:  # save model every 2000 iterations

            #torch.save(net.state_dict(), model_dir + "basnet_bsi_itr_%d_train_%3f_tar_%3f.pth" % (ite_num, running_loss / ite_num4val, running_tar_loss / ite_num4val))
            #running_loss = 0.0
            #running_tar_loss = 0.0
           
            #ite_num4val = 0

print('-------------Congratulations! Training Done!!!-------------')
