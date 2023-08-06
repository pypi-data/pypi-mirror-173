from typing import Dict
from typing import List

from pydantic.dataclasses import dataclass

from hc_pyconsul.lib.consul import ConsulAPI
from hc_pyconsul.lib.tracing import tracing


@dataclass
class ConsulCatalog(ConsulAPI):

    # pylint: disable=invalid-name
    @tracing('List Services')
    def list_services(self, dc: str = None, node_meta: List[str] = None, namespace: str = None) -> Dict[str, List[str]]:
        """
        Link to official docs:
            https://developer.hashicorp.com/consul/api-docs/catalog#list-services

        Parameters
        ----------
        dc: str = None
            Specifies the datacenter to query.
            This will default to the datacenter of the agent being queried.
        node_meta: List[str] = None
            Specifies a desired node metadata key/value in the form of key:value.
            This parameter can be specified multiple times,
            and filters the results to nodes with the specified key/value pairs.
        namespace: str = None
            Enterprise Only
            Specifies the namespace of the services you lookup.

        Returns
        -------
        services: Dict[str, List[str]]

        """
        params = {}
        if dc:
            params.update({
                'dc': dc
            })

        if node_meta:
            params.update({
                'node-meta': ','.join(meta_item for meta_item in node_meta)
            })

        if namespace:
            params.update({
                'ns': namespace
            })

        results = self.call_api(endpoint='/catalog/services', verb='GET', params=params)

        return results
