"""
Unit tests for business logic functions
"""

import pytest
from src.business_logic import (
    signup_for_activity_logic,
    remove_from_activity_logic,
    SuccessResult,
    ErrorResult
)


@pytest.fixture
def sample_activities():
    """Fixture providing sample activities data"""
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 2,
            "participants": ["michael@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 2,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 1,
            "participants": []
        }
    }


class TestSignupForActivityLogic:
    """Test cases for signup_for_activity_logic function"""

    def test_successful_signup(self, sample_activities):
        """Test successful signup for an activity"""
        result = signup_for_activity_logic(
            sample_activities,
            "Chess Club",
            "daniel@mergington.edu"
        )
        
        assert isinstance(result, SuccessResult)
        assert "daniel@mergington.edu" in sample_activities["Chess Club"]["participants"]
        assert result.message == "Signed up daniel@mergington.edu for Chess Club"

    def test_signup_activity_not_found(self, sample_activities):
        """Test signup for non-existent activity"""
        result = signup_for_activity_logic(
            sample_activities,
            "Nonexistent Activity",
            "test@mergington.edu"
        )
        
        assert isinstance(result, ErrorResult)
        assert result.code == 404
        assert result.message == "Activity not found"

    def test_signup_already_signed_up(self, sample_activities):
        """Test signup when student is already signed up"""
        result = signup_for_activity_logic(
            sample_activities,
            "Chess Club",
            "michael@mergington.edu"
        )
        
        assert isinstance(result, ErrorResult)
        assert result.code == 400
        assert "already signed up" in result.message

    def test_signup_activity_at_capacity(self, sample_activities):
        """Test signup when activity is at maximum capacity"""
        result = signup_for_activity_logic(
            sample_activities,
            "Programming Class",
            "new_student@mergington.edu"
        )
        
        assert isinstance(result, ErrorResult)
        assert result.code == 400
        assert "maximum capacity" in result.message

    def test_signup_empty_activity_name(self, sample_activities):
        """Test signup with empty activity name"""
        result = signup_for_activity_logic(
            sample_activities,
            "",
            "test@mergington.edu"
        )
        
        assert isinstance(result, ErrorResult)
        assert result.code == 404

    def test_signup_empty_email(self, sample_activities):
        """Test signup with empty email"""
        result = signup_for_activity_logic(
            sample_activities,
            "Chess Club",
            ""
        )
        
        assert isinstance(result, SuccessResult)
        assert "" in sample_activities["Chess Club"]["participants"]


class TestRemoveFromActivityLogic:
    """Test cases for remove_from_activity_logic function"""

    def test_successful_removal(self, sample_activities):
        """Test successful removal from an activity"""
        result = remove_from_activity_logic(
            sample_activities,
            "Chess Club",
            "michael@mergington.edu"
        )
        
        assert isinstance(result, SuccessResult)
        assert "michael@mergington.edu" not in sample_activities["Chess Club"]["participants"]
        assert result.message == "Removed michael@mergington.edu from Chess Club"

    def test_remove_activity_not_found(self, sample_activities):
        """Test removal from non-existent activity"""
        result = remove_from_activity_logic(
            sample_activities,
            "Nonexistent Activity",
            "test@mergington.edu"
        )
        
        assert isinstance(result, ErrorResult)
        assert result.code == 404
        assert result.message == "Activity not found"

    def test_remove_not_signed_up(self, sample_activities):
        """Test removal when student is not signed up"""
        result = remove_from_activity_logic(
            sample_activities,
            "Chess Club",
            "not_signed_up@mergington.edu"
        )
        
        assert isinstance(result, ErrorResult)
        assert result.code == 400
        assert "not signed up" in result.message

    def test_remove_empty_activity_name(self, sample_activities):
        """Test removal with empty activity name"""
        result = remove_from_activity_logic(
            sample_activities,
            "",
            "michael@mergington.edu"
        )
        
        assert isinstance(result, ErrorResult)
        assert result.code == 404

    def test_remove_empty_email(self, sample_activities):
        """Test removal with empty email"""
        result = remove_from_activity_logic(
            sample_activities,
            "Chess Club",
            ""
        )
        
        assert isinstance(result, ErrorResult)
        assert result.code == 400