"""
Logging configuration for the Spotify AI Music Recommendation System.

This module provides centralized logging configuration with appropriate
levels, formatters, and handlers for different components.
"""

import logging
import logging.handlers
import os
from pathlib import Path
from typing import Optional


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    log_dir: str = "logs",
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
    console_output: bool = True,
) -> logging.Logger:
    """
    Set up logging configuration for the application.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Name of log file (None for default based on app name)
        log_dir: Directory to store log files
        max_bytes: Maximum size of log file before rotation
        backup_count: Number of backup log files to keep
        console_output: Whether to also output logs to console

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger("spotify_ai")
    logger.setLevel(getattr(logging, log_level.upper()))

    # Clear any existing handlers
    logger.handlers.clear()

    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    simple_formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S"
    )

    # Add console handler if requested
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        logger.addHandler(console_handler)

    # Add file handler if log file is specified or can be created
    if log_file or log_dir:
        try:
            # Create log directory if it doesn't exist
            log_path = Path(log_dir)
            log_path.mkdir(exist_ok=True)

            # Determine log file name
            if not log_file:
                log_file = "spotify_ai.log"

            log_file_path = log_path / log_file

            # Create rotating file handler
            file_handler = logging.handlers.RotatingFileHandler(
                log_file_path,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding="utf-8",
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(detailed_formatter)
            logger.addHandler(file_handler)

        except (OSError, PermissionError) as e:
            # Log setup error to console if file logging fails
            console_logger = logging.getLogger("console_fallback")
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(simple_formatter)
            console_logger.addHandler(console_handler)
            console_logger.warning(f"Could not set up file logging: {e}")

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.

    Args:
        name: Name of the module/component requesting the logger

    Returns:
        Logger instance
    """
    return logging.getLogger(f"spotify_ai.{name}")


def log_api_request(
    logger: logging.Logger, endpoint: str, params: dict, response_time: float
):
    """
    Log API request details for monitoring.

    Args:
        logger: Logger instance to use
        endpoint: API endpoint that was called
        params: Parameters sent with the request
        response_time: Time taken for the request in seconds
    """
    logger.info(
        f"API Request - Endpoint: {endpoint}, "
        f"Params: {len(params)} items, "
        f"Response time: {response_time:.3f}s"
    )


def log_recommendation_request(
    logger: logging.Logger,
    song_name: str,
    artist_name: Optional[str],
    playlist_size: int,
    processing_time: float,
    success: bool,
):
    """
    Log recommendation request details for analytics.

    Args:
        logger: Logger instance to use
        song_name: Name of the song requested
        artist_name: Name of the artist (if provided)
        playlist_size: Number of recommendations requested
        processing_time: Time taken to process the request
        success: Whether the request was successful
    """
    status = "SUCCESS" if success else "FAILED"
    logger.info(
        f"Recommendation Request [{status}] - "
        f"Song: '{song_name}', "
        f"Artist: '{artist_name or 'N/A'}', "
        f"Size: {playlist_size}, "
        f"Time: {processing_time:.3f}s"
    )


def log_performance_metrics(
    logger: logging.Logger,
    operation: str,
    duration: float,
    memory_used: Optional[float] = None,
    items_processed: Optional[int] = None,
):
    """
    Log performance metrics for monitoring.

    Args:
        logger: Logger instance to use
        operation: Name of the operation being measured
        duration: Time taken in seconds
        memory_used: Memory usage in MB (optional)
        items_processed: Number of items processed (optional)
    """
    metrics = [f"Operation: {operation}", f"Duration: {duration:.3f}s"]

    if memory_used is not None:
        metrics.append(f"Memory: {memory_used:.2f}MB")

    if items_processed is not None:
        metrics.append(f"Items: {items_processed}")

    logger.info(f"Performance Metrics - {', '.join(metrics)}")


# Initialize default logger if this module is imported
_default_logger = None


def init_default_logging():
    """Initialize default logging configuration."""
    global _default_logger
    if _default_logger is None:
        log_level = os.getenv("LOG_LEVEL", "INFO")
        log_dir = os.getenv("LOG_DIR", "logs")
        _default_logger = setup_logging(
            log_level=log_level, log_dir=log_dir, console_output=True
        )
    return _default_logger


# Auto-initialize when module is imported
init_default_logging()
