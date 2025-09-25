#!/usr/bin/env python3
"""
Browser Use AI Agent to find nearest hospital to VIT Vellore
Uses Groq LLM provider with headless browser mode
"""

import asyncio
import os
from browser_use import Agent, Browser, ChatGroq
from dotenv import load_dotenv

load_dotenv()

async def search_hospital_near_vit():

    groq_api_key = os.getenv('GROQ_API_KEY')
    if not groq_api_key:
        print("Error: GROQ_API_KEY not found in environment variables")
        print("Please set your Groq API key in .env file")
        return

    llm = ChatGroq(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        api_key=groq_api_key
    )


    browser = Browser()

    task = """
    Find the nearest hospitals to VIT University Vellore (Tamil Nadu, India).
    For each hospital, extract:
    1. Hospital name and full address
    2. Distance from VIT Vellore
    3. Contact phone numbers

    Search on the browser for hospitals with high ratings.
    Focus on hospitals within 10-15 km radius of VIT Vellore.
    """

    print("Starting hospital search near VIT Vellore...")
    print("Using Groq LLM with headless browser mode")
    print("-" * 50)

    try:
        # Create and run the AI agent
        agent = Agent(
            task=task,
            llm=llm,
            browser=browser,
            use_vision=True,  # Enable vision for better web scraping
            max_steps=25,     # Allow more steps for comprehensive search
            verbose=True
        )

        result = await agent.run()

        print("\n" + "="*60)
        print("HOSPITAL SEARCH RESULTS")
        print("="*60)

      
        if result:
            print(result)
        else:
            print("No results obtained from the search")

        
        if hasattr(result, 'extracted_content') and result.extracted_content():
            print("\n EXTRACTED CONTENT:")
            print("-" * 30)
            extracted = result.extracted_content()
            if isinstance(extracted, list):
                for item in extracted:
                    print(f"• {item}")
            else:
                print(extracted)

        print("\n Search completed successfully!")

    except Exception as e:
        print(f" Error during hospital search: {str(e)}")
        print("Please check your Groq API key and internet connection")

    finally:
        
        await browser.stop()

def main():
    """Main function to run the hospital search"""
    print(" VIT Vellore Hospital Search Tool")
    print("Using Browser-Use AI Agent + Groq LLM")
    print("=" * 50)

    # Run the async search
    asyncio.run(search_hospital_near_vit())

if __name__ == "__main__":
    main()