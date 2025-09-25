from crewai.tools import BaseTool
from typing import Type, Dict, Any
from pydantic import BaseModel, Field
from browser_use import Agent as BrowserAgent
from langchain_groq import ChatGroq

import asyncio
import os
import json
import datetime


class BrowserToolInput(BaseModel):
    """Input schema for BrowserTool."""
    task: str = Field(..., description="The task for the browser to perform (e.g., 'Find hospitals near me', 'Search for doctor information')")


class BrowserTool(BaseTool):
    name: str = "browser_automation"
    description: str = (
        "Automate web browsing tasks to find healthcare information, search for hospitals, "
        "doctors, medical facilities, and gather health-related data from websites. "
        "Can navigate websites, extract information, and perform web searches."
    )
    args_schema: Type[BaseModel] = BrowserToolInput

    def _run(self, task: str) -> str:
        """Execute browser automation task."""
        try:
            # Use Groq API key
            api_key = os.getenv('GROQ_API_KEY')
            if not api_key:
                return "Error: Groq API key not found in environment variables"
            
            # Create Groq LLM instance
            llm = ChatGroq(
                model="meta-llama/llama-3.1-70b-versatile",
                api_key=api_key,
                temperature=0.3
            )
            
            agent = BrowserAgent(task=task, llm=llm)
            result = agent.run_sync()
            
            # Extract meaningful information from result
            if hasattr(result, 'final_result'):
                return str(result.final_result())
            elif hasattr(result, 'extracted_content'):
                content = result.extracted_content()
                if content:
                    return str(content[-1]) if isinstance(content, list) else str(content)
            
            return str(result)
            
        except Exception as e:
            return f"Error executing browser task: {str(e)}"


class WebSearchToolInput(BaseModel):
    """Input schema for WebSearchTool."""
    query: str = Field(..., description="Search query for finding health information")


class WebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = (
        "Search the web for health-related information, find hospitals, doctors, "
        "medical facilities, treatment options, and healthcare services. Returns "
        "relevant search results and extracted information."
    )
    args_schema: Type[BaseModel] = WebSearchToolInput

    def _run(self, query: str) -> str:
        """Execute web search task using browser automation."""
        try:
            api_key = os.getenv('GROQ_API_KEY')
            if not api_key:
                return "Error: Groq API key not found in environment variables"
            
            # Create Groq LLM instance with the specified model
            llm = ChatGroq(
                model="meta-llama/llama-3.1-70b-versatile",
                api_key=api_key,
                temperature=0.3
            )
            
            search_task = f"Search Google for: {query} and extract the most relevant information"
            agent = BrowserAgent(task=search_task, llm=llm)
            result = agent.run_sync()
            
            # Extract meaningful information from result
            if hasattr(result, 'final_result'):
                return str(result.final_result())
            elif hasattr(result, 'extracted_content'):
                content = result.extracted_content()
                if content:
                    return str(content[-1]) if isinstance(content, list) else str(content)
            
            return str(result)
            
        except Exception as e:
            return f"Error executing web search: {str(e)}"


class JSONStorageToolInput(BaseModel):
    """Input schema for JSONStorageTool."""
    prompt: str = Field(..., description="The prompt or query to store in JSON format")
    filename: str = Field(default="prompt", description="Filename for the JSON file (without extension)")
    category: str = Field(default="general", description="Category or type of the prompt (e.g., 'health', 'appointment', 'medication')")


class JSONStorageTool(BaseTool):
    name: str = "json_storage"
    description: str = (
        "Store prompts and queries in structured JSON format for processing. "
        "Useful for storing user health queries, appointment requests, medication questions, "
        "and other healthcare-related prompts for later analysis and response generation."
    )
    args_schema: Type[BaseModel] = JSONStorageToolInput

    def _run(self, prompt: str, filename: str = "prompt", category: str = "general") -> str:
        """Store prompt in JSON format."""
        try:
            # Create data directory if it doesn't exist
            data_dir = "data"
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            
            # Create JSON structure
            prompt_data = {
                "id": f"{filename}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "timestamp": datetime.datetime.now().isoformat(),
                "category": category,
                "prompt": prompt,
                "status": "stored",
                "processed": False
            }
            
            # Save to JSON file
            filepath = os.path.join(data_dir, f"{filename}_prompt.json")
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(prompt_data, f, indent=2, ensure_ascii=False)
            
            return f"Prompt successfully stored in {filepath}. ID: {prompt_data['id']}"
            
        except Exception as e:
            return f"Error storing prompt in JSON: {str(e)}"


