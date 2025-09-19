"""
    The base class for a weighting kernel.

"""
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS

# attr_dict = get_schema("base", SCHEMA_FN_PATHS)


class BaseWeightKernel(Base):
    """
    BaseWeightKernel

    A base class for defining a weighting kernel that can be applied to a feature
    to determine its contribution to a final weight value.

    This class is not intended to be used directly but to be subclassed by
    specific kernel types (e.g., MonotonicWeightKernel, CompositeWeightKernel).
    """
    # __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.from_dict(kwargs)

    def evaluate(self, values):
        """
        Evaluate the kernel on the input feature values.

        Parameters
        ----------
        values : np.ndarray or float
            The feature values to apply the weight kernel to.

        Returns
        -------
        weights : np.ndarray or float
            The resulting weight(s).
        """
        raise NotImplementedError("BaseWeightKernel cannot be evaluated directly.")


