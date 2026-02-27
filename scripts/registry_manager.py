#!/usr/bin/env python3
"""
EBF Registry Manager - Proactive Duplicate Prevention
======================================================

Provides a unified interface for all EBF registries with:
1. Automatic ID generation (duplicates impossible)
2. Validation before write
3. Thread-safe file locking
4. Backup before modification

USAGE:
    from registry_manager import CaseRegistry, TheoryRegistry, ParameterRegistry

    # Add new case with auto-generated ID
    case = CaseRegistry()
    new_id = case.add({
        'name': 'My New Case',
        'domain': ['finance', 'behavior'],
        '10C': {...}
    })
    print(f"Created {new_id}")  # CAS-910

    # Check if ID exists
    if case.exists('CAS-500'):
        print("ID already in use")

    # Get next available ID (without adding)
    next_id = case.next_id()  # CAS-911

REGISTRIES SUPPORTED:
    - CaseRegistry: CAS-XXX
    - TheoryRegistry: CAT-XX, MS-XX-XXX
    - ParameterRegistry: PAR-XX-XXX
    - PaperRegistry: PAP-xxxxx

Author: EBF Framework
Version: 1.0
"""

import re
import sys
import yaml
import fcntl
import shutil
from pathlib import Path
from datetime import datetime
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Optional, Dict, List, Any, Union

# Repository root
REPO_ROOT = Path(__file__).parent.parent

# Backup directory
BACKUP_DIR = REPO_ROOT / '.registry_backups'


class DuplicateIDError(Exception):
    """Raised when attempting to create an entry with an existing ID."""
    pass


class InvalidIDError(Exception):
    """Raised when an ID doesn't match the expected pattern."""
    pass


class RegistryManager(ABC):
    """
    Base class for all EBF registries with automatic ID management.

    Subclasses must implement:
        - _load_ids(): Extract all existing IDs from the registry file
        - _append_entry(): Add a new entry to the registry file
        - id_pattern: Regex pattern for valid IDs
        - id_format: Format string for generating new IDs
    """

    def __init__(self, registry_path: Path):
        self.path = registry_path
        self._cached_ids = None
        self._cache_mtime = None

    @property
    @abstractmethod
    def id_pattern(self) -> str:
        """Regex pattern for extracting IDs."""
        pass

    @abstractmethod
    def _load_ids(self) -> List[int]:
        """Load all numeric IDs from the registry."""
        pass

    @abstractmethod
    def _format_id(self, num: int, prefix: str = None) -> str:
        """Format a numeric ID into the registry's ID format."""
        pass

    @abstractmethod
    def _append_entry(self, entry: Dict, entry_id: str) -> None:
        """Append a new entry to the registry file."""
        pass

    def _get_ids(self, force_reload: bool = False) -> List[int]:
        """Get cached IDs, reloading if file changed."""
        if self.path.exists():
            current_mtime = self.path.stat().st_mtime
            if force_reload or self._cached_ids is None or self._cache_mtime != current_mtime:
                self._cached_ids = self._load_ids()
                self._cache_mtime = current_mtime
        else:
            self._cached_ids = []
        return self._cached_ids or []

    def exists(self, entry_id: str) -> bool:
        """Check if an ID already exists in the registry."""
        match = re.match(self.id_pattern, entry_id)
        if not match:
            return False
        num = int(match.group(1))
        return num in self._get_ids()

    def next_id(self, prefix: str = None) -> str:
        """Get the next available ID without creating an entry."""
        ids = self._get_ids(force_reload=True)
        next_num = max(ids) + 1 if ids else 1
        return self._format_id(next_num, prefix)

    def _create_backup(self) -> Path:
        """Create a backup of the registry before modification."""
        if not self.path.exists():
            return None

        BACKUP_DIR.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = BACKUP_DIR / f"{self.path.stem}_{timestamp}.yaml"
        shutil.copy2(self.path, backup_path)

        # Keep only last 10 backups per registry
        backups = sorted(BACKUP_DIR.glob(f"{self.path.stem}_*.yaml"))
        for old_backup in backups[:-10]:
            old_backup.unlink()

        return backup_path

    def add(self, entry: Dict, entry_id: str = None, prefix: str = None) -> str:
        """
        Add a new entry to the registry.

        Args:
            entry: The entry data (without ID)
            entry_id: Optional specific ID (will validate uniqueness)
            prefix: Optional prefix for ID generation (e.g., 'CM' for MS-CM-XXX)

        Returns:
            The assigned ID

        Raises:
            DuplicateIDError: If entry_id already exists
            InvalidIDError: If entry_id doesn't match expected pattern
        """
        # Generate or validate ID
        if entry_id is None or entry_id == 'AUTO':
            entry_id = self.next_id(prefix)
        else:
            # Validate format
            if not re.match(self.id_pattern, entry_id):
                raise InvalidIDError(f"ID '{entry_id}' doesn't match pattern {self.id_pattern}")
            # Check for duplicate
            if self.exists(entry_id):
                raise DuplicateIDError(f"ID '{entry_id}' already exists in {self.path.name}")

        # Create backup
        self._create_backup()

        # Use file locking for thread safety
        with open(self.path, 'a') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                # Re-check after acquiring lock (another process might have added)
                self._cached_ids = None  # Force reload
                if self.exists(entry_id):
                    raise DuplicateIDError(f"ID '{entry_id}' was created by another process")

                self._append_entry(entry, entry_id)

                # Update cache
                match = re.match(self.id_pattern, entry_id)
                if match and self._cached_ids is not None:
                    self._cached_ids.append(int(match.group(1)))
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

        return entry_id

    def validate_all(self) -> Dict[str, List[str]]:
        """Check for duplicates and return any found."""
        content = self.path.read_text() if self.path.exists() else ""
        matches = re.findall(self.id_pattern, content)

        seen = defaultdict(int)
        for m in matches:
            seen[m] += 1

        duplicates = {k: v for k, v in seen.items() if v > 1}
        return duplicates

    def status(self) -> Dict[str, Any]:
        """Get current status of the registry."""
        ids = self._get_ids(force_reload=True)
        return {
            'path': str(self.path),
            'count': len(ids),
            'highest': max(ids) if ids else 0,
            'next_available': self.next_id(),
            'duplicates': self.validate_all()
        }