class JSONResponseToolInput(BaseModel):
    """Input schema for JSONResponseTool."""
    response_data: str = Field(..., description="The response data to store in JSON format")
    prompt_id: str = Field(..., description="The ID of the original prompt this response is for")
    response_type: str = Field(default="general", description="Type of response (e.g., 'diagnosis', 'appointment', 'recommendation')")
    filename: str = Field(default="response", description="Filename for the response JSON file (without extension)")


class JSONResponseTool(BaseTool):
    name: str = "json_response"
    description: str = (
        "Store responses and analysis results in structured JSON format. "
        "Used for storing healthcare analysis results, appointment confirmations, "
        "medication recommendations, and other response data in organized JSON files."
    )
    args_schema: Type[BaseModel] = JSONResponseToolInput

    def _run(self, response_data: str, prompt_id: str, response_type: str = "general", filename: str = "response") -> str:
        """Store response in JSON format."""
        try:
            # Create data directory if it doesn't exist
            data_dir = "data"
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            
            # Try to parse response_data as JSON if it's a JSON string
            try:
                parsed_response = json.loads(response_data)
            except json.JSONDecodeError:
                # If not valid JSON, store as string
                parsed_response = response_data
            
            # Create JSON structure
            response_json = {
                "response_id": f"{filename}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "prompt_id": prompt_id,
                "timestamp": datetime.datetime.now().isoformat(),
                "response_type": response_type,
                "response_data": parsed_response,
                "status": "completed"
            }
            
            # Save to JSON file
            filepath = os.path.join(data_dir, f"{filename}_response.json")
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(response_json, f, indent=2, ensure_ascii=False)
            
            return f"Response successfully stored in {filepath}. Response ID: {response_json['response_id']}"
            
        except Exception as e:
            return f"Error storing response in JSON: {str(e)}"


class JSONProcessorToolInput(BaseModel):
    """Input schema for JSONProcessorTool."""
    prompt_file: str = Field(..., description="Path to the JSON file containing the prompt to process")


class JSONProcessorTool(BaseTool):
    name: str = "json_processor"
    description: str = (
        "Process stored prompts from JSON files and generate appropriate responses. "
        "Reads prompt JSON files, analyzes the content, and generates healthcare responses, "
        "recommendations, or analysis based on the stored prompt data."
    )
    args_schema: Type[BaseModel] = JSONProcessorToolInput

    def _run(self, prompt_file: str) -> str:
        """Process a stored prompt and generate response."""
        try:
            # Read the prompt JSON file
            if not os.path.exists(prompt_file):
                return f"Prompt file not found: {prompt_file}"
            
            with open(prompt_file, 'r', encoding='utf-8') as f:
                prompt_data = json.load(f)
            
            prompt = prompt_data.get('prompt', '')
            category = prompt_data.get('category', 'general')
            prompt_id = prompt_data.get('id', '')
            
            # Generate response based on category
            if category.lower() in ['health', 'medical', 'symptoms']:
                response = self._process_health_prompt(prompt)
            elif category.lower() in ['appointment', 'booking']:
                response = self._process_appointment_prompt(prompt)
            elif category.lower() in ['medication', 'medicine']:
                response = self._process_medication_prompt(prompt)
            else:
                response = self._process_general_prompt(prompt)
            
            # Store the response
            response_tool = JSONResponseTool()
            response_result = response_tool._run(
                response_data=response,
                prompt_id=prompt_id,
                response_type=category,
                filename=f"response_{category}"
            )
            
            # Update original prompt as processed
            prompt_data['processed'] = True
            prompt_data['processing_timestamp'] = datetime.datetime.now().isoformat()
            
            with open(prompt_file, 'w', encoding='utf-8') as f:
                json.dump(prompt_data, f, indent=2, ensure_ascii=False)
            
            return f"Prompt processed successfully. {response_result}"
            
        except Exception as e:
            return f"Error processing prompt: {str(e)}"
    
    def _process_health_prompt(self, prompt: str) -> str:
        """Process health-related prompts."""
        return json.dumps({
            "analysis": "Health prompt analysis completed",
            "recommendations": [
                "Consult with healthcare provider for proper diagnosis",
                "Monitor symptoms and keep a health diary",
                "Maintain regular check-ups"
            ],
            "urgency_level": "medium",
            "next_steps": "Schedule appointment if symptoms persist"
        })
    
    def _process_appointment_prompt(self, prompt: str) -> str:
        """Process appointment-related prompts."""
        return json.dumps({
            "appointment_status": "processing",
            "available_slots": ["2024-10-01 10:00", "2024-10-01 14:00", "2024-10-02 09:00"],
            "requirements": "Valid ID and insurance information",
            "confirmation": "Appointment request received and being processed"
        })
    
    def _process_medication_prompt(self, prompt: str) -> str:
        """Process medication-related prompts."""
        return json.dumps({
            "medication_analysis": "Medication query processed",
            "recommendations": [
                "Follow prescribed dosage",
                "Take with food if required",
                "Monitor for side effects"
            ],
            "reminders": "Set up daily medication reminders",
            "consultation": "Discuss with pharmacist or doctor for concerns"
        })
    
