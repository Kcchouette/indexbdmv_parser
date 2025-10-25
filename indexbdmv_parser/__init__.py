#!/usr/bin/env python3
"""
INDEX.BDMV Parser Module
Parses Blu-ray INDEX.BDMV files to detect UHD version like BDInfo
"""

import struct
import os
from typing import Optional
from pathlib import Path


class IndexBDMV:
    """
    Object containing information on Blu-ray INDEX.BDMV files
    """
    def __init__(self, filename: str):
        """
        Parse a Blu-ray INDEX.BDMV file to detect UHD version

        Args:
            filename: Path to the INDEX.BDMV file to be parsed

        Raises:
            ValueError: If parsing fails
            FileNotFoundError: If file doesn't exist
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"INDEX.BDMV file not found: {filename}")

        self.filename = filename
        self.is_uhd = False
        self.version = None

        # Parse INDEX.BDMV to detect version like BDInfo does
        with open(filename, mode="rb") as f:
            # Read first 8 bytes to get version indicator
            buffer = f.read(8)
            if len(buffer) >= 4:
                # Extract version string (first 4 bytes)
                version_bytes = buffer[:4]
                try:
                    self.version = version_bytes.decode('ascii', errors='ignore').rstrip('\0')
                    # BDInfo checks if version is "INDX0300" for UHD
                    self.is_uhd = self.version == "INDX0300"
                except:
                    self.version = None
                    self.is_uhd = False

    def __repr__(self):
        return "<IndexBDMV " + ", ".join([
            f"version='{self.version}'",
            f"is_uhd={self.is_uhd}"
        ]) + ">"


def find_index_file(directory: str) -> Optional[str]:
    """
    Find INDEX.BDMV file in Blu-ray directory structure

    Args:
        directory: Directory to search

    Returns:
        Path to INDEX.BDMV file or None if not found
    """
    directory_path = Path(directory)

    # Standard Blu-ray structure
    index_path = directory_path / "BDMV" / "INDEX.BDMV"
    if index_path.exists():
        return str(index_path)

    # Alternative location
    index_path = directory_path / "INDEX.BDMV"
    if index_path.exists():
        return str(index_path)

    # Check case variations
    for path in directory_path.rglob("INDEX.BDMV"):
        return str(path)
    for path in directory_path.rglob("index.bdmv"):
        return str(path)

    return None


def is_uhd_disc(directory: str) -> bool:
    """
    Check if a Blu-ray directory contains a UHD disc

    Args:
        directory: Blu-ray directory

    Returns:
        True if UHD, False otherwise
    """
    index_file = find_index_file(directory)
    if not index_file:
        return False

    try:
        index = IndexBDMV(index_file)
        return index.is_uhd
    except Exception:
        return False
