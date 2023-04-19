import torch
import torch.nn as nn

class Discriminator(nn.Module):

    def __init__(self, channels_img, features_d, use_dropout=False):
        super(Discriminator, self).__init__()
        self.use_dropout = use_dropout
        self.discriminator = nn.Sequential(
            # Input: N x channels_img x 64 x 64
            nn.utils.spectral_norm(
                nn.Conv2d(
                    channels_img,
                    features_d,
                    kernel_size=4,
                    stride=2,
                    padding=1
                )
            ), # 32x32
            nn.LeakyReLU(0.2),
            self._block(features_d, features_d*2, 4, 2, 1), # 16x16
            self._block(features_d*2, features_d*4, 4, 2, 1), # 8x8
            self._block(features_d*4, features_d*8, 4, 2, 1), # 4x4
            nn.utils.spectral_norm(
                nn.Conv2d(features_d*8, 1, 4, 2, 0)
            ), # 1x1
            nn.Sigmoid(),
        )

    def _block(self, in_channels, out_channels, kernel_size, stride, padding):
        block = nn.Sequential(
            nn.utils.spectral_norm(
                nn.Conv2d(
                    in_channels,
                    out_channels,
                    kernel_size,
                    stride,
                    padding,
                    bias=False
                )
            ),
            nn.BatchNorm2d(out_channels),
            nn.LeakyReLU(0.2)
        )

        if self.use_dropout:
            block.add_module('dropout', nn.Dropout(0.25))

        return block

    def forward(self, x):
        return self.discriminator(x)

class Generator(nn.Module):

    def __init__(self, z_dim, channels_img, features_g, use_dropout=False):
        super(Generator, self).__init__()
        self.use_dropout = use_dropout
        self.generator = nn.Sequential(
            # Input: N x z_dim x 1 x 1
            self._block(z_dim, features_g*16, 4, 1, 0), # 4 x 4
            self._block(features_g*16, features_g*8, 4, 2, 1), # 8 x 8
            self._block(features_g*8, features_g*4, 4, 2, 1), # 16 x 16
            self._block(features_g*4, features_g*2, 4, 2, 1), # 32 x 32
            nn.utils.spectral_norm(
                nn.ConvTranspose2d(
                    features_g*2,
                    channels_img,
                    kernel_size=4,
                    stride=2,
                    padding=1
                )
            ), # 64 x 64
            nn.Tanh(),
        )

    def _block(self, in_channels, out_channels, kernel_size, stride, padding):
        block = nn.Sequential(
            nn.utils.spectral_norm(
                nn.ConvTranspose2d(
                    in_channels,
                    out_channels,
                    kernel_size,
                    stride,
                    padding,
                    bias=False
                )
            ),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(),
        )

        if self.use_dropout:
            block.add_module('dropout', nn.Dropout(0.25))

        return block

    def forward(self, x):
        return self.generator(x)

def initialize_weights(model):
    for m in model.modules():
        if isinstance(m, (nn.Conv2d, nn.ConvTranspose2d)):
            nn.init.xavier_normal_(m.weight)
        elif isinstance(m, nn.BatchNorm2d):
            nn.init.constant_(m.weight, 1)
            nn.init.constant_(m.bias, 0)