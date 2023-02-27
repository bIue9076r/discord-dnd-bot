import game

game.startGame(0x123,0x0,0x12345)
game.startGame(0x123,0x0,0x12345,"new")
game.startGame(0x123,0x0,0x12375,"new2")

print(game.active_games)
print(game.agame_index)
print("\n")

game.joinGame(0x123,0x0,0x12365,"main","hi dude")
game.joinGame(0x123,0x0,0x12365,"new","hi dude")
game.joinGame(0x123,0x0,0x12365,"new2","hi dude")

print(game.active_games)
print(game.agame_index)
print("\n")

game.quitGame(0x123,0x0,0x12365,"main","hi dude")
game.quitGame(0x123,0x0,0x12365,"new","hi dude")
game.quitGame(0x123,0x0,0x12365,"new2","hi dude")

print(game.active_games)
print(game.agame_index)
print("\n")
