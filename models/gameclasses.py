class Tester():
	def __init__(self, first_name, last_name, email, id, age, gender='M'):
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.id = id
		self.age = age
		
class PlayerSocket():
	def __init__(self, symbol):
		self.is_free = True
		self.symbol = chr(int(symbol))
	
	def sit(self, first_name,socket):
		self.is_free = False
		self.first_name = first_name
		self.socket = socket
	
	def stand(self):
		self.is_free = True
		self.first_name = None
	
	def set_socket(self, socket):
		self.socket = socket
	
	def get_socket(self):
		return self.socket 
	
	def set_tester(self, tester):
		self.tester = tester
		
	def __str__(self):
		return 'Position %c - %s' % (self.symbol, self.first_name)
		
	def get_symbol(self):
		return self.symbol
		
	def set_player_tyad(self, tyad):
		self.tyad = tyad
		
	def get_player_tyad(self):
		return self.tyad
		
	def clear_player_tyad(self):
		self.set_player_tyad(None)
		
	def set_player_id(self, player_id):
		self.player_id = int(player_id)
		
	def get_player_id(self):
		return int(self.player_id)

class Tyad():
	def __init__(self):	
		self.player_a = None
		self.player_b = None
		self.player_a_turn = True
		self.is_free = True
	
	def set_player_a(self, player):
		self.player_a = player
		self.player_a.set_player_tyad(self)
		
	def get_player_a(self):
		return self.player_a
		
	def get_player_b(self):
		return self.player_b
	
	def set_player_b(self, player):
		self.player_b = player
		self.player_b.set_player_tyad(self)
	
	def clear_player_a(self):
		self.player_a.clear_player_tyad()
		self.player_a = None
	
	def clear_player_b(self):
		self.player_b.clear_player_tyad()
		self.player_b = None
	
	def change_turns(self):
		self.player_a_turn = False if self.player_a_turn else True
		
	def is_empty(self):
		return self.player_a is None and self.player_b is None
	
	def is_a_waiting(self):
		return self.player_a is not None and self.player_b is None
		
	def get_other_player(self, player):
		if player.get_symbol() == self.get_player_a().get_symbol():
			return self.get_player_b()
		else:
			return self.get_player_a()
			
	def __str__(self):
		return "tyad (player a, player b) : (%s, %s)" % (self.get_player_a().get_symbol(), 
											self.get_player_b().get_symbol())

class Network():
	def __init__(self, number_of_players, network, game_version, with_replacment):
		self.number_of_players = number_of_players
		self.players = [Player(str('A'+i)) for i in range(number_of_players)]
		self.tyads = [Tyad() for i in range(number_of_players/2)]
		self.network = network
		self.game_version = game_version
		self.with_replacment = with_replacment
		
	def get_players(self):
		return self.players
	

class Item():
	pass
	
class MicroGame():
	pass
	
class Round():
	pass
	
class Session():
	pass