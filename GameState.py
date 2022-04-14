from player import Player
from PlayerInput import playerinput
from PlayerActions import buyxp
from PlayerActions import champselect
from PlayerActions import level_check
from Items import itemcombine
from Shop import reroll
from Champions import Caitlyn, BlitzCrank, GangPlank, Alistar, Silco
from Items import Item

player1 = Player("player1", gold= 10000)
player2 = Player("player2")
player3 = Player("player3")
player4 = Player("player4")
player5 = Player("player5")
player6 = Player("player6")
player7 = Player("player7")
player8 = Player("player8")

players = [player1, player2, player3, player4, player5, player6, player7, player8]

pool = {1: [Caitlyn() for i in range(29)],
2: [BlitzCrank() for i in range(22)],
3: [GangPlank() for i in range(18)],
4: [Alistar() for i in range(12)],
5: [Silco() for i in range(10)]}

def gamestate(players, pool):
    new_action = playerinput()
    currentplayer = players[new_action[0]-1]
    currentaction = new_action[1]


    if currentaction == 1:
        # Buy a champ
        print(f"Shop is:\n{currentplayer.shopdisplay()}")
        while True:
            try:
                champtobuy = int(input("Which champion would you like to buy?\n"))
                if champtobuy in range(1, 6):
                    break
                else:
                    print("Please select a number between 1 and 5")

            except ValueError:
                print("Please type a number")

        level2 = False

        if currentplayer.shop[champtobuy-1] == 0:
            print("That slot is empty.")
            return

        elif currentplayer.gold < currentplayer.shop[champtobuy-1].cost:
            print("Sorry, you don't have enough gold!")
            return

        elif level_check(currentplayer, currentplayer.shop[champtobuy - 1], 1) != False:
            locations = level_check(currentplayer, currentplayer.shop[champtobuy - 1], 1)
            for loc in locations:
                if loc[0] == "bench":
                    currentplayer.bench[loc[1]] = 0
                if loc[0] == "board":
                    currentplayer.board[loc[1]][loc[2]] = 0
            level2 = True


        elif 0 not in currentplayer.bench:
            print("Sorry, no room on the bench.")
            return

        for i in range(9):
            if currentplayer.bench[i] == 0:
                currentplayer.bench[i] = currentplayer.shop[champtobuy-1]
                champbought = currentplayer.shop[champtobuy-1]
                currentplayer.shop[champtobuy-1] = 0
                if level2 == True:
                    currentplayer.bench[i].level = 2
                    if level_check(currentplayer, champbought, 2) != False:
                        champ_locations2 = level_check(currentplayer, champbought, 2)
                        for loc in champ_locations2:
                            if loc[0] == "bench":
                                currentplayer.bench[loc[1]] = 0
                            if loc[0] == "board":
                                currentplayer.board[loc[1]][loc[2]] = 0
                        currentplayer.bench[i].level = 3


                return







    if currentaction == 2:
        #Reroll
        if currentplayer.gold>1:
            currentplayer.shop = reroll(currentplayer, pool)
            print(f"Player {new_action[0]} has rerolled, new shop is {currentplayer.shopdisplay()}")
            currentplayer.gold += -1
        else:
            print("You don't have enough gold to reroll")

    if currentaction == 3:
        #sell a champ
        champtosell = champselect(currentplayer)

        if champtosell[0] == "bench":
            try:
                currentplayer.gold += currentplayer.bench[champtosell[1]].cost
                pool[currentplayer.bench[champtosell[1]].tier].append(currentplayer.bench[champtosell[1]] ** currentplayer.bench[champtosell[1]].tier)
                print(currentplayer.name + " has sold " + currentplayer.bench[champtosell[1].name])
                currentplayer.bench[champtosell[1]] = 0
            except AttributeError:
                print("There's no champion there, action cancelled.")

        if champtosell[0] == "field":
            try:
                currentplayer.gold += currentplayer.board[champtosell[1][0]][champtosell[1][1]].cost
                pool[currentplayer.board[champtosell[1][0]][champtosell[1][1]].tier].append(currentplayer.board[champtosell[1][0]][champtosell[1][1]] ** currentplayer.board[champtosell[1][0]][champtosell[1][1]].tier)
                print(currentplayer.name + " has sold " + currentplayer.board[champtosell[1][0]][champtosell[1][1]].name)
                currentplayer.board[champtosell[1][0]][champtosell[1][1]] = 0
            except AttributeError:
                print("There's no champion there, action cancelled.")
        # Sell a champ



    if currentaction == 4:
        # buying XP, 4 XP = 4 gold
        buyxp(currentplayer)

    if currentaction == 5:
        # Move a champ
        print(currentplayer.name+", select a champion to move")
        boardpointer = champselect(currentplayer)
        if boardpointer == "cancel":
            print("action cancelled")
            return

