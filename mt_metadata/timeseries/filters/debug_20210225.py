from mt_metadata.timeseries.filters.filter import Filter

qq = Filter()
print(qq)
from mt_metadata.timeseries.filters.time_delay_filter import TimeDelayFilter

tdf = TimeDelayFilter()
print(qq)
print(tdf)


# Out[4]:
# {
#     "filter": {
#         "calibration_date": "1980-01-01",
#         "name": null,
#         "type": null,
#         "units_in": null,
#         "units_out": null
#     }
# }


# Out[7]:
# {
#     "filter": {
#         "calibration_date": "1980-01-01",
#         "delay": null,
#         "name": null,
#         "type": null,
#         "units_in": null,
#         "units_out": null
#     }
# }
