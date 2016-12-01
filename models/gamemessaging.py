from models.gamemixins import SessionMixin, GameBroadcastMixin
from socketio.namespace import BaseNamespace

# The socket.io namespace
class GameNamespace(BaseNamespace, SessionMixin, GameBroadcastMixin):
	
	def on_register(self, nickname):
		print 'On nickname with %' , nickname
		if self.socket.server.game_has_free_position():
			self.player = self.socket.server.add_player(nickname,self.socket)
			self.player.set_socket(self.socket)
			self.socket.session['symbol'] = self.player.get_symbol()
			tyad = self.socket.server.get_avaiable_game_tyad(self.player)
			if tyad.is_empty():
				tyad.set_player_a(self.player)
				self.broadcast_event_just_me('announcement', 'Your player symbol is %s. Waiting for another player...' % self.socket.session['symbol'])
				
			elif tyad.is_a_waiting():
				tyad.set_player_b(self.player)
				self.broadcast_event_just_me('announcement', 'Your player symbol is %s. You are playing with %s' % (self.socket.session['symbol'], tyad.get_player_a().get_symbol() ))
			else:
				#Bad stuff - no open tyads even though there is a free position
				pass
			
		else:
			#Bad stuff - no free player positions
			pass
		
		print 'Current number of players is %d' % self.socket.server.get_number_of_players()

	def on_user_message(self, msg):
		self.send_message_to_other_player('msg_to_room', self.player, msg)
		from_player = self.player
		assert from_player is not None and from_player.get_player_id() is not None
		from_player_tyad = from_player.get_player_tyad()
		assert from_player_tyad is not None
		to_player = from_player_tyad.get_other_player(from_player)
		assert to_player is not None and to_player.get_player_id() is not None
		msg_id = self.socket.server.insert_message_to_db(msg, from_player.get_player_id(), to_player.get_player_id())
		assert msg_id is not None
		#msg = self.socket.server.get_message_from_db(msg_id, from_player, to_player)
		#self.emit_to_room('main_room', 'msg_to_room', self.socket.session['nickname'], msg)

	def recv_message(self, message):
		print "PING!!!", message
