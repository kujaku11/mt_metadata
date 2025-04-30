# from mt_metadata.timeseries.filtered_basemodel import Filtered, AppliedFilter

# f1 = Filtered()
# f1.filter_list.append(AppliedFilter(name="a", applied=True, stage=1))
# f1.filter_list.append(AppliedFilter(name="b", applied=True, stage=2))


# d = {
#     "filtered": {
#         "filter_list": [
#             {"applied_filter": {"name": "low pass", "applied": True, "stage": 1}},
#             {"applied_filter": {"name": "high pass", "applied": False, "stage": 2}},
#         ],
#         "comments": {"value": "Test comment"},
#     }
# }

# f2 = Filtered()
# f2.from_dict(d)

from mt_metadata.timeseries.run_basemodel import Run
from mt_metadata.timeseries.electric_basemodel import Electric

r = Run()
# r.copy()
# r.add_channel(Electric(component="ex"))
# existing_channels = r.channels.copy()
# existing_channels.remove("ex")
# r.channels = existing_channels
# print(r.channels.keys())

from mt_metadata.timeseries.filters.fir_filter_basemodel import FirFilter

f = FirFilter()
f.type = "fap"
