"""SQLModel models and enums for the application."""

from enum import Enum


class TaskStatus(str, Enum):
    """Task status enum."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskPriority(str, Enum):
    """Task priority enum."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class MessageRole(str, Enum):
    """Message role enum for chat messages."""
    USER = "user"
    ASSISTANT = "assistant"
