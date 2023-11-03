# Generic single-database configuration.

## Generating a migration for a new object in TDS

In order to generate a migration to add a new TDS object to the database and elastic search, a few steps must be followed. 

First, add your new object type into `tds/db/enums.py`. The object needs to be added in a few places as follows:

- Add it under `class ResourceType(str, Enum):` as `foo = "foo"`

If provenance is needed:

- Add it under `class ProvenanceType(str,Enum):` as `Foo = "Foo"`

Next, if you are establishing provenance for the object, add entries in a few more places:

Add a `ProvenanceType` into `tds/schema/provenance.py`. This should be added to the `provenance_type_to_abbr` as `ProvenanceType.Foo: "<first two letters of object name>"`