class JSONProcessorTool(BaseTool):
    name: str = "json_processor"
    description: str = (
        "Process stored prompts from JSON files and generate appropriate responses. "
        "Reads prompt JSON files, analyzes the content, and generates healthcare responses, "
        "recommendations, or analysis based on the stored prompt data."
    )
    args_schema: Type[BaseModel] = JSONProcessorToolInput

    def _run(self, prompt_file: str) -> str:
        """Process a stored prompt and generate response."""
        try:
            # Read the prompt JSON file
            if not os.path.exists(prompt_file):
                return f"Prompt file not found: {prompt_file}"
            
            with open(prompt_file, 'r', encoding='utf-8') as f:
                prompt_data = json.load(f)
            
            prompt = prompt_data.get('prompt', '')
            category = prompt_data.get('category', 'general')
            prompt_id = prompt_data.get('id', '')
            
            # Generate response based on category
            if category.lower() in ['health', 'medical', 'symptoms']:
                response = self._process_health_prompt(prompt)
            elif category.lower() in ['appointment', 'booking']:
                response = self._process_appointment_prompt(prompt)
            elif category.lower() in ['medication', 'medicine']:
                response = self._process_medication_prompt(prompt)
            else:
                response = self._process_general_prompt(prompt)
            
            # Store the response
            response_tool = JSONResponseTool()
            response_result = response_tool._run(
                response_data=response,
                prompt_id=prompt_id,
                response_type=category,
                filename=f"response_{category}"
            )
            
            # Update original prompt as processed
            prompt_data['processed'] = True
            prompt_data['processing_timestamp'] = datetime.datetime.now().isoformat()
            
            with open(prompt_file, 'w', encoding='utf-8') as f:
                json.dump(prompt_data, f, indent=2, ensure_ascii=False)
            
            return f"Prompt processed successfully. {response_result}"
            
        except Exception as e:
            return f"Error processing prompt: {str(e)}"
    
    def _process_health_prompt(self, prompt: str) -> str:
        """Process health-related prompts."""
        return json.dumps({
            "analysis": "Health prompt analysis completed",
            "recommendations": [
                "Consult with healthcare provider for proper diagnosis",
                "Monitor symptoms and keep a health diary",
                "Maintain regular check-ups"
            ],
            "urgency_level": "medium",
            "next_steps": "Schedule appointment if symptoms persist"
        })
    
    def _process_appointment_prompt(self, prompt: str) -> str:
        """Process appointment-related prompts."""
        return json.dumps({
            "appointment_status": "processing",
            "available_slots": ["2024-10-01 10:00", "2024-10-01 14:00", "2024-10-02 09:00"],
            "requirements": "Valid ID and insurance information",
            "confirmation": "Appointment request received and being processed"
        })
    
    def _process_medication_prompt(self, prompt: str) -> str:
        """Process medication-related prompts."""
        return json.dumps({
            "medication_analysis": "Medication query processed",
            "recommendations": [
                "Follow prescribed dosage",
                "Take with food if required",
                "Monitor for side effects"
            ],
            "reminders": "Set up daily medication reminders",
            "consultation": "Discuss with pharmacist or doctor for concerns"
        })
    
    def _process_general_prompt(self, prompt: str) -> str:
        """Process general prompts."""
        return json.dumps({
            "response": f"General query processed: {prompt}",
            "status": "completed",
            "additional_help": "Contact healthcare provider for specific medical advice"
        })


