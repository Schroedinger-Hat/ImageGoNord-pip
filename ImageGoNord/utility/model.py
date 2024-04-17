from functools import partial
import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import OrderedDict

device = "cuda" if torch.cuda.is_available() else "cpu"

class Conv2dAuto(nn.Conv2d):    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.padding =  (self.kernel_size[0] // 2, self.kernel_size[1] // 2)  #dynamic add padding based on the kernel_size       
conv3x3 = partial(Conv2dAuto, kernel_size=3, bias=False)      

def activation_func(activation):   #Activation function as mentioned in the paper - Leaky Relu
    return  nn.ModuleDict([
        ['relu', nn.ReLU(inplace=True)],
        ['leaky_relu', nn.LeakyReLU(negative_slope=0.01, inplace=True)],
        ['none', nn.Identity()]
    ])[activation]


class ResidualBlock(nn.Module):    
    def __init__(self, in_channels, out_channels, activation='relu'):
        super().__init__()
        self.in_channels, self.out_channels,self.activation =  in_channels, out_channels, activation
        self.blocks = nn.Identity()
        self.shortcut = nn.Identity()
        self.activate = activation_func(activation)   
    
    def forward(self, x):
        residual = x
        if self.should_apply_shortcut: residual = self.shortcut(x)
        x = self.blocks(x)
        x += residual
        x = self.activate(x)
        return x
    
    @property
    def should_apply_shortcut(self):
        return self.in_channels != self.out_channels

class ResNetResidualBlock(ResidualBlock):
    def __init__(self, in_channels, out_channels, expansion=1, downsampling=2, conv=conv3x3, *args, **kwargs):
        super().__init__(in_channels, out_channels)
        self.expansion, self.downsampling, self.conv = expansion, downsampling, conv
        self.shortcut = nn.Sequential(OrderedDict(
        {
            'conv' : nn.Conv2d(self.in_channels, self.expanded_channels, kernel_size=1,
                      stride=self.downsampling, bias=False, padding=0),
            'bn' : nn.InstanceNorm2d(self.expanded_channels)
            
        })) if self.should_apply_shortcut else None       
        
    @property
    def expanded_channels(self):
        return self.out_channels * self.expansion
    
    @property
    def should_apply_shortcut(self):
        return self.in_channels != self.expanded_channels

def conv_bn(in_channels, out_channels, conv, *args, **kwargs):
    return nn.Sequential(OrderedDict({'conv': conv(in_channels, out_channels, *args, **kwargs), 
                          'bn': nn.InstanceNorm2d(out_channels) }))
    
class ResNetBasicBlock(ResNetResidualBlock):
    expansion = 1
    def __init__(self, in_channels, out_channels, activation=nn.LeakyReLU, *args, **kwargs):
        super().__init__(in_channels, out_channels, *args, **kwargs)
        self.blocks = nn.Sequential(
            conv_bn(self.in_channels, self.out_channels,conv=self.conv, bias=False, stride=self.downsampling),
            activation(negative_slope=0.02),
            conv_bn(self.out_channels, self.expanded_channels,conv=self.conv, bias=False),
        )

class FeatureEncoder(nn.Module):

    def __init__(self,*args,**kwargs):
        super(FeatureEncoder,self).__init__()
        
        self.conv=nn.Conv2d(in_channels=3,out_channels=64,kernel_size=3,stride=1,padding=1)     #3xHxW 
        self.norm=nn.InstanceNorm2d(64)
        self.pool=nn.MaxPool2d(kernel_size=2, stride=2, padding=0)  

        self.res1 = ResNetBasicBlock(64, 128) 
        self.res2 = ResNetBasicBlock(128, 256)
        self.res3 = ResNetBasicBlock(256, 512)
             
    def forward(self, x):
        x = F.relu(self.norm(self.conv(x)))
        c4 = self.pool(x)
        c3 = self.res1(c4)
        c2 = self.res2(c3)
        c1 = self.res3(c2)
        return c1,c2,c3,c4

def de_conv(in_channels, out_channels,kernel_size=3):         #deconvolution 
    return nn.Sequential(
            nn.ConvTranspose2d(in_channels, out_channels,kernel_size=3,stride=2,output_padding=1, padding=1,bias=True),
            nn.InstanceNorm2d(out_channels),
            nn.LeakyReLU(negative_slope=0.02,inplace=True)
        )

class RecoloringDecoder(nn.Module):

    def __init__(self):
        super().__init__() 
        self.dconv_up_4 = de_conv(18 + 512, 256)                                              #pt,c1
        self.dconv_up_3 = de_conv(256 + 256, 128)                                             #c2,d1
        self.dconv_up_2 = de_conv(18 + 128 + 128, 64)                                         #pt,c3,d2
        self.dconv_up_1 = de_conv(18 + 64 + 64, 64)                                           #pt,c4,d3
        self.conv_last = nn.Conv2d(1 + 64, 2, kernel_size=3,padding=1)                        #Illu,d4

    def forward(self, c1, c2, c3, c4, target_palettes_1d, illu):
        bz, h, w = c1.shape[0], c1.shape[2], c1.shape[3]                                      #1,24,16
        tp_reshpaed = target_palettes_1d.reshape(bz,18,1,1)
        tp_c1 = tp_reshpaed.repeat(1,1,h,w)

        x = torch.cat((c1,tp_c1), 1)  
        x = self.dconv_up_4(x)

        x = torch.cat([c2, x], dim=1)                                                         #c2,d1(x)
        x = self.dconv_up_3(x)

        bz, h, w = x.shape[0], x.shape[2], x.shape[3]     
        tp_c3 = tp_reshpaed.repeat(1,1,h,w)
        x = torch.cat([tp_c3,c3,x], dim=1)                                                    #Pt,c3,x
        x = self.dconv_up_2(x)

        bz, h, w = x.shape[0], x.shape[2], x.shape[3]
        tp_c4 = tp_reshpaed.repeat(1,1,h,w)
        x = torch.cat([tp_c4,c4,x], dim=1)                                                    #Pt,c4,x
        x = self.dconv_up_1(x)

        illu = illu.view(illu.size(0), 1, illu.size(2), illu.size(3))  
        x = torch.cat((x, illu), dim = 1)
                                                             #illu,x
        x = self.conv_last(x)
        x = torch.tanh(x)
        return x