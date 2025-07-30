#!/usr/bin/env python3
"""
Example showing how to integrate the dataset with popular training frameworks.

This script demonstrates how to use the dataset with different ML frameworks
like Hugging Face Transformers, PyTorch, etc.
"""

import os
import sys
import json

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tools.data_preprocessor import (
    load_conversations,
    prepare_training_data,
    split_dataset,
    save_formatted_dataset
)

def example_huggingface_datasets():
    """Example: Convert to Hugging Face datasets format."""
    print("=" * 60)
    print("EXAMPLE: Hugging Face Datasets Integration")
    print("=" * 60)
    
    try:
        from datasets import Dataset
        print("✅ Hugging Face datasets library available")
    except ImportError:
        print("❌ Hugging Face datasets not installed. Install with: pip install datasets")
        return
    
    # Load and prepare data
    dataset_path = os.path.join("..", "data", "processed", "combined_dataset.jsonl")
    
    if not os.path.exists(dataset_path):
        print(f"Dataset file not found: {dataset_path}")
        return
    
    conversations = load_conversations(dataset_path)
    training_examples = prepare_training_data(conversations, include_context=True)
    splits = split_dataset(training_examples)
    
    # Convert to Hugging Face format
    def examples_to_hf_format(examples, format_type="alpaca"):
        """Convert training examples to Hugging Face dataset format."""
        data = []
        for example in examples:
            if format_type == "alpaca":
                data.append({
                    "instruction": "You are a helpful AI assistant. Respond to the user's question or request.",
                    "input": example.input_text.replace("Human:", "").replace("Assistant:", "").strip(),
                    "output": example.target_text
                })
            elif format_type == "simple":
                data.append({
                    "text": f"{example.input_text} {example.target_text}"
                })
        return data
    
    # Create datasets
    train_data = examples_to_hf_format(splits["train"], "alpaca")
    val_data = examples_to_hf_format(splits["validation"], "alpaca")
    
    train_dataset = Dataset.from_list(train_data)
    val_dataset = Dataset.from_list(val_data)
    
    print(f"Created Hugging Face datasets:")
    print(f"  Training: {len(train_dataset)} examples")
    print(f"  Validation: {len(val_dataset)} examples")
    print(f"  Features: {train_dataset.features}")
    
    # Show sample
    print(f"\nSample training example:")
    print(json.dumps(train_dataset[0], indent=2)[:300] + "...")
    
    return train_dataset, val_dataset

def example_pytorch_dataloader():
    """Example: Create PyTorch DataLoader."""
    print("\n" + "=" * 60)
    print("EXAMPLE: PyTorch DataLoader Integration")
    print("=" * 60)
    
    try:
        import torch
        from torch.utils.data import Dataset, DataLoader
        print("✅ PyTorch available")
    except ImportError:
        print("❌ PyTorch not installed. Install with: pip install torch")
        return
    
    # Load data
    dataset_path = os.path.join("..", "data", "processed", "combined_dataset.jsonl")
    
    if not os.path.exists(dataset_path):
        print(f"Dataset file not found: {dataset_path}")
        return
    
    conversations = load_conversations(dataset_path)
    training_examples = prepare_training_data(conversations, include_context=True)
    
    class ConversationDataset(Dataset):
        """PyTorch Dataset for conversational data."""
        
        def __init__(self, examples):
            self.examples = examples
        
        def __len__(self):
            return len(self.examples)
        
        def __getitem__(self, idx):
            example = self.examples[idx]
            return {
                "input_text": example.input_text,
                "target_text": example.target_text,
                "conversation_id": example.conversation_id,
                "turn_number": example.turn_number
            }
    
    # Create dataset and dataloader
    dataset = ConversationDataset(training_examples)
    dataloader = DataLoader(dataset, batch_size=4, shuffle=True)
    
    print(f"Created PyTorch dataset with {len(dataset)} examples")
    print(f"DataLoader batch size: 4")
    
    # Show sample batch
    print(f"\nSample batch:")
    for batch in dataloader:
        print(f"  Batch size: {len(batch['input_text'])}")
        print(f"  Input sample: {batch['input_text'][0][:100]}...")
        print(f"  Target sample: {batch['target_text'][0][:100]}...")
        break
    
    return dataset, dataloader

