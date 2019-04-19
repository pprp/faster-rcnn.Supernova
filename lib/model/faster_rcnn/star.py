from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import math
import torchvision.models as models
from model.faster_rcnn.faster_rcnn import _fasterRCNN
import pdb

class baseNet(nn.Module):
  def __init__(self,num_classes=2,init_weights=True):
    super(baseNet,self).__init__()
    self.num_classes = num_classes
    self.features = nn.Sequential(
      nn.Conv2d(3, 64, 3, padding=1 ),
      nn.Conv2d(64, 64, 3, padding=1 ),
      nn.MaxPool2d(kernel_size=2, stride=2),
      nn.Conv2d(64, 128, 3, padding=1 ),
      nn.Conv2d(128, 128, 3, padding=1 ),
      nn.MaxPool2d(kernel_size=2, stride=2),
      nn.Conv2d(128, 256, 3, padding=1 ),
      nn.Conv2d(256, 256, 3, padding=1 ),
      nn.Conv2d(256, 256, 3, padding=1 ),
      nn.MaxPool2d(kernel_size=2, stride=2),
      nn.Conv2d(256, 512, 3, padding=1 ),
      nn.Conv2d(512, 512, 3, padding=1 ),
      nn.Conv2d(512, 512, 3, padding=1 ),
      nn.MaxPool2d(kernel_size=2, stride=2),
      nn.Conv2d(512, 512, 3, padding=1 ),
      nn.Conv2d(512, 512, 3, padding=1 ),
      nn.Conv2d(512, 512, 3, padding=1 )
    )
    self.avgpool = nn.AdaptiveAvgPool2d((7, 7))
    self.classifier = nn.Sequential(
            nn.Linear(512 * 7 * 7, 4096),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(4096, self.num_classes),
        )
    if init_weights:
      self._initialize_weights()

  def forward(self, x):
    x = self.features(x)
    x = self.avgpool(x)
    x = x.view(x.size(0), -1)
    x = self.classifier(x)
    return x

  def _initialize_weights(self):
    for m in self.modules():
      if isinstance(m, nn.Conv2d):
        nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
        if m.bias is not None:
          nn.init.constant_(m.bias, 0)
      elif isinstance(m, nn.BatchNorm2d):
          nn.init.constant_(m.weight, 1)
          nn.init.constant_(m.bias, 0)
      elif isinstance(m, nn.Linear):
          nn.init.normal_(m.weight, 0, 0.01)
          nn.init.constant_(m.bias, 0)


class star(_fasterRCNN):
  def __init__(self, classes, pretrained=False, class_agnostic=False):
    #self.model_path = 'data/pretrained_model/vgg16_caffe.pth'
    self.dout_base_model = 512
    self.pretrained = pretrained
    self.class_agnostic = class_agnostic
    self.n_classes = len(classes)
    _fasterRCNN.__init__(self, classes, class_agnostic)

    # compo
    self.modules = nn.Sequential()

  def _init_modules(self):
    print("classes %d" % (self.n_classes))
    myvgg = baseNet(num_classes=self.n_classes)

    myvgg.classifier = nn.Sequential(*list(myvgg.classifier._modules.values())[:-1])
    # change -1 to -4
    #vgg.classifier = nn.Sequential(*list(vgg.classifier._modules.values())[:-1])
    # change -1 to -4
    # not using the last maxpool layer
    self.RCNN_base = nn.Sequential(*list(myvgg.features._modules.values())[:-1])

    # self.RCNN_base = _RCNN_base(vgg.features, self.classes, self.dout_base_model)

    self.RCNN_top = myvgg.classifier

    # not using the last maxpool layer
    # change 4096 to 100352
    self.RCNN_cls_score = nn.Linear(4096, self.n_classes)

    if self.class_agnostic:
      self.RCNN_bbox_pred = nn.Linear(4096, 4)
    else:
      self.RCNN_bbox_pred = nn.Linear(4096, 4 * self.n_classes)      

  def _head_to_tail(self, pool5):
    pool5_flat = pool5.view(pool5.size(0), -1)
    fc7 = self.RCNN_top(pool5_flat)

    return fc7

