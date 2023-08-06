from __future__ import annotations

from datetime import date, datetime
import json
import random
import string
from typing import List, Optional, Type, TypeVar, Union

from benchling_api_client.v2.alpha.models.app_config_item import AppConfigItem
from benchling_api_client.v2.alpha.models.base_manifest_config import BaseManifestConfig
from benchling_api_client.v2.alpha.models.benchling_app_manifest import BenchlingAppManifest
from benchling_api_client.v2.alpha.models.boolean_app_config_item import BooleanAppConfigItem
from benchling_api_client.v2.alpha.models.boolean_app_config_item_type import BooleanAppConfigItemType
from benchling_api_client.v2.alpha.models.date_app_config_item import DateAppConfigItem
from benchling_api_client.v2.alpha.models.date_app_config_item_type import DateAppConfigItemType
from benchling_api_client.v2.alpha.models.datetime_app_config_item import DatetimeAppConfigItem
from benchling_api_client.v2.alpha.models.datetime_app_config_item_type import DatetimeAppConfigItemType
from benchling_api_client.v2.alpha.models.dropdown_dependency import DropdownDependency
from benchling_api_client.v2.alpha.models.entity_schema_app_config_item import EntitySchemaAppConfigItem
from benchling_api_client.v2.alpha.models.entity_schema_dependency import EntitySchemaDependency
from benchling_api_client.v2.alpha.models.field_app_config_item import FieldAppConfigItem
from benchling_api_client.v2.alpha.models.field_app_config_item_type import FieldAppConfigItemType
from benchling_api_client.v2.alpha.models.float_app_config_item import FloatAppConfigItem
from benchling_api_client.v2.alpha.models.float_app_config_item_type import FloatAppConfigItemType
from benchling_api_client.v2.alpha.models.generic_api_identified_app_config_item import (
    GenericApiIdentifiedAppConfigItem,
)
from benchling_api_client.v2.alpha.models.generic_api_identified_app_config_item_type import (
    GenericApiIdentifiedAppConfigItemType,
)
from benchling_api_client.v2.alpha.models.integer_app_config_item import IntegerAppConfigItem
from benchling_api_client.v2.alpha.models.integer_app_config_item_type import IntegerAppConfigItemType
from benchling_api_client.v2.alpha.models.json_app_config_item import JsonAppConfigItem
from benchling_api_client.v2.alpha.models.json_app_config_item_type import JsonAppConfigItemType
from benchling_api_client.v2.alpha.models.linked_app_config_resource_summary import (
    LinkedAppConfigResourceSummary,
)
from benchling_api_client.v2.alpha.models.manifest_scalar_config import ManifestScalarConfig
from benchling_api_client.v2.alpha.models.resource_dependency import ResourceDependency
from benchling_api_client.v2.alpha.models.schema_dependency import SchemaDependency
from benchling_api_client.v2.alpha.models.secure_text_app_config_item import SecureTextAppConfigItem
from benchling_api_client.v2.alpha.models.secure_text_app_config_item_type import SecureTextAppConfigItemType
from benchling_api_client.v2.alpha.models.text_app_config_item import TextAppConfigItem
from benchling_api_client.v2.alpha.models.text_app_config_item_type import TextAppConfigItemType
from benchling_api_client.v2.alpha.models.workflow_task_schema_dependency import WorkflowTaskSchemaDependency
from benchling_api_client.v2.beta.models.scalar_config_types import ScalarConfigTypes
from benchling_api_client.v2.stable.extensions import UnknownType
from benchling_api_client.v2.stable.types import UNSET

from benchling_sdk.apps.config.dependencies import (
    _supported_config_item,
    BaseDependencies,
    ConfigurationReference,
    DependencyLinkStore,
    StaticConfigProvider,
)
from benchling_sdk.apps.config.scalars import DateTimeScalar, JsonType
from benchling_sdk.apps.helpers.config_helpers import (
    field_definitions_from_dependency,
    options_from_dependency,
    subtype_from_entity_schema_dependency,
    workflow_task_schema_output_from_dependency,
)

ManifestDependencies = Union[
    DropdownDependency,
    EntitySchemaDependency,
    ManifestScalarConfig,
    ResourceDependency,
    SchemaDependency,
    WorkflowTaskSchemaDependency,
    UnknownType,
]

D = TypeVar("D", bound=BaseDependencies)


