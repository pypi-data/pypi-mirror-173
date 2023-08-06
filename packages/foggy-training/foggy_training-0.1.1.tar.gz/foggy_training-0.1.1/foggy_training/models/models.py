from torch import nn
from torch.nn.functional import mse_loss, cross_entropy, softmax

from foggy_training.base import LightningExtended, Task


class LinearRegression(LightningExtended):
    def __init__(self, n_inputs=4):
        super().__init__(loss=mse_loss)
        self.linear = nn.Linear(n_inputs, 1)
        self.lr = 1e-3

    def forward(self, x):
        return self.linear(x)


class SoftmaxClassifier(LightningExtended):
    def __init__(self, n_inputs: int, n_classes: int, task: Task):
        super().__init__(loss=cross_entropy, task=task)
        self.linear = nn.Linear(n_inputs, n_classes)

    def forward(self, x):
        x = x['x']
        x = self.linear(x)
        return softmax(x, dim=-1)
