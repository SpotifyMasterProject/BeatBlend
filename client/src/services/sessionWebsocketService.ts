export default class SessionWebsocketService {
    socket: WebSocket | null
    reconnectTimeout: number;
    maxReconnectAttempts: number;
    reconnectAttempts: number;

    constructor() {
        this.reconnectTimeout = 2000;
        this.maxReconnectAttempts = 10;
        this.reconnectAttempts = 0;
        this.socket = null;
    }

    connect(sessionId: string, handler: ((message: any) => void)) {
        this.socket = new WebSocket(`ws://localhost:8000/ws/${sessionId}`)

        this.socket.onopen = () => {
            console.log('Websocket connection established!')
            this.reconnectAttempts = 0;
        }

        this.socket.onmessage = (event) => {
            console.log('Message received:' + event.data);
            handler(event.data);
        }

        this.socket.onclose = (event) => {
            console.log('Websocket disconnected! Attempting to reconnect.')
            if (event.code !== 1000) { // Do not attempt to reconnect if the connection was closed normally (code 1000)
                this.attemptReconnect(sessionId, handler);
            }
        }

        this.socket.onerror = (event) => {
            console.log('Websocket error:' + event)
            this.socket?.close()
        }
    }

    attemptReconnect(sessionId: string, handler: ((message: any) => void)) {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            setTimeout(() => {
                console.log('Attempting to reconnect to WebSocket...');
                this.reconnectAttempts++;
                this.connect(sessionId, handler);
            }, this.reconnectTimeout);
            this.reconnectTimeout *= 2; // Exponential backoff
        } else {
            console.log('Max reconnection attempts reached. Could not reconnect to WebSocket.');
        }
    }

    sendMessage(message: string) {
        if (this.socket?.readyState === WebSocket.OPEN) {
            this.socket?.send(message);
        } else {
            console.log('WebSocket is not open. Cannot send message.');
        }
    }

    close() {
        this.socket?.close(1000, 'Client closed connection.'); // Close with normal closure code 1000
    }
}