class MockBenchlingAppConfig:
    """
    Mock App Config.

    A helper class for easily mocking app config in various permutations.

    Easily mock all config items from a manifest model (which can be loaded from
    `benchling_sdk.apps.helpers.manifest_helpers.manifest_from_file()`.
    """

    _config_items = List[AppConfigItem]

    def __init__(self, config_items: List[AppConfigItem]):
        """
        Init Mock Benchling App Config.

        The class can be initialized by providing a list of AppConfigItem, but the recommended
        usage is to mock directly from a manifest, like `MockBenchlingAppConfig.from_manifest()`
        """
        self._config_items = config_items

    @classmethod
    def from_manifest(cls, manifest: BenchlingAppManifest) -> MockBenchlingAppConfig:
        """
        From Manifest.

        Reads a manifest amd mocks out all dependencies.
        """
        config_items = mock_app_config_items_from_manifest(manifest)
        return cls(config_items)

    def to_dependencies(self, target_dependencies: Type[D]) -> D:
        """
        To Dependencies.

        Convenience method for providing mocked app config to a target class extending BaseDependencies.
        """
        link_store = DependencyLinkStore(StaticConfigProvider(self.config_items))
        return target_dependencies.from_store(link_store)

    def with_replacement(self, replacement: ConfigurationReference) -> MockBenchlingAppConfig:
        """
        With Replacement.

        Returns a new MockBenchlingAppConfig with the app config item at the specified path replaced.
        """
        replaced_app_config = replace_mocked_config_item_by_path(
            self.config_items, replacement.path, replacement
        )
        return MockBenchlingAppConfig(replaced_app_config)

    def with_replacements(self, replacements: List[ConfigurationReference]) -> MockBenchlingAppConfig:
        """
        With Replacement.

        Returns a new MockBenchlingAppConfig with the app config item at the specified path replaced.
        """
        replaced_app_config = self.config_items
        for replacement in replacements:
            replaced_app_config = replace_mocked_config_item_by_path(
                replaced_app_config, replacement.path, replacement
            )
        return MockBenchlingAppConfig(replaced_app_config)

    @property
    def config_items(self) -> List[ConfigurationReference]:
        """List the config items in the mock app config, excluding any unknown types."""
        return [_supported_config_item(config_item) for config_item in self._config_items]

    @property
    def config_items_with_unknown(self) -> List[AppConfigItem]:
        """List the config items in the mock app config, including any unknown types."""
        return self._config_items


def mock_app_config_items_from_manifest(manifest: BenchlingAppManifest) -> List[AppConfigItem]:
    """
    Mock Benchling App Config Items.

    This method accepts an app manifest model and creates mocked values for app the app config.

    The concrete mocked out values, such as API Ids and schema names are nonsensical and random,
    but are valid.

    Code should avoid relying on specific values or conventions (such as API prefixes). If
    specific dependency values need to be tested in isolation, the caller can selectively
    override the randomized values with replace_mocked_config_item_by_path().
    """
    root_config_items = [_mock_dependency(dependency) for dependency in manifest.configuration]
    return [config_item for sub_config_items in root_config_items for config_item in sub_config_items]


def replace_mocked_config_item_by_path(
    original_config: List[AppConfigItem], replacement_path: List[str], replacement_item: AppConfigItem
) -> List[AppConfigItem]:
    """Return an updated list of app config items with a specific config item replaced with the provided mock."""
    replaced_config = [config for config in original_config if config.path != replacement_path]
    replaced_config.append(replacement_item)
    return replaced_config


def mock_bool_app_config_item(path: List[str], value: Optional[bool]) -> BooleanAppConfigItem:
    """Mock a bool app config item with a path and specified value."""
    return BooleanAppConfigItem(
        path=path,
        value=value,
        type=BooleanAppConfigItemType.BOOLEAN,
        id=_random_string("aci_"),
    )


def mock_date_app_config_item(path: List[str], value: Optional[date]) -> DateAppConfigItem:
    """Mock a date app config item with a path and specified value."""
    return DateAppConfigItem(
        path=path,
        value=value,
        type=DateAppConfigItemType.DATE,
        id=_random_string("aci_"),
    )


def mock_datetime_app_config_item(path: List[str], value: Optional[datetime]) -> DatetimeAppConfigItem:
    """Mock a datetime app config item with a path and specified value."""
    return DatetimeAppConfigItem(
        path=path,
        value=value.strftime(DateTimeScalar.expected_format()) if isinstance(value, datetime) else value,
        type=DatetimeAppConfigItemType.DATETIME,
        id=_random_string("aci_"),
    )


def mock_float_app_config_item(path: List[str], value: Optional[float]) -> FloatAppConfigItem:
    """Mock a float app config item with a path and specified value."""
    return FloatAppConfigItem(
        path=path,
        value=value,
        type=FloatAppConfigItemType.FLOAT,
        id=_random_string("aci_"),
    )


