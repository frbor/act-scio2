"""Copyright 2020 mnemonic AS <opensource@mnemonic.no>

Permission to use, copy, modify, and/or distribute this software for
any purpose with or without fee is hereby granted, provided that the
above copyright notice and this permission notice appear in all
copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL
DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR
PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.

---
Elasticsearch utilities for scio
"""

from typing import Iterator, Optional, Text, Tuple, List, Dict, Any

from elasticsearch import Elasticsearch


def es_client(
    host: Text,
    port: int = 9200,
    url_prefix: Optional[Text] = None,
    username: Optional[Text] = None,
    password: Optional[Text] = None,
    timeout: int = 180,
) -> Elasticsearch:
    """Elasticsearch client"""

    connection = {"host": host, "port": port, "scheme": "http"}

    if url_prefix:
        connection["url_prefx"] = url_prefix

    if username or password:
        http_auth: Optional[Tuple[Optional[Text], Optional[Text]]] = (
            username,
            password,
        )
    else:
        http_auth = None

    return Elasticsearch([connection], timeout=timeout, http_auth=http_auth)


def __body(
    start: Optional[Text] = None,
    end: Optional[Text] = None,
    query_string: Optional[Text] = None,
    size: int = 10000,
) -> Dict[str, Any]:
    body: Dict[str, Any] = {
        "size": size,
        "query": {"bool": {"must": []}},
    }

    if start or end:
        body["query"]["bool"]["must"].append(
            {
                "range": {
                    "Analyzed-Date": {
                        "gte": start,
                        "lte": end,
                    }
                }
            }
        )

    # Filter on query_string
    if query_string:
        body["query"]["bool"]["must"].append(
            {
                "query_string": {
                    "query": query_string,
                    "default_field": "_",
                }
            }
        )

    return body


def search(
    client: Elasticsearch,
    start: Optional[Text] = None,
    end: Optional[Text] = None,
    index: Text = "scio2",
    query_string: Optional[Text] = None,
    size=10000,
) -> Iterator[Dict[str, Any]]:
    """Aggregation"""

    body = __body(start, end, query_string, size)

    for hit in client.search(index=index, body=body)["hits"]["hits"]:
        yield hit["_source"]


def aggregation(
    client: Elasticsearch,
    term: Text,
    start: Optional[Text] = None,
    end: Optional[Text] = None,
    missing: bool = False,
    index: Text = "scio2",
    query_string: Optional[Text] = None,
) -> Iterator[Tuple[Text, int]]:
    """Aggregation"""

    body = __body(start, end, query_string, 0)

    body["aggs"] = {
        term: {
            "terms": {"field": term},
        }
    }

    response = client.search(index=index, body=body)

    for aggr in response["aggregations"][term]["buckets"]:
        yield aggr["key"], aggr["doc_count"]
