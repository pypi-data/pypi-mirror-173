# Aserto Directory gRPC client
This is an automatically generated client for interacting with Aserto's
[Directory service](https://docs.aserto.com/docs/overview/directory) using the gRPC protocol.

## Installation
### Using Pip
```sh
pip install aserto-directory
```
### Using Poetry
```sh
poetry add aserto-directory
```
## Usage
```py
import grpc
from aserto.directory.common.v2 import ObjectTypeRequest
from aserto.directory.reader.v2 import ReaderStub

with grpc.secure_channel(target=f"directory.prod.aserto.com:8443") as channel:
    reader = ReaderStub(channel)

    # List all object types in the directory
    response = client.GetObjectTypes(
        GetObjectTypesRequest(),
        metadata=(
            ("authorization", f"basic {ASERTO_DIRECTORY_API_KEY}"),
            ("aserto-tenant-id", ASERTO_TENANT_ID),
        ),
    )

    for object_type in response.results:
        print("Object Type:", object_type.name)
```