def mock_int_app_config_item(path: List[str], value: Optional[int]) -> IntegerAppConfigItem:
    """Mock an int app config item with a path and specified value."""
    return IntegerAppConfigItem(
        path=path,
        value=value,
        type=IntegerAppConfigItemType.INTEGER,
        id=_random_string("aci_"),
    )


def mock_json_app_config_item(path: List[str], value: Optional[JsonType]) -> JsonAppConfigItem:
    """Mock an int app config item with a path and specified value."""
    return JsonAppConfigItem(
        path=path,
        value=json.dumps(value) if value is not None else None,
        type=JsonAppConfigItemType.JSON,
        id=_random_string("aci_"),
    )


def mock_secure_text_app_config_item(path: List[str], value: Optional[str]) -> SecureTextAppConfigItem:
    """Mock a secure text app config item with a path and specified value."""
    return SecureTextAppConfigItem(
        path=path,
        value=value,
        type=SecureTextAppConfigItemType.SECURE_TEXT,
        id=_random_string("aci_"),
    )


def mock_text_app_config_item(path: List[str], value: Optional[str]) -> TextAppConfigItem:
    """Mock a text app config item with a path and specified value."""
    return TextAppConfigItem(
        path=path,
        value=value,
        type=TextAppConfigItemType.TEXT,
        id=_random_string("aci_"),
    )


def _mock_dependency(
    dependency: ManifestDependencies,
) -> List[AppConfigItem]:
    """Mock a dependency from its manifest definition."""
    if isinstance(dependency, DropdownDependency):
        linked_resource_id = _random_string("val_")
        config_item = GenericApiIdentifiedAppConfigItem(
            id=_random_string("aci_"),
            path=[dependency.name],
            type=GenericApiIdentifiedAppConfigItemType.DROPDOWN,
            value=_random_string("val_"),
            linked_resource=_mock_linked_resource(linked_resource_id),
        )
        sub_items = [
            _mock_subdependency(subdependency, dependency)
            for subdependency in options_from_dependency(dependency)
        ]
        return [config_item] + sub_items
    elif isinstance(dependency, EntitySchemaDependency):
        linked_resource_id = _random_string("val_")
        subtype = subtype_from_entity_schema_dependency(dependency)
        optional_subtype = subtype if subtype else UNSET
        config_item = EntitySchemaAppConfigItem(
            id=_random_string("aci_"),
            path=[dependency.name],
            type=optional_subtype,
            value=_random_string("val_"),
            linked_resource=_mock_linked_resource(linked_resource_id),
        )
        sub_items = [
            _mock_subdependency(subdependency, dependency)
            for subdependency in field_definitions_from_dependency(dependency)
        ]
        return [config_item] + sub_items
    elif isinstance(dependency, SchemaDependency):
        linked_resource_id = _random_string("val_")
        config_item = GenericApiIdentifiedAppConfigItem(
            id=_random_string("aci_"),
            path=[dependency.name],
            type=GenericApiIdentifiedAppConfigItemType(dependency.type),
            value=_random_string("val_"),
            linked_resource=_mock_linked_resource(linked_resource_id),
        )
        sub_items = [
            _mock_subdependency(subdependency, dependency)
            for subdependency in field_definitions_from_dependency(dependency)
        ]
        return [config_item] + sub_items
    elif isinstance(dependency, WorkflowTaskSchemaDependency):
        linked_resource_id = _random_string("val_")
        config_item = GenericApiIdentifiedAppConfigItem(
            id=_random_string("aci_"),
            path=[dependency.name],
            type=GenericApiIdentifiedAppConfigItemType.WORKFLOW_TASK_SCHEMA,
            value=linked_resource_id,
            linked_resource=_mock_linked_resource(linked_resource_id),
        )
        sub_items = [
            _mock_subdependency(subdependency, dependency)
            for subdependency in field_definitions_from_dependency(dependency)
        ]
        workflow_task_output = workflow_task_schema_output_from_dependency(dependency)
        if workflow_task_output:
            output_fields = field_definitions_from_dependency(workflow_task_output)
            output_items = [
                _mock_workflow_output_subdependency(subdependency, dependency)
                for subdependency in output_fields
            ]
            sub_items += output_items
        return [config_item] + sub_items
    elif isinstance(dependency, ManifestScalarConfig):
        return [_mock_scalar_dependency(dependency)]
    elif isinstance(dependency, UnknownType):
        return UnknownType(value="Unknown")
    else:
        linked_resource_id = _random_string("val_")
        return [
            GenericApiIdentifiedAppConfigItem(
                id=_random_string("aci_"),
                path=[dependency.name],
                type=GenericApiIdentifiedAppConfigItemType(dependency.type),
                value=linked_resource_id,
                linked_resource=_mock_linked_resource(linked_resource_id),
            )
        ]


