# %%
from datetime import datetime
from re import X
from typing import List

from sqlalchemy.sql.expression import false

# %%
today = datetime.today()
# %%
print(today)

# %%
print(today.date())
# %%
list1 = [1, 2, 3, 4, 5, 6]
flist = filter(lambda x: x % 2 == 0, list1)
mflist = map(lambda x: x + 1, flist)
fflist2 = filter(fflist, list1)
# %%
list(mflist)

# %%


def intplusone(x: int) -> int:
    return x + 1
# %%


def fflist(x: int) -> bool:
    return x % 2 == 0


# %%


def ffllfilter(x: List[int]) -> bool:
    print(x)
    return len(x)<3

# %%
llist1 = [[1, 2], [3, 4], [5, 6, 7], [8, 9]]
flllist1 = filter(ffllfilter, llist1)
list(flllist1)
# %%

# %%
