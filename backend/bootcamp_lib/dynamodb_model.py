# This file should be kept compatible with Python 3.7 syntax

from typing import Dict, Set, _GenericAlias
import dataclasses
from decimal import Decimal
import copy

from dynamodb_json import json_util  # type: ignore


class DynamoDbModelValueConversionError(Exception):
    pass


class DynamoDbModel:
    """Base model for entity validation and properties conversion to DynamoDB values.
    """

    __slots__ = ("_errors")
    _INTERNAL_FIELDS = ["_errors", "_convert_types", "_fields"]
    _validations: Dict[str, dict] = {}
    _convert_types: Dict[str, type] = None
    _fields: Set[str] = None

    def __init__(self):
        self._errors: Dict[str, dict] = {}

    def validate(self) -> bool:
        """Validate the object properties using the validation rules declared at model level.

        Returns:
            True if object is valid, False if there are errors
        """
        self._errors = {}
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)

            validations = self._validations.get(field.name)
            if validations:
                if validations.get("required") and (value is None or value == ""):
                    self._errors[field.name] = {"error": "field required", "value": value}
                    continue

            if field.type == bool and not isinstance(value, bool):
                self._errors[field.name] = {"error": "Not a boolean value", "value": value}

        return len(self._errors) == 0

    @property
    def validation_errors(self) -> Dict[str, dict]:
        """Returns a list of errors as a dictionary, with a key for every invalid object property.

        Dictionary format: {field_name: {"error": "Error message", "value": field_value}, ...}

        Returns:
            errors list a dictionary
        """
        return self._errors

    def to_dict(self) -> dict:
        """Converts the object to a dictionary

        Returns:
            The object as a dictionary
        """
        data = copy.copy(self.__dict__)
        for key in data.keys():
            if isinstance(data[key], DynamoDbModel):
                data[key] = data[key].to_dict()
            elif isinstance(data[key], list):
                data[key] = [
                    el.to_dict() if isinstance(el, DynamoDbModel) else el
                    for el in data[key]]
        return data

    def _to_dynamodb_dict(self, data: dict) -> dict:
        """Process the dictionary for DynamoDb compatibility. It alters the input dict.

        Args:
            data: the dictionary that should be made DynamoDb compliant.

        Returns:
            The altered dictionary which was given as input.
        """
        for key in list(data.keys()):
            if data[key] == "" or data[key] is None:
                del data[key]
            elif isinstance(data[key], float):
                data[key] = Decimal(str(data[key]))  # convert to str becase of a boto3 bug
            elif isinstance(data[key], dict):
                data[key] = self._to_dynamodb_dict(data[key])
            elif isinstance(data[key], list):
                data[key] = [
                    self._to_dynamodb_dict(el) if isinstance(el, dict) else el
                    for el in data[key]]
        return data

    def to_dynamodb_dict(self, serialize=False) -> dict:
        """Converts the object to a DynamoDB compatible dictionary.

        Empty string or None properties are removed, float values are converted to Decimal.

        Args:
            serialize: True if dictionary should be in DynamoDB format used by boto3 client,
                False if dictionary is returned in a simple format.

        Returns:
            The converted dictionary.
        """
        # remove empty values, even if now they are supported by dynamodb
        data = self._to_dynamodb_dict(self.to_dict())
        return json_util.dumps(data, as_dict=True) if serialize else data

    @staticmethod
    def dict_to_model(model_class, dict: dict):
        # Select the subset of a dictionary when a model class is initialized with a dictionary
        # which has other keys besides those supported by the model. Useful when loading a database
        # item but we want to initialise a subset model to be used in an API.
        # In most cases, the initialised model should match the database record fields,
        # if this changes and most dictionaries would need a resize, the approach should be changed.

        try:
            return model_class(**dict)
        except TypeError:
            # cache the fields names for the model class
            if not model_class._fields:
                model_class._fields = {field.name for field in dataclasses.fields(model_class)}

            new_dict = {prop: val for prop, val in dict.items() if prop in model_class._fields}
            return model_class(**new_dict)

    def __post_init__(self):
        super().__init__()
        if self.__class__._convert_types is None:
            self.__class__._convert_types = {}
            for field in dataclasses.fields(self.__class__):
                if field.type in (int, float):
                    self.__class__._convert_types[field.name] = field.type
                elif isinstance(field.type, _GenericAlias):
                    type_name = str(field.type)
                    if (type_name.startswith("typing.Union")
                            or type_name.startswith("typing.Optional")):
                        subtype = field.type.__args__[0]
                        if str(subtype).startswith("typing.List"):
                            if (subtype.__args__[0] in (int, float)
                                    or issubclass(subtype.__args__[0], DynamoDbModel)):
                                self.__class__._convert_types[field.name] = subtype.__args__[0]
                        elif (subtype in (int, float) or issubclass(subtype, DynamoDbModel)):
                            self.__class__._convert_types[field.name] = subtype
                    elif type_name.startswith("typing.List"):
                        self.__class__._convert_types[field.name] = field.type.__args__[0]
                elif issubclass(field.type, DynamoDbModel):
                    self.__class__._convert_types[field.name] = field.type

        if self.__class__._convert_types:
            for field_name, dest_type in self.__class__._convert_types.items():
                value = getattr(self, field_name)
                if value is None:
                    continue
                if isinstance(value, list):
                    if not issubclass(dest_type, DynamoDbModel):
                        value = [dest_type(el) for el in value]
                    else:
                        value = [
                            el if isinstance(el, DynamoDbModel)
                            else self.dict_to_model(dest_type, el)
                            for el in value]
                    setattr(self, field_name, value)
                elif not isinstance(value, dest_type):
                    if issubclass(dest_type, DynamoDbModel):
                        setattr(self, field_name, dest_type(**value))
                    else:
                        # If Numeric value is an empty string, it should be converted to None
                        # So we can differentiate between an empty string and None
                        if not value:
                            setattr(self, field_name, None)
                            continue
                        try:
                            setattr(self, field_name, dest_type(value))
                        except Exception as e:
                            raise DynamoDbModelValueConversionError(
                                f"Error converting field {field_name} to {dest_type}: {e}") from e