def example_custom_tokenization():
    """Example: Custom tokenization for training."""
    print("\n" + "=" * 60)
    print("EXAMPLE: Custom Tokenization")
    print("=" * 60)
    
    # Load data
    dataset_path = os.path.join("..", "data", "processed", "combined_dataset.jsonl")
    
    if not os.path.exists(dataset_path):
        print(f"Dataset file not found: {dataset_path}")
        return
    
    conversations = load_conversations(dataset_path)
    training_examples = prepare_training_data(conversations, include_context=True)
    
    # Simple tokenization example (word-level)
    def simple_tokenize(text):
        """Simple word-level tokenization."""
        return text.lower().split()
    
    # Tokenize examples
    tokenized_examples = []
    vocab = set()
    
    for example in training_examples[:5]:  # Just first 5 for demo
        input_tokens = simple_tokenize(example.input_text)
        target_tokens = simple_tokenize(example.target_text)
        
        vocab.update(input_tokens)
        vocab.update(target_tokens)
        
        tokenized_examples.append({
            "input_tokens": input_tokens,
            "target_tokens": target_tokens,
            "input_length": len(input_tokens),
            "target_length": len(target_tokens)
        })
    
    print(f"Tokenized {len(tokenized_examples)} examples")
    print(f"Vocabulary size: {len(vocab)}")
    
    # Show statistics
    input_lengths = [ex["input_length"] for ex in tokenized_examples]
    target_lengths = [ex["target_length"] for ex in tokenized_examples]
    
    print(f"\nToken length statistics:")
    print(f"  Input - Min: {min(input_lengths)}, Max: {max(input_lengths)}, Avg: {sum(input_lengths)/len(input_lengths):.1f}")
    print(f"  Target - Min: {min(target_lengths)}, Max: {max(target_lengths)}, Avg: {sum(target_lengths)/len(target_lengths):.1f}")
    
    # Show sample
    print(f"\nSample tokenized example:")
    sample = tokenized_examples[0]
    print(f"  Input tokens: {sample['input_tokens'][:10]}...")
    print(f"  Target tokens: {sample['target_tokens'][:10]}...")

def example_export_for_training():
    """Example: Export data in various formats for different frameworks."""
    print("\n" + "=" * 60)
    print("EXAMPLE: Export for Different Training Frameworks")
    print("=" * 60)
    
    # Load data
    dataset_path = os.path.join("..", "data", "processed", "combined_dataset.jsonl")
    
    if not os.path.exists(dataset_path):
        print(f"Dataset file not found: {dataset_path}")
        return
    
    conversations = load_conversations(dataset_path)
    training_examples = prepare_training_data(conversations, include_context=True)
    splits = split_dataset(training_examples)
    
    # Create output directory
    output_dir = "training_exports"
    os.makedirs(output_dir, exist_ok=True)
    
    # Export for different frameworks
    frameworks = {
        "alpaca": "For Alpaca-style fine-tuning",
        "chatml": "For ChatML format training",
        "simple": "For simple prompt-completion training"
    }
    
    for format_type, description in frameworks.items():
        print(f"\nExporting {format_type} format - {description}")
        
        # Save training splits
        train_file = os.path.join(output_dir, f"train_{format_type}.jsonl")
        val_file = os.path.join(output_dir, f"val_{format_type}.jsonl")
        test_file = os.path.join(output_dir, f"test_{format_type}.jsonl")
        
        save_formatted_dataset(splits["train"], train_file, format_type)
        save_formatted_dataset(splits["validation"], val_file, format_type)
        save_formatted_dataset(splits["test"], test_file, format_type)
        
        print(f"  ✅ Saved to {output_dir}/")
    
    # Create a summary file
    summary = {
        "dataset_info": {
            "total_conversations": len(conversations),
            "total_examples": len(training_examples),
            "train_examples": len(splits["train"]),
            "val_examples": len(splits["validation"]),
            "test_examples": len(splits["test"])
        },
        "formats": frameworks,
        "files": {
            format_type: [
                f"train_{format_type}.jsonl",
                f"val_{format_type}.jsonl", 
                f"test_{format_type}.jsonl"
            ] for format_type in frameworks.keys()
        }
    }
    
    with open(os.path.join(output_dir, "dataset_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n✅ Export complete! Files saved to {output_dir}/")
    print(f"📄 Summary saved to {output_dir}/dataset_summary.json")

def main():
    """Run all training integration examples."""
    print("Conversational AI Dataset - Training Integration Examples")
    print("=" * 70)
    
    try:
        # Change to the examples directory
        os.chdir(os.path.dirname(__file__))
        
        # Run examples
        example_huggingface_datasets()
        example_pytorch_dataloader()
        example_custom_tokenization()
        example_export_for_training()
        
        print("\n" + "=" * 70)
        print("All training integration examples completed!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
