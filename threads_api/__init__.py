"""
Threads API - Unofficial Python Automation Toolkit for Meta Threads
"""

from .auth import SessionAuth
from .client import ThreadsClient
from .media import MediaUploader

# Alias ThreadsBot to ThreadsClient for backward compatibility
ThreadsBot = ThreadsClient

__version__ = "1.0.0"
__all__ = ["ThreadsClient", "ThreadsBot", "SessionAuth", "MediaUploader"]
