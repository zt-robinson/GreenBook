#!/usr/bin/env python3
"""
Generate Multiple Courses Script
Tests the duplicate detection system by generating multiple courses
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from courses.generate_complete_course import generate_complete_course, insert_course_to_database, load_data

def generate_multiple_courses(num_courses=10):
    """Generate multiple courses to test duplicate detection"""
    print(f"🏌️  Generating {num_courses} courses to test duplicate detection...")
    print("=" * 80)
    
    # Load data
    cities_df = load_data()
    if cities_df is None:
        print("❌ Failed to load cities data")
        return
    
    successful_courses = 0
    duplicate_avoided = 0
    
    for i in range(num_courses):
        print(f"\n🔄 Generating course {i+1}/{num_courses}...")
        
        # Generate course
        course = generate_complete_course(cities_df=cities_df)
        
        if course:
            # Try to insert into database
            course_id = insert_course_to_database(course)
            if course_id:
                successful_courses += 1
                print(f"✅ Course {i+1}: {course['name']} (ID: {course_id})")
            else:
                duplicate_avoided += 1
                print(f"⚠️  Course {i+1}: {course['name']} - Duplicate avoided")
        else:
            print(f"❌ Course {i+1}: Failed to generate")
    
    print(f"\n🎉 Generation Complete!")
    print(f"✅ Successfully created: {successful_courses} courses")
    print(f"⚠️  Duplicates avoided: {duplicate_avoided} courses")
    print(f"📊 Success rate: {successful_courses/(successful_courses+duplicate_avoided)*100:.1f}%")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Generate multiple golf courses')
    parser.add_argument('--count', type=int, default=10, help='Number of courses to generate (default: 10)')
    
    args = parser.parse_args()
    generate_multiple_courses(args.count) 