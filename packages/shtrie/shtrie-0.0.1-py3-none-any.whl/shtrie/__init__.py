"""
Single hash table trie
"""

from typing import Any, Tuple, Dict


TabKey = Tuple[int, int, Any]
TabVal = Tuple[int, bool, Any]
Trie = Dict[TabKey, TabVal]
Member = Any
MemberWithPayload = Tuple[Member, Any]
ROW_KEY = 0
TERMINAL_KEY = 1
PAYLOAD_KEY = 2


def _first(i: MemberWithPayload) -> Member:
    return i[0]


def list_to_trie(members_with_payload: list[MemberWithPayload]) -> Trie:
    """Construct a trie from sorted members with payload."""
    trie: Trie = {}
    if members_with_payload is None or len(members_with_payload) == 0:
        return trie
    sorted_members_with_payload = sorted(members_with_payload, key=_first)
    for i, (members, payload) in enumerate(sorted_members_with_payload):
        row_no = 0
        for j, member in enumerate(members):
            is_terminal = len(members) == j + 1
            member = members[j]
            key: TabKey = (row_no, j, member)
            if key in trie:
                row_no = trie[key][0]
            else:
                val = (i, is_terminal, payload if is_terminal else None)
                trie[key] = val
                row_no = i
    return trie


def lookup(trie: Trie,
           i: int,
           offset: int,
           member_part: Any) -> None | TabVal:
    """Lookup is done by searching an element of members in the tree."""
    key = (i, offset, member_part)
    if key not in trie:
        return None
    return trie[key]
