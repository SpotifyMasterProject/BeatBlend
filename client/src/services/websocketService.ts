export default class WebsocketService {
    socket: WebSocket
    handler: ((message: any) => void) | null

    constructor() {
        this.socket = new WebSocket('ws://localhost:8000/ws')
        this.handler = null

        this.socket.onopen = () => {
            console.log('Websocket connection established!')
        }

        this.socket.onmessage = (event) => {
            console.log('Message received:' + event.data)
            if (this.handler) {
                this.handler(event.data)
            }
        }

        this.socket.onclose = () => {
            console.log('Websocket connection closed!')
            //TODO @jemaie: implement (automatic) reconnection logic
        }

        this.socket.onerror = (event) => {
            console.log('Websocket error:' + event)
        }
    }

    // Not implemented yet. Only supporting simplex operations currently (receiving messages).
    sendMessage() {
        return
    }

    close() {
        if (this.socket) {
            this.socket.close()
        }
    }

    setMessageHandler(messageHandler: (message: any) => void) {
        this.handler = messageHandler
    }
}