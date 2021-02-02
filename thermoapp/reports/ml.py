"""Handles the utils of
machine learning.
"""

# Local
import os
import importlib
from typing import Any
import collections
import cv2

# Data
import numpy as np
import pandas as pd

# Omegaconf
from omegaconf import OmegaConf, DictConfig

# Albumentations
from albumentations.core.composition import Compose
import albumentations as A

# torch
import torch
from torch.utils.data import Dataset, DataLoader

# pytorch-lighting
import pytorch_lightning as pl


def get_cfg():
    """Get cfg object, with the preloaded
    configs.
    """

    cfg =  {'logging': {'log': True},
                        'data': { 'num_workers': 0, 
                        'batch_size': 12},
            'augmentation': {'valid': {'augs': [{'class_name': 'albumentations.pytorch.transforms.ToTensorV2', 
                                                    'params': {'p': 1.0}}],
                                        'bbox_params': {'format': 'pascal_voc', 
                                                        'label_fields': ['labels']}}}}

    return OmegaConf.create(cfg)


def load_obj(obj_path: str, default_obj_path: str = "") -> Any:
    """Extract an object from a given path.
        Args:
            obj_path: Path to an object to be extracted, 
            including the object name.
            default_obj_path: Default object path.
        Returns:
            Extracted object.
        Raises:
            AttributeError: When the object does not have 
            the given named attribute.
    """

    obj_path_list = obj_path.rsplit(".", 1)
    obj_path = obj_path_list.pop(0) if len(obj_path_list) > 1 else default_obj_path  
    obj_name = obj_path_list[0]
    module_obj = importlib.import_module(obj_path)
    
    if not hasattr(module_obj, obj_name):
        raise AttributeError(
            f"Object `{obj_name}` cannot be loaded from `{obj_path}`."
        )
    
    return getattr(module_obj, obj_name)


def collate_fn(batch):
    """Handles the pack of
    batches in a dataloder.
    """
    return tuple(zip(*batch))


def flatten_omegaconf(d, sep="_"):
    """Unroll the omegaconf."""
    d = OmegaConf.to_container(d)

    obj = collections.OrderedDict()

    def recurse(t, parent_key=""):

        if isinstance(t, list):
            for i in range(len(t)):
                recurse(t[i], parent_key + sep + str(i) if parent_key else str(i))
        elif isinstance(t, dict):
            for k, v in t.items():
                recurse(v, parent_key + sep + k if parent_key else k)
        else:
            obj[parent_key] = t

    recurse(d)
    obj = {k: v for k, v in obj.items() if type(v) in [int, float]}

    return obj


def eval_model(test_loader, 
               results, 
               detection_threshold, 
               device, 
               lit_model):
    """Evaluates an image on
    the model.
    """
    
    for images, _, image_ids in test_loader:
    
        images = list(image.to(device) for image in images)
        outputs = lit_model(images)

        for i, image in enumerate(images):

            boxes = outputs[i]['boxes'].data.cpu().numpy()
            scores = outputs[i]['scores'].data.cpu().numpy()
            
            boxes = boxes[scores >= detection_threshold].astype(np.int32)
            scores = scores[scores >= detection_threshold]
            image_id = image_ids[i]

            for s, b in zip(scores, boxes.astype(int)):
                result = {
                'image_id': image_id,
                'x1': b[0],
                'y1': b[1],
                'x2': b[2],
                'y2': b[3],
                'score': s,
                }

            
                results.append(result)
    
    return results


