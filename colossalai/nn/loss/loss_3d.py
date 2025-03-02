from colossalai.constants import INPUT_GROUP_3D, WEIGHT_GROUP_3D
from colossalai.nn.layer.parallel_3d import reduce_by_batch_3d
from colossalai.nn.layer.parallel_3d._utils import get_parallel_mode_from_env
from colossalai.registry import LOSSES
from torch.nn.functional import cross_entropy
from torch.nn.modules.loss import _Loss

@LOSSES.register_module
class CrossEntropyLoss3D(_Loss):
    """
    Cross entropy loss for 3D parallelism

    :param depth: depth for 3D parallelism
    :type depth: int
    :param reduction: whether to average the loss, defaults to True
    :type reduction: bool, optional
    """
    def __init__(self, reduction=True, *args, **kwargs):
        super().__init__()
        self.input_parallel_mode = get_parallel_mode_from_env(INPUT_GROUP_3D)
        self.weight_parallel_mode = get_parallel_mode_from_env(WEIGHT_GROUP_3D)
        self.reduction_mean = reduction
        self.loss_args = args
        self.loss_kwargs = kwargs

    def forward(self, logits, targets):
        loss = cross_entropy(logits, targets, reduction='none', *self.loss_args, **self.loss_kwargs)
        if self.reduction_mean:
            loss = loss.mean()
            loss = reduce_by_batch_3d.apply(loss, self.input_parallel_mode, self.weight_parallel_mode, True)
        return loss
