#!/usr/bin/env python3
"""
Simplified CrewAI runner without build tool dependencies
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def run_simple_crew():
    """Run CrewAI without complex dependencies"""
    
    print("🤖 Starting Simplified CrewAI Lab Analysis")
    print("=" * 45)
    
    try:
        # Import simplified components
        from crewai import Agent, Task, Crew, Process
        from langchain_groq import ChatGroq
        
        print("✅ CrewAI components loaded successfully")
        
        # Check API key
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            print("❌ GROQ_API_KEY not found")
            return
        
        print("✅ Groq API Key configured")
        
        # Create LLM
        llm = ChatGroq(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            api_key=api_key,
            temperature=0.1
        )
        
        print("✅ Groq LLM initialized")
        
        # Create simplified lab analysis agent
        lab_agent = Agent(
            role="Lab Report Analyst",
            goal="Analyze lab report images and extract medical data using hybrid OCR + AI approach",
            backstory="""You are an expert medical data analyst who specializes in processing 
            lab report images. You use OCR to extract text and then analyze it with AI to 
            provide comprehensive medical insights.""",
            llm=llm,
            verbose=True
        )
        
        print("✅ Lab Analysis Agent created")
        
        # Create lab analysis task
        lab_task = Task(
            description="""Process lab report images from the images folder using hybrid approach:
            
            1. Scan the images folder for lab report images
            2. Extract text using OCR methods
            3. Analyze extracted text with Groq AI for medical insights
            4. Provide comprehensive JSON output with:
               - Patient information
               - All lab parameters with values and reference ranges
               - Abnormal findings with clinical interpretations
               - Health recommendations and follow-up guidance
            
            Focus on accuracy and provide detailed medical analysis.""",
            expected_output="""Complete JSON object containing:
            - patient_info: name, age, gender, ID
            - lab_info: lab name, report ID, dates
            - test_results: all parameters with values, units, ranges, status
            - abnormal_findings: detailed clinical interpretations
            - overall_assessment: health status and recommendations""",
            agent=lab_agent
        )
        
        print("✅ Lab Analysis Task created")
        
        # Create simplified crew
        crew = Crew(
            agents=[lab_agent],
            tasks=[lab_task],
            process=Process.sequential,
            verbose=True
        )
        
        print("✅ CrewAI Crew assembled")
        print("🚀 Starting lab report analysis...")
        
        # Run the crew
        result = crew.kickoff()
        
        print("✅ CrewAI Analysis Completed!")
        print("=" * 50)
        print("RESULT:")
        print(result)
        print("=" * 50)
        
        # Save result
        with open("crewai_lab_result.txt", "w") as f:
            f.write(str(result))
        
        print("💾 Result saved to: crewai_lab_result.txt")
        
        return result
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Falling back to hybrid processor...")
        
        # Fallback to our working hybrid system
        try:
            from hybrid_lab_processor import process_lab_report_hybrid
            result = process_lab_report_hybrid()
            print("✅ Hybrid processor completed successfully!")
            return result
        except Exception as e2:
            print(f"❌ Hybrid fallback failed: {e2}")
            return None
        
    except Exception as e:
        print(f"❌ CrewAI error: {e}")
        print("💡 This is likely due to missing build dependencies")
        
        # Fallback to hybrid system
        print("🔄 Using working hybrid system instead...")
        try:
            from hybrid_lab_processor import process_lab_report_hybrid
            result = process_lab_report_hybrid()
            print("✅ Hybrid system completed successfully!")
            return result
        except Exception as e2:
            print(f"❌ Hybrid fallback failed: {e2}")
            return None

if __name__ == "__main__":
    print("🏥 Lab Report Analysis System")
    print("Trying CrewAI, falling back to hybrid if needed...")
    print()
    
    result = run_simple_crew()
    
    if result:
        print("\n🎉 Lab report analysis completed!")
        print("Your medical data has been processed and analyzed.")
    else:
        print("\n😞 Analysis failed. Check the errors above.")