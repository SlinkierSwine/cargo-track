import json
import pika
import threading
from typing import Any, Dict, Callable
import structlog


class Subscriber:
    def __init__(self, host: str = "localhost", port: int = 5672, username: str = "guest", password: str = "guest") -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None
        self.channel = None
        self.handlers: Dict[str, Callable[[Dict[str, Any]], None]] = {}
        self.is_listening = False
        self.logger = structlog.get_logger(self.__class__.__name__)
    
    def connect(self) -> None:
        """Connect to RabbitMQ"""
        try:
            credentials = pika.PlainCredentials(self.username, self.password)
            parameters = pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                credentials=credentials
            )
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            
            # Declare exchange
            self.channel.exchange_declare(
                exchange='cargo_track_events',
                exchange_type='topic',
                durable=True
            )
            
            self.logger.info("Connected to RabbitMQ")
        except Exception as e:
            self.logger.error("Failed to connect to RabbitMQ", error=str(e))
            raise
    
    def disconnect(self) -> None:
        """Disconnect from RabbitMQ"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            self.logger.info("Disconnected from RabbitMQ")
    
    def subscribe(self, event_type: str, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Subscribe to an event type with a handler function"""
        if not self.connection or self.connection.is_closed:
            self.connect()
        
        try:
            # Declare queue
            queue_name = f"{event_type}_queue"
            self.channel.queue_declare(queue=queue_name, durable=True)
            
            # Bind queue to exchange
            self.channel.queue_bind(
                exchange='cargo_track_events',
                queue=queue_name,
                routing_key=event_type
            )
            
            # Store handler
            self.handlers[event_type] = handler
            
            self.logger.info("Subscribed to event", event_type=event_type)
        except Exception as e:
            self.logger.error("Failed to subscribe to event", event_type=event_type, error=str(e))
            raise
    
    def unsubscribe(self, event_type: str) -> None:
        """Unsubscribe from an event type"""
        if event_type in self.handlers:
            del self.handlers[event_type]
            self.logger.info("Unsubscribed from event", event_type=event_type)
    
    def _message_handler(self, ch, method, properties, body) -> None:
        """Handle incoming messages"""
        try:
            message = json.loads(body)
            event_type = message.get('event_type')
            event_data = message.get('event_data', {})
            
            if event_type in self.handlers:
                self.handlers[event_type](event_data)
                ch.basic_ack(delivery_tag=method.delivery_tag)
                self.logger.info("Message processed", event_type=event_type)
            else:
                self.logger.warning("No handler found for event", event_type=event_type)
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as e:
            self.logger.error("Error processing message", error=str(e))
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    
    def start_listening(self) -> None:
        """Start listening for events"""
        if not self.connection or self.connection.is_closed:
            self.connect()
        
        if not self.handlers:
            self.logger.warning("No handlers registered")
            return
        
        try:
            self.is_listening = True
            
            # Set up consumers for all subscribed events
            for event_type in self.handlers.keys():
                queue_name = f"{event_type}_queue"
                self.channel.basic_consume(
                    queue=queue_name,
                    on_message_callback=self._message_handler,
                    auto_ack=False
                )
            
            self.logger.info("Started listening for events")
            
            # Start consuming in a separate thread
            def consume():
                try:
                    self.channel.start_consuming()
                except KeyboardInterrupt:
                    self.stop_listening()
            
            thread = threading.Thread(target=consume, daemon=True)
            thread.start()
            
        except Exception as e:
            self.logger.error("Failed to start listening", error=str(e))
            raise
    
    def stop_listening(self) -> None:
        """Stop listening for events"""
        if self.is_listening and self.channel:
            self.channel.stop_consuming()
            self.is_listening = False
            self.logger.info("Stopped listening for events") 