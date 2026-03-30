"""
Business logic for activity management in Mergington High School API
"""

from typing import Dict, Any, Union


class SuccessResult:
    """Represents a successful operation result"""
    def __init__(self, message: str, data: Dict[str, Any] = None):
        self.message = message
        self.data = data or {}


class ErrorResult:
    """Represents an error operation result"""
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code


def signup_for_activity_logic(
    activities: Dict[str, Dict[str, Any]],
    activity_name: str,
    email: str
) -> Union[SuccessResult, ErrorResult]:
    """
    Business logic for signing up a student for an activity
    
    Args:
        activities: Dictionary of all activities
        activity_name: Name of the activity to sign up for
        email: Student email address
        
    Returns:
        SuccessResult if signup successful, ErrorResult if failed
    """
    # Validate activity exists
    if activity_name not in activities:
        return ErrorResult("Activity not found", code=404)
    
    activity = activities[activity_name]
    
    # Validate student is not already signed up
    if email in activity["participants"]:
        return ErrorResult("Student is already signed up for this activity", code=400)
    
    # Validate activity is not at max capacity
    if len(activity["participants"]) >= activity["max_participants"]:
        return ErrorResult("Activity is at maximum capacity", code=400)
    
    # Add student
    activity["participants"].append(email)
    return SuccessResult(f"Signed up {email} for {activity_name}")


def remove_from_activity_logic(
    activities: Dict[str, Dict[str, Any]],
    activity_name: str,
    email: str
) -> Union[SuccessResult, ErrorResult]:
    """
    Business logic for removing a student from an activity
    
    Args:
        activities: Dictionary of all activities
        activity_name: Name of the activity to remove from
        email: Student email address
        
    Returns:
        SuccessResult if removal successful, ErrorResult if failed
    """
    # Validate activity exists
    if activity_name not in activities:
        return ErrorResult("Activity not found", code=404)
    
    activity = activities[activity_name]
    
    # Validate student is signed up
    if email not in activity["participants"]:
        return ErrorResult("Student is not signed up for this activity", code=400)
    
    # Remove student
    activity["participants"].remove(email)
    return SuccessResult(f"Removed {email} from {activity_name}")