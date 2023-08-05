"""DB config
These are a set of object for defining a database table in a dialect agnostic way.
"""
from dataclasses import dataclass
from enum import Enum

from sqlalchemy import ForeignKey


class DBDatatype(Enum):
    """A generic datatype that should be supported by all database types."""

    TEXT = "text"
    DATE = "date"
    INT = "int"
    FLOAT = "float"
    BOOLEAN = "boolean"


@dataclass
class DBAttributeConfig:
    """A config for a table attribute(column)."""

    name: str
    datatype: DBDatatype

    def __post_init__(self) -> None:
        if not isinstance(self.datatype, DBDatatype):
            raise TypeError(f"Param datatype is not of type DBDatatype:{self.datatype}")


@dataclass
class DBForeignKey:
    """A foreign key in a database object attribute."""

    name: str
    foreign_object_name: str
    foreign_attribute_name: str


class ConfigAttributeError(Exception):
    """ConfigAttributeError"""

    def __init__(self, message: str, object_name: str) -> None:
        self.message = message
        self.object_name = object_name
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.message}: {self.object_name}"


class ConfigKeyError(Exception):
    """ConfigKeyError"""

    def __init__(self, message: str, object_name: str, key: str = None) -> None:
        self.message = message
        self.object_name = object_name
        self.key = key
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.key is None:
            return f"{self.message}: {self.object_name}"
        return f"{self.message}: {self.object_name}; {self.key}"


@dataclass
class DBObjectConfig:
    """A config for a generic database object."""

    name: str
    attributes: list[DBAttributeConfig]
    primary_keys: list[str]
    foreign_keys: list[DBForeignKey]

    def __post_init__(self) -> None:
        self._check_attributes()
        self._check_primary_keys()
        self._check_foreign_keys()

    def get_attribute_names(self) -> list[str]:
        """Returns a list of names of the attributes

        Returns:
            List[str]: A list of names of the attributes
        """
        return [att.name for att in self.attributes]

    def get_foreign_key_names(self) -> list[str]:
        """Returns a list of names of the foreign keys

        Returns:
            List[str]: A list of names of the foreign keys
        """
        return [key.name for key in self.foreign_keys]

    def get_foreign_key_by_name(self, name: str) -> DBForeignKey:
        """Returns foreign key

        Args:
            name (str): name of the foreign key

        Returns:
            DBForeignKey: The foreign key asked for
        """
        return [key for key in self.foreign_keys if key.name == name][0]

    def _check_attributes(self) -> None:
        if len(self.attributes) == 0:
            raise ConfigAttributeError("Attributes is empty", self.name)
        if len(self.get_attribute_names()) != len(set(self.get_attribute_names())):
            raise ConfigAttributeError("Attributes has duplicates", self.name)

    def _check_primary_keys(self) -> None:
        if len(self.primary_keys) == 0:
            raise ConfigKeyError("Primary keys is empty", self.name)
        for key in self.primary_keys:
            self._check_primary_key(key)

    def _check_primary_key(self, key: ForeignKey) -> None:
        if key not in self.get_attribute_names():
            raise ConfigKeyError(
                "Primary key is missing from attributes", self.name, key
            )

    def _check_foreign_keys(self) -> None:
        for key in self.foreign_keys:
            self._check_foreign_key(key)

    def _check_foreign_key(self, key: ForeignKey) -> None:
        if key.name not in self.get_attribute_names():
            raise ConfigKeyError(
                "Foreign key is missing from attributes", self.name, key
            )
        if key.foreign_object_name == self.name:
            raise ConfigKeyError(
                "Foreign key references its own object", self.name, key
            )


class ConfigForeignKeyObjectError(Exception):
    """ConfigForeignKeyObjectError"""

    def __init__(
        self, foreign_key: str, object_name: str, foreign_object_name: str
    ) -> None:
        self.message = "Foreign key references object which does not exist in config."
        self.foreign_key = foreign_key
        self.object_name = object_name
        self.foreign_object_name = foreign_object_name
        super().__init__(self.message)

    def __str__(self) -> str:
        msg = (
            f"Foreign key '{self.foreign_key}' in object '{self.object_name}' references object"
            f"'{self.foreign_object_name}' which does not exist in config."
        )
        return msg


class ConfigForeignKeyObjectError2(Exception):
    """ConfigForeignKeyObjectError2"""

    def __init__(
        self,
        foreign_key: str,
        object_name: str,
        foreign_object_name: str,
        foreign_object_attribute: str,
    ) -> None:
        self.message = "Foreign key references attribute which does not exist."
        self.foreign_key = foreign_key
        self.object_name = object_name
        self.foreign_object_name = foreign_object_name
        self.foreign_object_attribute = foreign_object_attribute
        super().__init__(self.message)

    def __str__(self) -> str:
        msg = (
            f"Foreign key '{self.foreign_key}' in object '{self.object_name}' references"
            f"attribute '{self.foreign_object_attribute}' which does not exist in object"
            f"'{self.foreign_object_name}'"
        )
        return msg


@dataclass
class DBConfig:
    """A group of configs for generic database tables."""

    configs: list[DBObjectConfig]

    def __post_init__(self) -> None:
        for config in self.configs:
            self._check_foreign_keys(config)

    def get_config_names(self) -> list[str]:
        """Returns a list of names of the configs

        Returns:
            List[str]: A list of names of the configs
        """
        return [config.name for config in self.configs]

    def get_config_by_name(self, name: str) -> DBObjectConfig:
        """Returns the config

        Args:
            name (str): name of the config

        Returns:
            DBObjectConfig: The DBObjectConfig asked for
        """
        return [config for config in self.configs if config.name == name][0]

    def _check_foreign_keys(self, config: DBObjectConfig) -> None:
        for key in config.foreign_keys:
            self._check_foreign_key_object(config, key)
            self._check_foreign_key_attribute(config, key)

    def _check_foreign_key_object(
        self, config: DBObjectConfig, key: ForeignKey
    ) -> None:
        if key.foreign_object_name not in self.get_config_names():
            raise ConfigForeignKeyObjectError(
                foreign_key=key,
                object_name=config.name,
                foreign_object_name=key.foreign_object_name,
            )

    def _check_foreign_key_attribute(
        self, config: DBObjectConfig, key: ForeignKey
    ) -> None:
        foreign_config = self.get_config_by_name(key.foreign_object_name)
        if key.foreign_attribute_name not in foreign_config.get_attribute_names():
            raise ConfigForeignKeyObjectError2(
                foreign_key=key,
                object_name=config.name,
                foreign_object_name=key.foreign_object_name,
                foreign_object_attribute=key.foreign_attribute_name,
            )
