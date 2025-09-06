#!/usr/bin/env python3
import os
import yaml
import json
import re
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Optional, List

class PatternFirstAgent(ABC):
    """Base agent that enforces pattern-first generation"""
    
    def __init__(self, domain: str):
        self.domain = domain
        self.philosophy = Path(".ai/philosophy.md").read_text()
        self.patterns_dir = Path(f".ai/patterns/{domain}")
        self.patterns_dir.mkdir(parents=True, exist_ok=True)
    
    def execute(self, task: str) -> str:
        """Pattern-first execution flow"""
        try:
            # 1. Search for existing pattern
            pattern = self.find_pattern(task)
            
            if not pattern:
                print(f"No pattern found for: {task}")
                print("Creating new pattern with philosophical constraints...")
                
                # 2. Create pattern under constraints
                pattern = self.create_pattern(task)
                
                # 3. Validate pattern
                validation_result = self.validate_pattern(pattern)
                if not validation_result['valid']:
                    raise ValueError(f"Pattern validation failed: {validation_result['errors']}")
                
                # 4. Save pattern
                pattern_path = self.save_pattern(pattern, task)
                print(f"Pattern created and saved: {pattern_path}")
            
            # 5. Generate code from pattern
            code = self.generate_from_pattern(pattern, task)
            
            # 6. Log metrics
            self.log_metrics(task, pattern is not None)
            
            return code
            
        except Exception as e:
            return self.handle_error(e, task)
    
    def find_pattern(self, task: str) -> Optional[Dict]:
        """Search for existing patterns by checking task metadata"""
        if not self.patterns_dir.exists():
            return None
        
        task_lower = task.lower()
        best_match = None
        best_score = 0
        
        for pattern_file in self.patterns_dir.glob("*.md"):
            try:
                pattern = self.parse_pattern_file(pattern_file)
                pattern_task = pattern.get('metadata', {}).get('task', '').lower()
                
                # Calculate match score
                score = 0
                task_words = set(task_lower.split())
                pattern_words = set(pattern_task.split())
                
                # Check for exact match
                if task_lower == pattern_task:
                    return pattern
                
                # Check for word overlap
                common_words = task_words & pattern_words
                if common_words:
                    score = len(common_words) / max(len(task_words), len(pattern_words))
                
                # Update best match
                if score > best_score and score > 0.3:  # Minimum 30% match
                    best_match = pattern
                    best_score = score
                    
            except Exception:
                continue
        
        return best_match
    
    @abstractmethod
    def create_pattern(self, task: str) -> Dict:
        """Create a new pattern under philosophical constraints - implement in subclass"""
        pass
    
    def validate_pattern(self, pattern: Dict) -> Dict:
        """Validate pattern against philosophy"""
        errors = []
        warnings = []
        
        # Check required metadata
        required_metadata = ['task', 'complexity', 'tags', 'dependencies']
        for field in required_metadata:
            if field not in pattern.get('metadata', {}):
                errors.append(f"Missing required metadata: {field}")
        
        # Check code quality
        code = pattern.get('code', '')
        if len(code.strip()) < 50:
            errors.append("Pattern code too short")
        
        if 'TODO' in code or 'pass' in code:
            errors.append("Pattern contains incomplete sections")
        
        # Check complexity
        complexity = pattern.get('metadata', {}).get('complexity', 0)
        if complexity > 5:
            warnings.append(f"Pattern complexity {complexity} exceeds recommended max 5")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    def save_pattern(self, pattern: Dict, task: str) -> str:
        """Save pattern to filesystem"""
        # Generate filename
        filename = re.sub(r'[^\w\s-]', '', task.lower())
        filename = re.sub(r'[-\s]+', '-', filename)[:50] + '.md'
        filepath = self.patterns_dir / filename
        
        # Format pattern as markdown
        content = self.format_pattern_markdown(pattern)
        
        # Write to file
        filepath.write_text(content)
        
        return str(filepath)
    
    def format_pattern_markdown(self, pattern: Dict) -> str:
        """Format pattern dictionary as markdown - context first, then code"""
        metadata = pattern.get('metadata', {})
        
        # Add timestamps
        metadata['created'] = datetime.now().isoformat()
        metadata['updated'] = datetime.now().isoformat()
        metadata['version'] = '1.0.0'
        
        frontmatter = yaml.dump(metadata, default_flow_style=False)
        
        return f"""---
{frontmatter}---

# {metadata.get('task', 'Pattern')}

## Description

{pattern.get('description', '')}

## Setup Instructions

{pattern.get('setup', 'No additional setup required.')}

## Usage

{pattern.get('usage', '')}

## Notes

{pattern.get('notes', '')}

## Code

```{pattern.get('language', 'typescript')}
{pattern.get('code', '')}
```
"""
    
    def generate_from_pattern(self, pattern: Dict, task: str) -> str:
        """Generate code from pattern"""
        # For now, return the pattern code directly
        # In a full implementation, this would adapt the pattern to the specific task
        return pattern.get('code', '')
    
    def handle_error(self, error: Exception, task: str) -> str:
        """Handle errors gracefully"""
        error_message = f"Error processing task '{task}': {str(error)}"
        
        # Log error
        self.log_error(error_message)
        
        return f"""
## Error Encountered

{error_message}

### Troubleshooting Steps:
1. Check that the philosophy.md file exists
2. Verify the pattern directory structure
3. Try creating the pattern manually first

### Fallback Action:
You can create the pattern manually in: {self.patterns_dir}
"""
    
    def log_metrics(self, task: str, pattern_reused: bool):
        """Track usage metrics"""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'task': task,
            'domain': self.domain,
            'pattern_reused': pattern_reused,
            'patterns_total': len(list(self.patterns_dir.glob('*.md')))
        }
        
        metrics_file = Path('.ai/metrics.jsonl')
        with open(metrics_file, 'a') as f:
            f.write(json.dumps(metrics) + '\n')
    
    def log_error(self, error_message: str):
        """Log errors for debugging"""
        error_log = Path('.ai/errors.log')
        with open(error_log, 'a') as f:
            f.write(f"{datetime.now().isoformat()} - {error_message}\n")
    
    def parse_pattern_file(self, filepath: Path) -> Dict:
        """Parse pattern file into dictionary"""
        content = filepath.read_text()
        
        # Extract frontmatter
        match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
        if not match:
            return {}
        
        metadata = yaml.safe_load(match.group(1))
        body = match.group(2)
        
        # Extract code block
        code_match = re.search(r'```\w*\n(.*?)\n```', body, re.DOTALL)
        code = code_match.group(1) if code_match else ''
        
        # Extract sections
        description = self.extract_section(body, 'Description', '## Code')
        setup = self.extract_section(body, '## Setup Instructions', '## Usage')
        usage = self.extract_section(body, '## Usage', '## Notes')
        notes = self.extract_section(body, '## Notes', None)
        
        return {
            'metadata': metadata,
            'description': description.strip(),
            'code': code,
            'setup': setup.strip(),
            'usage': usage.strip(),
            'notes': notes.strip(),
            'language': metadata.get('language', 'typescript')
        }
    
    def extract_section(self, text: str, start: str, end: Optional[str]) -> str:
        """Extract a section from markdown text"""
        start_idx = text.find(start)
        if start_idx == -1:
            return ''
        
        start_idx += len(start)
        
        if end:
            end_idx = text.find(end, start_idx)
            if end_idx == -1:
                return text[start_idx:].strip()
            return text[start_idx:end_idx].strip()
        
        return text[start_idx:].strip()