from .data_extracter import DataExtracter


class ObjectListDataExtracter(DataExtracter):
    def __init__(self):
        super().__init__()

    def extract(self, obj_list: list, key: str):
        try:
            dict_key, dict_value = key.split("=")
            dict_key = dict_key.strip()
            dict_value = dict_value.strip()
            for obj in obj_list:
                if obj.get(dict_key, None) is not None and obj.get(dict_key) == dict_value:
                    return obj
            return None
        except Exception:
            return None
