from datetime import datetime, timedelta
from typing import Any

from agent_infra.system_logger import SystemLogger
from qdrant_client.http.models import FieldCondition, Filter, Range

from .memory_ingest import cloud_qdrant, local_qdrant
from .memory_search import CLOUD_COLLECTION, LOCAL_COLLECTION, check_connection

logger = SystemLogger()


def prune_collection(client: Any, collection_name: str, max_age_days: int = 90) -> None:
    """Prunes old records from a specific collection."""
    logger.info("prune_start", {"collection": collection_name})

    try:
        cutoff_time = (datetime.now() - timedelta(days=max_age_days)).timestamp()

        # Use Qdrant's delete with a filter on created_at
        # Note: We assume created_at is stored as a float in the payload
        client.delete(
            collection_name=collection_name,
            points_selector=Filter(
                must=[FieldCondition(key="created_at", range=Range(lt=cutoff_time))]
            ),
        )

        logger.info(
            "prune_success",
            {"collection": collection_name, "max_age_days": max_age_days},
        )

    except (RuntimeError, ConnectionError, ValueError) as e:
        logger.error("prune_failure", {"collection": collection_name, "error": str(e)})


def run_prune_cycle(max_age_days: int = 90) -> None:
    """Prunes all managed collections of records older than max_age_days."""
    # Check local connection
    if not check_connection(local_qdrant):
        logger.error("prune_conn_failure", {"tier": "local"})
    else:
        prune_collection(local_qdrant, LOCAL_COLLECTION, max_age_days)

    # Check cloud connection
    if cloud_qdrant:
        if not check_connection(cloud_qdrant):
            logger.error("prune_conn_failure", {"tier": "cloud"})
        else:
            prune_collection(cloud_qdrant, CLOUD_COLLECTION, max_age_days)
    else:
        logger.info("prune_skip", {"tier": "cloud", "reason": "Client not available"})

    logger.info("prune_cycle_complete", {})


if __name__ == "__main__":
    # Allow running manually via CLI
    run_prune_cycle()
