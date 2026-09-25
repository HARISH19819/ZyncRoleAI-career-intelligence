from typing import Dict, List, Optional
from app.ingestion.base import JobSourceAdapter
from app.ingestion.adzuna import AdzunaSourceAdapter
from app.ingestion.jooble_and_muse import JoobleSourceAdapter, TheMuseSourceAdapter
from app.ingestion.ats_sources import GreenhouseSourceAdapter, LeverSourceAdapter, AshbySourceAdapter
from app.ingestion.gated_sources import (
    RemotiveSourceAdapter, linkedin_adapter, indeed_adapter, naukri_adapter, internshala_adapter
)
from app.ingestion.generic_feed import demo_source_adapter


class SourceRegistry:
    """Central registry managing all pluggable job source adapters."""

    def __init__(self):
        self._sources: Dict[str, JobSourceAdapter] = {}
        self._register_defaults()

    def _register_defaults(self):
        adapters = [
            AdzunaSourceAdapter(),
            JoobleSourceAdapter(),
            TheMuseSourceAdapter(),
            GreenhouseSourceAdapter(),
            LeverSourceAdapter(),
            AshbySourceAdapter(),
            RemotiveSourceAdapter(),
            linkedin_adapter,
            indeed_adapter,
            naukri_adapter,
            internshala_adapter,
            demo_source_adapter,
        ]
        for adapter in adapters:
            self._sources[adapter.source_id] = adapter

    def get_source(self, source_id: str) -> Optional[JobSourceAdapter]:
        return self._sources.get(source_id)

    def list_all_sources(self) -> List[Dict[str, any]]:
        return [adapter.get_source_metadata() for adapter in self._sources.values()]

    def get_enabled_sources(self) -> List[JobSourceAdapter]:
        return [adapter for adapter in self._sources.values() if adapter.enabled]


source_registry = SourceRegistry()
