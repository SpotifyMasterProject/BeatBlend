export default class WebsocketService {
    socket: WebSocket
    handler: ((message: any) => void) | null
    reconnectTimeout: number;
    maxReconnectAttempts: number;
    reconnectAttempts: number;

    constructor() {
        this.handler = null;
        this.reconnectTimeout = 2000;
        this.maxReconnectAttempts = 10;
        this.reconnectAttempts = 0;
        this.connect();
    }

    connect() {
        this.socket = new WebSocket('ws://localhost:8000/ws')
        this.handler = null

        this.socket.onopen = () => {
            console.log('Websocket connection established!')
            this.reconnectAttempts = 0;
        }

        this.socket.onmessage = (event) => {
            console.log('Message received:' + event.data)
            if (this.handler) {
                this.handler(event.data)
            }
        }

        this.socket.onclose = (event) => {
            console.log('Websocket disconnected! Attempting to reconnect.')
            if (event.code !== 1000) { // Do not attempt to reconnect if the connection was closed normally (code 1000)
                this.attemptReconnect();
            }
        }

        this.socket.onerror = (event) => {
            console.log('Websocket error:' + event)
            this.socket.close()
        }
    }

    attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            setTimeout(() => {
                console.log('Attempting to reconnect to WebSocket...');
                this.reconnectAttempts++;
                this.connect();
            }, this.reconnectTimeout);
            this.reconnectTimeout *= 2; // Exponential backoff
        } else {
            console.log('Max reconnection attempts reached. Could not reconnect to WebSocket.');
        }
    }

    // Not implemented yet. Only supporting simplex operations currently (receiving messages).
    sendMessage(message: string) {
        if (this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(message);
        } else {
            console.log('WebSocket is not open. Cannot send message.');
        }
    }

    close() {
        if (this.socket) {
            this.socket.close(1000, 'Client closed connection.'); // Close with normal closure code 1000
        }
    }

    setMessageHandler(messageHandler: (message: any) => void) {
        this.handler = messageHandler
    }
}