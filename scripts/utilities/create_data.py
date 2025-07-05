#!/usr/bin/env python3
"""
Comprehensive Data Creation Tool
Allows creation of courses or players from a single menu.
"""

import subprocess
import os
import sys

def show_menu():
    print("\n🎉 Data Creation Tool")
    print("=" * 40)
    print("1. Create a course")
    print("2. Create a player")
    print("3. Exit")
    print("=" * 40)

def create_course():
    script_path = os.path.join(os.path.dirname(__file__), '../courses/generate_complete_course.py')
    print("\n🏌️  Creating a course...")
    subprocess.run([sys.executable, script_path])

def create_player():
    script_path = os.path.join(os.path.dirname(__file__), '../players/generate_complete_player.py')
    print("\n👤 Creating a player...")
    subprocess.run([sys.executable, script_path])

def main():
    while True:
        show_menu()
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            if choice == '1':
                create_course()
            elif choice == '2':
                create_player()
            elif choice == '3':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-3.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 