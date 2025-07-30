#!/usr/bin/env python3
"""
Example script showing how to use the conversational dataset for training.
This is a basic example - adapt based on your specific model and framework.
"""

import json
import os
import random
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class TrainingExample:
    """Represents a single training example."""
    input_text: str
    target_text: str
    conversation_id: int
    turn_number: int

def load_conversations(file_path: str) -> List[Dict[str, Any]]:
    """Load conversations from JSONL file."""
    conversations = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                conversations.append(json.loads(line))
    return conversations

def prepare_training_data(conversations: List[Dict[str, Any]], 
                         include_context: bool = True) -> List[TrainingExample]:
    """
    Convert conversations into training examples.
    
    Args:
        conversations: List of conversation dictionaries
        include_context: Whether to include previous messages as context
    
    Returns:
        List of TrainingExample objects
    """
    training_examples = []
    
    for conv_id, conversation in enumerate(conversations):
        messages = conversation["messages"]
        
        # Extract user-assistant pairs
        for i in range(0, len(messages) - 1, 2):
            if (i + 1 < len(messages) and 
                messages[i]["role"] == "user" and 
                messages[i + 1]["role"] == "assistant"):
                
                user_message = messages[i]["content"]
                assistant_message = messages[i + 1]["content"]
                
                # Build context if requested and available
                context = ""
                if include_context and i > 0:
                    # Include previous messages as context
                    context_messages = messages[:i]
                    context_parts = []
                    for msg in context_messages:
                        role = "Human" if msg["role"] == "user" else "Assistant"
                        context_parts.append(f"{role}: {msg['content']}")
                    context = "\n".join(context_parts) + "\n"
                
                # Format input text
                input_text = f"{context}Human: {user_message}\nAssistant:"
                
                training_examples.append(TrainingExample(
                    input_text=input_text.strip(),
                    target_text=assistant_message,
                    conversation_id=conv_id,
                    turn_number=i // 2
                ))
    
    return training_examples

def create_prompt_format(example: TrainingExample, format_type: str = "alpaca") -> Dict[str, str]:
    """
    Format training example for different training frameworks.
    
    Args:
        example: TrainingExample object
        format_type: "alpaca", "chatml", or "simple"
    
    Returns:
        Dictionary with formatted prompt
    """
    if format_type == "alpaca":
        return {
            "instruction": "You are a helpful AI assistant. Respond to the user's question or request.",
            "input": example.input_text.replace("Human:", "").replace("Assistant:", "").strip(),
            "output": example.target_text
        }
    
    elif format_type == "chatml":
        return {
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": example.input_text.replace("Human:", "").replace("Assistant:", "").strip()},
                {"role": "assistant", "content": example.target_text}
            ]
        }
    
    elif format_type == "simple":
        return {
            "prompt": example.input_text,
            "completion": example.target_text
        }
    
    else:
        raise ValueError(f"Unknown format type: {format_type}")

def split_dataset(examples: List[TrainingExample], 
                 train_ratio: float = 0.8, 
                 val_ratio: float = 0.1,
                 test_ratio: float = 0.1) -> Dict[str, List[TrainingExample]]:
    """Split dataset into train/validation/test sets."""
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6, "Ratios must sum to 1.0"
    
    # Shuffle examples
    shuffled = examples.copy()
    random.shuffle(shuffled)
    
    n = len(shuffled)
    train_end = int(n * train_ratio)
    val_end = train_end + int(n * val_ratio)
    
    return {
        "train": shuffled[:train_end],
        "validation": shuffled[train_end:val_end],
        "test": shuffled[val_end:]
    }

def save_formatted_dataset(examples: List[TrainingExample], 
                          output_file: str, 
                          format_type: str = "alpaca"):
    """Save formatted dataset to file."""
    formatted_examples = []
    
    for example in examples:
        formatted = create_prompt_format(example, format_type)
        formatted_examples.append(formatted)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for example in formatted_examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')
    
    print(f"Saved {len(formatted_examples)} examples to {output_file}")

def print_example_preview(examples: List[TrainingExample], num_examples: int = 3):
    """Print a few examples to preview the data."""
    print(f"\n=== Preview of {num_examples} Training Examples ===")
    
    for i, example in enumerate(examples[:num_examples]):
        print(f"\n--- Example {i+1} ---")
        print(f"Input: {example.input_text[:200]}{'...' if len(example.input_text) > 200 else ''}")
        print(f"Target: {example.target_text[:200]}{'...' if len(example.target_text) > 200 else ''}")
        print(f"Conversation ID: {example.conversation_id}, Turn: {example.turn_number}")

def main():
    """Main function to demonstrate dataset preparation."""
    print("Conversational Dataset Training Preparation")
    print("=" * 50)

    # Load dataset from processed directory
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
    dataset_file = os.path.join(data_dir, "processed", "combined_dataset.jsonl")

    if not os.path.exists(dataset_file):
        print(f"Dataset file not found: {dataset_file}")
        print("Please run the dataset analyzer first to create the combined dataset.")
        return

    conversations = load_conversations(dataset_file)
    print(f"Loaded {len(conversations)} conversations from {dataset_file}")
    
    # Prepare training data
    training_examples = prepare_training_data(conversations, include_context=True)
    print(f"Created {len(training_examples)} training examples")
    
    # Preview examples
    print_example_preview(training_examples)
    
    # Split dataset
    splits = split_dataset(training_examples, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1)
    print(f"\nDataset splits:")
    print(f"  Training: {len(splits['train'])} examples")
    print(f"  Validation: {len(splits['validation'])} examples")
    print(f"  Test: {len(splits['test'])} examples")
    
    # Save in different formats to splits directory
    splits_dir = os.path.join(data_dir, "splits")
    formats = ["alpaca", "chatml", "simple"]

    for format_type in formats:
        print(f"\nSaving in {format_type} format...")
        save_formatted_dataset(splits["train"], os.path.join(splits_dir, f"train_{format_type}.jsonl"), format_type)
        save_formatted_dataset(splits["validation"], os.path.join(splits_dir, f"val_{format_type}.jsonl"), format_type)
        save_formatted_dataset(splits["test"], os.path.join(splits_dir, f"test_{format_type}.jsonl"), format_type)
    
    print("\n✅ Dataset preparation complete!")
    print("\nNext steps:")
    print("1. Choose the format that matches your training framework")
    print("2. Adjust hyperparameters based on your model size")
    print("3. Consider data augmentation if you need more examples")
    print("4. Monitor training metrics and adjust as needed")

if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(42)
    main()
