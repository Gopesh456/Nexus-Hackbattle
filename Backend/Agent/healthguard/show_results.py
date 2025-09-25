#!/usr/bin/env python3
"""
Display the latest lab analysis results in terminal
"""

import json
import os
from pathlib import Path

def display_latest_results():
    """Display the most recent lab analysis results"""
    
    # Find the most recent analysis file
    current_dir = Path(".")
    analysis_files = list(current_dir.glob("llama_scout_lab_analysis_*.json"))
    
    if not analysis_files:
        print("❌ No lab analysis files found!")
        return
    
    # Get the most recent file
    latest_file = max(analysis_files, key=os.path.getctime)
    
    print("🏥 LAB REPORT ANALYSIS RESULTS")
    print("=" * 80)
    print(f"📄 File: {latest_file.name}")
    print("=" * 80)
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract the analysis content
        analysis_content = data.get('analysis_content', '')
        
        # Find the JSON part in the analysis content
        start_json = analysis_content.find('```json\n{')
        end_json = analysis_content.rfind('\n```')
        
        if start_json != -1 and end_json != -1:
            json_str = analysis_content[start_json + 8:end_json]  # Skip ```json\n
            try:
                analysis_data = json.loads(json_str)
                
                # Display Patient Info
                patient_info = analysis_data.get('patient_info', {})
                print(f"\n👤 PATIENT INFORMATION:")
                print(f"   Name: {patient_info.get('name', 'N/A')}")
                print(f"   Age: {patient_info.get('age', 'N/A')}")
                print(f"   Gender: {patient_info.get('gender', 'N/A')}")
                print(f"   Patient ID: {patient_info.get('patient_id', 'N/A')}")
                
                # Display Lab Details
                lab_details = analysis_data.get('lab_details', {})
                print(f"\n🏥 LAB DETAILS:")
                print(f"   Facility: {lab_details.get('facility_name', 'N/A')}")
                print(f"   Doctor: {lab_details.get('referring_doctor', 'N/A')}")
                print(f"   Collection Date: {lab_details.get('collection_date', 'N/A')}")
                
                # Display Abnormal Findings
                clinical_summary = analysis_data.get('clinical_summary', {})
                abnormal_findings = clinical_summary.get('abnormal_findings', [])
                
                print(f"\n🚨 ABNORMAL FINDINGS:")
                if abnormal_findings:
                    for finding in abnormal_findings:
                        print(f"   ❌ {finding}")
                else:
                    print("   ✅ No abnormal findings detected")
                
                # Display Test Results
                print(f"\n📊 COMPLETE TEST RESULTS:")
                print("-" * 90)
                print(f"{'Parameter':<30} {'Value':<10} {'Unit':<8} {'Range':<15} {'Status'}")
                print("-" * 90)
                
                test_results = analysis_data.get('test_results', [])
                for test in test_results:
                    param = test.get('parameter', '')[:29]
                    value = str(test.get('value', ''))[:9]
                    unit = test.get('unit', '')[:7]
                    range_val = test.get('reference_range', '')[:14]
                    status = test.get('status', '')
                    
                    # Status symbols
                    if status == "Normal":
                        symbol = "✅"
                    elif status in ["Low", "High"]:
                        symbol = "❌"
                    else:
                        symbol = "⚠️"
                    
                    print(f"{param:<30} {value:<10} {unit:<8} {range_val:<15} {symbol} {status}")
                
                print("-" * 90)
                
                # Display Clinical Assessment
                overall_assessment = clinical_summary.get('overall_assessment', '')
                if overall_assessment:
                    print(f"\n🩺 CLINICAL ASSESSMENT:")
                    print(f"   {overall_assessment}")
                
                # Display Recommendations
                recommendations = clinical_summary.get('recommendations', [])
                if recommendations:
                    print(f"\n💊 RECOMMENDATIONS:")
                    for i, rec in enumerate(recommendations, 1):
                        print(f"   {i}. {rec}")
                
                # Display AI Insights
                ai_insights = analysis_data.get('ai_insights', {})
                if ai_insights:
                    print(f"\n🤖 AI INSIGHTS:")
                    
                    pattern_analysis = ai_insights.get('pattern_analysis', '')
                    if pattern_analysis:
                        print(f"   🔍 Pattern Analysis: {pattern_analysis}")
                    
                    risk_assessment = ai_insights.get('risk_assessment', '')
                    if risk_assessment:
                        print(f"   ⚠️ Risk Assessment: {risk_assessment}")
                    
                    lifestyle_recs = ai_insights.get('lifestyle_recommendations', [])
                    if lifestyle_recs:
                        print(f"\n   🥗 Lifestyle Recommendations:")
                        for i, rec in enumerate(lifestyle_recs, 1):
                            print(f"      {i}. {rec}")
                    
                    monitoring = ai_insights.get('monitoring_suggestions', [])
                    if monitoring:
                        print(f"\n   📅 Monitoring Suggestions:")
                        for i, mon in enumerate(monitoring, 1):
                            print(f"      {i}. {mon}")
                
                # Display Technical Info
                print(f"\n🤖 TECHNICAL DETAILS:")
                print(f"   Model: {data.get('model_used', 'N/A')}")
                print(f"   Timestamp: {data.get('analysis_timestamp', 'N/A')}")
                
                usage_stats = data.get('usage_stats', {})
                if usage_stats:
                    print(f"   Total Tokens: {usage_stats.get('total_tokens', 'N/A')}")
                    print(f"   Processing Time: {usage_stats.get('total_time', 0):.2f}s")
                
                print("\n" + "=" * 80)
                print("✅ Lab Analysis Display Complete!")
                print("=" * 80)
                
            except json.JSONDecodeError as e:
                print(f"❌ Error parsing nested JSON: {e}")
                print("Raw analysis content:")
                print(analysis_content[:1000] + "..." if len(analysis_content) > 1000 else analysis_content)
        else:
            print("❌ Could not find JSON structure in analysis content")
            print("Raw content preview:")
            print(analysis_content[:500] + "..." if len(analysis_content) > 500 else analysis_content)
            
    except Exception as e:
        print(f"❌ Error reading analysis file: {e}")

if __name__ == "__main__":
    display_latest_results()