class SessionMixin(object):
	def __init__(self, *args, **kwargs):
		super(SessionMixin, self).__init__(*args, **kwargs)
		if 'rooms' not in self.session:
			self.session['rooms'] = set()  # a set of simple strings
	
	def join(self, room):
		"""Lets a user join a room on a specific Namespace."""
		self.session['rooms'].add(self._get_room_name(room))
	
	def leave(self, room):
		"""Lets a user leave a room on a specific Namespace."""
		self.session['rooms'].remove(self._get_room_name(room))
	
	def _get_room_name(self, room):
		return self.ns_name + '_' + room
	
	def emit_to_room(self, room, event, *args):
		#self.emit_to_room('main_room', 'msg_to_room', self.socket.session['nickname'], msg)
		"""This is sent to all in the room (in this particular Namespace)"""
		pkt = dict(type="event",
				name=event,
				args=args,
				endpoint=self.ns_name)
		room_name = self._get_room_name(room)
		for sessid, socket in self.socket.server.sockets.iteritems():
			print (str(sessid) + ':' + str(socket))
			if 'rooms' not in socket.session:
				continue
			if room_name in socket.session['rooms'] and self.socket != socket:
				socket.send_packet(pkt)
	
	def send_message_to_other_player(self, event, player, *args):
		"""This is sent to the other player in the tyad"""
		pkt = dict(type="event",
					name=event,
					args=args,
					endpoint=self.ns_name)
		tyad = player.get_player_tyad()
		print str(tyad)
		if tyad is None:
			#Bad stuff - this player has no tyad
			pass
		other_player = tyad.get_other_player(player)
		print str(other_player)
		if other_player is None:
			#Bad stuff - there is no other player in the tyad
			pass
		socket = other_player.get_socket()
		socket.send_packet(pkt)
		
	
class GameBroadcastMixin(object):
	"""Mix in this class with your Namespace to have a broadcast event method.
	Use it like this:
	class MyNamespace(BaseNamespace, BroadcastMixin):
		def on_chatmsg(self, event):
			self.broadcast_event('chatmsg', event)
	"""
	
	def broadcast_event(self, event, *args):
		"""
		This is sent to all in the sockets in this particular Namespace,
		including itself.
		"""
		pkt = dict(type="event",
					name=event,
					args=args,
					endpoint=self.ns_name)
	
		for sessid, socket in self.socket.server.sockets.iteritems():
			socket.send_packet(pkt)
	
	def broadcast_event_just_me(self, event, *args):
		"""
		This is sent only to the socket itself
		"""
		pkt = dict(type="event",
					name=event,
					args=args,
					endpoint=self.ns_name)
	
		self.socket.send_packet(pkt)
		
	def broadcast_event_not_me(self, event, *args):
		"""
		This is sent to all in the sockets in this particular Namespace,
		except itself.
		"""
		pkt = dict(type="event",
					name=event,
					args=args,
					endpoint=self.ns_name)
	
		for sessid, socket in self.socket.server.sockets.iteritems():
			if socket is not self.socket:
				socket.send_packet(pkt)
	
	