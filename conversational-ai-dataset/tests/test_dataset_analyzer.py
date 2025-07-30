#!/usr/bin/env python3
"""
Unit tests for the dataset analyzer module.
"""

import unittest
import tempfile
import json
import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tools.dataset_analyzer import (
    load_jsonl,
    validate_conversation_format,
    analyze_dataset,
    combine_datasets
)

class TestDatasetAnalyzer(unittest.TestCase):
    """Test cases for dataset analyzer functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.valid_conversation = {
            "messages": [
                {"role": "user", "content": "Hello, how are you?"},
                {"role": "assistant", "content": "I'm doing well, thank you! How can I help you today?"}
            ]
        }
        
        self.invalid_conversation_missing_messages = {
            "data": [
                {"role": "user", "content": "Hello"}
            ]
        }
        
        self.invalid_conversation_empty_content = {
            "messages": [
                {"role": "user", "content": ""},
                {"role": "assistant", "content": "Hello!"}
            ]
        }
        
        self.invalid_conversation_wrong_role = {
            "messages": [
                {"role": "human", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"}
            ]
        }
    
    def test_validate_conversation_format_valid(self):
        """Test validation of a valid conversation."""
        errors = validate_conversation_format(self.valid_conversation)
        self.assertEqual(len(errors), 0, "Valid conversation should have no errors")
    
    def test_validate_conversation_format_missing_messages(self):
        """Test validation when messages key is missing."""
        errors = validate_conversation_format(self.invalid_conversation_missing_messages)
        self.assertIn("Missing 'messages' key", errors)
    
    def test_validate_conversation_format_empty_content(self):
        """Test validation when content is empty."""
        errors = validate_conversation_format(self.invalid_conversation_empty_content)
        self.assertTrue(any("empty content" in error for error in errors))
    
    def test_validate_conversation_format_wrong_role(self):
        """Test validation when role is invalid."""
        errors = validate_conversation_format(self.invalid_conversation_wrong_role)
        self.assertTrue(any("invalid role" in error for error in errors))
    
    def test_load_jsonl_valid_file(self):
        """Test loading a valid JSONL file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            json.dump(self.valid_conversation, f)
            f.write('\n')
            json.dump(self.valid_conversation, f)
            f.write('\n')
            temp_file = f.name
        
        try:
            conversations = load_jsonl(temp_file)
            self.assertEqual(len(conversations), 2)
            self.assertEqual(conversations[0], self.valid_conversation)
        finally:
            os.unlink(temp_file)
    
    def test_load_jsonl_nonexistent_file(self):
        """Test loading a non-existent file."""
        conversations = load_jsonl("nonexistent_file.jsonl")
        self.assertEqual(len(conversations), 0)
    
    def test_load_jsonl_invalid_json(self):
        """Test loading a file with invalid JSON."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            f.write('{"valid": "json"}\n')
            f.write('invalid json line\n')
            f.write('{"another": "valid"}\n')
            temp_file = f.name
        
        try:
            conversations = load_jsonl(temp_file)
            # Should load the valid lines and skip the invalid one
            self.assertEqual(len(conversations), 2)
        finally:
            os.unlink(temp_file)
    
    def test_analyze_dataset(self):
        """Test dataset analysis function."""
        # Create a temporary dataset file
        conversations = [self.valid_conversation, self.valid_conversation]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            for conv in conversations:
                json.dump(conv, f)
                f.write('\n')
            temp_file = f.name
        
        try:
            stats = analyze_dataset(temp_file)
            
            self.assertEqual(stats["total_conversations"], 2)
            self.assertEqual(stats["total_messages"], 4)
            self.assertEqual(stats["user_messages"], 2)
            self.assertEqual(stats["assistant_messages"], 2)
            self.assertEqual(stats["avg_conversation_length"], 2.0)
            self.assertEqual(len(stats["validation_errors"]), 0)
        finally:
            os.unlink(temp_file)
    
    def test_analyze_dataset_with_errors(self):
        """Test dataset analysis with validation errors."""
        conversations = [self.valid_conversation, self.invalid_conversation_empty_content]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            for conv in conversations:
                json.dump(conv, f)
                f.write('\n')
            temp_file = f.name
        
        try:
            stats = analyze_dataset(temp_file)
            
            self.assertEqual(stats["total_conversations"], 2)
            self.assertGreater(len(stats["validation_errors"]), 0)
        finally:
            os.unlink(temp_file)
    
    def test_combine_datasets(self):
        """Test combining multiple dataset files."""
        # Create two temporary dataset files
        conversations1 = [self.valid_conversation]
        conversations2 = [self.valid_conversation, self.valid_conversation]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f1:
            json.dump(conversations1[0], f1)
            f1.write('\n')
            temp_file1 = f1.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f2:
            for conv in conversations2:
                json.dump(conv, f2)
                f2.write('\n')
            temp_file2 = f2.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f3:
            temp_output = f3.name
        
        try:
            combine_datasets([temp_file1, temp_file2], temp_output)
            
            # Check the combined file
            combined_conversations = load_jsonl(temp_output)
            self.assertEqual(len(combined_conversations), 3)
        finally:
            os.unlink(temp_file1)
            os.unlink(temp_file2)
            os.unlink(temp_output)

class TestDatasetAnalyzerIntegration(unittest.TestCase):
    """Integration tests for dataset analyzer."""
    
    def test_full_analysis_workflow(self):
        """Test the complete analysis workflow."""
        # Create a more complex dataset
        conversations = [
            {
                "messages": [
                    {"role": "user", "content": "What is Python?"},
                    {"role": "assistant", "content": "Python is a programming language."}
                ]
            },
            {
                "messages": [
                    {"role": "user", "content": "How do I learn it?"},
                    {"role": "assistant", "content": "Start with basic syntax and practice regularly."},
                    {"role": "user", "content": "Any book recommendations?"},
                    {"role": "assistant", "content": "I recommend 'Automate the Boring Stuff with Python'."}
                ]
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            for conv in conversations:
                json.dump(conv, f)
                f.write('\n')
            temp_file = f.name
        
        try:
            # Analyze the dataset
            stats = analyze_dataset(temp_file)
            
            # Verify comprehensive statistics
            self.assertEqual(stats["total_conversations"], 2)
            self.assertEqual(stats["total_messages"], 6)
            self.assertEqual(stats["user_messages"], 3)
            self.assertEqual(stats["assistant_messages"], 3)
            self.assertEqual(stats["max_conversation_length"], 4)
            self.assertEqual(stats["min_conversation_length"], 2)
            self.assertEqual(stats["avg_conversation_length"], 3.0)
            
            # Check that all conversations are valid
            self.assertEqual(len(stats["validation_errors"]), 0)
            
        finally:
            os.unlink(temp_file)

if __name__ == '__main__':
    unittest.main()
