"""
Advanced Lab Report Image Processing Tool
Extracts and analyzes lab data from medical report images using OCR and AI.
"""

import cv2
import numpy as np
import pytesseract
import re
from PIL import Image, ImageEnhance, ImageFilter
from typing import Dict, List, Tuple, Any, Optional
import json
from datetime import datetime
import base64
import io


class LabReportImageProcessor:
    """
    Advanced image processor for medical lab reports.
    Uses OCR, image preprocessing, and AI text analysis.
    """
    
    def __init__(self):
        self.common_lab_parameters = {
            # Blood Chemistry
            'glucose': {'unit': 'mg/dL', 'normal_range': '70-100'},
            'cholesterol': {'unit': 'mg/dL', 'normal_range': '<200'},
            'hdl': {'unit': 'mg/dL', 'normal_range': '>40'},
            'ldl': {'unit': 'mg/dL', 'normal_range': '<100'},
            'triglycerides': {'unit': 'mg/dL', 'normal_range': '<150'},
            'creatinine': {'unit': 'mg/dL', 'normal_range': '0.6-1.2'},
            'bun': {'unit': 'mg/dL', 'normal_range': '7-20'},
            'uric_acid': {'unit': 'mg/dL', 'normal_range': '3.4-7.0'},
            
            # Complete Blood Count (CBC)
            'hemoglobin': {'unit': 'g/dL', 'normal_range': '12.0-16.0'},
            'hematocrit': {'unit': '%', 'normal_range': '36-46'},
            'rbc': {'unit': 'million/μL', 'normal_range': '4.2-5.4'},
            'wbc': {'unit': 'thousand/μL', 'normal_range': '4.5-11.0'},
            'platelets': {'unit': 'thousand/μL', 'normal_range': '150-450'},
            'mcv': {'unit': 'fL', 'normal_range': '80-100'},
            'mch': {'unit': 'pg', 'normal_range': '27-32'},
            'mchc': {'unit': 'g/dL', 'normal_range': '32-36'},
            
            # Liver Function
            'alt': {'unit': 'U/L', 'normal_range': '7-56'},
            'ast': {'unit': 'U/L', 'normal_range': '10-40'},
            'alkaline_phosphatase': {'unit': 'U/L', 'normal_range': '44-147'},
            'bilirubin_total': {'unit': 'mg/dL', 'normal_range': '0.3-1.2'},
            'bilirubin_direct': {'unit': 'mg/dL', 'normal_range': '0.0-0.3'},
            
            # Thyroid
            'tsh': {'unit': 'mIU/L', 'normal_range': '0.4-4.0'},
            't3': {'unit': 'ng/dL', 'normal_range': '80-200'},
            't4': {'unit': 'μg/dL', 'normal_range': '5.0-12.0'},
            
            # Vitamins & Minerals
            'vitamin_d': {'unit': 'ng/mL', 'normal_range': '30-100'},
            'vitamin_b12': {'unit': 'pg/mL', 'normal_range': '200-900'},
            'iron': {'unit': 'μg/dL', 'normal_range': '60-170'},
            'calcium': {'unit': 'mg/dL', 'normal_range': '8.5-10.5'},
            'magnesium': {'unit': 'mg/dL', 'normal_range': '1.7-2.2'},
        }
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Preprocess the image for better OCR accuracy.
        
        Args:
            image_path: Path to the lab report image
            
        Returns:
            Preprocessed image as numpy array
        """
        try:
            # Read image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Could not read image from {image_path}")
            
            # Convert to RGB
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Convert to PIL Image for advanced processing
            pil_img = Image.fromarray(img_rgb)
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(pil_img)
            pil_img = enhancer.enhance(1.5)
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(pil_img)
            pil_img = enhancer.enhance(2.0)
            
            # Convert back to numpy array
            img_array = np.array(pil_img)
            
            # Convert to grayscale
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Apply adaptive thresholding
            thresh = cv2.adaptiveThreshold(
                blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
            
            # Morphological operations to clean up the image
            kernel = np.ones((2, 2), np.uint8)
            cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
            
            return cleaned
            
        except Exception as e:
            raise Exception(f"Error preprocessing image: {str(e)}")
    
    def extract_text_from_image(self, image_path: str) -> str:
        """
        Extract text from lab report image using OCR.
        
        Args:
            image_path: Path to the lab report image
            
        Returns:
            Extracted text as string
        """
        try:
            # Preprocess image
            processed_img = self.preprocess_image(image_path)
            
            # Configure Tesseract for medical text
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,:;()[]/-<>=+ '
            
            # Extract text using OCR
            text = pytesseract.image_to_string(processed_img, config=custom_config)
            
            return text.strip()
            
        except Exception as e:
            raise Exception(f"Error extracting text from image: {str(e)}")
    
    def parse_lab_parameters(self, text: str) -> Dict[str, Any]:
        """
        Parse lab parameters from extracted text using pattern matching and AI analysis.
        
        Args:
            text: Raw text extracted from image
            
        Returns:
            Dictionary containing parsed lab parameters
        """
        try:
            parsed_data = {
                'lab_results': {},
                'lab_normal_ranges': {},
                'patient_info': {},
                'test_metadata': {}
            }
            
            # Clean and normalize text
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            # Extract patient information
            self._extract_patient_info(lines, parsed_data)
            
            # Extract test metadata
            self._extract_test_metadata(lines, parsed_data)
            
            # Extract lab parameters and values
            self._extract_lab_values(lines, parsed_data)
            
            return parsed_data
            
        except Exception as e:
            raise Exception(f"Error parsing lab parameters: {str(e)}")
    
    def _extract_patient_info(self, lines: List[str], parsed_data: Dict[str, Any]):
        """Extract patient information from text lines."""
        patient_patterns = {
            'name': [
                r'(?:patient|name)[\s:]+([a-zA-Z\s]+)',
                r'(?:mr|mrs|ms)\.?\s+([a-zA-Z\s]+)',
            ],
            'age': [
                r'(?:age)[\s:]+(\d+)',
                r'(\d+)\s*(?:years?|yrs?|y)',
            ],
            'gender': [
                r'(?:gender|sex)[\s:]+([mf](?:ale)?)',
                r'\b(male|female|m|f)\b',
            ],
            'date': [
                r'(?:date|collected|report)[\s:]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            ]
        }
        
        text_combined = ' '.join(lines).lower()
        
        for field, patterns in patient_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text_combined, re.IGNORECASE)
                if match:
                    parsed_data['patient_info'][field] = match.group(1).strip()
                    break
    
    def _extract_test_metadata(self, lines: List[str], parsed_data: Dict[str, Any]):
        """Extract test metadata from text lines."""
        # Look for lab/hospital name
        for line in lines[:5]:  # Check first 5 lines
            if any(keyword in line.lower() for keyword in ['laboratory', 'lab', 'hospital', 'clinic', 'medical']):
                if len(line) > 5 and not any(char.isdigit() for char in line):
                    parsed_data['test_metadata']['lab_name'] = line.strip()
                    break
        
        # Look for report type
        report_patterns = [
            r'(complete blood count|cbc)',
            r'(comprehensive metabolic panel|cmp)',
            r'(basic metabolic panel|bmp)',
            r'(lipid panel)',
            r'(liver function test|lft)',
            r'(thyroid function test|tft)',
        ]
        
        text_combined = ' '.join(lines).lower()
        for pattern in report_patterns:
            match = re.search(pattern, text_combined)
            if match:
                parsed_data['test_metadata']['report_type'] = match.group(1)
                break
    
    def _extract_lab_values(self, lines: List[str], parsed_data: Dict[str, Any]):
        """Extract lab values and normal ranges from text lines."""
        # Common patterns for lab values
        value_patterns = [
            # Pattern: Parameter Name    Value    Unit    Normal Range
            r'([a-zA-Z\s]+?)\s+(\d+\.?\d*)\s*([a-zA-Z/%μ]+)?\s*(?:(?:normal|ref|reference)?\s*:?\s*)?([<>]?\d+\.?\d*\s*[-–]\s*[<>]?\d+\.?\d*|[<>]\d+\.?\d*)',
            
            # Pattern: Parameter: Value Unit (Normal: range)
            r'([a-zA-Z\s]+?):\s*(\d+\.?\d*)\s*([a-zA-Z/%μ]+)?\s*\((?:normal|ref):\s*([^)]+)\)',
            
            # Pattern: Parameter Value Unit Normal Range
            r'([a-zA-Z\s]+?)\s+(\d+\.?\d*)\s+([a-zA-Z/%μ]+)\s+([<>]?\d+\.?\d*\s*[-–]\s*[<>]?\d+\.?\d*)',
            
            # Simple pattern: Parameter Value
            r'([a-zA-Z\s]+?)\s+(\d+\.?\d*)\s*([a-zA-Z/%μ]+)?',
        ]
        
        for line in lines:
            # Skip header lines and non-data lines
            if any(skip_word in line.lower() for skip_word in ['patient', 'hospital', 'laboratory', 'report', 'date']):
                continue
            
            for pattern in value_patterns:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    param_name = match.group(1).strip().lower()
                    param_value = match.group(2)
                    param_unit = match.group(3) if len(match.groups()) > 2 and match.group(3) else ''
                    normal_range = match.group(4) if len(match.groups()) > 3 and match.group(4) else ''
                    
                    # Clean parameter name
                    param_name = re.sub(r'[^\w\s]', '', param_name).strip()
                    param_name = re.sub(r'\s+', '_', param_name)
                    
                    if len(param_name) > 2 and param_value:
                        # Try to match with known parameters
                        matched_param = self._match_parameter(param_name)
                        if matched_param:
                            parsed_data['lab_results'][matched_param] = {
                                'value': float(param_value),
                                'unit': param_unit or self.common_lab_parameters[matched_param]['unit'],
                                'raw_name': match.group(1).strip()
                            }
                            
                            if normal_range:
                                parsed_data['lab_normal_ranges'][matched_param] = normal_range
                            else:
                                parsed_data['lab_normal_ranges'][matched_param] = self.common_lab_parameters[matched_param]['normal_range']
    
    def _match_parameter(self, param_name: str) -> Optional[str]:
        """Match extracted parameter name with known lab parameters."""
        param_name = param_name.lower().replace('_', ' ')
        
        # Direct matches
        if param_name in self.common_lab_parameters:
            return param_name
        
        # Fuzzy matching with common abbreviations and variations
        matches = {
            'glucose': ['glucose', 'blood glucose', 'fasting glucose', 'random glucose'],
            'cholesterol': ['cholesterol', 'total cholesterol', 'chol'],
            'hdl': ['hdl', 'hdl cholesterol', 'high density lipoprotein'],
            'ldl': ['ldl', 'ldl cholesterol', 'low density lipoprotein'],
            'triglycerides': ['triglycerides', 'tg', 'trigs'],
            'creatinine': ['creatinine', 'creat', 'cr'],
            'bun': ['bun', 'blood urea nitrogen', 'urea'],
            'hemoglobin': ['hemoglobin', 'hgb', 'hb'],
            'hematocrit': ['hematocrit', 'hct', 'hct'],
            'rbc': ['rbc', 'red blood cells', 'red blood cell count', 'erythrocytes'],
            'wbc': ['wbc', 'white blood cells', 'white blood cell count', 'leukocytes'],
            'platelets': ['platelets', 'plt', 'platelet count'],
            'alt': ['alt', 'alanine aminotransferase', 'sgpt'],
            'ast': ['ast', 'aspartate aminotransferase', 'sgot'],
            'tsh': ['tsh', 'thyroid stimulating hormone'],
            't3': ['t3', 'triiodothyronine'],
            't4': ['t4', 'thyroxine'],
        }
        
        for standard_name, variations in matches.items():
            if any(variation in param_name for variation in variations):
                return standard_name
        
        return None
    
    def analyze_results(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze lab results and provide interpretation.
        
        Args:
            parsed_data: Parsed lab data
            
        Returns:
            Analysis with interpretations and recommendations
        """
        try:
            analysis = {
                'interpretation_summary': '',
                'interpretation_abnormalities': [],
                'recommendations': [],
                'severity_level': 'normal'
            }
            
            abnormal_count = 0
            critical_count = 0
            
            for param, result in parsed_data['lab_results'].items():
                value = result['value']
                normal_range = parsed_data['lab_normal_ranges'].get(param, '')
                
                # Parse normal range
                is_abnormal, severity = self._check_abnormal(param, value, normal_range)
                
                if is_abnormal:
                    abnormal_count += 1
                    if severity == 'critical':
                        critical_count += 1
                    
                    analysis['interpretation_abnormalities'].append(
                        f"{param.replace('_', ' ').title()}: {value} {result['unit']} (Normal: {normal_range})"
                    )
            
            # Generate summary
            total_tests = len(parsed_data['lab_results'])
            if abnormal_count == 0:
                analysis['interpretation_summary'] = f"All {total_tests} test parameters are within normal limits."
                analysis['severity_level'] = 'normal'
            elif critical_count > 0:
                analysis['interpretation_summary'] = f"{critical_count} critical and {abnormal_count - critical_count} abnormal values found out of {total_tests} tests."
                analysis['severity_level'] = 'critical'
                analysis['recommendations'].append("Immediate medical consultation recommended due to critical values.")
            else:
                analysis['interpretation_summary'] = f"{abnormal_count} abnormal values found out of {total_tests} tests."
                analysis['severity_level'] = 'abnormal'
                analysis['recommendations'].append("Follow-up with healthcare provider recommended.")
            
            # Add specific recommendations based on abnormal values
            self._add_specific_recommendations(parsed_data, analysis)
            
            return analysis
            
        except Exception as e:
            raise Exception(f"Error analyzing results: {str(e)}")
    
    def _check_abnormal(self, param: str, value: float, normal_range: str) -> Tuple[bool, str]:
        """Check if a parameter value is abnormal and determine severity."""
        try:
            # Parse normal range
            if '<' in normal_range:
                max_val = float(re.search(r'<(\d+\.?\d*)', normal_range).group(1))
                if value >= max_val:
                    severity = 'critical' if value > max_val * 1.5 else 'abnormal'
                    return True, severity
            elif '>' in normal_range:
                min_val = float(re.search(r'>(\d+\.?\d*)', normal_range).group(1))
                if value <= min_val:
                    severity = 'critical' if value < min_val * 0.5 else 'abnormal'
                    return True, severity
            elif '-' in normal_range:
                range_match = re.search(r'(\d+\.?\d*)\s*[-–]\s*(\d+\.?\d*)', normal_range)
                if range_match:
                    min_val = float(range_match.group(1))
                    max_val = float(range_match.group(2))
                    if value < min_val or value > max_val:
                        severity = 'critical' if (value < min_val * 0.5 or value > max_val * 1.5) else 'abnormal'
                        return True, severity
            
            return False, 'normal'
            
        except Exception:
            return False, 'normal'
    
    def _add_specific_recommendations(self, parsed_data: Dict[str, Any], analysis: Dict[str, Any]):
        """Add specific recommendations based on abnormal lab values."""
        recommendations_map = {
            'glucose': 'Consider dietary modifications and glucose monitoring.',
            'cholesterol': 'Consider dietary changes and lipid management.',
            'creatinine': 'Kidney function evaluation may be needed.',
            'hemoglobin': 'Iron studies and anemia workup may be indicated.',
            'alt': 'Liver function monitoring recommended.',
            'ast': 'Liver function monitoring recommended.',
            'tsh': 'Thyroid function evaluation recommended.',
        }
        
        for param in analysis['interpretation_abnormalities']:
            param_key = param.split(':')[0].lower().replace(' ', '_')
            if param_key in recommendations_map:
                rec = recommendations_map[param_key]
                if rec not in analysis['recommendations']:
                    analysis['recommendations'].append(rec)
    
    def process_lab_report_image(self, image_path: str) -> Dict[str, Any]:
        """
        Complete processing pipeline for lab report image.
        
        Args:
            image_path: Path to the lab report image
            
        Returns:
            Complete processed lab report data
        """
        try:
            # Extract text from image
            extracted_text = self.extract_text_from_image(image_path)
            
            # Parse lab parameters
            parsed_data = self.parse_lab_parameters(extracted_text)
            
            # Analyze results
            analysis = self.analyze_results(parsed_data)
            
            # Combine all data
            result = {
                'lab_test_name': parsed_data['test_metadata'].get('report_type', 'Lab Report'),
                'lab_date_conducted': parsed_data['patient_info'].get('date', datetime.now().strftime('%Y-%m-%d')),
                'lab_results': {param: data['value'] for param, data in parsed_data['lab_results'].items()},
                'lab_normal_ranges': parsed_data['lab_normal_ranges'],
                'patient_info': parsed_data['patient_info'],
                'interpretation_summary': analysis['interpretation_summary'],
                'interpretation_abnormalities': analysis['interpretation_abnormalities'],
                'recommendation_date': datetime.now().strftime('%Y-%m-%d'),
                'recommendation_action': '; '.join(analysis['recommendations']) if analysis['recommendations'] else 'No specific recommendations at this time.',
                'severity_level': analysis['severity_level'],
                'extracted_text': extracted_text,
                'processing_timestamp': datetime.now().isoformat(),
                'message': f"Lab report processed successfully. {len(parsed_data['lab_results'])} parameters extracted and analyzed."
            }
            
            return result
            
        except Exception as e:
            return {
                'error': True,
                'message': f"Error processing lab report: {str(e)}",
                'processing_timestamp': datetime.now().isoformat()
            }


def process_base64_image(base64_string: str, filename: str = "temp_lab_report.jpg") -> Dict[str, Any]:
    """
    Process lab report from base64 encoded image string.
    
    Args:
        base64_string: Base64 encoded image
        filename: Temporary filename to use
        
    Returns:
        Processed lab report data
    """
    try:
        # Decode base64 image
        image_data = base64.b64decode(base64_string)
        
        # Create PIL Image
        image = Image.open(io.BytesIO(image_data))
        
        # Save temporarily
        temp_path = f"/tmp/{filename}"
        image.save(temp_path)
        
        # Process the image
        processor = LabReportImageProcessor()
        result = processor.process_lab_report_image(temp_path)
        
        # Clean up temp file
        import os
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        return result
        
    except Exception as e:
        return {
            'error': True,
            'message': f"Error processing base64 image: {str(e)}",
            'processing_timestamp': datetime.now().isoformat()
        }


# Example usage
if __name__ == "__main__":
    processor = LabReportImageProcessor()
    
    # Example with image file
    try:
        result = processor.process_lab_report_image("path/to/lab_report.jpg")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")