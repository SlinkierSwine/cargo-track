import json
import pika
from typing import Any, Dict
import structlog


class Publisher:
    def __init__(self, host: str, port: int, username: str, password: str, exchange: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.exchange = exchange
        self.connection = None
        self.channel = None
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
            self.logger.info("Connected to RabbitMQ")
        except Exception as e:
            self.logger.error("Failed to connect to RabbitMQ", error=str(e))
            raise
    
    def disconnect(self) -> None:
        """Disconnect from RabbitMQ"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            self.logger.info("Disconnected from RabbitMQ")
    
    def publish(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """Publish an event to RabbitMQ"""
        if not self.connection or self.connection.is_closed:
            self.connect()
        
        try:
            # Declare exchange
            self.channel.exchange_declare(
                exchange='cargo_track_events',
                exchange_type='topic',
                durable=True
            )
            
            # Prepare message
            message = {
                'event_type': event_type,
                'event_data': event_data,
                'timestamp': str(event_data.get('timestamp', ''))
            }
            
            # Publish message
            self.channel.basic_publish(
                exchange='cargo_track_events',
                routing_key=event_type,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                    content_type='application/json'
                )
            )
            
            self.logger.info("Event published", event_type=event_type)
        except Exception as e:
            self.logger.error("Failed to publish event", event_type=event_type, error=str(e))
            raise 