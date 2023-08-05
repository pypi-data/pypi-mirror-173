# ashe

✨ `ashe` is a super extension of Python.

## 1 Feature

1. System

   - size

2. Dict

   - merge
   - remove

3. List

   - reverse

4. String

   - find

5. File

   - read
   - write

6. Date

   - today
   - yesterday
   - get_interval_days

## 2 Getting Started

### installation

```shell
pip install ashe -U
```

### usage

```Python
from ashe import *

# get size
n = 1
print(size(n))
# 28

# reverse the list
l = [1, 2, 3]
print(reverse(l))
# [3, 2, 1]

# remove key and value from dict
d = {"a": 1, "b": 2}
print(remove("a", d))
# {'b': 2}

# get today and yesterday
print(today())
# 2022-10-23
print(yesterday())
# 2022-10-22
print(get_interval_days(interval=3))
# ["2022-10-21", "2022-10-22", "2022-10-23"]
```

## 3 Consistency

\- Why `reverse(list)` not `list.reverse()`?

\- Because `len(list)` not `list.len()`.

> I find built-in method named `reversed` 🤦‍.

## 4 License

[![](https://award.dovolopor.com?lt=License&rt=MIT&rbc=green)](./LICENSE)
