"""
File Manager

Handles file creation, writing, and directory management.
"""

import os
import shutil
from pathlib import Path
from typing import List, Union


class FileManager:
    """File manager for handling file operations."""

    def __init__(self, base_directory: Union[str, Path]):
        """
        Initialize the file manager.
        
        Args:
            base_directory: Base directory for file operations
        """
        self.base_directory = Path(base_directory)

    async def write_file(self, file_path: Union[str, Path], content: str) -> None:
        """
        Write content to a file.
        
        Args:
            file_path: Relative path to the file
            content: Content to write to the file
        """
        full_path = self.base_directory / file_path
        
        # Ensure directory exists
        await self.ensure_directory(full_path.parent)
        
        # Write file
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)

    async def ensure_directory(self, directory: Union[str, Path]) -> None:
        """
        Ensure a directory exists.
        
        Args:
            directory: Directory path to ensure exists
        """
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)

    async def read_file(self, file_path: Union[str, Path]) -> str:
        """
        Read file content.
        
        Args:
            file_path: Relative path to the file
            
        Returns:
            File content as string
        """
        full_path = self.base_directory / file_path
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()

    async def file_exists(self, file_path: Union[str, Path]) -> bool:
        """
        Check if a file exists.
        
        Args:
            file_path: Relative path to the file
            
        Returns:
            True if file exists, False otherwise
        """
        full_path = self.base_directory / file_path
        return full_path.exists() and full_path.is_file()

    async def delete_file(self, file_path: Union[str, Path]) -> None:
        """
        Delete a file.
        
        Args:
            file_path: Relative path to the file
        """
        full_path = self.base_directory / file_path
        if full_path.exists():
            full_path.unlink()

    async def list_directory(self, dir_path: Union[str, Path] = "") -> List[str]:
        """
        List directory contents.
        
        Args:
            dir_path: Relative directory path
            
        Returns:
            List of file and directory names
        """
        full_path = self.base_directory / dir_path
        if full_path.exists() and full_path.is_dir():
            return [item.name for item in full_path.iterdir()]
        return []

    async def copy_file(self, source_path: Union[str, Path], target_path: Union[str, Path]) -> None:
        """
        Copy a file.
        
        Args:
            source_path: Source file path
            target_path: Target file path
        """
        source_full_path = self.base_directory / source_path
        target_full_path = self.base_directory / target_path
        
        # Ensure target directory exists
        await self.ensure_directory(target_full_path.parent)
        
        # Copy file
        shutil.copy2(source_full_path, target_full_path)

    def get_full_path(self, relative_path: Union[str, Path]) -> Path:
        """
        Get full path from relative path.
        
        Args:
            relative_path: Relative path
            
        Returns:
            Full path as Path object
        """
        return self.base_directory / relative_path
