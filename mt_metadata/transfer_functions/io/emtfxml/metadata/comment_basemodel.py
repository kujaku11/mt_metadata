# =====================================================
# Imports
# =====================================================
from xml.etree import cElementTree as et

from loguru import logger

from mt_metadata.common import Comment as CommonComment
from mt_metadata.transfer_functions.io.emtfxml.metadata import helpers


# =====================================================
class Comment(CommonComment):
    def read_dict(self, input_dict: dict) -> None:
        """

        :param input_dict: read the input dictionary and populate the model fields.
        :type input_dict: dict
        :return: None
        :rtype: None

        """
        key = input_dict["comments"]
        if isinstance(key, str):
            self.value = key
        elif isinstance(key, dict):
            try:
                self.value = key["value"]
            except KeyError:
                logger.debug("No value in comment")

            try:
                self.author = key["author"]
            except KeyError:
                logger.debug("No author of comment")
            try:
                self.time_stamp = key["date"]
            except KeyError:
                logger.debug("No date for comment")
        else:
            raise TypeError(f"Comment cannot parse type {type(key)}")

    def to_xml(self, string: bool = False, required: bool = True) -> et.Element | str:
        """convert the comment to XML format.

        :param string: if True, return the XML as a string, defaults to False
        :type string: bool, optional
        :param required: if True, include required fields, defaults to True
        :type required: bool, optional
        :return: XML element or string representation of the comment
        :rtype: et.Element | str
        """

        author_value = self.author if self.author is not None else ""
        root = et.Element(self.__class__.__name__ + "s", {"author": author_value})
        value_text = self.value if self.value is not None else ""
        root.text = value_text

        if string:
            return helpers.element_to_string(root)
        return root
