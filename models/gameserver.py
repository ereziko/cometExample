from socketio.server import SocketIOServer
from models.gameclasses import PlayerSocket, Tyad
from types import *

class GameServer(SocketIOServer):
	def __init__(self, mysql, *args, **kwargs):
		self.player_counter = 0
		self.configuration = {'number_of_players' : 8}
		self.init_new_game_session(self.configuration)
		self.mysql = mysql
		self.connection = None
		
		super(GameServer, self).__init__(*args, **kwargs)
	
	def get_db_connection(self):
		if self.connection is None:
			self.connection = self.mysql.connect()
		return self.connection	
	
	def init_new_game_session(self, configuration):
		print 'Initalized new game with this configuration:'
		print configuration
		self.players = [PlayerSocket(str(ord('A')+i)) for i in range(configuration.get('number_of_players'))]
		self.tyads = [Tyad() for i in range(configuration.get('number_of_players'))]
		
	def add_player(self, nickname, socket):
		self.player_counter += 1
		for p in self.players:
			if p.is_free:
				p.sit(nickname,socket)
				#unit test
				player_id = self.add_player_to_db(nickname)
				db_nickname = self.get_player_nickname_from_db(player_id)
				assert nickname == db_nickname
				#end test
				p.set_player_id(player_id)
				return p
		#Bad stuff should happen - means the game is full.
	
	def add_player_to_db(self, nickname):
		assert nickname is not None
		connection = self.get_db_connection()
		cursor = connection.cursor()
		cursor.execute("INSERT INTO player (nickname) values (%s); ", nickname)
		cursor.execute("SELECT player_id from player where nickname = %s", nickname)
		player_id = int(cursor.fetchone()[0])
		return player_id
	
	def get_player_nickname_from_db(self, player_id):
		assert player_id is not None
		connection = self.get_db_connection()
		cursor = connection.cursor()
		cursor.execute("SELECT nickname from player where player_id = %s", player_id)
		nickname = str(cursor.fetchone()[0])
		return nickname
	
	
	def remove_player(self, nickname, socket):
		pass
	
	def get_number_of_players(self):
		counter = 0
		for p in self.players:
			if p.is_free is False:
				counter += 1
		return counter
	
	def game_has_free_position(self):
		for p in self.players:
			if p.is_free:
				return True
		return False
		
	def get_avaiable_game_tyad(self, player):
		for t in self.tyads:
			#someone is waiting and it's legal
			if t.is_a_waiting() and self.is_legal_tyad(self.configuration):
				return t
		#if we get here it means either no a waiting or 
		#for all a which is waiting it's not legal to play with this player
		for t in self.tyads:
			if t.is_empty():
				return t
		#Bad stuff 
	
	def is_legal_tyad(self, configuration):
		return True
	
	def insert_message_to_db(self, msg, from_player_id, to_player_id):
		assert msg is not None 
		assert from_player_id is not None and type(from_player_id) is IntType
		assert to_player_id is not None and type(to_player_id) is IntType
		print ("INSERT INTO message (message, to_player_id, from_player_id) values (%s, %d, %d);", (msg, to_player_id, from_player_id))
		connection = self.get_db_connection()
		cursor = connection.cursor()
		cursor.execute("INSERT INTO message (message, to_player_id, from_player_id) values (%s, %s, %s);", (msg, to_player_id, from_player_id)) 
		cursor.execute("SELECT message_id from message where message = %s and to_player_id = %s and from_player_id = %s", (msg, to_player_id, from_player_id))
		msg_id = int(cursor.fetchone()[0])
		print msg_id
		return msg_id
	
	def __del__(self):
		self.connection.close()
				