class CaseRegistry(RegistryManager):
    """Manager for case-registry.yaml (CAS-XXX format)."""

    def __init__(self):
        super().__init__(REPO_ROOT / 'data' / 'case-registry.yaml')

    @property
    def id_pattern(self) -> str:
        return r'CAS-(\d+)'

    def _load_ids(self) -> List[int]:
        """Extract all CAS-XXX IDs from case-registry.yaml (definitions only)."""
        ids = []
        if self.path.exists():
            content = self.path.read_text()
            # Match ONLY case definitions, not references:
            # Format 1: "  CAS-123:" (old dict style, 2 spaces indent + colon)
            # Format 2: "    id: CAS-123" (new list style)
            # Exclude: "- CAS-123" (references in related_cases arrays)
            definition_pattern = r'(?:^  CAS-(\d+):)|(?:^\s+id:\s*CAS-(\d+))'
            for match in re.finditer(definition_pattern, content, re.MULTILINE):
                num = match.group(1) or match.group(2)
                if num:
                    ids.append(int(num))
        return ids

    def validate_all(self) -> Dict[str, List[str]]:
        """Check for duplicate DEFINITIONS only (not references)."""
        ids = self._load_ids()
        seen = defaultdict(int)
        for num in ids:
            seen[num] += 1
        return {f"CAS-{k}": v for k, v in seen.items() if v > 1}

    def _format_id(self, num: int, prefix: str = None) -> str:
        return f"CAS-{num}"

    def _append_entry(self, entry: Dict, entry_id: str) -> None:
        """Append a new case to the registry in list format."""
        # Build the YAML entry
        entry_with_id = {'id': entry_id, **entry}

        yaml_str = "\n  # " + "=" * 75 + "\n"
        yaml_str += f"  # {entry_id}: {entry.get('name', entry.get('title', 'Unnamed Case'))}\n"
        yaml_str += "  # " + "=" * 75 + "\n"
        yaml_str += "  - " + yaml.dump(entry_with_id, default_flow_style=False, allow_unicode=True, sort_keys=False).replace('\n', '\n    ').rstrip() + "\n"

        with open(self.path, 'a') as f:
            f.write(yaml_str)


class TheoryCategoryRegistry(RegistryManager):
    """Manager for theory-catalog.yaml CAT-XX entries."""

    def __init__(self):
        super().__init__(REPO_ROOT / 'data' / 'theory-catalog.yaml')

    @property
    def id_pattern(self) -> str:
        return r'CAT-(\d+)'

    def _load_ids(self) -> List[int]:
        """Extract all CAT-XX IDs from theory-catalog.yaml (definitions only)."""
        ids = []
        if self.path.exists():
            content = self.path.read_text()
            # Only match category definitions: "  - id: CAT-XX"
            matches = re.findall(r'^\s+-\s+id:\s*CAT-(\d+)', content, re.MULTILINE)
            ids = [int(m) for m in matches]
        return ids

    def validate_all(self) -> Dict[str, List[str]]:
        """Check for duplicate DEFINITIONS only."""
        ids = self._load_ids()
        seen = defaultdict(int)
        for num in ids:
            seen[num] += 1
        return {f"CAT-{k}": v for k, v in seen.items() if v > 1}

    def _format_id(self, num: int, prefix: str = None) -> str:
        return f"CAT-{num}"

    def _append_entry(self, entry: Dict, entry_id: str) -> None:
        """Append a new category - requires manual integration."""
        raise NotImplementedError(
            "Categories require manual integration into theory-catalog.yaml structure. "
            f"Use ID {entry_id} when adding manually."
        )


