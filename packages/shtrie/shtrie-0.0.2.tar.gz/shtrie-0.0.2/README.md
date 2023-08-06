# shtrie

Single-hash-table Trie

## Usage

```
>>> import shtrie
>>> trie = shtrie.list_to_trie([("CAT", 100), ("RAT", 200), ("DOG", 300)])
>>> from shtrie import PAYLOAD_KEY, ROW_KEY, TERMINAL_KEY
>>> from shtrie import lookup
>>> val0 = lookup(trie, 0, 0, "C")
>>> val0[TERMINAL_KEY]
False
>>> val1 = lookup(trie, val0[ROW_KEY], 1, "A")
>>> val2 = lookup(trie, val1[ROW_KEY], 2, "T")
>>> val2
(0, True, 100)
>>> lookup(trie, 0, 0, "O")
```
