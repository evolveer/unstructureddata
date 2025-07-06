#!/usr/bin/env python3
"""
Data Organization Structure Suggester

This script suggests optimal folder structures for organizing unsorted, unstructured data
based on different organizational approaches and data types.
"""

import os
import json
from datetime import datetime
from pathlib import Path


class DataOrganizerSuggester:
    """Suggests folder structures for organizing unstructured data."""
    
    def __init__(self):
        self.base_structures = {
            'by_type': {
                'Documents': {
                    'PDFs': [],
                    'Word_Documents': [],
                    'Spreadsheets': [],
                    'Presentations': [],
                    'Text_Files': [],
                    'Archives': []
                },
                'Media': {
                    'Images': {
                        'Photos': [],
                        'Screenshots': [],
                        'Graphics': [],
                        'Icons': []
                    },
                    'Videos': {
                        'Personal': [],
                        'Work': [],
                        'Educational': []
                    },
                    'Audio': {
                        'Music': [],
                        'Recordings': [],
                        'Podcasts': []
                    }
                },
                'Code_and_Development': {
                    'Projects': [],
                    'Scripts': [],
                    'Documentation': [],
                    'Resources': []
                },
                'Data_Files': {
                    'Databases': [],
                    'CSV_Files': [],
                    'JSON_Files': [],
                    'XML_Files': [],
                    'Logs': []
                },
                'Miscellaneous': {
                    'Temporary': [],
                    'Unsorted': [],
                    'To_Review': []
                }
            },
            
            'by_project': {
                'Active_Projects': {
                    'Project_A': {
                        'Documents': [],
                        'Media': [],
                        'Data': [],
                        'Resources': []
                    },
                    'Project_B': {
                        'Documents': [],
                        'Media': [],
                        'Data': [],
                        'Resources': []
                    }
                },
                'Completed_Projects': {
                    'Archive_2024': [],
                    'Archive_2023': []
                },
                'Templates_and_Resources': {
                    'Document_Templates': [],
                    'Media_Assets': [],
                    'Reference_Materials': []
                },
                'Inbox': {
                    'New_Items': [],
                    'To_Categorize': []
                }
            },
            
            'by_date': {
                '2024': {
                    'Q1_Jan_Mar': {
                        'January': [],
                        'February': [],
                        'March': []
                    },
                    'Q2_Apr_Jun': {
                        'April': [],
                        'May': [],
                        'June': []
                    },
                    'Q3_Jul_Sep': {
                        'July': [],
                        'August': [],
                        'September': []
                    },
                    'Q4_Oct_Dec': {
                        'October': [],
                        'November': [],
                        'December': []
                    }
                },
                '2023': {
                    'Archive': []
                }
            },
            
            'hybrid_approach': {
                '01_Inbox': {
                    'New_Items': [],
                    'Processing': [],
                    'Quick_Access': []
                },
                '02_Active_Work': {
                    'Current_Projects': {
                        'Project_Alpha': {
                            'Documents': [],
                            'Media': [],
                            'Data': []
                        }
                    },
                    'Daily_Tasks': [],
                    'Meetings_and_Notes': []
                },
                '03_Resources': {
                    'Templates': [],
                    'Reference_Materials': [],
                    'Tools_and_Utilities': []
                },
                '04_Archive': {
                    'By_Year': {
                        '2024': [],
                        '2023': []
                    },
                    'Completed_Projects': []
                },
                '05_Personal': {
                    'Photos': [],
                    'Documents': [],
                    'Media': []
                }
            }
        }
        
        self.file_type_mappings = {
            'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
            'spreadsheets': ['.xls', '.xlsx', '.csv', '.ods'],
            'presentations': ['.ppt', '.pptx', '.odp'],
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg'],
            'videos': ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv'],
            'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
            'archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c'],
            'data': ['.json', '.xml', '.sql', '.db', '.sqlite']
        }
    
    def suggest_structure(self, approach='hybrid_approach'):
        """
        Suggest a folder structure based on the specified approach.
        
        Args:
            approach (str): The organizational approach to use
                          ('by_type', 'by_project', 'by_date', 'hybrid_approach')
        
        Returns:
            dict: The suggested folder structure
        """
        if approach not in self.base_structures:
            raise ValueError(f"Unknown approach: {approach}")
        
        return self.base_structures[approach]
    
    def create_folder_structure(self, base_path, structure, dry_run=True):
        """
        Create the actual folder structure on the filesystem.
        
        Args:
            base_path (str): The base directory where folders will be created
            structure (dict): The folder structure to create
            dry_run (bool): If True, only print what would be created
        
        Returns:
            list: List of created/would-be-created folders
        """
        created_folders = []
        base_path = Path(base_path)
        
        def create_recursive(current_path, struct):
            for folder_name, contents in struct.items():
                folder_path = current_path / folder_name
                created_folders.append(str(folder_path))
                
                if not dry_run:
                    folder_path.mkdir(parents=True, exist_ok=True)
                    # Create a README file in each folder
                    readme_path = folder_path / "README.md"
                    if not readme_path.exists():
                        with open(readme_path, 'w') as f:
                            f.write(f"# {folder_name}\n\nThis folder is for organizing {folder_name.lower().replace('_', ' ')} files.\n")
                
                if isinstance(contents, dict):
                    create_recursive(folder_path, contents)
        
        create_recursive(base_path, structure)
        return created_folders
    
    def analyze_existing_data(self, data_path):
        """
        Analyze existing unstructured data and suggest appropriate organization.
        
        Args:
            data_path (str): Path to the directory containing unstructured data
        
        Returns:
            dict: Analysis results and recommendations
        """
        data_path = Path(data_path)
        if not data_path.exists():
            return {"error": f"Path {data_path} does not exist"}
        
        file_analysis = {
            'total_files': 0,
            'file_types': {},
            'large_files': [],
            'recommendations': []
        }
        
        # Analyze files
        for file_path in data_path.rglob('*'):
            if file_path.is_file():
                file_analysis['total_files'] += 1
                suffix = file_path.suffix.lower()
                
                # Count file types
                file_analysis['file_types'][suffix] = file_analysis['file_types'].get(suffix, 0) + 1
                
                # Check for large files (>100MB)
                try:
                    size_mb = file_path.stat().st_size / (1024 * 1024)
                    if size_mb > 100:
                        file_analysis['large_files'].append({
                            'path': str(file_path),
                            'size_mb': round(size_mb, 2)
                        })
                except:
                    pass
        
        # Generate recommendations
        recommendations = []
        
        # Recommend structure based on file types
        doc_files = sum(file_analysis['file_types'].get(ext, 0) for ext in self.file_type_mappings['documents'])
        media_files = sum(file_analysis['file_types'].get(ext, 0) for ext in 
                         self.file_type_mappings['images'] + self.file_type_mappings['videos'] + self.file_type_mappings['audio'])
        
        if doc_files > media_files:
            recommendations.append("Consider using 'by_project' approach - you have many document files")
        elif media_files > doc_files:
            recommendations.append("Consider using 'by_type' approach - you have many media files")
        else:
            recommendations.append("Consider using 'hybrid_approach' for balanced organization")
        
        if len(file_analysis['large_files']) > 0:
            recommendations.append("Consider creating a separate 'Large_Files' folder for files >100MB")
        
        if file_analysis['total_files'] > 1000:
            recommendations.append("Consider using date-based organization due to large number of files")
        
        file_analysis['recommendations'] = recommendations
        return file_analysis
    
    def generate_organization_plan(self, data_path, approach='hybrid_approach', output_file=None):
        """
        Generate a complete organization plan for the given data.
        
        Args:
            data_path (str): Path to unstructured data
            approach (str): Organization approach to use
            output_file (str): Optional file to save the plan
        
        Returns:
            dict: Complete organization plan
        """
        analysis = self.analyze_existing_data(data_path)
        structure = self.suggest_structure(approach)
        
        plan = {
            'timestamp': datetime.now().isoformat(),
            'data_path': str(data_path),
            'approach': approach,
            'analysis': analysis,
            'suggested_structure': structure,
            'implementation_steps': [
                "1. Backup your original data",
                "2. Create the suggested folder structure",
                "3. Sort files by type/category",
                "4. Move files to appropriate folders",
                "5. Create index/catalog files",
                "6. Set up regular maintenance schedule"
            ]
        }
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(plan, f, indent=2)
        
        return plan
    
    def print_structure(self, structure, indent=0):
        """Print the folder structure in a readable format."""
        for folder_name, contents in structure.items():
            print("  " * indent + f"📁 {folder_name}")
            if isinstance(contents, dict):
                self.print_structure(contents, indent + 1)
            elif isinstance(contents, list) and contents:
                for item in contents:
                    print("  " * (indent + 1) + f"📄 {item}")


