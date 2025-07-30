#!/usr/bin/env python3
"""
Basic usage examples for the Conversational AI Dataset.

This script demonstrates how to use the main tools and functions
provided by the dataset package.
"""

import os
import sys

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tools.dataset_analyzer import (
    load_jsonl,
    analyze_dataset,
    print_dataset_report,
    validate_conversation_format
)
from tools.data_preprocessor import (
    load_conversations,
    prepare_training_data,
    split_dataset,
    create_prompt_format,
    save_formatted_dataset
)

def example_1_basic_analysis():
    """Example 1: Basic dataset analysis."""
    print("=" * 60)
    print("EXAMPLE 1: Basic Dataset Analysis")
    print("=" * 60)
    
    # Path to the dataset file
    dataset_path = os.path.join("..", "data", "processed", "combined_dataset.jsonl")
    
    if not os.path.exists(dataset_path):
        print(f"Dataset file not found: {dataset_path}")
        print("Please run the dataset analyzer first to create the combined dataset.")
        return
    
    # Load and analyze the dataset
    print("Loading dataset...")
    conversations = load_jsonl(dataset_path)
    print(f"Loaded {len(conversations)} conversations")
    
    # Validate a few conversations
    print("\nValidating conversations...")
    for i, conv in enumerate(conversations[:3]):
        errors = validate_conversation_format(conv)
        if errors:
            print(f"Conversation {i+1} has errors: {errors}")
        else:
            print(f"Conversation {i+1}: ✅ Valid")
    
    # Generate full report
    print("\nGenerating full analysis report...")
    print_dataset_report(dataset_path)

def example_2_data_preparation():
    """Example 2: Prepare data for training."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Data Preparation for Training")
    print("=" * 60)
    
    # Load conversations
    dataset_path = os.path.join("..", "data", "processed", "combined_dataset.jsonl")
    
    if not os.path.exists(dataset_path):
        print(f"Dataset file not found: {dataset_path}")
        return
    
    conversations = load_conversations(dataset_path)
    print(f"Loaded {len(conversations)} conversations")
    
    # Prepare training examples
    print("\nPreparing training examples...")
    training_examples = prepare_training_data(conversations, include_context=True)
    print(f"Created {len(training_examples)} training examples")
    
    # Show a few examples
    print("\nSample training examples:")
    for i, example in enumerate(training_examples[:2]):
        print(f"\n--- Example {i+1} ---")
        print(f"Input: {example.input_text[:100]}...")
        print(f"Target: {example.target_text[:100]}...")
        print(f"Conversation ID: {example.conversation_id}, Turn: {example.turn_number}")
    
    # Split the dataset
    print("\nSplitting dataset...")
    splits = split_dataset(training_examples, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1)
    print(f"Training examples: {len(splits['train'])}")
    print(f"Validation examples: {len(splits['validation'])}")
    print(f"Test examples: {len(splits['test'])}")
    
    return splits

def example_3_format_conversion():
    """Example 3: Convert to different training formats."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Format Conversion")
    print("=" * 60)
    
    # Get training examples from previous example
    dataset_path = os.path.join("..", "data", "processed", "combined_dataset.jsonl")
    
    if not os.path.exists(dataset_path):
        print(f"Dataset file not found: {dataset_path}")
        return
    
    conversations = load_conversations(dataset_path)
    training_examples = prepare_training_data(conversations, include_context=True)
    
    # Take a sample example
    if not training_examples:
        print("No training examples available")
        return
    
    sample_example = training_examples[0]
    
    # Convert to different formats
    formats = ["alpaca", "chatml", "simple"]
    
    for format_type in formats:
        print(f"\n--- {format_type.upper()} Format ---")
        formatted = create_prompt_format(sample_example, format_type)
        
        # Pretty print the formatted example
        import json
        print(json.dumps(formatted, indent=2, ensure_ascii=False)[:300] + "...")

def example_4_custom_filtering():
    """Example 4: Custom filtering and processing."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Custom Filtering and Processing")
    print("=" * 60)
    
    dataset_path = os.path.join("..", "data", "processed", "combined_dataset.jsonl")
    
    if not os.path.exists(dataset_path):
        print(f"Dataset file not found: {dataset_path}")
        return
    
    conversations = load_conversations(dataset_path)
    
    # Filter conversations by length
    short_conversations = [conv for conv in conversations if len(conv["messages"]) == 2]
    long_conversations = [conv for conv in conversations if len(conv["messages"]) > 2]
    
    print(f"Short conversations (2 messages): {len(short_conversations)}")
    print(f"Long conversations (>2 messages): {len(long_conversations)}")
    
    # Filter by message length
    technical_conversations = []
    for conv in conversations:
        for message in conv["messages"]:
            if any(keyword in message["content"].lower() for keyword in 
                   ["python", "code", "programming", "algorithm", "function"]):
                technical_conversations.append(conv)
                break
    
    print(f"Technical conversations: {len(technical_conversations)}")
    
    # Show topics distribution
    topics = {
        "technical": 0,
        "health": 0,
        "creative": 0,
        "advice": 0,
        "other": 0
    }
    
    for conv in conversations:
        content = " ".join([msg["content"].lower() for msg in conv["messages"]])
        
        if any(word in content for word in ["python", "code", "programming", "computer"]):
            topics["technical"] += 1
        elif any(word in content for word in ["health", "sleep", "exercise", "diet"]):
            topics["health"] += 1
        elif any(word in content for word in ["story", "creative", "write", "art"]):
            topics["creative"] += 1
        elif any(word in content for word in ["advice", "help", "should", "recommend"]):
            topics["advice"] += 1
        else:
            topics["other"] += 1
    
    print("\nTopic distribution:")
    for topic, count in topics.items():
        print(f"  {topic.capitalize()}: {count}")

def main():
    """Run all examples."""
    print("Conversational AI Dataset - Usage Examples")
    print("=" * 60)
    
    try:
        # Change to the examples directory
        os.chdir(os.path.dirname(__file__))
        
        # Run examples
        example_1_basic_analysis()
        example_2_data_preparation()
        example_3_format_conversion()
        example_4_custom_filtering()
        
        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        print("Make sure you have run the dataset analyzer to create the processed dataset.")

if __name__ == "__main__":
    main()
