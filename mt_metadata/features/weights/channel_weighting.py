"""
    Container for weighting strategy to apply to a single tf estimation
    having a single output channel (usually one of "ex", "ey", "hz").

"""

class ChannelWeighting(Base):
    """
    Per-output-channel weighting strategy.
    Combines multiple feature-based kernels using a specified method.
    """
    
