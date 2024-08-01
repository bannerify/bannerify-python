<!-- Start SDK Example Usage [usage] -->
```python
# Synchronous Example
from bannerify import Bannerify
import os

s = Bannerify(
    bearer_auth=os.getenv("BEARER_AUTH", ""),
)


res = s.get_v1_liveness()

if res is not None:
    # handle response
    pass
```

</br>

The same SDK client can also be used to make asychronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
from bannerify import Bannerify
import os

async def main():
    s = Bannerify(
        bearer_auth=os.getenv("BEARER_AUTH", ""),
    )
    res = await s.get_v1_liveness_async()
    if res is not None:
        # handle response
        pass

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->