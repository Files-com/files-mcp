from __future__ import annotations

from typing import Callable
from typing import MutableMapping


SdkRequestMutator = Callable[
    [
        str,
        str,
        str | None,
        str | None,
        str | None,
        MutableMapping[str, str],
        dict | None,
    ],
    MutableMapping[str, str] | None,
]

_sdk_request_mutator: SdkRequestMutator | None = None


def set_sdk_request_mutator(mutator: SdkRequestMutator | None) -> None:
    global _sdk_request_mutator
    _sdk_request_mutator = mutator


def apply_sdk_request_mutator(
    method: str,
    path: str,
    api_key: str | None,
    session_id: str | None,
    language: str | None,
    headers: MutableMapping[str, str],
    params: dict | None,
) -> MutableMapping[str, str]:
    if _sdk_request_mutator is None:
        return headers

    mutated_headers = _sdk_request_mutator(
        method,
        path,
        api_key,
        session_id,
        language,
        headers,
        params,
    )
    if mutated_headers is None:
        return headers
    return mutated_headers
