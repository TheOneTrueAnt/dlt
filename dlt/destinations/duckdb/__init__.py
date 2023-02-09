from typing import Type

from dlt.common.schema.schema import Schema
from dlt.common.configuration import with_config
from dlt.common.configuration.accessors import config
from dlt.common.data_writers.escape import escape_postgres_identifier, escape_duckdb_literal
from dlt.common.destination import DestinationCapabilitiesContext, JobClientBase, DestinationClientConfiguration

from dlt.destinations.duckdb.configuration import DuckDbClientConfiguration


@with_config(spec=DuckDbClientConfiguration, namespaces=("destination", "duckdb",))
def _configure(config: DuckDbClientConfiguration = config.value) -> DuckDbClientConfiguration:
    return config


def capabilities() -> DestinationCapabilitiesContext:
    caps = DestinationCapabilitiesContext()
    caps.preferred_loader_file_format = "insert_values"
    caps.supported_loader_file_formats = ["insert_values"]
    caps.escape_identifier = escape_postgres_identifier
    caps.escape_literal = escape_duckdb_literal
    caps.max_identifier_length = 65536
    caps.max_column_identifier_length = 65536
    caps.max_query_length = 32 * 1024 * 1024
    caps.is_max_query_length_in_bytes = True
    caps.max_text_data_type_length = 1024 * 1024 * 1024
    caps.is_max_text_data_type_length_in_bytes = True
    caps.supports_ddl_transactions = True

    return caps


def client(schema: Schema, initial_config: DestinationClientConfiguration = config.value) -> JobClientBase:
    # import client when creating instance so capabilities and config specs can be accessed without dependencies installed
    from dlt.destinations.duckdb.duck import DuckDbClient

    return DuckDbClient(schema, _configure(initial_config))  # type: ignore


def spec() -> Type[DestinationClientConfiguration]:
    return DuckDbClientConfiguration