def _mock_scalar_dependency(dependency: ManifestScalarConfig) -> AppConfigItem:
    if dependency.type == ScalarConfigTypes.BOOLEAN:
        return mock_bool_app_config_item([dependency.name], _mock_scalar_value(dependency.type))
    elif dependency.type == ScalarConfigTypes.DATE:
        return mock_date_app_config_item([dependency.name], _mock_scalar_value(dependency.type))
    elif dependency.type == ScalarConfigTypes.DATETIME:
        return mock_datetime_app_config_item([dependency.name], _mock_scalar_value(dependency.type))
    elif dependency.type == ScalarConfigTypes.FLOAT:
        return mock_float_app_config_item([dependency.name], _mock_scalar_value(dependency.type))
    elif dependency.type == ScalarConfigTypes.INTEGER:
        return mock_int_app_config_item([dependency.name], _mock_scalar_value(dependency.type))
    elif dependency.type == ScalarConfigTypes.JSON:
        # _mock_scalar_value returns str so convert back to JSON
        json_value = json.loads(_mock_scalar_value(dependency.type))
        return mock_json_app_config_item([dependency.name], json_value)
    elif dependency.type == ScalarConfigTypes.SECURE_TEXT:
        return mock_secure_text_app_config_item([dependency.name], _mock_scalar_value(dependency.type))
    else:
        return mock_text_app_config_item([dependency.name], _mock_scalar_value(dependency.type))


def _mock_subdependency(subdependency: BaseManifestConfig, parent_config) -> AppConfigItem:
    if isinstance(parent_config, DropdownDependency):
        linked_resource_id = _random_string("opt_")
        return GenericApiIdentifiedAppConfigItem(
            id=_random_string("aci_"),
            path=[parent_config.name, subdependency.name],
            type=GenericApiIdentifiedAppConfigItemType.DROPDOWN_OPTION,
            value=linked_resource_id,
            linked_resource=_mock_linked_resource(linked_resource_id),
        )
    elif isinstance(parent_config, (EntitySchemaDependency, SchemaDependency, WorkflowTaskSchemaDependency)):
        path = [parent_config.name, subdependency.name]
        linked_resource_id = _random_string("tsf_")
        app_config = FieldAppConfigItem(
            id=_random_string("aci_"),
            path=path,
            type=FieldAppConfigItemType.FIELD,
            value=linked_resource_id,
            linked_resource=_mock_linked_resource(linked_resource_id),
        )
        return app_config


def _mock_workflow_output_subdependency(subdependency: BaseManifestConfig, parent_config) -> AppConfigItem:
    linked_resource_id = _random_string("tsf_")
    app_config = FieldAppConfigItem(
        id=_random_string("aci_"),
        path=[parent_config.name, "output", subdependency.name],
        type=FieldAppConfigItemType.FIELD,
        value=linked_resource_id,
        linked_resource=_mock_linked_resource(linked_resource_id),
    )
    return app_config


def _mock_linked_resource(id: str, name: Optional[str] = None) -> LinkedAppConfigResourceSummary:
    return LinkedAppConfigResourceSummary(id=id, name=name if name else _random_string("Resource Name"))


def _mock_scalar_value(scalar_type: ScalarConfigTypes) -> Optional[str]:
    """Mock a scalar config value from its manifest definition."""
    if scalar_type == scalar_type.BOOLEAN:
        return "true"
    elif scalar_type == scalar_type.DATE:
        return date.today().strftime("%Y-%m-%d")
    elif scalar_type == scalar_type.DATETIME:
        return datetime.now().strftime(DateTimeScalar.expected_format())
    elif scalar_type == scalar_type.FLOAT:
        return str(random.random())
    elif scalar_type == scalar_type.INTEGER:
        return str(random.randint(-1000, 1000))
    elif scalar_type == scalar_type.JSON:
        return json.dumps(
            {_random_string(): [_random_string(), _random_string()], _random_string(): random.random()}
        )
    return _random_string()


def _random_string(prefix: str = "", random_length: int = 20) -> str:
    """Generate a randomized string up to a specified length with an optional prefix."""
    delimited_prefix = f"{prefix}-" if prefix else ""
    return f"{delimited_prefix}{''.join(random.choice(string.ascii_letters) for i in range(random_length))}"
