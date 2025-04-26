from mt_metadata.timeseries.filtered_basemodel import Filtered, AppliedFilter

f1 = Filtered()
f1.filter_list.append(AppliedFilter(name="a", applied=True, stage=1))
f1.filter_list.append(AppliedFilter(name="b", applied=True, stage=2))


f2 = Filtered()
f2.from_dict(f1.to_dict())
