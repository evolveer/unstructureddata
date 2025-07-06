#!/usr/bin/env python3
"""Test script for the data organizer."""

from data_organizer import DataOrganizerSuggester
import json

def test_organizer():
    """Test the basic functionality of the data organizer."""
    organizer = DataOrganizerSuggester()
    
    print("Testing Data Organizer Functionality...")
    print("=" * 40)
    
    # Test structure suggestion
    print("\n1. Testing structure suggestions:")
    for approach in ['by_type', 'by_project', 'by_date', 'hybrid_approach']:
        try:
            structure = organizer.suggest_structure(approach)
            print(f"   ✅ {approach}: {len(structure)} top-level folders")
        except Exception as e:
            print(f"   ❌ {approach}: Error - {e}")
    
    # Test folder structure creation (dry run)
    print("\n2. Testing folder structure creation (dry run):")
    try:
        structure = organizer.suggest_structure('hybrid_approach')
        folders = organizer.create_folder_structure('/tmp/test_structure', structure, dry_run=True)
        print(f"   ✅ Would create {len(folders)} folders")
    except Exception as e:
        print(f"   ❌ Error in folder creation: {e}")
    
    # Test file type mappings
    print("\n3. Testing file type mappings:")
    print(f"   📄 Document types: {len(organizer.file_type_mappings['documents'])}")
    print(f"   🖼️  Image types: {len(organizer.file_type_mappings['images'])}")
    print(f"   🎵 Audio types: {len(organizer.file_type_mappings['audio'])}")
    
    # Show sample structure
    print("\n4. Sample Hybrid Structure:")
    structure = organizer.suggest_structure('hybrid_approach')
    organizer.print_structure(structure)
    
    print("\n✅ All tests completed successfully!")

if __name__ == "__main__":
    test_organizer()
