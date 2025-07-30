#!/usr/bin/env python3
"""
Unit tests for the data preprocessor module.
"""

import unittest
import tempfile
import json
import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tools.data_preprocessor import (
    TrainingExample,
    load_conversations,
    prepare_training_data,
    create_prompt_format,
    split_dataset,
    save_formatted_dataset
)

class TestDataPreprocessor(unittest.TestCase):
    """Test cases for data preprocessor functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_conversations = [
            {
                "messages": [
                    {"role": "user", "content": "What is AI?"},
                    {"role": "assistant", "content": "AI stands for Artificial Intelligence."}
                ]
            },
            {
                "messages": [
                    {"role": "user", "content": "How does it work?"},
                    {"role": "assistant", "content": "AI systems learn from data to make predictions."},
                    {"role": "user", "content": "Can you give an example?"},
                    {"role": "assistant", "content": "Sure! Image recognition is a common AI application."}
                ]
            }
        ]
    
    def test_training_example_creation(self):
        """Test TrainingExample dataclass."""
        example = TrainingExample(
            input_text="Human: Hello\nAssistant:",
            target_text="Hello! How can I help you?",
            conversation_id=0,
            turn_number=0
        )
        
        self.assertEqual(example.input_text, "Human: Hello\nAssistant:")
        self.assertEqual(example.target_text, "Hello! How can I help you?")
        self.assertEqual(example.conversation_id, 0)
        self.assertEqual(example.turn_number, 0)
    
    def test_load_conversations(self):
        """Test loading conversations from file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            for conv in self.sample_conversations:
                json.dump(conv, f)
                f.write('\n')
            temp_file = f.name
        
        try:
            conversations = load_conversations(temp_file)
            self.assertEqual(len(conversations), 2)
            self.assertEqual(conversations[0], self.sample_conversations[0])
        finally:
            os.unlink(temp_file)
    
    def test_prepare_training_data_without_context(self):
        """Test preparing training data without context."""
        examples = prepare_training_data(self.sample_conversations, include_context=False)

        # Should have 3 examples: 1 from first conversation + 2 from multi-turn conversation
        self.assertEqual(len(examples), 3)
        
        # Check first example
        first_example = examples[0]
        self.assertIn("What is AI?", first_example.input_text)
        self.assertEqual(first_example.target_text, "AI stands for Artificial Intelligence.")
        self.assertEqual(first_example.conversation_id, 0)
        self.assertEqual(first_example.turn_number, 0)
        
        # Check second example (from multi-turn conversation)
        second_example = examples[1]
        self.assertIn("How does it work?", second_example.input_text)
        self.assertEqual(second_example.target_text, "AI systems learn from data to make predictions.")
        self.assertEqual(second_example.conversation_id, 1)
        self.assertEqual(second_example.turn_number, 0)
    
    def test_prepare_training_data_with_context(self):
        """Test preparing training data with context."""
        examples = prepare_training_data(self.sample_conversations, include_context=True)

        # Should have 3 examples: 1 from first conversation + 2 from multi-turn conversation
        self.assertEqual(len(examples), 3)
        
        # Find the example with context (second turn of multi-turn conversation)
        context_example = None
        for example in examples:
            if example.turn_number == 1:
                context_example = example
                break
        
        self.assertIsNotNone(context_example)
        # Should include previous messages as context
        self.assertIn("How does it work?", context_example.input_text)
        self.assertIn("AI systems learn", context_example.input_text)
    
    def test_create_prompt_format_alpaca(self):
        """Test creating Alpaca format."""
        example = TrainingExample(
            input_text="Human: What is Python?\nAssistant:",
            target_text="Python is a programming language.",
            conversation_id=0,
            turn_number=0
        )
        
        formatted = create_prompt_format(example, "alpaca")
        
        self.assertIn("instruction", formatted)
        self.assertIn("input", formatted)
        self.assertIn("output", formatted)
        self.assertEqual(formatted["output"], "Python is a programming language.")
        self.assertIn("What is Python?", formatted["input"])
    
    def test_create_prompt_format_chatml(self):
        """Test creating ChatML format."""
        example = TrainingExample(
            input_text="Human: What is Python?\nAssistant:",
            target_text="Python is a programming language.",
            conversation_id=0,
            turn_number=0
        )
        
        formatted = create_prompt_format(example, "chatml")
        
        self.assertIn("messages", formatted)
        self.assertEqual(len(formatted["messages"]), 3)  # system, user, assistant
        self.assertEqual(formatted["messages"][0]["role"], "system")
        self.assertEqual(formatted["messages"][1]["role"], "user")
        self.assertEqual(formatted["messages"][2]["role"], "assistant")
        self.assertEqual(formatted["messages"][2]["content"], "Python is a programming language.")
    
    def test_create_prompt_format_simple(self):
        """Test creating simple format."""
        example = TrainingExample(
            input_text="Human: What is Python?\nAssistant:",
            target_text="Python is a programming language.",
            conversation_id=0,
            turn_number=0
        )
        
        formatted = create_prompt_format(example, "simple")
        
        self.assertIn("prompt", formatted)
        self.assertIn("completion", formatted)
        self.assertEqual(formatted["prompt"], "Human: What is Python?\nAssistant:")
        self.assertEqual(formatted["completion"], "Python is a programming language.")
    
    def test_create_prompt_format_invalid(self):
        """Test creating format with invalid type."""
        example = TrainingExample(
            input_text="Human: Hello\nAssistant:",
            target_text="Hello!",
            conversation_id=0,
            turn_number=0
        )
        
        with self.assertRaises(ValueError):
            create_prompt_format(example, "invalid_format")
    
    def test_split_dataset(self):
        """Test dataset splitting."""
        examples = prepare_training_data(self.sample_conversations, include_context=False)
        
        splits = split_dataset(examples, train_ratio=0.6, val_ratio=0.2, test_ratio=0.2)
        
        self.assertIn("train", splits)
        self.assertIn("validation", splits)
        self.assertIn("test", splits)
        
        total_examples = len(splits["train"]) + len(splits["validation"]) + len(splits["test"])
        self.assertEqual(total_examples, len(examples))
    
    def test_split_dataset_invalid_ratios(self):
        """Test dataset splitting with invalid ratios."""
        examples = prepare_training_data(self.sample_conversations, include_context=False)
        
        with self.assertRaises(AssertionError):
            split_dataset(examples, train_ratio=0.5, val_ratio=0.3, test_ratio=0.3)  # Sum > 1
    
    def test_save_formatted_dataset(self):
        """Test saving formatted dataset."""
        examples = prepare_training_data(self.sample_conversations, include_context=False)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            temp_file = f.name
        
        try:
            save_formatted_dataset(examples, temp_file, "alpaca")
            
            # Read back and verify
            with open(temp_file, 'r') as f:
                lines = f.readlines()
            
            self.assertEqual(len(lines), len(examples))
            
            # Parse first line and check format
            first_line = json.loads(lines[0])
            self.assertIn("instruction", first_line)
            self.assertIn("input", first_line)
            self.assertIn("output", first_line)
            
        finally:
            os.unlink(temp_file)

