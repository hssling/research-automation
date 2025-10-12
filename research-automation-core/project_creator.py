#!/usr/bin/env python3
"""
Research Project Creator
Command-line interface for creating new research projects using templates
"""

import argparse
import sys
from pathlib import Path
from project_template_generator import ResearchProjectTemplate

def main():
    """Main function for command-line usage"""

    parser = argparse.ArgumentParser(
        description="Create standardized research projects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a systematic review project
  python project_creator.py create my_sys_review systematic_review

  # Create a meta-analysis project
  python project_creator.py create diabetes_meta meta_analysis --output-dir ./projects

  # List available research types
  python project_creator.py list
        """
    )

    # Create subparsers for different actions
    subparsers = parser.add_subparsers(dest='action', help='Available actions')

    # Create subparser
    create_parser = subparsers.add_parser('create', help='Create a new research project')
    create_parser.add_argument('name', help='Project name')
    create_parser.add_argument('type', choices=[
        'systematic_review', 'meta_analysis', 'bibliometrics', 'omics_single',
        'observational_study', 'clinical_trial', 'custom'
    ], help='Research type')
    create_parser.add_argument('--output-dir', '-o', default='.',
                              help='Output directory for new project (default: current directory)')
    create_parser.add_argument('--no-git', action='store_true',
                              help='Do not initialize git repository')

    # List subparser
    list_parser = subparsers.add_parser('list', help='List available research project types')

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        return

    template_generator = ResearchProjectTemplate()

    if args.action == 'create':
        try:
            project_path = template_generator.create_project(
                args.name,
                args.type,
                args.output_dir,
                init_git=not getattr(args, 'no_git', False)
            )
            print(f"\n✅ Successfully created research project!")
            print(f"📁 Location: {project_path}")
            print(f"📋 Research Type: {args.type}")
            print(f"\n🚀 Ready to start your research project!")

        except Exception as e:
            print(f"❌ Error creating project: {e}")
            sys.exit(1)

    elif args.action == 'list':
        print("Available research project types:")
        print("=" * 40)
        project_types = [
            ("systematic_review", "Standard systematic review with PRISMA"),
            ("meta_analysis", "Meta-analysis with statistical methods"),
            ("bibliometrics", "Bibliometric analysis and citation networks"),
            ("omics_single", "Single omics analysis (RNA-seq, proteomics)"),
            ("observational_study", "Observational study analysis"),
            ("clinical_trial", "Clinical trial data analysis"),
            ("custom", "Custom research project structure")
        ]

        for ptype, description in project_types:
            print(f"{ptype:<25} - {description}")
        print("\nTo create a project:")
        print("  python project_creator.py create [name] [type]")

if __name__ == "__main__":
    main()