class TheoryModelRegistry(RegistryManager):
    """Manager for theory-catalog.yaml MS-XX-XXX entries."""

    def __init__(self):
        super().__init__(REPO_ROOT / 'data' / 'theory-catalog.yaml')
        self._prefix_ids = None

    @property
    def id_pattern(self) -> str:
        return r'MS-([A-Z]{2,4})-(\d{3})'

    def _load_ids(self) -> List[int]:
        """Not used directly - see _load_prefix_ids."""
        return []

    def _load_prefix_ids(self) -> Dict[str, List[int]]:
        """Load all MS-XX-XXX IDs grouped by prefix."""
        ids = defaultdict(list)
        if self.path.exists():
            content = self.path.read_text()
            matches = re.findall(r'id:\s*MS-([A-Z]{2,4})-(\d{3})', content)
            for prefix, num in matches:
                ids[prefix].append(int(num))
        return ids

    def _get_prefix_ids(self, prefix: str, force_reload: bool = False) -> List[int]:
        """Get IDs for a specific prefix."""
        if force_reload or self._prefix_ids is None:
            self._prefix_ids = self._load_prefix_ids()
        return self._prefix_ids.get(prefix, [])

    def _format_id(self, num: int, prefix: str = None) -> str:
        if not prefix:
            raise ValueError("MS-XX-XXX requires a prefix (e.g., 'CM', 'SP', 'RD')")
        return f"MS-{prefix}-{num:03d}"

    def exists(self, entry_id: str) -> bool:
        """Check if a MS-XX-XXX ID exists."""
        match = re.match(self.id_pattern, entry_id)
        if not match:
            return False
        prefix, num = match.groups()
        return int(num) in self._get_prefix_ids(prefix)

    def next_id(self, prefix: str = None) -> str:
        """Get next available MS-XX-XXX ID for given prefix."""
        if not prefix:
            raise ValueError("MS-XX-XXX requires a prefix (e.g., 'CM', 'SP', 'RD')")
        ids = self._get_prefix_ids(prefix, force_reload=True)
        next_num = max(ids) + 1 if ids else 1
        return self._format_id(next_num, prefix)

    def _append_entry(self, entry: Dict, entry_id: str) -> None:
        """Append a new theory - requires manual integration."""
        raise NotImplementedError(
            "Theories require manual integration into theory-catalog.yaml structure. "
            f"Use ID {entry_id} when adding manually."
        )

    def validate_all(self) -> Dict[str, List[str]]:
        """Check for duplicate DEFINITIONS only (not references)."""
        self._prefix_ids = self._load_prefix_ids()
        duplicates = {}
        for prefix, ids in self._prefix_ids.items():
            seen = defaultdict(int)
            for num in ids:
                seen[num] += 1
            for num, count in seen.items():
                if count > 1:
                    duplicates[f"MS-{prefix}-{num:03d}"] = count
        return duplicates

    def status(self) -> Dict[str, Any]:
        """Get status for all MS prefixes."""
        self._prefix_ids = self._load_prefix_ids()
        return {
            'path': str(self.path),
            'total_theories': sum(len(v) for v in self._prefix_ids.values()),
            'prefixes': {
                prefix: {
                    'count': len(ids),
                    'highest': max(ids) if ids else 0,
                    'next': self._format_id(max(ids) + 1 if ids else 1, prefix)
                }
                for prefix, ids in sorted(self._prefix_ids.items())
            }
        }


class ParameterRegistry(RegistryManager):
    """Manager for parameter-registry.yaml (PAR-XX-XXX format)."""

    def __init__(self):
        super().__init__(REPO_ROOT / 'data' / 'parameter-registry.yaml')
        self._prefix_ids = None

    @property
    def id_pattern(self) -> str:
        return r'PAR-([A-Z]{2,4})-(\d{3})'

    def _load_ids(self) -> List[int]:
        """Not used directly - see _load_prefix_ids."""
        return []

    def _load_prefix_ids(self) -> Dict[str, List[int]]:
        """Load all PAR-XX-XXX IDs grouped by prefix."""
        ids = defaultdict(list)
        if self.path.exists():
            content = self.path.read_text()
            matches = re.findall(r'id:\s*PAR-([A-Z]{2,4})-(\d{3})', content)
            for prefix, num in matches:
                ids[prefix].append(int(num))
        return ids

    def _get_prefix_ids(self, prefix: str, force_reload: bool = False) -> List[int]:
        """Get IDs for a specific prefix."""
        if force_reload or self._prefix_ids is None:
            self._prefix_ids = self._load_prefix_ids()
        return self._prefix_ids.get(prefix, [])

    def _format_id(self, num: int, prefix: str = None) -> str:
        if not prefix:
            raise ValueError("PAR-XX-XXX requires a prefix (e.g., 'CM', 'BEH', 'COMP')")
        return f"PAR-{prefix}-{num:03d}"

    def exists(self, entry_id: str) -> bool:
        """Check if a PAR-XX-XXX ID exists."""
        match = re.match(self.id_pattern, entry_id)
        if not match:
            return False
        prefix, num = match.groups()
        return int(num) in self._get_prefix_ids(prefix)

    def next_id(self, prefix: str = None) -> str:
        """Get next available PAR-XX-XXX ID for given prefix."""
        if not prefix:
            raise ValueError("PAR-XX-XXX requires a prefix (e.g., 'CM', 'BEH', 'COMP')")
        ids = self._get_prefix_ids(prefix, force_reload=True)
        next_num = max(ids) + 1 if ids else 1
        return self._format_id(next_num, prefix)

    def _append_entry(self, entry: Dict, entry_id: str) -> None:
        """Append a new parameter to the registry."""
        entry_with_id = {'id': entry_id, **entry}

        yaml_str = "\n  # " + "-" * 60 + "\n"
        yaml_str += f"  # {entry_id}\n"
        yaml_str += "  # " + "-" * 60 + "\n"
        yaml_str += "  - " + yaml.dump(entry_with_id, default_flow_style=False, allow_unicode=True, sort_keys=False).replace('\n', '\n    ').rstrip() + "\n"

        with open(self.path, 'a') as f:
            f.write(yaml_str)

    def validate_all(self) -> Dict[str, List[str]]:
        """Check for duplicate DEFINITIONS only (not references)."""
        self._prefix_ids = self._load_prefix_ids()
        duplicates = {}
        for prefix, ids in self._prefix_ids.items():
            seen = defaultdict(int)
            for num in ids:
                seen[num] += 1
            for num, count in seen.items():
                if count > 1:
                    duplicates[f"PAR-{prefix}-{num:03d}"] = count
        return duplicates

    def status(self) -> Dict[str, Any]:
        """Get status for all PAR prefixes."""
        self._prefix_ids = self._load_prefix_ids()
        return {
            'path': str(self.path),
            'total_parameters': sum(len(v) for v in self._prefix_ids.values()),
            'prefixes': {
                prefix: {
                    'count': len(ids),
                    'highest': max(ids) if ids else 0,
                    'next': self._format_id(max(ids) + 1 if ids else 1, prefix)
                }
                for prefix, ids in sorted(self._prefix_ids.items())
            }
        }


