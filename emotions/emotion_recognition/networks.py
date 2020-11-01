"""
This file is largely the same as the file `networks.py`
of the PyPI package facial-emotion-recognition (version 0.3.4),
which has been released under MIT license by Rayyan Akhtar.

-------------------------------------------------------------------------------

MIT License

Copyright (c) 2020 Rayyan Akhtar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

-------------------------------------------------------------------------------
"""
import torch.nn as nn


class NetworkBasic(nn.Module):
    """Network described by facial-emotion-recognition package."""
    def __init__(self, in_c, nl, out_f):
        super(NetworkBasic, self).__init__()
        self.in_c, self.nl, self.out_f = in_c, nl, out_f

        self.conv_1 = nn.Sequential(
            nn.ReflectionPad2d(padding=1),
            nn.Conv2d(in_channels=self.in_c, out_channels=self.nl, kernel_size=(3, 3), stride=1, padding=0),
            nn.BatchNorm2d(self.nl),
            nn.ReLU(inplace=True)
        )

        self.conv_2 = nn.Sequential(
            nn.ReflectionPad2d(padding=1),
            nn.Conv2d(in_channels=self.nl, out_channels=2*self.nl, kernel_size=(3, 3), stride=2, padding=0),
            nn.BatchNorm2d(2*self.nl),
            nn.ReLU(inplace=True)
        )

        self.conv_3 = nn.Sequential(
            nn.ReflectionPad2d(padding=1),
            nn.Conv2d(in_channels=2*self.nl, out_channels=4 * self.nl, kernel_size=(3, 3), stride=2, padding=0),
            nn.BatchNorm2d(4 * self.nl),
            nn.ReLU(inplace=True)
        )

        self.conv_4 = nn.Sequential(
            nn.ReflectionPad2d(padding=1),
            nn.Conv2d(in_channels=4 * self.nl, out_channels=8 * self.nl, kernel_size=(3, 3), stride=2, padding=0),
            nn.BatchNorm2d(8 * self.nl),
            nn.ReLU(inplace=True)
        )

        self.linear = nn.Sequential(
            nn.Linear(in_features=256*6*6, out_features=256),
            nn.ReLU(inplace=True),
            nn.Linear(in_features=256, out_features=self.out_f),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.conv_1(x)
        x = self.conv_2(x)
        x = self.conv_3(x)
        x = self.conv_4(x)
        x = x.reshape((x.shape[0], -1))
        x = self.linear(x)
        return x
