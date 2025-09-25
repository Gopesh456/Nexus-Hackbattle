#!/usr/bin/env python
import sys
import warnings
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env'))

from healthguard.crew import Healthguard

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run_single_agent(agent_name: str):
    """
    Run a single agent by name.
    """
    inputs = {
        'user_name': 'John Doe',
        'user_age': 35,
        'user_symptoms': ['fever', 'cough', 'headache'],
        'medicine_name': 'Paracetamol',
        'medicine_dosage': '500mg',
        'medicine_frequency': '3 times per day',
        'medicine_timing': ['8:00 AM', '2:00 PM', '8:00 PM'],
        'medicine_quantity_available': 30,
        'medicine_special_instructions': 'Take with food',
        'lab_test_name': 'Blood Test',
        'lab_date_conducted': '2024-09-20',
        'health_data_sources': ['Fitbit', 'Manual input'],
        'health_key_metrics': {'heart_rate': 75, 'blood_pressure': '120/80'},
        'user_command': 'Set a reminder for medication',
        'current_year': str(datetime.now().year)
    }

    try:
        result = Healthguard().run_single_agent(agent_name=agent_name, inputs=inputs)
        print(f"Agent '{agent_name}' execution completed successfully!")
        print(f"Result: {result}")
        return result

    except Exception as e:
        raise Exception(f"An error occurred while running agent '{agent_name}': {e}")
        
        

def interactive_agent_selection():
    """
    Interactive mode to let user select which agent to run.
    """
    print("HealthGuard Agent Selection")
    print("=" * 40)
    print("Available Agents:")
    print("1. Nurse Agent - Book appointments and assess symptoms")
    print("2. Medication Agent - Manage medicines and reminders")
    print("3. Labs Agent - Handle lab test results and reports")
    print("4. Guardian Agent - Health monitoring and alerts")
    print("5. Voice Agent - Voice-based health assistance")
    print("6. Run Full Crew - Execute all agents together")
    print("0. Exit")
    print("=" * 40)

    while True:
        try:
            choice = input("Select an agent (0-6): ").strip()

            if choice == "0":
                print("Goodbye!")
                return

            elif choice == "1":
                print("\n Running Nurse Agent...")
                run_single_agent("nurse")
                break

            elif choice == "2":
                print("\n Running Medication Agent...")
                run_single_agent("med")
                break

            elif choice == "3":
                print("\n Running Labs Agent...")
                run_single_agent("labs")
                break

            elif choice == "4":
                print("\n Running Guardian Agent...")
                run_single_agent("guardian")
                break

            elif choice == "5":
                print("\n Running Voice Agent...")
                run_single_agent("voice")
                break

            elif choice == "6":
                print("\n Running Full Crew...")
                run()
                break

            else:
                print(" Invalid choice. Please select 0-6.")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            return
        except Exception as e:
            print(f" Error: {e}")
            return


def run():
    """
    Run the full crew.
    """
    inputs = {
        'user_name': 'John Doe',
        'user_age': 35,
        'user_symptoms': ['fever', 'cough', 'headache'],
        'medicine_name': 'Paracetamol',
        'medicine_dosage': '500mg',
        'medicine_frequency': '3 times per day',
        'medicine_timing': ['8:00 AM', '2:00 PM', '8:00 PM'],
        'medicine_quantity_available': 30,
        'medicine_special_instructions': 'Take with food',
        'lab_test_name': 'Blood Test',
        'lab_date_conducted': '2024-09-20',
        'health_data_sources': ['Fitbit', 'Manual input'],
        'health_key_metrics': {'heart_rate': 75, 'blood_pressure': '120/80'},
        'user_command': 'Set a reminder for medication',
        'current_year': str(datetime.now().year)
    }

    try:
        result = Healthguard().crew().kickoff(inputs=inputs)
        print("Crew execution completed successfully!")
        print(f"Result: {result}")
        return result

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'user_name': 'Jane Smith',
        'user_age': 28,
        'user_symptoms': ['chest pain', 'shortness of breath'],
        'medicine_name': 'Aspirin',
        'medicine_dosage': '100mg',
        'medicine_frequency': 'once daily',
        'medicine_timing': ['9:00 AM'],
        'medicine_quantity_available': 60,
        'medicine_special_instructions': 'Take with water',
        'lab_test_name': 'ECG',
        'lab_date_conducted': '2024-09-15',
        'health_data_sources': ['Apple Watch', 'Health App'],
        'health_key_metrics': {'steps': 8500, 'calories': 2100},
        'user_command': 'Check my health status',
        'current_year': str(datetime.now().year)
    }
    try:
        Healthguard().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Healthguard().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'user_name': 'Alice Johnson',
        'user_age': 45,
        'user_symptoms': ['nausea', 'dizziness'],
        'medicine_name': 'Ibuprofen',
        'medicine_dosage': '200mg',
        'medicine_frequency': 'twice daily',
        'medicine_timing': ['8:00 AM', '8:00 PM'],
        'medicine_quantity_available': 20,
        'medicine_special_instructions': 'Take after meals',
        'lab_test_name': 'Thyroid Function Test',
        'lab_date_conducted': '2024-09-10',
        'health_data_sources': ['Manual input', 'Scale'],
        'health_key_metrics': {'weight': 68.5, 'bmi': 24.2},
        'user_command': 'Schedule a doctor appointment',
        'current_year': str(datetime.now().year)
    }

    try:
        result = Healthguard().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
        print("Crew test completed successfully!")
        print(f"Test Result: {result}")
        return result

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("HealthGuard - No arguments provided, starting interactive mode...")
        interactive_agent_selection()
        sys.exit(0)

    command = sys.argv[1].lower()

    if command == "run":
        run()
    elif command == "interactive":
        interactive_agent_selection()
    elif command == "run_agent":
        if len(sys.argv) != 3:
            print("Usage: python main.py run_agent <agent_name>")
            print("Available agents: nurse, med, labs, guardian, voice")
            sys.exit(1)
        agent_name = sys.argv[2].lower()
        run_single_agent(agent_name)
    elif command == "train":
        if len(sys.argv) != 4:
            print("Usage: python main.py train <n_iterations> <filename>")
            sys.exit(1)
        train()
    elif command == "test":
        if len(sys.argv) != 4:
            print("Usage: python main.py test <n_iterations> <eval_llm>")
            sys.exit(1)
        test()
    elif command == "replay":
        if len(sys.argv) != 3:
            print("Usage: python main.py replay <task_id>")
            sys.exit(1)
        replay()
    else:
        print(f"Unknown command: {command}")
        print("Available commands:")
        print("  python main.py                        # Interactive agent selection")
        print("  python main.py run                    # Run the full crew")
        print("  python main.py interactive            # Interactive agent selection")
        print("  python main.py run_agent <agent_name> # Run a single agent (nurse, med, labs, guardian, voice)")
        print("  python main.py train <n_iterations> <filename>  # Train the crew")
        print("  python main.py test <n_iterations> <eval_llm>   # Test the crew")
        print("  python main.py replay <task_id>       # Replay from a specific task")
        sys.exit(1)
