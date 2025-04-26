from mt_metadata.timeseries.filtered_basemodel import Filtered, AppliedFilter

f1 = Filtered()
f1.filter_list.append(AppliedFilter(name="a", applied=True, stage=1))
f1.filter_list.append(AppliedFilter(name="b", applied=True, stage=2))


d = {
    "filtered": {
        "filter_list": [
            {"applied_filter": {"name": "low pass", "applied": True, "stage": 1}},
            {"applied_filter": {"name": "high pass", "applied": False, "stage": 2}},
        ],
        "comments": {"value": "Test comment"},
    }
}

f2 = Filtered()
f2.from_dict(d)
