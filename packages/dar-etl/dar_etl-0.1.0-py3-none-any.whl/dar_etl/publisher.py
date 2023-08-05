from datetime import datetime
from datetime import timezone
import logging

from confluent_kafka import KafkaError
from confluent_kafka import Message
from confluent_kafka import Producer

from dar_etl.config import Config
from dar_etl.parsing.parser import Metadata
from dar_etl.schemas.base_model import DarBaseModel


class DarEntryPublisher:
    def __init__(self, config: Config) -> None:
        host = config.kafka.host
        port = config.kafka.port
        self.producer = Producer({"bootstrap.servers": f"{host}:{port}"})

    def publish(self, metadata: Metadata) -> None:
        self.producer.poll(0)

        self.producer.produce(
            topic=metadata.root.value,
            key=self._message_key(dar_model=metadata.dar_model),
            value=metadata.dar_model.json().encode(encoding="utf-8"),
            on_delivery=self._on_delivery,
            timestamp=self._message_timestamp(dar_model=metadata.dar_model),
            headers=self._message_headers(metadata=metadata),
        )

    def flush(self) -> None:
        self.producer.flush()

    def _message_headers(self, metadata: Metadata) -> dict[str, bytes]:
        processed_timestamp = datetime.now(tz=timezone.utc).isoformat()
        return {
            "json_file": metadata.filename.encode(encoding="utf-8"),
            "processed_timestamp": processed_timestamp.encode("utf-8"),
        }

    def _message_key(self, dar_model: DarBaseModel) -> bytes | None:
        id_local = dar_model.id_local
        if id_local:
            return id_local.encode(encoding="UTF-8")
        return None

    def _message_timestamp(self, dar_model: DarBaseModel) -> int:
        effect_from = dar_model.effect_from
        if effect_from:
            return int(effect_from.timestamp() * 1000)
        return 0

    def _on_delivery(self, error: KafkaError, message: Message) -> None:
        if error:
            logging.error("Failed to publish.")
        else:
            logging.debug("Published %s successfully", message.key())
