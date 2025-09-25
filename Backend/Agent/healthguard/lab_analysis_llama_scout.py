#!/usr/bin/env python3
"""
Lab Report Analysis using meta-llama/llama-4-scout-17b-16e-instruct via Groq API
Converts images from the images folder to base64 and analyzes using the specified model
"""

import os
import base64
import json
import requests
from pathlib import Path
from datetime import datetime

class LabAnalysisLlamaScout:
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY')
        self.images_folder = Path("c:/Users/MALAVIKA/Documents/GitHub/Nexus-Hackbattle/Backend/Agent/images")
        self.model = "meta-llama/llama-4-scout-17b-16e-instruct"
        self.groq_base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.supported_formats = {'.jpg', '.jpeg', '.png'}
    
    def convert_image_to_base64(self, image_path: Path) -> str:
        """Convert image file to base64 string"""
        try:
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
                base64_encoded = base64.b64encode(image_data).decode('utf-8')
            return base64_encoded
        except Exception as e:
            raise Exception(f"Failed to convert image to base64: {e}")
    
    def get_lab_images(self) -> list:
        """Get all lab report images from the images folder"""
        if not self.images_folder.exists():
            raise Exception(f"Images folder not found: {self.images_folder}")
        
        image_files = []
        for ext in ['*.jpg', '*.jpeg', '*.png']:
            image_files.extend(list(self.images_folder.glob(ext)))
        
        return image_files
    
    def analyze_lab_report_with_llama_scout(self, image_path: Path) -> dict:
        """Analyze lab report using meta-llama/llama-4-scout-17b-16e-instruct"""
        
        if not self.api_key:
            raise Exception("GROQ_API_KEY environment variable not found")
        
        print(f"🏥 Analyzing lab report: {image_path.name}")
        print(f"🤖 Using model: {self.model}")
        
        # Convert image to base64
        base64_image = self.convert_image_to_base64(image_path)
        print(f"✅ Image converted to base64 ({len(base64_image)} characters)")
        
        # Prepare API request
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": """You are an expert medical AI assistant specializing in comprehensive lab report analysis. Your task is to analyze lab report images with the highest accuracy and provide detailed medical insights.

Please extract ALL visible information and provide a thorough analysis including:
1. Complete patient demographics and identification
2. Laboratory facility information
3. All test parameters with exact values, units, and reference ranges
4. Clinical interpretation of results
5. Identification of abnormal values and their significance
6. Health recommendations and follow-up suggestions

Return your analysis in a structured JSON format for easy processing."""
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"""Please analyze this lab report image ({image_path.name}) comprehensively and extract all medical data.

Provide a detailed JSON response with the following structure:
{{
  "patient_info": {{
    "name": "extracted patient name",
    "age": "patient age",
    "gender": "patient gender",
    "patient_id": "patient ID if available"
  }},
  "lab_details": {{
    "facility_name": "laboratory name",
    "address": "lab address",
    "report_id": "report identification",
    "collection_date": "sample collection date",
    "report_date": "report generation date",
    "referring_doctor": "doctor name if available"
  }},
  "test_results": [
    {{
      "parameter": "test name",
      "value": "measured value",
      "unit": "measurement unit",
      "reference_range": "normal range",
      "status": "normal/abnormal/critical",
      "clinical_significance": "medical interpretation"
    }}
  ],
  "clinical_summary": {{
    "abnormal_findings": ["list of abnormal results"],
    "critical_values": ["list of critical results"],
    "overall_assessment": "general health assessment",
    "recommendations": ["list of medical recommendations"],
    "follow_up_required": "yes/no with details"
  }},
  "ai_insights": {{
    "pattern_analysis": "analysis of result patterns",
    "risk_assessment": "health risk evaluation",
    "lifestyle_recommendations": ["lifestyle suggestions"],
    "monitoring_suggestions": ["what to monitor going forward"]
  }}
}}

Be extremely thorough and accurate in your extraction and analysis."""
                        },
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
            "temperature": 0.1
        }
        
        print("🚀 Sending to Groq API with Llama Scout model...")
        
        try:
            response = requests.post(
                self.groq_base_url,
                headers=headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_content = result['choices'][0]['message']['content']
                usage = result.get('usage', {})
                
                print("✅ SUCCESS! Lab Report Analysis Complete!")
                
                # Save the analysis
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                analysis_file = f"llama_scout_lab_analysis_{timestamp}.json"
                
                analysis_data = {
                    "image_analyzed": str(image_path),
                    "model_used": self.model,
                    "analysis_timestamp": timestamp,
                    "analysis_content": ai_content,
                    "usage_stats": usage,
                    "raw_response": result
                }
                
                with open(analysis_file, 'w', encoding='utf-8') as f:
                    json.dump(analysis_data, f, indent=2, ensure_ascii=False)
                
                print(f"💾 Analysis saved to: {analysis_file}")
                
                # Show API usage stats
                print(f"\n📊 API Usage Statistics:")
                print(f"   Model: {result.get('model', 'N/A')}")
                print(f"   Total Tokens: {usage.get('total_tokens', 'N/A')}")
                print(f"   Prompt Tokens: {usage.get('prompt_tokens', 'N/A')}")
                print(f"   Completion Tokens: {usage.get('completion_tokens', 'N/A')}")
                
                return analysis_data
                
            else:
                error_msg = f"Groq API Error: {response.status_code} - {response.text}"
                print(f"❌ {error_msg}")
                
                if response.status_code == 401:
                    print("🔑 Check your GROQ_API_KEY - it might be invalid")
                elif response.status_code == 429:
                    print("⏰ Rate limit exceeded - try again in a moment")
                elif response.status_code == 400:
                    print("📝 Bad request - check if the model supports vision")
                
                raise Exception(error_msg)
                
        except requests.exceptions.Timeout:
            error_msg = "Request timed out - the image might be too large"
            print(f"⏰ {error_msg}")
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
    
    def process_all_lab_images(self) -> list:
        """Process all lab images in the images folder"""
        results = []
        
        try:
            image_files = self.get_lab_images()
            
            if not image_files:
                print("❌ No lab report images found in the images folder")
                return results
            
            print(f"📸 Found {len(image_files)} lab report image(s):")
            for img in image_files:
                print(f"   • {img.name}")
            
            # Process each image
            for image_path in image_files:
                try:
                    analysis_result = self.analyze_lab_report_with_llama_scout(image_path)
                    results.append(analysis_result)
                    print(f"✅ Successfully analyzed: {image_path.name}\n")
                except Exception as e:
                    print(f"❌ Failed to analyze {image_path.name}: {e}\n")
                    results.append({
                        "image_analyzed": str(image_path),
                        "error": str(e),
                        "status": "failed"
                    })
            
            return results
            
        except Exception as e:
            print(f"❌ Error processing images: {e}")
            return results

def main():
    """Main function to run the lab analysis"""
    print("🏥 Lab Report Analysis with Llama Scout")
    print("=" * 45)
    
    analyzer = LabAnalysisLlamaScout()
    results = analyzer.process_all_lab_images()
    
    if results:
        successful = sum(1 for r in results if 'error' not in r)
        failed = len(results) - successful
        
        print(f"\n📊 Analysis Summary:")
        print(f"   Total images: {len(results)}")
        print(f"   Successfully analyzed: {successful}")
        print(f"   Failed: {failed}")
        
        if successful > 0:
            print(f"\n🎉 Lab report analysis completed successfully!")
            print(f"   Check the generated JSON files for detailed results.")
        else:
            print(f"\n😞 No images were successfully analyzed.")
    else:
        print(f"\n❌ No images found to analyze.")

if __name__ == "__main__":
    main()