# =============================================================================
# NEW REGISTRIES (v1.27)
# =============================================================================

class ModelRegistry(RegistryManager):
    """Manager for model-registry.yaml (MOD-XXX format)."""

    def __init__(self):
        super().__init__(REPO_ROOT / 'data' / 'model-registry.yaml')

    @property
    def id_pattern(self) -> str:
        return r'MOD-(\d+)'

    def _load_ids(self) -> List[int]:
        """Extract all MOD-XXX IDs from model-registry.yaml (definitions only)."""
        ids = []
        if self.path.exists():
            content = self.path.read_text()
            # Match model definitions: "- id: MOD-XXX"
            matches = re.findall(r'^\s*-\s+id:\s*MOD-(\d+)', content, re.MULTILINE)
            ids = [int(m) for m in matches]
        return ids

    def validate_all(self) -> Dict[str, List[str]]:
        """Check for duplicate DEFINITIONS only."""
        ids = self._load_ids()
        seen = defaultdict(int)
        for num in ids:
            seen[num] += 1
        return {f"MOD-{k}": v for k, v in seen.items() if v > 1}

    def _format_id(self, num: int, prefix: str = None) -> str:
        return f"MOD-{num:03d}"

    def _append_entry(self, entry: Dict, entry_id: str) -> None:
        """Append a new model - requires manual integration."""
        raise NotImplementedError(
            "Models require manual integration into model-registry.yaml structure. "
            f"Use ID {entry_id} when adding manually."
        )


class OutputRegistry(RegistryManager):
    """Manager for output-registry.yaml (OUT-XXX format)."""

    def __init__(self):
        super().__init__(REPO_ROOT / 'data' / 'output-registry.yaml')

    @property
    def id_pattern(self) -> str:
        return r'OUT-(\d+)'

    def _load_ids(self) -> List[int]:
        """Extract all OUT-XXX IDs from output-registry.yaml (definitions only)."""
        ids = []
        if self.path.exists():
            content = self.path.read_text()
            # Match output definitions: "- id: OUT-XXX"
            matches = re.findall(r'^\s*-\s+id:\s*OUT-(\d+)', content, re.MULTILINE)
            ids = [int(m) for m in matches]
        return ids

    def validate_all(self) -> Dict[str, List[str]]:
        """Check for duplicate DEFINITIONS only."""
        ids = self._load_ids()
        seen = defaultdict(int)
        for num in ids:
            seen[num] += 1
        return {f"OUT-{k}": v for k, v in seen.items() if v > 1}

    def _format_id(self, num: int, prefix: str = None) -> str:
        return f"OUT-{num:03d}"

    def _append_entry(self, entry: Dict, entry_id: str) -> None:
        """Append a new output entry."""
        entry_with_id = {'id': entry_id, **entry}

        yaml_str = "\n- " + yaml.dump(entry_with_id, default_flow_style=False, allow_unicode=True, sort_keys=False).replace('\n', '\n  ').rstrip() + "\n"

        with open(self.path, 'a') as f:
            f.write(yaml_str)


class SkillRegistry(RegistryManager):
    """Manager for skill-registry.yaml (SKL-{CAT}-{NNN} format)."""

    def __init__(self):
        super().__init__(REPO_ROOT / 'data' / 'skill-registry.yaml')
        self._prefix_ids = None

    @property
    def id_pattern(self) -> str:
        return r'SKL-([A-Z]{2,4})-(\d{3})'

    def _load_ids(self) -> List[int]:
        """Not used directly - see _load_prefix_ids."""
        return []

    def _load_prefix_ids(self) -> Dict[str, List[int]]:
        """Load all SKL-XX-XXX IDs grouped by category."""
        ids = defaultdict(list)
        if self.path.exists():
            content = self.path.read_text()
            matches = re.findall(r'id:\s*["\']?SKL-([A-Z]{2,4})-(\d{3})["\']?', content)
            for prefix, num in matches:
                ids[prefix].append(int(num))
        return ids

    def _get_prefix_ids(self, prefix: str, force_reload: bool = False) -> List[int]:
        """Get IDs for a specific prefix."""
        if force_reload or self._prefix_ids is None:
            self._prefix_ids = self._load_prefix_ids()
        return self._prefix_ids.get(prefix, [])

    def _format_id(self, num: int, prefix: str = None) -> str:
        if not prefix:
            raise ValueError("SKL-XX-XXX requires a prefix (e.g., 'PRJ', 'FRM', 'DOC')")
        return f"SKL-{prefix}-{num:03d}"

    def exists(self, entry_id: str) -> bool:
        """Check if a SKL-XX-XXX ID exists."""
        match = re.match(self.id_pattern, entry_id)
        if not match:
            return False
        prefix, num = match.groups()
        return int(num) in self._get_prefix_ids(prefix)

    def next_id(self, prefix: str = None) -> str:
        """Get next available SKL-XX-XXX ID for given prefix."""
        if not prefix:
            raise ValueError("SKL-XX-XXX requires a prefix (e.g., 'PRJ', 'FRM', 'DOC')")
        ids = self._get_prefix_ids(prefix, force_reload=True)
        next_num = max(ids) + 1 if ids else 1
        return self._format_id(next_num, prefix)

    def _append_entry(self, entry: Dict, entry_id: str) -> None:
        """Append a new skill - requires manual integration."""
        raise NotImplementedError(
            "Skills require manual integration into skill-registry.yaml structure. "
            f"Use ID {entry_id} when adding manually."
        )

    def validate_all(self) -> Dict[str, List[str]]:
        """Check for duplicate DEFINITIONS only."""
        self._prefix_ids = self._load_prefix_ids()
        duplicates = {}
        for prefix, ids in self._prefix_ids.items():
            seen = defaultdict(int)
            for num in ids:
                seen[num] += 1
            for num, count in seen.items():
                if count > 1:
                    duplicates[f"SKL-{prefix}-{num:03d}"] = count
        return duplicates

    def status(self) -> Dict[str, Any]:
        """Get status for all SKL prefixes."""
        self._prefix_ids = self._load_prefix_ids()
        return {
            'path': str(self.path),
            'total_skills': sum(len(v) for v in self._prefix_ids.values()),
            'prefixes': {
                prefix: {
                    'count': len(ids),
                    'highest': max(ids) if ids else 0,
                    'next': self._format_id(max(ids) + 1 if ids else 1, prefix)
                }
                for prefix, ids in sorted(self._prefix_ids.items())
            }
        }


