from .constants import API_ROOT_URL

from typing import Any, Optional

import requests


def query_api(
    URI: str, query_params: Optional[dict[str, Any]] = None, *, paging: bool = True
) -> dict[str, Any]:
    def query_endpoint(
        url: str, params: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        r = requests.get(url, params=params)
        print(r.url)
        endpoint_data: dict[str, Any] = r.json()

        if "Paging" in endpoint_data and "Next" in endpoint_data["Paging"] and paging:
            paging_url: str = endpoint_data["Paging"]["Next"]
            return endpoint_data["Items"] + query_endpoint(paging_url)
        else:
            return endpoint_data["Items"]

    api_url: str = f"{API_ROOT_URL}{URI}"
    return query_endpoint(api_url, query_params)
