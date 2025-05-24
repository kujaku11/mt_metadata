class TaperWeightKernel(BaseWeightKernel):
    def __init__(self, low_cut, high_cut, style="hann", **kwargs):
        super().__init__(**kwargs)
        self.low_kernel = MonotonicWeightKernel(
            threshold="low cut",
            transition_lower_bound=low_cut[0],
            transition_upper_bound=low_cut[1],
            half_window_style=style
        )
        self.high_kernel = MonotonicWeightKernel(
            threshold="high cut",
            transition_lower_bound=high_cut[0],
            transition_upper_bound=high_cut[1],
            half_window_style=style
        )

    def evaluate(self, values):
        return self.low_kernel.evaluate(values) * self.high_kernel.evaluate(values)