class ForecastRegistry(RegistryManager):
    """Manager for forecast-registry.yaml (FCT-{DOMAIN}-{YYYY}-{NNN} format)."""

    def __init__(self):
        super().__init__(REPO_ROOT / 'data' / 'forecast-registry.yaml')
        self._domain_year_ids = None

    @property
    def id_pattern(self) -> str:
        return r'FCT-([A-Z]{2,4})-(\d{4})-(\d{3})'

    def _load_ids(self) -> List[int]:
        """Not used directly - see _load_domain_year_ids."""
        return []

    def _load_domain_year_ids(self) -> Dict[str, Dict[int, List[int]]]:
        """Load all FCT-DOM-YYYY-NNN IDs grouped by domain and year."""
        ids = defaultdict(lambda: defaultdict(list))
        if self.path.exists():
            content = self.path.read_text()
            matches = re.findall(r'id:\s*["\']?FCT-([A-Z]{2,4})-(\d{4})-(\d{3})["\']?', content)
            for domain, year, num in matches:
                ids[domain][int(year)].append(int(num))
        return ids

    def _get_domain_year_ids(self, domain: str, year: int, force_reload: bool = False) -> List[int]:
        """Get IDs for a specific domain and year."""
        if force_reload or self._domain_year_ids is None:
            self._domain_year_ids = self._load_domain_year_ids()
        return self._domain_year_ids.get(domain, {}).get(year, [])

    def _format_id(self, num: int, prefix: str = None) -> str:
        # prefix format: "DOMAIN-YEAR" e.g., "POL-2026"
        if not prefix or '-' not in prefix:
            year = datetime.now().year
            domain = prefix or 'OTH'
            return f"FCT-{domain}-{year}-{num:03d}"
        parts = prefix.split('-')
        domain = parts[0]
        year = parts[1] if len(parts) > 1 else datetime.now().year
        return f"FCT-{domain}-{year}-{num:03d}"

    def exists(self, entry_id: str) -> bool:
        """Check if a FCT-DOM-YYYY-NNN ID exists."""
        match = re.match(self.id_pattern, entry_id)
        if not match:
            return False
        domain, year, num = match.groups()
        return int(num) in self._get_domain_year_ids(domain, int(year))

    def next_id(self, prefix: str = None) -> str:
        """Get next available FCT ID. prefix = 'DOMAIN' or 'DOMAIN-YEAR'."""
        year = datetime.now().year
        domain = 'OTH'
        if prefix:
            if '-' in prefix:
                parts = prefix.split('-')
                domain = parts[0]
                year = int(parts[1]) if len(parts) > 1 else year
            else:
                domain = prefix
        ids = self._get_domain_year_ids(domain, year, force_reload=True)
        next_num = max(ids) + 1 if ids else 1
        return f"FCT-{domain}-{year}-{next_num:03d}"

    def _append_entry(self, entry: Dict, entry_id: str) -> None:
        """Append a new forecast - requires manual integration."""
        raise NotImplementedError(
            "Forecasts require manual integration into forecast-registry.yaml structure. "
            f"Use ID {entry_id} when adding manually."
        )

    def validate_all(self) -> Dict[str, List[str]]:
        """Check for duplicate DEFINITIONS only."""
        self._domain_year_ids = self._load_domain_year_ids()
        duplicates = {}
        for domain, years in self._domain_year_ids.items():
            for year, ids in years.items():
                seen = defaultdict(int)
                for num in ids:
                    seen[num] += 1
                for num, count in seen.items():
                    if count > 1:
                        duplicates[f"FCT-{domain}-{year}-{num:03d}"] = count
        return duplicates

    def status(self) -> Dict[str, Any]:
        """Get status for all FCT domains/years."""
        self._domain_year_ids = self._load_domain_year_ids()
        total = sum(sum(len(y) for y in d.values()) for d in self._domain_year_ids.values())
        domains = {}
        for domain, years in sorted(self._domain_year_ids.items()):
            domains[domain] = {
                'years': {
                    year: {
                        'count': len(ids),
                        'highest': max(ids) if ids else 0
                    }
                    for year, ids in sorted(years.items())
                },
                'total': sum(len(ids) for ids in years.values())
            }
        return {
            'path': str(self.path),
            'total_forecasts': total,
            'domains': domains
        }


