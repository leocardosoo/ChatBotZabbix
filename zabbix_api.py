# zabbix_api.py
import requests
from typing import List, Optional, Dict
from config import ZABBIX_URL, ZABBIX_TOKEN

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {ZABBIX_TOKEN}"
}


def _call(method: str, params: dict):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "auth": None,  # quando usamos token, auth vai no header
        "id": 1
    }
    resp = requests.post(ZABBIX_URL, json=payload, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    if "error" in data:
        raise Exception(f"Zabbix API error: {data['error']}")
    return data.get("result")


def get_problemas(severity_min: Optional[int] = None) -> List[dict]:
    """
    Retorna triggers em PROBLEM (value=1).
    severity_min: 0..5 (0=Not classified, 5=Disaster). Se passado, filtra severidade >= severity_min.
    """
    params = {
        "output": ["triggerid", "description", "priority", "lastchange", "value"],
        "filter": {"value": 1},
        "expandDescription": True,
        "selectHosts": ["host"],
        "sortfield": "lastchange",
        "sortorder": "DESC",
        "limit": 100
    }
    res = _call("trigger.get", params)
    if severity_min is not None:
        res = [t for t in res if int(t.get("priority", 0)) >= int(severity_min)]
    return res


def get_hosts(search: Optional[str] = None) -> List[dict]:
    params = {"output": ["hostid", "host", "name"], "sortfield": "host"}
    if search:
        params["search"] = {"host": search}
        params["searchWildcardsEnabled"] = True
    return _call("host.get", params)


def get_host_by_name(hostname: str) -> Optional[dict]:
    res = _call("host.get", {"filter": {"host": [hostname]}, "output": ["hostid", "host", "name"], "selectInterfaces": ["ip"]})
    return res[0] if res else None


def get_items_by_hostid(hostid: str) -> List[dict]:
    return _call("item.get", {"hostids": hostid, "output": ["itemid", "key_", "name", "lastvalue", "delay"]})


def get_groups() -> List[dict]:
    return _call("hostgroup.get", {"output": ["groupid", "name"]})


def get_item_by_key(hostid: str, key: str) -> Optional[dict]:
    items = _call("item.get", {"hostids": hostid, "search": {"key_": key}, "output": ["itemid", "key_", "name", "lastvalue"]})
    return items[0] if items else None


def get_history(itemid: str, limit: int = 50) -> List[dict]:
    # history.get aceita diferentes types; we'll ask for the generic history and hope Zabbix returns data for numeric items
    params = {
        "output": "extend",
        "history": 0,  # 0 = numeric float, 3 = numeric unsigned; if empty for some items, result will be []
        "itemids": itemid,
        "sortfield": "clock",
        "sortorder": "ASC",
        "limit": limit
    }
    # Try numeric float (0) then unsigned int (3) if empty
    res = _call("history.get", params)
    if res:
        return res
    params["history"] = 3
    return _call("history.get", params)
