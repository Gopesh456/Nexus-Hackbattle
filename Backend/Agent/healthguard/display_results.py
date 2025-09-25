#!/usr/bin/env python3
"""
Display lab analysis results in terminal with nice formatting
"""

import json
import os
from pathlib import Path

def display_lab_analysis():
    """Display the lab analysis results in a formatted way in terminal"""
    
    # Find the most recent analysis file
    current_dir = Path(".")
    analysis_files = list(current_dir.glob("*lab_analysis_*.json"))
    
    if not analysis_files:
        print("❌ No lab analysis files found!")
        return
    
    # Get the most recent file
    latest_file = max(analysis_files, key=os.path.getctime)
    
    print("🏥 LAB ANALYSIS RESULTS")
    print("=" * 60)
    print(f"📄 File: {latest_file.name}")
    print("=" * 60)
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract the analysis content JSON from the string
        analysis_content = data.get('analysis_content', '')
        
        # Find the JSON part in the analysis content
        start_json = analysis_content.find('{')
        end_json = analysis_content.rfind('}') + 1
        
        if start_json != -1 and end_json != -1:
            json_str = analysis_content[start_json:end_json]
            analysis_data = json.loads(json_str)
            
            # Display Patient Info
            patient_info = analysis_data.get('patient_info', {})
            print(f"👤 PATIENT: {patient_info.get('name', 'N/A')}")
            print(f"📅 Age: {patient_info.get('age', 'N/A')}")
            print(f"⚧ Gender: {patient_info.get('gender', 'N/A')}")
            print(f"🆔 ID: {patient_info.get('patient_id', 'N/A')}")
            print()
            
            # Display Lab Details
            lab_details = analysis_data.get('lab_details', {})
            print(f"🏥 LAB: {lab_details.get('facility_name', 'N/A')}")
            print(f"👨‍⚕️ Doctor: {lab_details.get('referring_doctor', 'N/A')}")
            print(f"📅 Date: {lab_details.get('collection_date', 'N/A')}")
            print()
            
            # Display Abnormal Findings
            clinical_summary = analysis_data.get('clinical_summary', {})
            abnormal_findings = clinical_summary.get('abnormal_findings', [])
            
            if abnormal_findings:
                print("🚨 ABNORMAL FINDINGS:")
                print("-" * 40)
                for finding in abnormal_findings:
                    print(f"❌ {finding}")
                print()
            
            # Display Test Results Table Header
            print("📊 COMPLETE TEST RESULTS:")
            print("-" * 80)
            print(f"{'PARAMETER':<25} {'VALUE':<10} {'UNIT':<8} {'RANGE':<15} {'STATUS':<10}")
            print("-" * 80)
            
            # Display Test Results
            test_results = analysis_data.get('test_results', [])
            for test in test_results:
                param = test.get('parameter', '')[:24]
                value = str(test.get('value', ''))[:9]
                unit = test.get('unit', '')[:7]
                range_val = test.get('reference_range', '')[:14]
                status = test.get('status', '')
                
                # Color coding based on status
                if status.lower() == 'low' or status.lower() == 'high':
                    status_symbol = "❌"
                elif status.lower() == 'borderline':
                    status_symbol = "⚠️"
                else:
                    status_symbol = "✅"
                
                print(f"{param:<25} {value:<10} {unit:<8} {range_val:<15} {status_symbol} {status}")
            
            print("-" * 80)
            print()
            
            # Display Clinical Assessment
            overall_assessment = clinical_summary.get('overall_assessment', '')
            if overall_assessment:
                print("🔍 CLINICAL ASSESSMENT:")
                print("-" * 40)
                print(f"{overall_assessment}")
                print()
            
            # Display Recommendations
            recommendations = clinical_summary.get('recommendations', [])
            if recommendations:
                print("💡 RECOMMENDATIONS:")
                print("-" * 40)
                for i, rec in enumerate(recommendations, 1):
                    print(f"{i}. {rec}")
                print()
            
            # Display AI Insights
            ai_insights = analysis_data.get('ai_insights', {})
            if ai_insights:
                print("🤖 AI INSIGHTS:")
                print("-" * 40)
                
                pattern_analysis = ai_insights.get('pattern_analysis', '')
                if pattern_analysis:
                    print(f"🔍 Pattern Analysis:")
                    print(f"   {pattern_analysis}")
                    print()
                
                risk_assessment = ai_insights.get('risk_assessment', '')
                if risk_assessment:
                    print(f"⚠️ Risk Assessment:")
                    print(f"   {risk_assessment}")
                    print()
                
                lifestyle_recs = ai_insights.get('lifestyle_recommendations', [])
                if lifestyle_recs:
                    print(f"🥗 Lifestyle Recommendations:")
                    for i, rec in enumerate(lifestyle_recs, 1):
                        print(f"   {i}. {rec}")
                    print()
                
                monitoring = ai_insights.get('monitoring_suggestions', [])
                if monitoring:
                    print(f"📅 Monitoring Suggestions:")
                    for i, mon in enumerate(monitoring, 1):
                        print(f"   {i}. {mon}")
                    print()
            
            # Display Technical Info
            print("🤖 TECHNICAL DETAILS:")
            print("-" * 40)
            print(f"Model: {data.get('model_used', 'N/A')}")
            print(f"Timestamp: {data.get('analysis_timestamp', 'N/A')}")
            
            usage_stats = data.get('usage_stats', {})
            if usage_stats:
                print(f"Tokens Used: {usage_stats.get('total_tokens', 'N/A')}")
                print(f"Processing Time: {usage_stats.get('total_time', 'N/A'):.2f}s")
            
            print()
            print("=" * 60)
            print("✅ Lab Analysis Display Complete!")
            print("=" * 60)
            
        else:
            print("❌ Could not parse analysis content")
            
    except Exception as e:
        print(f"❌ Error reading analysis file: {e}")

if __name__ == "__main__":
    display_lab_analysis()