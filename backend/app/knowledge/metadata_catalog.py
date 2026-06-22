"""Metadata catalog for knowledge management."""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class CatalogEntryType(Enum):
    """Types of catalog entries."""

    DATABASE = "database"
    TABLE = "table"
    VIEW = "view"
    REPORT = "report"
    DATASET = "dataset"
    DOCUMENT = "document"


@dataclass
class CatalogEntry:
    """Represents a single catalog entry."""

    id: str
    name: str
    entry_type: CatalogEntryType
    description: str = ""
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    owner: str = ""
    access_level: str = "public"


class MetadataCatalog:
    """Manages a catalog of metadata entries for knowledge discovery."""

    def __init__(self):
        """Initialize metadata catalog."""
        self.entries: Dict[str, CatalogEntry] = {}
        self.index: Dict[str, List[str]] = {}  # tag -> list of entry IDs

    def add_entry(self, entry: CatalogEntry) -> bool:
        """Add an entry to the catalog.

        Args:
            entry: CatalogEntry to add

        Returns:
            True if entry added successfully, False otherwise
        """
        try:
            if entry.id in self.entries:
                logger.warning(f"Entry with ID {entry.id} already exists")
                return False

            self.entries[entry.id] = entry
            
            # Index by tags
            for tag in entry.tags:
                if tag not in self.index:
                    self.index[tag] = []
                self.index[tag].append(entry.id)
            
            logger.info(f"Added catalog entry: {entry.id}")
            return True
        except Exception as e:
            logger.error(f"Error adding catalog entry: {e}")
            return False

    def remove_entry(self, entry_id: str) -> bool:
        """Remove an entry from the catalog.

        Args:
            entry_id: ID of the entry to remove

        Returns:
            True if entry removed successfully, False otherwise
        """
        try:
            if entry_id not in self.entries:
                logger.warning(f"Entry with ID {entry_id} not found")
                return False

            entry = self.entries.pop(entry_id)
            
            # Remove from index
            for tag in entry.tags:
                if tag in self.index:
                    self.index[tag].remove(entry_id)
                    if not self.index[tag]:
                        del self.index[tag]
            
            logger.info(f"Removed catalog entry: {entry_id}")
            return True
        except Exception as e:
            logger.error(f"Error removing catalog entry: {e}")
            return False

    def get_entry(self, entry_id: str) -> Optional[CatalogEntry]:
        """Retrieve an entry from the catalog.

        Args:
            entry_id: ID of the entry to retrieve

        Returns:
            CatalogEntry or None if not found
        """
        return self.entries.get(entry_id)

    def search_by_tag(self, tag: str) -> List[CatalogEntry]:
        """Search catalog entries by tag.

        Args:
            tag: Tag to search for

        Returns:
            List of matching CatalogEntry objects
        """
        entry_ids = self.index.get(tag, [])
        return [self.entries[eid] for eid in entry_ids if eid in self.entries]

    def search_by_name(self, name: str) -> List[CatalogEntry]:
        """Search catalog entries by name (partial match).

        Args:
            name: Name or partial name to search for

        Returns:
            List of matching CatalogEntry objects
        """
        results = []
        for entry in self.entries.values():
            if name.lower() in entry.name.lower():
                results.append(entry)
        return results

    def search_by_type(self, entry_type: CatalogEntryType) -> List[CatalogEntry]:
        """Search catalog entries by type.

        Args:
            entry_type: Type of entry to search for

        Returns:
            List of matching CatalogEntry objects
        """
        return [e for e in self.entries.values() if e.entry_type == entry_type]

    def update_entry(self, entry_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing catalog entry.

        Args:
            entry_id: ID of the entry to update
            updates: Dictionary of fields to update

        Returns:
            True if entry updated successfully, False otherwise
        """
        try:
            if entry_id not in self.entries:
                logger.warning(f"Entry with ID {entry_id} not found")
                return False

            entry = self.entries[entry_id]
            for key, value in updates.items():
                if hasattr(entry, key):
                    setattr(entry, key, value)
            
            entry.updated_at = datetime.now().isoformat()
            logger.info(f"Updated catalog entry: {entry_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating catalog entry: {e}")
            return False

    def list_all_entries(self) -> List[CatalogEntry]:
        """List all entries in the catalog.

        Returns:
            List of all CatalogEntry objects
        """
        return list(self.entries.values())

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the catalog.

        Returns:
            Dictionary containing catalog statistics
        """
        type_counts = {}
        for entry in self.entries.values():
            entry_type = entry.entry_type.value
            type_counts[entry_type] = type_counts.get(entry_type, 0) + 1

        return {
            "total_entries": len(self.entries),
            "total_tags": len(self.index),
            "entries_by_type": type_counts,
            "tags": list(self.index.keys()),
        }