class TestDataPreprocessorIntegration(unittest.TestCase):
    """Integration tests for data preprocessor."""
    
    def test_full_preprocessing_workflow(self):
        """Test the complete preprocessing workflow."""
        # Create a more complex dataset
        conversations = [
            {
                "messages": [
                    {"role": "user", "content": "What is machine learning?"},
                    {"role": "assistant", "content": "Machine learning is a subset of AI."}
                ]
            },
            {
                "messages": [
                    {"role": "user", "content": "How do neural networks work?"},
                    {"role": "assistant", "content": "Neural networks process information through layers."},
                    {"role": "user", "content": "What about deep learning?"},
                    {"role": "assistant", "content": "Deep learning uses many layers in neural networks."}
                ]
            },
            {
                "messages": [
                    {"role": "user", "content": "Can you give me an example?"},
                    {"role": "assistant", "content": "Image recognition is a common application."}
                ]
            }
        ]
        
        # Prepare training data
        examples = prepare_training_data(conversations, include_context=True)
        
        # Should have examples from all conversations
        self.assertGreater(len(examples), 0)
        
        # Split dataset
        splits = split_dataset(examples, train_ratio=0.7, val_ratio=0.2, test_ratio=0.1)
        
        # Verify splits
        total = len(splits["train"]) + len(splits["validation"]) + len(splits["test"])
        self.assertEqual(total, len(examples))
        
        # Test different formats
        formats = ["alpaca", "chatml", "simple"]
        
        for format_type in formats:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
                temp_file = f.name
            
            try:
                save_formatted_dataset(splits["train"], temp_file, format_type)
                
                # Verify file was created and has content
                with open(temp_file, 'r') as f:
                    lines = f.readlines()
                
                self.assertEqual(len(lines), len(splits["train"]))
                
                # Verify format
                first_example = json.loads(lines[0])
                if format_type == "alpaca":
                    self.assertIn("instruction", first_example)
                elif format_type == "chatml":
                    self.assertIn("messages", first_example)
                elif format_type == "simple":
                    self.assertIn("prompt", first_example)
                    
            finally:
                os.unlink(temp_file)

if __name__ == '__main__':
    unittest.main()
