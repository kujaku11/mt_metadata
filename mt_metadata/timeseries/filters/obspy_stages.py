import obspy

from mt_metadata.filters.coefficient_filter import CoefficientFilter
from pole_zero_filter import PoleZeroFilter

def create_coefficent_filter_from_stage(stage):
    coeff_filter = CoefficientFilter()
    coeff_filter = coeff_filter.from_obspy_stage(stage)
    return coeff_filter
    

def create_pole_zero_filter_from_stage(stage):
    #interesting.  The Stage is pretty nicely keyed up already.
    #is there a cute one-liner to package all its attrs into a mapping?
    #kwargs dict so we can pass, for example **Stages?
    stage_dict = stage.__dict__
    pz_filter = PoleZeroFilter(**stage_dict)
    zpg = pz_filter.zero_pole_gain_representation()
    plot_it = False
    if plot_it:
        sampling_rate = 10.0
        frequency_axis = np.fft.fftfreq(1000, d=1./sampling_rate)

        angular_frequency_axis = 2 * np.pi * frequency_axis
        frequency_axis = np.logspace(-1, 5, num=100)
        w = 2. * np.pi * frequency_axis
        complex_response = pz_filter.complex_response(frequency_axis)
        plot_response(zpk_obs=zpg, w_values=w, title=pz_filter.name)
    #plot the response function in pole_zero land, and as a function of
    return pz_filter



def create_filter_from_stage(stage):
    #this works on a single stage
    if isinstance(stage, obspy.core.inventory.response.PolesZerosResponseStage):
        create_pole_zero_filter_from_stage(stage)
    elif isinstance(stage, obspy.core.inventory.response.CoefficientsTypeResponseStage):
        create_coefficent_filter_from_stage(stage)
    else:
        print("Filter Stage of Type {} not known".format(type(stage)))
        raise Exception