# This part of the code figures out the champions and spaces to be swapped.

        if boardpointer[0] == "bench":
            champtomove = currentplayer.bench[boardpointer[1]]

        if boardpointer[0] == "board":
            champtomove = currentplayer.board[boardpointer[1][0]][boardpointer[1][1]]

        if champtomove == 0:
            print("This space is empty, please try again")
            return

        print(currentplayer.name+", select a space to move to")
        targetpointer = champselect(currentplayer)
        if targetpointer == "cancel":
            print("action cancelled")
            return

        if targetpointer[0] == "bench":
            occupiedspace = currentplayer.bench[targetpointer[1]]

        if targetpointer[0] == "board":
            occupiedspace = currentplayer.board[targetpointer[1][0]][targetpointer[1][1]]

# This part of the code does the actual swapping

        if boardpointer[0] == "bench" and targetpointer[0] == "bench":
            currentplayer.bench[boardpointer[1]] = occupiedspace
            currentplayer.bench[targetpointer[1]] = champtomove

        elif boardpointer[0] == "bench" and targetpointer[0] == "board":
            currentplayer.bench[boardpointer[1]] = occupiedspace
            currentplayer.board[targetpointer[1][0]][targetpointer[1][1]] = champtomove

        elif boardpointer[0] == "board" and targetpointer[0] == "bench":
            currentplayer.board[boardpointer[1][0]][boardpointer[1][1]] = occupiedspace
            currentplayer.bench[targetpointer[1]] = champtomove

        elif boardpointer[0] == "board" and targetpointer[0] == "bench":
            currentplayer.board[boardpointer[1][0]][boardpointer[1][1]] = occupiedspace
            currentplayer.board[targetpointer[1][0]][targetpointer[1][1]] = champtomove


    if currentaction == 6:
    # Put an item on a champ, item cap is 10

        print(f"Your items:\n{currentplayer.items}")

        while True:
            itemchoice = input("select an item\n")
            if itemchoice.lower() == "cancel":
                print("Action canceled")
                return
            else:
                try:
                    if currentplayer.items[int(itemchoice)] != 0:
                        break
                    else:
                        print("Please enter a slot that contains an item")
                except ValueError:
                    print("Oops, please enter a number")

        print("Select a champion to give this item to")
        champtogiveitem = champselect(currentplayer)
        if champtogiveitem[0] == "bench":
            for item in currentplayer.bench[champtogiveitem[1]]:
                if item == 0:
                    item = currentplayer.items[itemchoice]
                    print(f"{currentplayer.bench[champtogiveitem[1]]} has been given {currentplayer.items[itemchoice]}")
                    currentplayer.items[itemchoice] = 0
                    return


                if item.tier == 1:
                    item = itemcombine(item, currentplayer.items[itemchoice])
                    print(f"{currentplayer.bench[champtogiveitem[1]]} has been given {currentplayer.items[itemchoice]} to craft {item}")
                    currentplayer.items[itemchoice] = 0
                    return
            print("This Champion has a full inventory")
            return

        if champtogiveitem[0] == "board":
            for item in currentplayer.board[champtogiveitem[1][0]][champtogiveitem[1][1]]:
                if item == 0:
                    item = currentplayer.items[itemchoice]
                    print(f"{currentplayer.board[champtogiveitem[1][0]][champtogiveitem[1][1]]} has been given {currentplayer.items[itemchoice]}")
                    currentplayer.items[itemchoice] = 0
                    return

                if item.tier == 1:
                    item = itemcombine(item, currentplayer.items[itemchoice])
                    print(
                        f"{currentplayer.board[champtogiveitem[1][0]][champtogiveitem[1][1]]} has been given {currentplayer.items[itemchoice]} to craft {item}")
                    currentplayer.items[itemchoice] = 0
                    return
            print("This Champion has a full inventory")

    if currentaction == 7:
        print(currentplayer.status())









while True:
    gamestate(players, pool)