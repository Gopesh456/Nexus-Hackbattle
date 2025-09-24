"""
Integration tool for health agents to use the database-or-input pattern.
This tool bridges the Django backend with the CrewAI health agents.
"""

import requests
import json
from typing import Dict, Any, Optional, List


class HealthDataIntegration:
    """
    Integration class to connect health agents with the database-or-input system.
    """
    
    def __init__(self, base_url: str = "http://localhost:8000", user_id: int = 1):
        self.base_url = base_url
        self.user_id = user_id
    
    def get_user_profile_or_prompt(self, user_input_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Get user profile from database or use provided input data.
        
        Args:
            user_input_data: Optional user input data if prompting for new info
            
        Returns:
            User profile data
        """
        try:
            if user_input_data:
                # POST new user data
                response = requests.post(
                    f"{self.base_url}/healthapp/api/profile/",
                    data=json.dumps({**user_input_data, 'user_id': self.user_id}),
                    headers={'Content-Type': 'application/json'}
                )
            else:
                # GET existing data
                response = requests.get(
                    f"{self.base_url}/healthapp/api/profile/",
                    params={'user_id': self.user_id}
                )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'success': False, 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_medicine_data_or_prompt(self, medicine_name: Optional[str] = None, 
                                   user_input_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Get medicine data from database or use provided input data.
        
        Args:
            medicine_name: Optional specific medicine to search for
            user_input_data: Optional user input data for new medicine record
            
        Returns:
            Medicine data
        """
        try:
            if user_input_data:
                # POST new medicine data
                response = requests.post(
                    f"{self.base_url}/healthapp/api/medicines/",
                    data=json.dumps({**user_input_data, 'user_id': self.user_id}),
                    headers={'Content-Type': 'application/json'}
                )
            else:
                # GET existing data
                params = {'user_id': self.user_id}
                if medicine_name:
                    params['medicine_name'] = medicine_name
                    
                response = requests.get(
                    f"{self.base_url}/healthapp/api/medicines/",
                    params=params
                )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'success': False, 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_appointment_data_or_prompt(self, user_input_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Get appointment history from database or create new appointment.
        
        Args:
            user_input_data: Optional user input data for new appointment
            
        Returns:
            Appointment data
        """
        try:
            if user_input_data:
                # POST new appointment data
                response = requests.post(
                    f"{self.base_url}/healthapp/api/appointments/",
                    data=json.dumps({**user_input_data, 'user_id': self.user_id}),
                    headers={'Content-Type': 'application/json'}
                )
            else:
                # GET existing data
                response = requests.get(
                    f"{self.base_url}/healthapp/api/appointments/",
                    params={'user_id': self.user_id}
                )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'success': False, 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_lab_results(self, test_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get lab results from database.
        
        Args:
            test_name: Optional specific test to search for
            
        Returns:
            Lab results data
        """
        try:
            params = {'user_id': self.user_id}
            if test_name:
                params['test_name'] = test_name
                
            response = requests.get(
                f"{self.base_url}/healthapp/api/lab-results/",
                params=params
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'success': False, 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def check_available_data(self) -> Dict[str, Any]:
        """
        Check what data is available in the database for the user.
        
        Returns:
            Summary of available data
        """
        try:
            response = requests.post(
                f"{self.base_url}/healthapp/api/check-data/",
                data=json.dumps({'user_id': self.user_id}),
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'success': False, 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}


def simulate_user_input_prompt(prompt_message: str, input_fields: List[str]) -> Dict[str, Any]:
    """
    Simulate user input prompt. In a real application, this would be replaced
    with actual user interface interaction.
    
    Args:
        prompt_message: Message to display to user
        input_fields: List of fields to collect from user
        
    Returns:
        Dictionary with user input data
    """
    print(f"\n{prompt_message}")
    user_input = {}
    
    for field in input_fields:
        if field in ['age', 'medicine_quantity_available', 'hospital_distance_km']:
            try:
                value = input(f"Enter {field.replace('_', ' ')}: ")
                user_input[field] = int(float(value)) if 'age' in field or 'quantity' in field else float(value)
            except ValueError:
                user_input[field] = None
        elif field in ['user_symptoms', 'medicine_timing', 'interpretation_abnormalities']:
            # Handle list fields
            value = input(f"Enter {field.replace('_', ' ')} (comma-separated): ")
            user_input[field] = [item.strip() for item in value.split(',') if item.strip()]
        else:
            user_input[field] = input(f"Enter {field.replace('_', ' ')}: ")
    
    return user_input


# Example usage functions for health agents
def nurse_get_patient_data_or_input(user_id: int = 1) -> Dict[str, Any]:
    """
    Function for nurse agent to get patient data or collect input.
    """
    integration = HealthDataIntegration(user_id=user_id)
    
    # Check what data is available
    availability = integration.check_available_data()
    
    if not availability['success']:
        return {'error': 'Failed to check data availability'}
    
    data_summary = availability['data']
    result = {}
    
    # Get or collect user profile
    if not data_summary['user_profile']['available'] or not data_summary['user_profile']['complete']:
        print("User profile incomplete. Collecting basic information...")
        user_input = simulate_user_input_prompt(
            "Please provide your basic information:",
            ['age', 'phone', 'emergency_contact']
        )
        profile_result = integration.get_user_profile_or_prompt(user_input)
        result['profile'] = profile_result
    else:
        result['profile'] = integration.get_user_profile_or_prompt()
    
    # Get appointment history
    appointment_result = integration.get_appointment_data_or_prompt()
    result['appointments'] = appointment_result
    
    return result


def medicine_agent_get_data_or_input(user_id: int = 1, medicine_name: str = None) -> Dict[str, Any]:
    """
    Function for medicine agent to get medicine data or collect input.
    """
    integration = HealthDataIntegration(user_id=user_id)
    
    # Try to get existing medicine data
    result = integration.get_medicine_data_or_prompt(medicine_name)
    
    if result['success'] and result['data'].get('needs_input'):
        print("No medicine records found. Collecting medicine information...")
        user_input = simulate_user_input_prompt(
            "Please provide medicine details:",
            ['medicine_name', 'medicine_dosage', 'medicine_frequency', 
             'medicine_timing', 'medicine_quantity_available', 'medicine_special_instructions']
        )
        result = integration.get_medicine_data_or_prompt(user_input_data=user_input)
    
    return result


# Example of how to integrate with CrewAI tools
class DatabaseOrInputTool:
    """
    CrewAI compatible tool for database-or-input pattern.
    """
    
    def __init__(self, user_id: int = 1):
        self.integration = HealthDataIntegration(user_id=user_id)
    
    def get_patient_profile(self, collect_if_missing: bool = True) -> str:
        """
        Tool function to get patient profile with automatic input collection.
        """
        try:
            result = self.integration.get_user_profile_or_prompt()
            
            if result['success']:
                if result['data'].get('needs_input') and collect_if_missing:
                    # In a real implementation, this would trigger user interface
                    return "Patient profile incomplete. Please collect: age, phone, emergency contact"
                else:
                    data = result['data']
                    return f"Patient Profile: Name: {data['user_name']}, Age: {data['user_age']}, Phone: {data['phone']}"
            else:
                return f"Error retrieving patient profile: {result['error']}"
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_medicine_history(self, medicine_name: str = None) -> str:
        """
        Tool function to get medicine history.
        """
        try:
            result = self.integration.get_medicine_data_or_prompt(medicine_name)
            
            if result['success']:
                if result['data'].get('needs_input'):
                    return f"No medicine records found{' for ' + medicine_name if medicine_name else ''}. Please collect medicine details."
                elif result['data'].get('found_in_database'):
                    records = result['data']['records']
                    summary = f"Found {len(records)} medicine record(s):\n"
                    for record in records:
                        summary += f"- {record['medicine_name']}: {record['medicine_dosage']}, {record['medicine_frequency']}\n"
                    return summary
            else:
                return f"Error retrieving medicine data: {result['error']}"
                
        except Exception as e:
            return f"Error: {str(e)}"