class ImgDataset(Dataset):

    def __init__(self,
                 mode: str = 'train',
                 image_dir: str = '',
                 cfg: DictConfig = None,
                 transforms: Compose = None):
        """

        Args:
            dataframe: dataframe with image id and bboxes
            mode: train/val/test
            cfg: config with parameters
            image_dir: path to images
            transforms: albumentations
        """
        self.image_dir = image_dir
        self.mode = mode
        self.cfg = cfg
        self.image_ids = os.listdir(self.image_dir) 
        self.transforms = transforms

    def __getitem__(self, idx: int):
        image_id = self.image_ids[idx].split('.')[0]
        #print(image_id)

        image = cv2.imread(f'{self.image_dir}/{image_id}.jpg', cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32)

        # normalization.
        image /= 255.0

        # test dataset must have some values so that transforms work.
        target = {'labels': torch.as_tensor([[0]], dtype=torch.float32),
                    'boxes': torch.as_tensor([[0, 0, 0, 0]], dtype=torch.float32)}

        # for train and valid test create target dict.
        if self.mode != 'test':
            image_data = self.df.loc[self.df['image_id'] == image_id]
            boxes = image_data[['x', 'y', 'x1', 'y1']].values

            areas = image_data['area'].values
            areas = torch.as_tensor(areas, dtype=torch.float32)

            # there is only one class
            labels = torch.ones((image_data.shape[0],), dtype=torch.int64)
            iscrowd = torch.zeros((image_data.shape[0],), dtype=torch.int64)

            target['boxes'] = boxes
            target['labels'] = labels
            target['image_id'] = torch.tensor([idx])
            target['area'] = areas
            target['iscrowd'] = iscrowd

            if self.transforms:
                image_dict = {
                    'image': image,
                    'bboxes': target['boxes'],
                    'labels': labels
                    }
                image_dict = self.transforms(**image_dict)
                image = image_dict['image']
                target['boxes'] = torch.as_tensor(image_dict['bboxes'], 
                                                    dtype=torch.float32)

        else:
            image_dict = {
                    'image': image,
                    'bboxes': target['boxes'],
                    'labels': target['labels']
                }
            image = self.transforms(**image_dict)['image']
            
        return image, target, image_id
        

    def __len__(self) -> int:
        return len(self.image_ids)


class LitImg(pl.LightningModule):

    def __init__(self, 
                 hparams: DictConfig = None, 
                 cfg: DictConfig = None, 
                 model = None):
        super(LitImg, self).__init__()
        self.cfg = cfg
        self.hparams = hparams
        self.model = model

    def forward(self, x, *args, **kwargs):
        return self.model(x)

    def configure_optimizers(self):
        if 'decoder_lr' in self.cfg.optimizer.params.keys():
            params = [
                {'params': self.model.decoder.parameters(), 'lr': self.cfg.optimizer.params.lr},
                {'params': self.model.encoder.parameters(), 'lr': self.cfg.optimizer.params.decoder_lr},
            ]
            optimizer = load_obj(self.cfg.optimizer.class_name)(params)

        else:
            optimizer = load_obj(self.cfg.optimizer.class_name)(self.model.parameters(), **self.cfg.optimizer.params)
        scheduler = load_obj(self.cfg.scheduler.class_name)(optimizer, **self.cfg.scheduler.params)

        return [optimizer], [{"scheduler": scheduler,
                              "interval": self.cfg.scheduler.step,
                              'monitor': self.cfg.scheduler.monitor}]


def calculate_temp_bbox(imgdir):
    """Calculate the bounding box
    of the temperature in the image.
    """
    cfg = get_cfg()

    valid_augs_list = [load_obj(i['class_name'])(**i['params']) for i in cfg['augmentation']['valid']['augs']]
    valid_bbox_params = OmegaConf.to_container((cfg['augmentation']['valid']['bbox_params']))
    valid_augs = A.Compose(valid_augs_list, bbox_params=valid_bbox_params)
        
    test_dataset = ImgDataset('test',
                               imgdir,
                               cfg,
                               valid_augs)
        
    test_loader = DataLoader(test_dataset,
                                 batch_size=1,
                                 num_workers=0,
                                 shuffle=False,
                                 collate_fn=collate_fn)
        
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    model = torch.load(os.path.dirname(os.path.abspath(__file__))+'/model.pth',
                           map_location=device)
        
    detection_threshold = 0.5
    results = []
    model.eval()

    hparams = flatten_omegaconf(cfg)

    lit_model = LitImg(hparams=hparams, 
                           cfg=cfg, 
                           model=model)

    res = eval_model(test_loader, 
                         results, 
                         detection_threshold, 
                         device, 
                         lit_model)

    return res