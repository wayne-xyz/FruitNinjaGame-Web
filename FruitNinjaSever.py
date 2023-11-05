import tornado.ioloop
import tornado.web
import tornado.websocket

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    connections = set()

    def check_origin(self, origin):
        return True
    
    # https://stackoverflow.com/questions/24851207/tornado-403-get-warning-when-opening-websocket
    
    def open(self):
        print("WebSocket connection opened")
        WebSocketHandler.connections.add(self)

    def on_message(self, message):
        print(f"Received message: {message}")
        # Forward the message to all connected clients (except the sender)
        for connection in WebSocketHandler.connections:
            if connection != self:
                connection.write_message(f"Forwarded message: {message}")

    def on_close(self):
        print("WebSocket connection closed")
        WebSocketHandler.connections.remove(self)
 
def make_app():
    return tornado.web.Application([
        (r"/websocket", WebSocketHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("WebSocket server is running on port 8888")
    tornado.ioloop.IOLoop.current().start()