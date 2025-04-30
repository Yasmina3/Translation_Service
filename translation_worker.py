# translation_worker.py

import asyncio
import json
import logging
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from gemini_mock import translate_title
from gemini_api import translate_title

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TranslationService")

# Kafka config
KAFKA_BOOTSTRAP = "localhost:9092"
REQUEST_TOPIC = "translation_requests"
RESPONSE_TOPIC = "translation_responses"

async def run_translation_worker():
    logger.info("Starting Translation Service...")

    consumer = AIOKafkaConsumer(
        REQUEST_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        group_id="translator-group"
    )
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP
    )

    await consumer.start()
    await producer.start()

    try:
        async for msg in consumer:
            try:
                payload = json.loads(msg.value.decode())
                logger.info(f"Received: {payload}")

                document_id = payload["document_id"]
                title_en = payload["title_en"]

                title_es = await translate_title(title_en)

                result = {
                    "document_id": document_id,
                    "title_es": title_es
                }

                await producer.send_and_wait(
                    RESPONSE_TOPIC,
                    json.dumps(result).encode()
                )
                logger.info(f"Published: {result}")

            except Exception as e:
                logger.error(f"❌ Error processing message: {e}", exc_info=True)
    finally:
        await consumer.stop()
        await producer.stop()
        logger.info("Translation Service shut down.")

if __name__ == "__main__":
    asyncio.run(run_translation_worker())
