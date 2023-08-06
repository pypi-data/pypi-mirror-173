# TODO: ADD support for array type fields while parsing eg: data.Median.[0].value
import logging
import re
from typing import Any, Dict, List

from .constants import RegexConstants
from .extracter.key_data_extracter import KeyDataExtracter
from .extracter.list_data_extracter import ListDataExtracter
from .extracter.object_list_data_extracter import ObjectListDataExtracter
# from .extracter.ListRangeDataExtracter import ListRangeDataExtractor
from .extracter.object_list_data_regex_extracter import \
    ObjectListDataRegexExtracter


class JSONQL:
    """
    Class to query JSON
    """

    def __init__(self, json: Dict):
        if not isinstance(json, dict):
            raise TypeError("Arg json should be of type dict")
        self.json = json
        self.picked_json = {}

    def pick(
        self, key: str = None, keys: list = [], key_delimiter: str = ".", key_mapping: dict = {}
    ):
        """Extract key from provided JSON object and returns new object of specified keys

        Keyword Arguments:
            key {str} -- A single key that needs to be extracted (default: {None})
            keys {list} -- A list of keys that needs to be extracted (default: {[]})
            key_delimiter {str} -- JSON object level separator used in the keys provided
                                    (default: {'.'})

        Returns:
            JSONQL -- object of JSONQL to allow functional chaining
        """
        if key is not None:
            final_obj = self._recursive_find(self.json, key.split(key_delimiter), 0)
            self.picked_json[key_mapping.get(key, key)] = final_obj
        elif len(keys) > 0:
            for key in keys:
                final_obj = self._recursive_find(self.json, key.split(key_delimiter), 0)
                self.picked_json[key_mapping.get(key, key)] = final_obj
        return self

    def _recursive_find(self, obj: Dict, level_list: List, index: int = 0):
        """recursively find and extract the requested keys

        Keyword Arguments:
            obj {dict} -- object on which extraction needs to be done
            level_list {list} -- list of key depth
            index {int} -- index of the level list (default: {0})

        Returns:
            [type] -- The request value/dict/list
        """
        try:
            current_level_obj = self._process_key(obj, level_list[index])
            if index == (len(level_list) - 1):
                return current_level_obj
            else:
                if current_level_obj is not None:
                    return self._recursive_find(current_level_obj, level_list, index + 1)
                else:
                    return None
        except Exception as ex:
            logging.error(ex)
            return None

    def _process_key(self, obj: Any, key: str) -> Any:
        """processes the key to make it usable for extraction and decides extraction type

        :param obj: obj on which key needs to be processed
        :param key: the key which needs to extracted

        :returns: extracted value
        """
        if re.match(RegexConstants.INDEXED_ARRAY, key):
            key = int(re.findall(RegexConstants.INDEXED_ARRAY, key)[0])
            return ListDataExtracter().extract(obj, key)
        elif re.match(RegexConstants.DICT_ARRAY_SEARCH, key):
            key = re.findall(RegexConstants.DICT_ARRAY_SEARCH, key)[0]
            return ObjectListDataExtracter().extract(obj, key)
        elif re.match(RegexConstants.DICT_ARRAY_REGEX_SEARCH, key):
            key = re.findall(RegexConstants.DICT_ARRAY_REGEX_SEARCH, key)[0]
            return ObjectListDataRegexExtracter().extract(obj, key)
        elif re.match(RegexConstants.NESTED_LIST, key):
            key = re.findall(RegexConstants.NESTED_LIST, key)[0]
            for item in obj:
                returned_value = self._process_key(item, key)
                if returned_value is not None:
                    return returned_value
        else:
            return KeyDataExtracter().extract(obj, key)
        # TODO: add support for range of array index
        # elif re.match(RegexConstants.RANGE_INDEXED_ARRAY, key):
        #     key = re.findall(RegexConstants.RANGE_INDEXED_ARRAY, key)[0]
        #     extracter = ListRangeDataExtractor()

    def remove(self, key: str = None, keys: list = []):
        # TODO: Add remove key functionality
        pass

    def exec(self):
        """fetches the final object with extracted keys and their values

        Returns:
            dict -- the dictionary with final extracted values
        """
        return self.picked_json
