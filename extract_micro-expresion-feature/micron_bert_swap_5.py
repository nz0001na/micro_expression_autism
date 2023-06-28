import torch
import torch.nn as nn
import torch.nn.functional as F
import cv2
from torchvision import transforms
import numpy as np
import os
import scipy.io as sio


os.environ["CUDA_VISIBLE_DEVICES"] = "0,2,3"
device = torch.device("cuda")

img_size = 224
imagenet_mean = np.array([0.485, 0.456, 0.406])
imagenet_std = np.array([0.229, 0.224, 0.225])

def image_to_tensor(image):
    x = torch.tensor(image)

    # make it a batch-like
    x = x.unsqueeze(dim=0)
    x = torch.einsum("nhwc->nchw", x).float()
    return x.cuda()


def preprocess(image, img_size):
    image = cv2.resize(image, (img_size, img_size)) / 255
    image = image - imagenet_mean
    image = image / imagenet_std
    return image


def load_image(frame_path, img_size):
    # print(frame_path)
    image = cv2.imread(frame_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return preprocess(image, img_size)


def get_model(checkpoint):
    checkpoint = torch.load(checkpoint)
    args = checkpoint["args"]
    print(args)
    print(checkpoint["epoch"])

    import models.mae as mae_dict

    if "mae" in args.model_name:
        import models.mae as mae_dict

        model = mae_dict.__dict__[args.model_name](
            has_decoder=args.has_decoder,
            aux_cls=args.aux_cls,
            img_size=args.img_size,
            att_loss=args.att_loss,
            diag_att=args.diag_att,
            # DINO params,
            enable_dino=args.enable_dino,
            out_dim=args.out_dim,
            local_crops_number=args.local_crops_number,
            warmup_teacher_temp=args.warmup_teacher_temp,
            teacher_temp=args.teacher_temp,
            warmup_teacher_temp_epochs=args.warmup_teacher_temp_epochs,
            epochs=args.epochs,
        )

    model_state_dict = {}
    for k, v in checkpoint["model"].items():
        model_state_dict[k.replace("module.", "")] = v

    model.load_state_dict(model_state_dict)
    return model, args


ro = '2_data_ADOS/'
src_path = ro + '7_cleaned_spotted_apex/1_frames_swap_70/'
dst_path = ro + '9_cleaned_spotted_feature/9_cleaned_spotted_mbert_feature_swap_70/'

checkpoint = 'checkpoints/CASME2-is224-p8-b16-ep200.pth'
# model = get_model(checkpoint).cuda()
model, args = get_model(checkpoint)
model = model.to(device)
model.eval()

catg_list = os.listdir(src_path)
for catg in catg_list:
    # if catg not in ['4_Not-ASD_bright', '4_Not-ASD_flip', '4_Not-ASD_hiseql']:
    #     continue
    id_list = os.listdir(src_path + catg)
    for ids in id_list:
        sce_list = os.listdir(src_path + catg + '/' + ids)
        for sce in sce_list:
            print(catg + '/' + ids + '/' + sce)

            dst_fold = dst_path + catg + '/' + ids + '/' + sce + '/'
            if not os.path.exists(dst_fold):
                os.makedirs(dst_fold)

            frm_list = os.listdir(src_path + catg + '/' + ids + '/' + sce)
            for frm in frm_list:
                img_path = src_path + catg + '/' + ids + '/' + sce + '/' + frm
                dst_file = dst_fold + frm.split('.')[0] + '.mat'
                if os.path.exists(dst_file) is True:
                    continue

                # To extract features
                image = load_image(img_path, img_size)
                image_tensor = image_to_tensor(image)

                with torch.no_grad():
                    features = model.extract_features(image_tensor)
                    features = features.detach().cpu().numpy()

                    dic = {}
                    dic['name'] = frm
                    dic['feature'] = features
                    sio.savemat(dst_file, dic)

                    # print('d')
                    # Use this features for finetunning.