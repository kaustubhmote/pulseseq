from bruker.api.topspin import Topspin
from bruker.data import nmr
import inspect
import bruker
from base import dialog

# print(inspect.getsource(dialog))

top = Topspin()
dp = top.getDataProvider()
run = top.executeCommand

import sys


print(sys.argv)


out = dialog("Test", "this is a test", labels=["Label1"], types=["e"], values=["1"], comments=["test"])

# print(out)

# print("Topspin installation :" + top.getInstallationDirectory())
# print("Topspin version :" + top.getVersion())
# print("Current dataset :" + str(dp.getCurrentDatasetIdentifier()))

# print("#---bruker.api.topspin methods\n")
# for i in dir(bruker.api.topspin):
#     print(i, end="\n")



# print("#---top methods\n")
# for i in dir(top):
#     print(i, end="\n")


# print("#---dataprovider methods\n")
# for i in dir(dp):
#     print(i, end="\n")


# print("\n")
# print("#---nmr methods\n")

# for i in dir(nmr):
#     print(i, end="\n")