class HospitalSearchToolInput(BaseModel):
    """Input schema for HospitalSearchTool."""
    location: str = Field(default="VIT Vellore", description="Location to search for hospitals near")
    specialty: str = Field(default="", description="Medical specialty to filter hospitals by (optional)")


class UserSelectionToolInput(BaseModel):
    """Input schema for UserSelectionTool."""
    options: str = Field(..., description="JSON string containing hospital data with nearest_hospital and preferred_hospital")
    selection_type: str = Field(..., description="Type of selection: 'hospital' or 'doctor'")
    user_preference: str = Field(default="", description="User's preferred doctor name (optional)")


class UserSelectionTool(BaseTool):
    name: str = "user_selection"
    description: str = (
        "Handle user preferences and selections for hospitals and doctors from structured hospital data. "
        "For doctor selection, if the preferred doctor is not available, automatically selects the next best doctor by rating. "
        "Allows choosing between nearest hospital and preferred hospital options."
    )
    args_schema: Type[BaseModel] = UserSelectionToolInput

    def _run(self, options: str, selection_type: str, user_preference: str = "") -> str:
        """Handle user selection for hospitals or doctors."""
        try:
            # Parse the options JSON
            import json
            hospital_data = json.loads(options)

            if selection_type == "hospital":
                return self._handle_hospital_selection(hospital_data, user_preference)
            elif selection_type == "doctor":
                return self._handle_doctor_selection(hospital_data, user_preference)
            else:
                return f"Invalid selection type: {selection_type}. Use 'hospital' or 'doctor'."

        except json.JSONDecodeError:
            return f"Error parsing options JSON: {options}"
        except Exception as e:
            return f"Error in user selection: {str(e)}"

    def _handle_hospital_selection(self, hospital_data: dict, user_preference: str = "") -> str:
        """Handle hospital selection logic."""
        # For now, default to nearest hospital since that's the primary requirement
        nearest_hospital = hospital_data.get('nearest_hospital')
        if nearest_hospital:
            return json.dumps({
                "selection_type": "hospital",
                "selected_hospital": nearest_hospital,
                "selection_method": "nearest_hospital",
                "available_options": [nearest_hospital, hospital_data.get('preferred_hospital')]
            })

        return json.dumps({"error": "No hospitals available for selection"})

    def _handle_doctor_selection(self, hospital_data: dict, user_preference: str = "") -> str:
        """Handle doctor selection logic with fallback to next best doctor."""
        nearest_hospital = hospital_data.get('nearest_hospital', {})
        preferred_hospital = hospital_data.get('preferred_hospital', {})

        if user_preference:
            # User has specified a preferred doctor - search in both hospitals
            all_doctors = []
            all_doctors.extend(nearest_hospital.get('doctors', []))
            all_doctors.extend(preferred_hospital.get('doctors', []))

            # Look for exact match first
            for doctor in all_doctors:
                if user_preference.lower() in doctor.get('doctor_name', '').lower():
                    # Find which hospital this doctor belongs to
                    hospital = nearest_hospital if doctor in nearest_hospital.get('doctors', []) else preferred_hospital
                    return json.dumps({
                        "selection_type": "doctor",
                        "selected_doctor": doctor,
                        "selected_hospital": hospital,
                        "selection_method": "user_preference_found",
                        "selection_reason": f"Found your preferred doctor: {doctor.get('doctor_name')}"
                    })

        # If no preference or preference not found, select best doctor from nearest hospital
        nearest_doctors = nearest_hospital.get('doctors', [])
        if nearest_doctors:
            # Sort doctors by rating (highest first)
            sorted_doctors = sorted(nearest_doctors, 
                                  key=lambda x: float(x.get('rating', '0').split('/')[0]), 
                                  reverse=True)
            best_doctor = sorted_doctors[0]

            reason = f"Selected highest rated doctor: {best_doctor.get('doctor_name')} ({best_doctor.get('rating')})"
            if user_preference:
                reason = f"Your preferred doctor '{user_preference}' was not found. {reason}"

            return json.dumps({
                "selection_type": "doctor",
                "selected_doctor": best_doctor,
                "selected_hospital": nearest_hospital,
                "selection_method": "auto_selected_best_rated",
                "selection_reason": reason,
                "available_doctors": sorted_doctors[:3]  # Show top 3 options
            })

        return json.dumps({"error": "No doctors available for selection"})