class SessionRegistry(RegistryManager):
    """Manager for model-building-session.yaml (EBF-S-{YYYY}-{MM}-{DD}-{DOMAIN}-{SEQ} format)."""

    def __init__(self):
        super().__init__(REPO_ROOT / 'data' / 'model-building-session.yaml')
        self._domain_date_ids = None

    @property
    def id_pattern(self) -> str:
        return r'EBF-S-(\d{4})-(\d{2})-(\d{2})-([A-Z]{2,4})-(\d{3})'

    def _load_ids(self) -> List[int]:
        """Not used directly - see _load_domain_date_ids."""
        return []

    def _load_domain_date_ids(self) -> Dict[str, Dict[str, List[int]]]:
        """Load all EBF-S-YYYY-MM-DD-DOM-SEQ IDs grouped by domain and date."""
        ids = defaultdict(lambda: defaultdict(list))
        if self.path.exists():
            content = self.path.read_text()
            pattern = r'id:\s*["\']?EBF-S-(\d{4})-(\d{2})-(\d{2})-([A-Z]{2,4})-(\d{3})["\']?'
            matches = re.findall(pattern, content)
            for year, month, day, domain, seq in matches:
                date_key = f"{year}-{month}-{day}"
                ids[domain][date_key].append(int(seq))
        return ids

    def _format_id(self, num: int, prefix: str = None) -> str:
        # prefix format: "DOMAIN" or "DOMAIN-YYYY-MM-DD"
        today = datetime.now()
        date_str = today.strftime('%Y-%m-%d')
        domain = 'OTH'
        if prefix:
            if '-' in prefix and len(prefix) > 4:  # Has date
                parts = prefix.split('-', 1)
                domain = parts[0]
                date_str = parts[1] if len(parts) > 1 else date_str
            else:
                domain = prefix
        return f"EBF-S-{date_str}-{domain}-{num:03d}"

    def _get_domain_date_ids(self, domain: str, date_str: str, force_reload: bool = False) -> List[int]:
        """Get IDs for a specific domain and date."""
        if force_reload or self._domain_date_ids is None:
            self._domain_date_ids = self._load_domain_date_ids()
        return self._domain_date_ids.get(domain, {}).get(date_str, [])

    def exists(self, entry_id: str) -> bool:
        """Check if a session ID exists."""
        match = re.match(self.id_pattern, entry_id)
        if not match:
            return False
        year, month, day, domain, seq = match.groups()
        date_str = f"{year}-{month}-{day}"
        return int(seq) in self._get_domain_date_ids(domain, date_str)

    def next_id(self, prefix: str = None) -> str:
        """Get next available session ID. prefix = 'DOMAIN' or 'DOMAIN-YYYY-MM-DD'."""
        today = datetime.now()
        date_str = today.strftime('%Y-%m-%d')
        domain = 'OTH'
        if prefix:
            if '-' in prefix and len(prefix) > 4:  # Has date
                parts = prefix.split('-', 1)
                domain = parts[0]
                date_str = parts[1]
            else:
                domain = prefix
        ids = self._get_domain_date_ids(domain, date_str, force_reload=True)
        next_num = max(ids) + 1 if ids else 1
        return f"EBF-S-{date_str}-{domain}-{next_num:03d}"

    def _append_entry(self, entry: Dict, entry_id: str) -> None:
        """Append a new session - requires manual integration."""
        raise NotImplementedError(
            "Sessions require manual integration into model-building-session.yaml structure. "
            f"Use ID {entry_id} when adding manually."
        )

    def validate_all(self) -> Dict[str, List[str]]:
        """Check for duplicate DEFINITIONS only."""
        self._domain_date_ids = self._load_domain_date_ids()
        duplicates = {}
        for domain, dates in self._domain_date_ids.items():
            for date_str, ids in dates.items():
                seen = defaultdict(int)
                for num in ids:
                    seen[num] += 1
                for num, count in seen.items():
                    if count > 1:
                        duplicates[f"EBF-S-{date_str}-{domain}-{num:03d}"] = count
        return duplicates

    def status(self) -> Dict[str, Any]:
        """Get status for all sessions by domain."""
        self._domain_date_ids = self._load_domain_date_ids()
        total = sum(sum(len(d) for d in dates.values()) for dates in self._domain_date_ids.values())
        domains = {}
        for domain, dates in sorted(self._domain_date_ids.items()):
            domains[domain] = {
                'count': sum(len(ids) for ids in dates.values()),
                'dates': len(dates),
                'latest': max(dates.keys()) if dates else None
            }
        return {
            'path': str(self.path),
            'total_sessions': total,
            'domains': domains,
            'next_for_today': self.next_id()
        }


