class DataUtils(object):



    @staticmethod
    def get_json_field_dot_notation(key, json):
        x = json
        keys = key.split(".")
        for key in keys:
            x = x[key]
        return x