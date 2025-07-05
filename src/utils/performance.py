"""
Performance monitoring utilities for the Spotify AI system.

This module provides tools for measuring and monitoring application performance,
including response times, memory usage, and system metrics.
"""

import functools
import time
from contextlib import contextmanager
from typing import Callable, Generator, Optional

import psutil

from .logging_config import get_logger

logger = get_logger("performance")


class PerformanceMonitor:
    """
    Context manager and decorator for monitoring function performance.

    Usage as context manager:
        with PerformanceMonitor("operation_name"):
            # code to monitor
            pass

    Usage as decorator:
        @PerformanceMonitor.monitor("function_name")
        def my_function():
            pass
    """

    def __init__(self, operation_name: str, log_result: bool = True):
        self.operation_name = operation_name
        self.log_result = log_result
        self.start_time = None
        self.start_memory = None
        self.duration = None
        self.memory_used = None

    def __enter__(self):
        self.start_time = time.time()
        self.start_memory = self._get_memory_usage()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.duration = time.time() - self.start_time
        current_memory = self._get_memory_usage()
        if self.start_memory is not None and current_memory is not None:
            self.memory_used = current_memory - self.start_memory

        if self.log_result:
            self._log_performance()

    @staticmethod
    def _get_memory_usage() -> Optional[float]:
        """Get current memory usage in MB."""
        try:
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024  # Convert to MB
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None

    def _log_performance(self):
        """Log performance metrics."""
        metrics = [f"Operation: {self.operation_name}"]

        if self.duration is not None:
            metrics.append(f"Duration: {self.duration:.3f}s")

        if self.memory_used is not None:
            metrics.append(f"Memory: {self.memory_used:+.2f}MB")

        logger.info(f"Performance - {', '.join(metrics)}")

    @classmethod
    def monitor(cls, operation_name: str, log_result: bool = True):
        """
        Decorator for monitoring function performance.

        Args:
            operation_name: Name of the operation being monitored
            log_result: Whether to automatically log the results
        """

        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                with cls(operation_name, log_result):
                    return func(*args, **kwargs)

            return wrapper

        return decorator


@contextmanager
def monitor_operation(operation_name: str) -> Generator[PerformanceMonitor, None, None]:
    """
    Context manager for monitoring operation performance.

    Args:
        operation_name: Name of the operation being monitored

    Yields:
        PerformanceMonitor instance for accessing metrics
    """
    monitor = PerformanceMonitor(operation_name)
    with monitor:
        yield monitor


def measure_response_time(func: Callable) -> Callable:
    """
    Simple decorator to measure and log function response time.

    Args:
        func: Function to measure

    Returns:
        Wrapped function with timing
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f"Function '{func.__name__}' completed in {duration:.3f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                f"Function '{func.__name__}' failed after {duration:.3f}s: {e}"
            )
            raise

    return wrapper


class SystemMetrics:
    """Utility class for collecting system metrics."""

    @staticmethod
    def get_memory_info() -> dict:
        """Get current memory information."""
        try:
            memory = psutil.virtual_memory()
            return {
                "total_mb": memory.total / 1024 / 1024,
                "available_mb": memory.available / 1024 / 1024,
                "used_mb": memory.used / 1024 / 1024,
                "percent": memory.percent,
            }
        except Exception as e:
            logger.warning(f"Could not retrieve memory info: {e}")
            return {}

    @staticmethod
    def get_cpu_info() -> dict:
        """Get current CPU information."""
        try:
            return {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "cpu_count": psutil.cpu_count(),
                "load_avg": (
                    psutil.getloadavg() if hasattr(psutil, "getloadavg") else None
                ),
            }
        except Exception as e:
            logger.warning(f"Could not retrieve CPU info: {e}")
            return {}

    @staticmethod
    def get_disk_info() -> dict:
        """Get current disk information."""
        try:
            disk = psutil.disk_usage("/")
            return {
                "total_gb": disk.total / 1024 / 1024 / 1024,
                "used_gb": disk.used / 1024 / 1024 / 1024,
                "free_gb": disk.free / 1024 / 1024 / 1024,
                "percent": (disk.used / disk.total) * 100,
            }
        except Exception as e:
            logger.warning(f"Could not retrieve disk info: {e}")
            return {}

    @classmethod
    def get_all_metrics(cls) -> dict:
        """Get all available system metrics."""
        return {
            "memory": cls.get_memory_info(),
            "cpu": cls.get_cpu_info(),
            "disk": cls.get_disk_info(),
            "timestamp": time.time(),
        }


def log_system_metrics():
    """Log current system metrics."""
    metrics = SystemMetrics.get_all_metrics()

    if metrics.get("memory"):
        memory = metrics["memory"]
        logger.info(
            f"Memory Usage: {memory.get('used_mb', 0):.1f}MB "
            f"({memory.get('percent', 0):.1f}%) of "
            f"{memory.get('total_mb', 0):.1f}MB total"
        )

    if metrics.get("cpu"):
        cpu = metrics["cpu"]
        logger.info(f"CPU Usage: {cpu.get('cpu_percent', 0):.1f}%")

    if metrics.get("disk"):
        disk = metrics["disk"]
        logger.info(
            f"Disk Usage: {disk.get('used_gb', 0):.1f}GB "
            f"({disk.get('percent', 0):.1f}%) of "
            f"{disk.get('total_gb', 0):.1f}GB total"
        )


# Performance monitoring decorator for common operations
monitor_ml_operation = PerformanceMonitor.monitor("ml_operation")
monitor_api_request = PerformanceMonitor.monitor("api_request")
monitor_recommendation = PerformanceMonitor.monitor("recommendation_generation")