class InterventionRegistry(RegistryManager):
    """Manager for intervention-registry.yaml (PRJ-XXX format)."""

    def __init__(self):
        super().__init__(REPO_ROOT / 'data' / 'intervention-registry.yaml')

    @property
    def id_pattern(self) -> str:
        return r'PRJ-(\d+)'

    def _load_ids(self) -> List[int]:
        """Extract all PRJ-XXX IDs from intervention-registry.yaml."""
        ids = []
        if self.path.exists():
            content = self.path.read_text()
            # Match PRJ-XXX in keys or id fields
            matches = re.findall(r'PRJ-(\d+)', content)
            ids = list(set(int(m) for m in matches))  # Unique only
        return ids

    def validate_all(self) -> Dict[str, List[str]]:
        """Check for duplicate DEFINITIONS only."""
        ids = self._load_ids()
        seen = defaultdict(int)
        for num in ids:
            seen[num] += 1
        return {f"PRJ-{k}": v for k, v in seen.items() if v > 1}

    def _format_id(self, num: int, prefix: str = None) -> str:
        return f"PRJ-{num:03d}"

    def _append_entry(self, entry: Dict, entry_id: str) -> None:
        """Append a new intervention project - requires manual integration."""
        raise NotImplementedError(
            "Intervention projects require manual integration into intervention-registry.yaml structure. "
            f"Use ID {entry_id} when adding manually."
        )


class ResearcherRegistry(RegistryManager):
    """Manager for researcher-registry.yaml (RES-{LASTNAME}-{INITIAL} format)."""

    def __init__(self):
        super().__init__(REPO_ROOT / 'data' / 'researcher-registry.yaml')

    @property
    def id_pattern(self) -> str:
        return r'RES-([A-Z]+)-([A-Z])'

    def _load_ids(self) -> List[int]:
        """Not applicable for name-based IDs."""
        return []

    def _load_researcher_ids(self) -> List[str]:
        """Load all RES-NAME-X IDs."""
        ids = []
        if self.path.exists():
            content = self.path.read_text()
            matches = re.findall(r'RES-([A-Z]+-[A-Z])', content)
            ids = list(set(f"RES-{m}" for m in matches))
        return ids

    def _format_id(self, num: int, prefix: str = None) -> str:
        # For researchers, the "prefix" is actually the full name pattern
        if not prefix:
            raise ValueError("Researcher ID requires name (e.g., 'FEHR-E')")
        return f"RES-{prefix.upper()}"

    def exists(self, entry_id: str) -> bool:
        """Check if a researcher ID exists."""
        ids = self._load_researcher_ids()
        return entry_id.upper() in [i.upper() for i in ids]

    def next_id(self, prefix: str = None) -> str:
        """For researchers, just validate/return the provided ID."""
        if not prefix:
            raise ValueError("Researcher ID requires name (e.g., 'FEHR-E' for Ernst Fehr)")
        res_id = f"RES-{prefix.upper()}"
        if self.exists(res_id):
            raise DuplicateIDError(f"Researcher {res_id} already exists")
        return res_id

    def _append_entry(self, entry: Dict, entry_id: str) -> None:
        """Append a new researcher - requires manual integration."""
        raise NotImplementedError(
            "Researchers require manual integration into researcher-registry.yaml structure. "
            f"Use ID {entry_id} when adding manually."
        )

    def validate_all(self) -> Dict[str, List[str]]:
        """Check for duplicate researcher IDs."""
        if not self.path.exists():
            return {}
        content = self.path.read_text()
        matches = re.findall(r'RES-([A-Z]+-[A-Z])', content)
        seen = defaultdict(int)
        for m in matches:
            seen[f"RES-{m}"] += 1
        return {k: v for k, v in seen.items() if v > 1}

    def status(self) -> Dict[str, Any]:
        """Get status of researcher registry."""
        ids = self._load_researcher_ids()
        return {
            'path': str(self.path),
            'total_researchers': len(ids),
            'researchers': sorted(ids)[:10] if len(ids) > 10 else sorted(ids),
            'duplicates': self.validate_all()
        }


class FormulaRegistry(RegistryManager):
    """Manager for formula-registry.yaml (FRM-XXX format)."""

    def __init__(self):
        super().__init__(REPO_ROOT / 'data' / 'formula-registry.yaml')

    @property
    def id_pattern(self) -> str:
        return r'FRM-(\d+)'

    def _load_ids(self) -> List[int]:
        """Extract all FRM-XXX IDs from formula-registry.yaml."""
        ids = []
        if self.path.exists():
            content = self.path.read_text()
            # Match formula definitions
            matches = re.findall(r'id:\s*["\']?FRM-(\d+)["\']?', content)
            ids = [int(m) for m in matches]
        return ids

    def validate_all(self) -> Dict[str, List[str]]:
        """Check for duplicate DEFINITIONS only."""
        ids = self._load_ids()
        seen = defaultdict(int)
        for num in ids:
            seen[num] += 1
        return {f"FRM-{k}": v for k, v in seen.items() if v > 1}

    def _format_id(self, num: int, prefix: str = None) -> str:
        return f"FRM-{num:03d}"

    def _append_entry(self, entry: Dict, entry_id: str) -> None:
        """Append a new formula - requires manual integration."""
        raise NotImplementedError(
            "Formulas require manual integration into formula-registry.yaml structure. "
            f"Use ID {entry_id} when adding manually."
        )


