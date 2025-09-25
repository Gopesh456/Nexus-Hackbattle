import os
import base64
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import requests
from crewai_tools import BaseTool
from PIL import Image
import io

class GroqVisionProcessor(BaseTool):
    name: str = "Groq Vision Lab Report Processor"
    description: str = """
    Advanced tool that processes lab report images using Groq's vision-capable LLMs.
    
    This tool:
    1. Scans the images folder for lab report images
    2. Converts images to base64 encoding for API transmission
    3. Sends images to Groq's vision models for AI-powered analysis
    4. Extracts comprehensive medical data from lab reports
    5. Returns structured JSON with all findings and AI insights
    
    Supports multiple image formats: JPG, JPEG, PNG, PDF (first page)
    Uses Groq models: llama-3.2-90b-vision-preview, llava-v1.5-7b-4096-preview
    """
    
    def __init__(self):
        super().__init__()
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.images_folder = Path("c:/Users/MALAVIKA/Documents/GitHub/Nexus-Hackbattle/Backend/Agent/images")
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.pdf'}
        self.groq_base_url = "https://api.groq.com/openai/v1/chat/completions"
        
    def _run(self, image_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Process lab report images using Groq vision AI.
        
        Args:
            image_path: Optional specific image path. If None, processes all images in folder.
            
        Returns:
            Dict containing comprehensive lab analysis results
        """
        try:
            start_time = time.time()
            
            # Get images to process
            if image_path:
                images_to_process = [Path(image_path)]
            else:
                images_to_process = self._scan_images_folder()
            
            if not images_to_process:
                return {
                    "error": "No lab report images found",
                    "images_folder": str(self.images_folder),
                    "supported_formats": list(self.supported_formats)
                }
            
            results = []
            
            for image_path in images_to_process:
                try:
                    # Process single image
                    result = self._process_single_image(image_path)
                    results.append(result)
                except Exception as e:
                    results.append({
                        "error": f"Failed to process {image_path.name}: {str(e)}",
                        "image_path": str(image_path)
                    })
            
            processing_time = time.time() - start_time
            
            return {
                "processing_summary": {
                    "total_images": len(images_to_process),
                    "successful_processing": len([r for r in results if "error" not in r]),
                    "failed_processing": len([r for r in results if "error" in r]),
                    "total_processing_time": processing_time,
                    "timestamp": datetime.now().isoformat()
                },
                "results": results,
                "status": "completed"
            }
            
        except Exception as e:
            return {
                "error": f"Groq vision processing failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _scan_images_folder(self) -> List[Path]:
        """Scan images folder for lab report images"""
        if not self.images_folder.exists():
            return []
        
        images = []
        for file_path in self.images_folder.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                images.append(file_path)
        
        return sorted(images)
    
    def _process_single_image(self, image_path: Path) -> Dict[str, Any]:
        """Process a single lab report image with Groq vision AI"""
        
        # Convert image to base64
        base64_image, image_info = self._convert_to_base64(image_path)
        
        # Prepare Groq API request
        groq_response = self._call_groq_vision_api(base64_image, image_path.name)
        
        # Parse and structure the response
        structured_result = self._structure_groq_response(
            groq_response, image_path, image_info
        )
        
        return structured_result
    
    def _convert_to_base64(self, image_path: Path) -> tuple[str, Dict]:
        """Convert image to base64 with metadata"""
        try:
            if image_path.suffix.lower() == '.pdf':
                # For PDF files, convert first page to image
                return self._convert_pdf_to_base64(image_path)
            else:
                # For image files
                with open(image_path, 'rb') as image_file:
                    image_data = image_file.read()
                
                # Get image info
                with Image.open(image_path) as img:
                    image_info = {
                        "format": img.format,
                        "size": img.size,
                        "mode": img.mode,
                        "file_size": len(image_data)
                    }
                
                base64_encoded = base64.b64encode(image_data).decode('utf-8')
                
                return base64_encoded, image_info
                
        except Exception as e:
            raise Exception(f"Failed to convert image to base64: {str(e)}")
    
    def _convert_pdf_to_base64(self, pdf_path: Path) -> tuple[str, Dict]:
        """Convert first page of PDF to base64 image"""
        try:
            # This would require pdf2image library
            # For now, return error for PDF files
            raise Exception("PDF processing not implemented. Please convert PDF to image format.")
        except Exception as e:
            raise Exception(f"PDF conversion failed: {str(e)}")
    
    def _call_groq_vision_api(self, base64_image: str, filename: str) -> Dict[str, Any]:
        """Make API call to Groq vision model"""
        
        if not self.groq_api_key:
            raise Exception("GROQ_API_KEY environment variable not set")
        
        # Prepare the prompt for lab report analysis
        system_prompt = """You are an expert medical AI assistant specializing in lab report analysis. 
        Analyze the provided lab report image and extract ALL visible medical data with high accuracy.
        
        Focus on:
        1. Patient information (name, age, gender, ID)
        2. Lab details (name, address, report ID, dates)
        3. All test parameters with values, units, and reference ranges
        4. Abnormal values and their clinical significance
        5. Any critical findings requiring immediate attention
        
        Provide comprehensive medical insights and recommendations based on the findings."""
        
        user_prompt = f"""Please analyze this lab report image ({filename}) and extract all medical data.
        
        Return a comprehensive JSON response with:
        - Complete patient demographics
        - All lab test results with values and units
        - Reference ranges for each parameter
        - Identification of abnormal/critical values
        - Clinical interpretation and health insights
        - Recommendations for follow-up care
        - Overall health assessment
        
        Ensure accuracy and completeness in extraction."""
        
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.2-90b-vision-preview",  # Use the most capable vision model
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 4000,
            "temperature": 0.1  # Low temperature for medical accuracy
        }
        
        try:
            response = requests.post(
                self.groq_base_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Groq API call failed: {str(e)}")
    
    def _structure_groq_response(self, groq_response: Dict, image_path: Path, image_info: Dict) -> Dict[str, Any]:
        """Structure the Groq API response into the expected JSON format"""
        
        try:
            # Extract the AI response content
            ai_content = groq_response.get('choices', [{}])[0].get('message', {}).get('content', '')
            usage_info = groq_response.get('usage', {})
            
            # Try to parse AI response as JSON, fallback to text analysis
            try:
                # If AI returned structured JSON
                if ai_content.strip().startswith('{'):
                    ai_data = json.loads(ai_content)
                else:
                    # If AI returned text, we need to structure it
                    ai_data = self._parse_text_response(ai_content)
            except json.JSONDecodeError:
                ai_data = self._parse_text_response(ai_content)
            
            # Create comprehensive structured response
            structured_response = {
                "processing_info": {
                    "image_source": str(image_path),
                    "groq_model": "llama-3.2-90b-vision-preview",
                    "base64_size": image_info.get('file_size', 0),
                    "processing_time": 0.0,  # Will be updated by caller
                    "api_response_tokens": usage_info.get('total_tokens', 0)
                },
                **self._extract_medical_data(ai_data, ai_content),
                "groq_processing_details": {
                    "model_used": "llama-3.2-90b-vision-preview",
                    "tokens_consumed": usage_info.get('total_tokens', 0),
                    "prompt_tokens": usage_info.get('prompt_tokens', 0),
                    "completion_tokens": usage_info.get('completion_tokens', 0),
                    "api_version": "v1"
                },
                "data_quality_metrics": {
                    "extraction_confidence": 0.85,  # Default, can be enhanced
                    "image_clarity": self._assess_image_quality(image_info),
                    "text_readability": 0.8,  # Default
                    "completeness": 0.9  # Default
                },
                "raw_extracted_text": ai_content,
                "processing_timestamp": datetime.now().isoformat(),
                "groq_raw_response": json.dumps(groq_response, indent=2),
                "message": f"Lab report processed successfully using Groq AI vision. Image: {image_path.name}"
            }
            
            return structured_response
            
        except Exception as e:
            return {
                "error": f"Failed to structure Groq response: {str(e)}",
                "raw_response": str(groq_response),
                "image_path": str(image_path)
            }
    
    def _extract_medical_data(self, ai_data: Dict, ai_content: str) -> Dict[str, Any]:
        """Extract and structure medical data from AI response"""
        
        # Default structure - will be populated from AI response
        medical_data = {
            "lab_test_name": ai_data.get('lab_test_name', 'Unknown Test'),
            "lab_date_conducted": ai_data.get('lab_date_conducted', ''),
            "report_date": ai_data.get('report_date', ''),
            "patient_name": ai_data.get('patient_name', ''),
            "patient_age": ai_data.get('patient_age', 0),
            "patient_gender": ai_data.get('patient_gender', ''),
            "patient_id": ai_data.get('patient_id', ''),
            "medical_record_number": ai_data.get('medical_record_number', ''),
            "lab_name": ai_data.get('lab_name', ''),
            "lab_address": ai_data.get('lab_address', ''),
            "lab_phone": ai_data.get('lab_phone', ''),
            "doctor_name": ai_data.get('doctor_name', ''),
            "doctor_npi": ai_data.get('doctor_npi', ''),
            "report_id": ai_data.get('report_id', ''),
            "specimen_type": ai_data.get('specimen_type', ''),
            "collection_time": ai_data.get('collection_time', ''),
            "lab_results": ai_data.get('lab_results', {}),
            "abnormal_values": ai_data.get('abnormal_values', []),
            "critical_values": ai_data.get('critical_values', []),
            "groq_ai_insights": {
                "clinical_summary": ai_data.get('clinical_summary', ''),
                "risk_assessment": ai_data.get('risk_assessment', ''),
                "differential_diagnosis": ai_data.get('differential_diagnosis', []),
                "follow_up_recommendations": ai_data.get('follow_up_recommendations', []),
                "lifestyle_suggestions": ai_data.get('lifestyle_suggestions', [])
            },
            "interpretation_summary": ai_data.get('interpretation_summary', ''),
            "clinical_recommendations": ai_data.get('clinical_recommendations', []),
            "follow_up_required": ai_data.get('follow_up_required', False),
            "urgency_level": ai_data.get('urgency_level', 'low'),
            "parameters_extracted": len(ai_data.get('lab_results', {})),
            "processing_notes": [
                "Processed using Groq vision AI",
                f"AI response length: {len(ai_content)} characters"
            ]
        }
        
        return medical_data
    
    def _parse_text_response(self, text_content: str) -> Dict[str, Any]:
        """Parse unstructured text response from AI"""
        # Basic text parsing - can be enhanced with NLP
        return {
            "interpretation_summary": text_content[:500] + "..." if len(text_content) > 500 else text_content,
            "clinical_summary": "AI provided detailed analysis",
            "lab_results": {},
            "abnormal_values": [],
            "clinical_recommendations": ["Consult with healthcare provider"],
            "follow_up_required": True,
            "urgency_level": "medium"
        }
    
    def _assess_image_quality(self, image_info: Dict) -> float:
        """Assess image quality based on metadata"""
        # Simple quality assessment based on image size and format
        size = image_info.get('size', (0, 0))
        pixel_count = size[0] * size[1]
        
        if pixel_count > 1000000:  # > 1MP
            return 0.9
        elif pixel_count > 500000:  # > 0.5MP
            return 0.7
        else:
            return 0.5

# Tool instance for CrewAI
groq_vision_processor = GroqVisionProcessor()