#!/usr/bin/env python3
"""
Organize skill zip files into intelligently named categories.
"""
import os
import zipfile
import shutil
from pathlib import Path
from collections import defaultdict

def categorize_skill(filename):
    """
    Categorize a skill based on its filename.
    Returns a category name for organizing.
    """
    # Remove version numbers and .zip extension
    name = filename.replace('.zip', '')
    name_lower = name.lower()
    
    # Document processing skills
    if any(doc_type in name_lower for doc_type in ['pdf', 'docx', 'pptx', 'xlsx', 'qmd']):
        return 'document-processing'
    
    # iOS/Mobile development
    if any(ios_term in name_lower for ios_term in ['ios', 'mobile', 'xcode', 'swift', 'simulator']):
        return 'ios-mobile'
    
    # Web/Frontend development
    if any(web_term in name_lower for web_term in [
        'react', 'next', 'angular', 'vue', 'frontend', 'css', 'scss', 'sass', 
        'tailwind', 'shadcn', 'html', 'javascript', 'typescript', 'three'
    ]):
        return 'web-frontend'
    
    # Backend/Database
    if any(backend_term in name_lower for backend_term in [
        'postgres', 'mysql', 'sql', 'database', 'convex', 'pocketbase'
    ]):
        return 'backend-database'
    
    # Search and research
    if any(search_term in name_lower for search_term in [
        'exa', 'search', 'tavily', 'research', 'arxiv', 'firecrawl'
    ]):
        return 'search-research'
    
    # Browser automation
    if any(browser_term in name_lower for browser_term in ['browser', 'playwright']):
        return 'browser-automation'
    
    # Best practices
    if 'best-practices' in name_lower or 'best practices' in name_lower:
        return 'best-practices'
    
    # Security
    if any(sec_term in name_lower for sec_term in ['security', 'vault', 'prompt-guard']):
        return 'security'
    
    # AI/ML
    if any(ai_term in name_lower for ai_term in ['ai', 'rag', 'lm-studio', 'hallucination']):
        return 'ai-ml'
    
    # Blockchain/Crypto
    if any(crypto_term in name_lower for crypto_term in ['coinbase', 'wallet', 'onchain', 'usdc', 'trade']):
        return 'blockchain-crypto'
    
    # Development tools
    if any(dev_term in name_lower for dev_term in [
        'agent', 'plugin', 'cli', 'debugger', 'code-review', 'changelog',
        'skill-vetter', 'capability-evolver'
    ]):
        return 'dev-tools'
    
    # Infrastructure/DevOps
    if any(infra_term in name_lower for infra_term in ['terraform', 'stripe']):
        return 'infrastructure-devops'
    
    # Data science
    if any(data_term in name_lower for data_term in ['numpy', 'pandas']):
        return 'data-science'
    
    # Writing/Content
    if any(content_term in name_lower for content_term in [
        'writing', 'humanizer', 'obsidian', 'markdown', 'librarian'
    ]):
        return 'writing-content'
    
    # Vendor-specific (Claude, Anthropic, etc.)
    if any(vendor in name_lower for vendor in ['claude', 'anthropic', 'openai', 'sdk']):
        return 'vendor-specific'
    
    # Catch-all for main/generic skills
    if name_lower in ['skills-main', 'skills-main-2', 'agent-skills-main', 
                      'spellbook-master', 'claude-skills-main', 'sap-skills-main']:
        return 'core-collections'
    
    # Default: other
    return 'other'

def main():
    """Main function to organize skills."""
    base_dir = Path('/home/runner/work/skill-jam/skill-jam')
    staging_dir = base_dir / 'skills-staging'
    
    # Create staging directory
    staging_dir.mkdir(exist_ok=True)
    
    # Find all zip files
    zip_files = list(base_dir.glob('*.zip'))
    
    # Categorize and organize
    categories = defaultdict(list)
    for zip_file in zip_files:
        category = categorize_skill(zip_file.name)
        categories[category].append(zip_file)
    
    # Create category directories and extract files
    for category, files in sorted(categories.items()):
        category_dir = staging_dir / category
        category_dir.mkdir(exist_ok=True)
        
        print(f"\n{category.upper()} ({len(files)} skills)")
        print("=" * 60)
        
        for zip_file in sorted(files):
            # Extract to category directory
            extract_dir = category_dir / zip_file.stem
            
            try:
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                print(f"  ✓ {zip_file.name}")
            except Exception as e:
                print(f"  ✗ {zip_file.name} - Error: {e}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("ORGANIZATION SUMMARY")
    print("=" * 60)
    for category, files in sorted(categories.items()):
        print(f"{category:30s} : {len(files):3d} skills")
    print(f"\nTotal: {len(zip_files)} skills organized")

if __name__ == '__main__':
    main()
