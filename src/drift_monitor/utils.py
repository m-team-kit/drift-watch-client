"""Utility functions for drift monitor."""

import numpy as np


def convert_to_serializable(obj):
    """Recursively convert objects to JSON serializable formats."""
    if isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_to_serializable(element) for element in obj]
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.generic, np.number)):
        return obj.item()
    return obj