class HospitalSearchToolInput(BaseModel):
    """Input schema for HospitalSearchTool."""
    location: str = Field(default="VIT Vellore", description="Location to search for hospitals near")
    specialty: str = Field(default="", description="Medical specialty to filter hospitals by (optional)")


class HospitalSearchTool(BaseTool):
    name: str = "hospital_search"
    description: str = (
        "Search for the nearest hospital to VIT Vellore based on ratings and collect contact information. "
        "Finds the highest-rated hospital closest to VIT Vellore with contact details and available specialists."
    )
    args_schema: Type[BaseModel] = HospitalSearchToolInput

    def _run(self, location: str = "VIT Vellore", specialty: str = "") -> str:
        """Search for the nearest hospital to VIT Vellore based on ratings."""
        try:
            # Get Groq API key
            api_key = os.getenv('GROQ_API_KEY')
            if not api_key:
                return "Error: Groq API key not found in environment variables"

            # Create Groq LLM instance
            llm = ChatGroq(
                model="meta-llama/llama-3.1-70b-versatile",
                api_key=api_key,
                temperature=0.3
            )

            # Build search task focused on nearest hospital by ratings
            if specialty:
                task = f"""
                Find the NEAREST hospital to {location} with the BEST ratings that specializes in {specialty}.
                Focus on finding the single highest-rated hospital closest to {location}.

                CRITICAL: Make sure to collect the COMPLETE contact phone number.

                Return information for this hospital:
                1. Hospital name
                2. COMPLETE contact phone number (include area code, all digits)
                3. Hospital rating/review score
                4. Distance from {location}
                5. Full address
                6. Available specialists in {specialty}
                7. Emergency services availability

                Structure the response as JSON with this exact format:
                {{
                  "hospital_name": "Hospital Name",
                  "hospital_contact": "Complete Phone Number",
                  "hospital_rating": "4.8/5",
                  "hospital_distance_km": 2.5,
                  "hospital_address": "Full Address",
                  "available_specialists": ["{specialty}"],
                  "emergency_services": true
                }}

                PRIORITY: Ensure the contact number is complete and accurate.
                """
            else:
                task = f"""
                Find the NEAREST hospital to {location} with the BEST ratings.
                Focus on finding the single highest-rated hospital closest to {location}.

                CRITICAL: Make sure to collect the COMPLETE contact phone number.

                Return information for this hospital:
                1. Hospital name
                2. COMPLETE contact phone number (include area code, all digits)
                3. Hospital rating/review score
                4. Distance from {location}
                5. Full address
                6. Available medical specialties
                7. Emergency services availability

                Structure the response as JSON with this exact format:
                {{
                  "hospital_name": "Hospital Name",
                  "hospital_contact": "Complete Phone Number",
                  "hospital_rating": "4.8/5",
                  "hospital_distance_km": 2.5,
                  "hospital_address": "Full Address",
                  "available_specialists": ["General Medicine"],
                  "emergency_services": true
                }}

                PRIORITY: Ensure the contact number is complete and accurate.
                """

            # Create browser agent
            agent = BrowserAgent(task=task, llm=llm)

            # Run synchronously
            result = agent.run_sync()

            # Extract and format the result
            if hasattr(result, 'final_result'):
                return str(result.final_result())
            elif hasattr(result, 'extracted_content'):
                content = result.extracted_content()
                if content:
                    return str(content[-1]) if isinstance(content, list) else str(content)

            return str(result)

        except Exception as e:
            return f"Error searching for hospitals: {str(e)}"


# Create tool instances
browser_tool = BrowserTool()
web_search_tool = WebSearchTool()
json_storage_tool = JSONStorageTool()
json_response_tool = JSONResponseTool()
json_processor_tool = JSONProcessorTool()
hospital_search_tool = HospitalSearchTool()
user_selection_tool = UserSelectionTool()

# Export tools for CrewAI
tools = [browser_tool, web_search_tool, json_storage_tool, json_response_tool, json_processor_tool, hospital_search_tool, user_selection_tool]