# Convenience function for quick access
def get_registry(registry_type: str) -> RegistryManager:
    """
    Get a registry manager by type.

    Args:
        registry_type: One of 'case', 'category', 'theory', 'parameter', 'model',
                       'output', 'skill', 'forecast', 'session', 'intervention',
                       'researcher', 'formula'

    Returns:
        The appropriate RegistryManager instance
    """
    registries = {
        # Original registries
        'case': CaseRegistry,
        'cas': CaseRegistry,
        'category': TheoryCategoryRegistry,
        'cat': TheoryCategoryRegistry,
        'theory': TheoryModelRegistry,
        'ms': TheoryModelRegistry,
        'parameter': ParameterRegistry,
        'par': ParameterRegistry,
        # New registries (v1.27)
        'model': ModelRegistry,
        'mod': ModelRegistry,
        'output': OutputRegistry,
        'out': OutputRegistry,
        'skill': SkillRegistry,
        'skl': SkillRegistry,
        'forecast': ForecastRegistry,
        'fct': ForecastRegistry,
        'session': SessionRegistry,
        'ses': SessionRegistry,
        'intervention': InterventionRegistry,
        'prj': InterventionRegistry,
        'researcher': ResearcherRegistry,
        'res': ResearcherRegistry,
        'formula': FormulaRegistry,
        'frm': FormulaRegistry,
    }

    registry_type = registry_type.lower()
    if registry_type not in registries:
        raise ValueError(f"Unknown registry type: {registry_type}. Use one of: {list(set(registries.keys()))}")

    return registries[registry_type]()


# CLI Interface
def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='EBF Registry Manager - Proactive Duplicate Prevention',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get next available case ID
  python registry_manager.py case --next

  # Get next theory ID for Crisis Management prefix
  python registry_manager.py theory --next --prefix CM

  # Check if an ID exists
  python registry_manager.py case --exists CAS-500

  # Show status of all registries
  python registry_manager.py --status

  # Add a new case (interactive)
  python registry_manager.py case --add --name "My Case" --domain finance,behavior
        """
    )

    parser.add_argument('registry', nargs='?',
                        choices=['case', 'category', 'theory', 'parameter', 'model',
                                 'output', 'skill', 'forecast', 'session', 'intervention',
                                 'researcher', 'formula'],
                        help='Registry type')
    parser.add_argument('--next', action='store_true', help='Get next available ID')
    parser.add_argument('--exists', metavar='ID', help='Check if ID exists')
    parser.add_argument('--prefix', help='Prefix for MS/PAR IDs (e.g., CM, BEH)')
    parser.add_argument('--status', action='store_true', help='Show status of all registries')
    parser.add_argument('--validate', action='store_true', help='Check for duplicates')

    args = parser.parse_args()

    if args.status:
        print("=" * 70)
        print("EBF REGISTRY MANAGER STATUS")
        print("=" * 70)

        all_registries = [
            ('Case', CaseRegistry),
            ('Category', TheoryCategoryRegistry),
            ('Theory', TheoryModelRegistry),
            ('Parameter', ParameterRegistry),
            ('Model', ModelRegistry),
            ('Output', OutputRegistry),
            ('Skill', SkillRegistry),
            ('Forecast', ForecastRegistry),
            ('Session', SessionRegistry),
            ('Intervention', InterventionRegistry),
            ('Researcher', ResearcherRegistry),
            ('Formula', FormulaRegistry),
        ]

        for name, cls in all_registries:
            print(f"\n{name} Registry:")
            try:
                reg = cls()
                status = reg.status()

                # Handle different status formats
                if 'count' in status:
                    print(f"  Count: {status['count']}, Highest: {status['highest']}")
                    print(f"  Next available: {status['next_available']}")
                elif 'prefixes' in status:
                    total_key = [k for k in status.keys() if k.startswith('total_')][0] if any(k.startswith('total_') for k in status.keys()) else None
                    total = status.get(total_key, 0) if total_key else 0
                    print(f"  Total: {total}")
                    for prefix, info in list(status['prefixes'].items())[:5]:
                        print(f"    {prefix}: {info['count']} entries, next = {info['next']}")
                    if len(status['prefixes']) > 5:
                        print(f"    ... and {len(status['prefixes']) - 5} more prefixes")
                elif 'domains' in status:
                    total_key = [k for k in status.keys() if k.startswith('total_')][0] if any(k.startswith('total_') for k in status.keys()) else None
                    total = status.get(total_key, 0) if total_key else 0
                    print(f"  Total: {total}")
                    for domain, info in list(status['domains'].items())[:5]:
                        if isinstance(info, dict):
                            count = info.get('count', info.get('total', 0))
                            print(f"    {domain}: {count} entries")
                elif 'total_researchers' in status:
                    print(f"  Total researchers: {status['total_researchers']}")
                    if status.get('researchers'):
                        print(f"    Examples: {', '.join(status['researchers'][:5])}")
                elif 'next_for_today' in status:
                    print(f"  Total sessions: {status.get('total_sessions', 0)}")
                    print(f"  Next for today: {status['next_for_today']}")

                dups = status.get('duplicates', {})
                if dups:
                    print(f"  ⚠️  DUPLICATES: {dups}")
                else:
                    print(f"  ✅ No duplicates")
            except Exception as e:
                print(f"  Error: {e}")

        print()
        return 0

    if not args.registry:
        parser.print_help()
        return 1

    try:
        registry = get_registry(args.registry)

        if args.next:
            print(registry.next_id(args.prefix))
        elif args.exists:
            if registry.exists(args.exists):
                print(f"✅ {args.exists} EXISTS")
                return 0
            else:
                print(f"❌ {args.exists} AVAILABLE")
                return 1
        elif args.validate:
            dups = registry.validate_all()
            if dups:
                print(f"❌ DUPLICATES FOUND: {dups}")
                return 1
            else:
                print("✅ No duplicates")
                return 0
        else:
            status = registry.status()
            print(yaml.dump(status, default_flow_style=False))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
