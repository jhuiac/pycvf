import time
import irclib
import ircbot

# Connection information
network = 'irc.freenode.net'
port = 6667
channels = [ '#irclib', '#paris', '#tokyo', '#linux' ] 
nick = 'PyCVFTest'
name = 'PyCVFBOT'

# Create a dictionary to store statistics in
statistics = {}

# Create our bot class
class StatBot ( ircbot.SingleServerIRCBot ):
   # Join the channel when welcomed
   def on_anything(self, connection, event):
       print "on anything"
       print event.source()
       print event.target()
       print event.arguments()
       print dir(event)
   def on_welcome ( self, connection, event ):
      connection.add_global_handler("all_events",self.on_anything)
      print event
      self.channels=connection.list()
      print self.channels
      #for channel in channels:
      #  print "joining ",channel
      #  connection.join ( channel )
      #  connection.server.names(channel)
   # React to channel messages
   def on_pubmsg ( self, connection, event ):
      source = event.source().split ( '!' ) [ 0 ]
      # A regular message has been sent to us
      print event
      print time.time()
      print event.source()
      print event.target()
      print event.arguments()

# Create the bot
bot = StatBot ( [( network, port )], nick, name )
bot.start()


#def listen_to_server(ircserver,port=6667,nickname="pycvfboat",rooms)
#   irc = irclib.IRC()
#   server = irc.server()
#   server.connect(ircserver,port, nickname)
#   for room in rooms:
#      irc.server.join(room)
          
