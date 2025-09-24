#!/usr/bin/env python3
"""
Example script demonstrating JSON prompt storage and response generation
for the HealthGuard system.
"""

import sys
import os
import json
from datetime import datetime

# Add the src directory to the path so we can import our tools
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from healthguard.tools.custom_tool import (
    JSONStorageTool, 
    JSONResponseTool, 
    JSONProcessorTool
)

def demonstrate_json_workflow():
    """Demonstrate the complete JSON prompt storage and response workflow."""
    
    print("=" * 60)
    print("HealthGuard JSON Prompt Storage & Response Demo")
    print("=" * 60)
    
    # Initialize tools
    storage_tool = JSONStorageTool()
    processor_tool = JSONProcessorTool()
    
    # Example prompts for different categories
    example_prompts = [
        {
            "prompt": "I have been feeling dizzy and experiencing headaches for the past 3 days. Should I be concerned?",
            "category": "health",
            "filename": "health_query"
        },
        {
            "prompt": "I need to book an appointment with a cardiologist for next week.",
            "category": "appointment", 
            "filename": "appointment_request"
        },
        {
            "prompt": "Can I take ibuprofen with my blood pressure medication?",
            "category": "medication",
            "filename": "medication_query"
        }
    ]
    
    stored_files = []
    
    print("\n1. STORING PROMPTS IN JSON FORMAT")
    print("-" * 40)
    
    for i, example in enumerate(example_prompts, 1):
        print(f"\nExample {i}: {example['category'].title()} Query")
        print(f"Prompt: {example['prompt'][:50]}...")
        
        # Store the prompt
        result = storage_tool._run(
            prompt=example['prompt'],
            filename=example['filename'],
            category=example['category']
        )
        print(f"Storage Result: {result}")
        
        # Extract the filepath from the result for processing
        if "data/" in result:
            filepath = result.split("data/")[1].split(".")[0] + ".json"
            stored_files.append(f"data/{filepath}")
    
    print("\n2. PROCESSING STORED PROMPTS")
    print("-" * 40)
    
    for i, filepath in enumerate(stored_files, 1):
        if os.path.exists(filepath):
            print(f"\nProcessing file {i}: {filepath}")
            
            # Process the stored prompt
            result = processor_tool._run(prompt_file=filepath)
            print(f"Processing Result: {result}")
        else:
            print(f"File not found: {filepath}")
    
    print("\n3. EXAMINING GENERATED FILES")
    print("-" * 40)
    
    # List all files in the data directory
    data_dir = "data"
    if os.path.exists(data_dir):
        files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
        
        print(f"\nGenerated files in {data_dir}/:")
        for file in sorted(files):
            filepath = os.path.join(data_dir, file)
            print(f"  - {file}")
            
            # Show a snippet of each file
            with open(filepath, 'r') as f:
                data = json.load(f)
                if 'prompt' in data:
                    print(f"    Type: Prompt | Category: {data.get('category', 'N/A')}")
                elif 'response_data' in data:
                    print(f"    Type: Response | Response Type: {data.get('response_type', 'N/A')}")
    else:
        print("No data directory found.")
    
    print("\n" + "=" * 60)
    print("Demo completed! Check the 'data/' directory for generated JSON files.")
    print("=" * 60)

def show_usage_examples():
    """Show examples of how to use the JSON tools in CrewAI tasks."""
    
    print("\n" + "=" * 60)
    print("USAGE EXAMPLES FOR CREWAI TASKS")
    print("=" * 60)
    
    examples = {
        "Store a health query": {
            "tool": "json_storage",
            "example": "json_storage(prompt='Patient reports chest pain and shortness of breath', filename='emergency_query', category='health')"
        },
        "Process stored prompt": {
            "tool": "json_processor", 
            "example": "json_processor(prompt_file='data/health_query_prompt.json')"
        },
        "Store a custom response": {
            "tool": "json_response",
            "example": "json_response(response_data='{\"diagnosis\": \"preliminary assessment needed\"}', prompt_id='health_20241001_120000', response_type='medical')"
        }
    }
    
    for title, info in examples.items():
        print(f"\n{title}:")
        print(f"  Tool: {info['tool']}")
        print(f"  Example: {info['example']}")

if __name__ == "__main__":
    try:
        demonstrate_json_workflow()
        show_usage_examples()
        
        print(f"\n✅ JSON workflow demonstration completed successfully!")
        print(f"📁 Check the 'data/' directory for all generated JSON files.")
        
    except Exception as e:
        print(f"❌ Error during demonstration: {str(e)}")
        import traceback
        traceback.print_exc()