from player import Player
from Champions import Caitlyn
from PlayerActions import level_check

x = Player(name = "test", bench=[Caitlyn(), Caitlyn(), 0, 0, 0, 0, 0, 0, 0])




print(x.fieldstatus())
print(x.status())