def main():
    """Main function to demonstrate the data organizer."""
    organizer = DataOrganizerSuggester()
    
    print("🗂️  Data Organization Structure Suggester")
    print("=" * 50)
    
    # Show available approaches
    print("\nAvailable Organization Approaches:")
    approaches = ['by_type', 'by_project', 'by_date', 'hybrid_approach']
    for i, approach in enumerate(approaches, 1):
        print(f"{i}. {approach.replace('_', ' ').title()}")
    
    # Get user choice
    try:
        choice = input("\nSelect an approach (1-4) or press Enter for hybrid: ").strip()
        if choice:
            approach = approaches[int(choice) - 1]
        else:
            approach = 'hybrid_approach'
    except (ValueError, IndexError):
        approach = 'hybrid_approach'
    
    print(f"\n📋 Suggested Structure ({approach.replace('_', ' ').title()}):")
    print("-" * 40)
    
    structure = organizer.suggest_structure(approach)
    organizer.print_structure(structure)
    
    # Ask if user wants to create the structure
    create_structure = input("\nWould you like to create this structure? (y/N): ").strip().lower()
    if create_structure == 'y':
        base_path = input("Enter the base path where folders should be created: ").strip()
        if base_path:
            try:
                dry_run = input("Dry run first? (Y/n): ").strip().lower() != 'n'
                folders = organizer.create_folder_structure(base_path, structure, dry_run=dry_run)
                
                if dry_run:
                    print(f"\n🔍 Dry run - Would create {len(folders)} folders:")
                    for folder in folders[:10]:  # Show first 10
                        print(f"  📁 {folder}")
                    if len(folders) > 10:
                        print(f"  ... and {len(folders) - 10} more folders")
                else:
                    print(f"\n✅ Created {len(folders)} folders successfully!")
                    
            except Exception as e:
                print(f"\n❌ Error creating folders: {e}")
    
    # Offer to analyze existing data
    analyze_data = input("\nWould you like to analyze existing unstructured data? (y/N): ").strip().lower()
    if analyze_data == 'y':
        data_path = input("Enter the path to your unstructured data: ").strip()
        if data_path:
            try:
                analysis = organizer.analyze_existing_data(data_path)
                if 'error' not in analysis:
                    print(f"\n📊 Analysis Results:")
                    print(f"Total files: {analysis['total_files']}")
                    print(f"File types found: {len(analysis['file_types'])}")
                    print(f"Large files (>100MB): {len(analysis['large_files'])}")
                    
                    print("\n💡 Recommendations:")
                    for rec in analysis['recommendations']:
                        print(f"  • {rec}")
                else:
                    print(f"\n❌ {analysis['error']}")
            except Exception as e:
                print(f"\n❌ Error analyzing data: {e}")
    
    print("\n🎉 Thank you for using the Data Organization Structure Suggester!")
    print("Remember to backup your data before reorganizing!")


if __name__ == "__main__":
    main()

