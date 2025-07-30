#!/usr/bin/env python3
"""
Utility script for analyzing and validating conversational datasets.
"""

import json
import os
from typing import Dict, List, Any
from collections import Counter

def load_jsonl(file_path: str) -> List[Dict[str, Any]]:
    """Load conversations from a JSONL file."""
    conversations = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line:
                    try:
                        conversation = json.loads(line)
                        conversations.append(conversation)
                    except json.JSONDecodeError as e:
                        print(f"Error parsing line {line_num}: {e}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    return conversations

def validate_conversation_format(conversation: Dict[str, Any]) -> List[str]:
    """Validate that a conversation follows the expected format."""
    errors = []
    
    if "messages" not in conversation:
        errors.append("Missing 'messages' key")
        return errors
    
    messages = conversation["messages"]
    if not isinstance(messages, list):
        errors.append("'messages' should be a list")
        return errors
    
    if len(messages) == 0:
        errors.append("Empty messages list")
        return errors
    
    for i, message in enumerate(messages):
        if not isinstance(message, dict):
            errors.append(f"Message {i} is not a dictionary")
            continue
            
        if "role" not in message:
            errors.append(f"Message {i} missing 'role' key")
        elif message["role"] not in ["user", "assistant"]:
            errors.append(f"Message {i} has invalid role: {message['role']}")
            
        if "content" not in message:
            errors.append(f"Message {i} missing 'content' key")
        elif not isinstance(message["content"], str):
            errors.append(f"Message {i} content is not a string")
        elif len(message["content"].strip()) == 0:
            errors.append(f"Message {i} has empty content")
    
    return errors

def analyze_dataset(file_path: str) -> Dict[str, Any]:
    """Analyze a conversational dataset and return statistics."""
    conversations = load_jsonl(file_path)
    
    if not conversations:
        return {"error": "No conversations loaded"}
    
    stats = {
        "file_name": os.path.basename(file_path),
        "total_conversations": len(conversations),
        "total_messages": 0,
        "user_messages": 0,
        "assistant_messages": 0,
        "conversation_lengths": [],
        "message_lengths": [],
        "validation_errors": [],
        "avg_conversation_length": 0,
        "avg_message_length": 0,
        "max_conversation_length": 0,
        "min_conversation_length": float('inf'),
    }
    
    for i, conversation in enumerate(conversations):
        # Validate format
        errors = validate_conversation_format(conversation)
        if errors:
            stats["validation_errors"].append(f"Conversation {i+1}: {', '.join(errors)}")
            continue
        
        messages = conversation["messages"]
        conversation_length = len(messages)
        stats["conversation_lengths"].append(conversation_length)
        stats["total_messages"] += conversation_length
        stats["max_conversation_length"] = max(stats["max_conversation_length"], conversation_length)
        stats["min_conversation_length"] = min(stats["min_conversation_length"], conversation_length)
        
        for message in messages:
            role = message["role"]
            content = message["content"]
            content_length = len(content)
            
            stats["message_lengths"].append(content_length)
            
            if role == "user":
                stats["user_messages"] += 1
            elif role == "assistant":
                stats["assistant_messages"] += 1
    
    # Calculate averages
    if stats["conversation_lengths"]:
        stats["avg_conversation_length"] = sum(stats["conversation_lengths"]) / len(stats["conversation_lengths"])
    
    if stats["message_lengths"]:
        stats["avg_message_length"] = sum(stats["message_lengths"]) / len(stats["message_lengths"])
    
    if stats["min_conversation_length"] == float('inf'):
        stats["min_conversation_length"] = 0
    
    return stats

def print_dataset_report(file_path: str):
    """Print a comprehensive report about the dataset."""
    stats = analyze_dataset(file_path)
    
    if "error" in stats:
        print(f"Error: {stats['error']}")
        return
    
    print(f"\n=== Dataset Analysis: {stats['file_name']} ===")
    print(f"Total conversations: {stats['total_conversations']}")
    print(f"Total messages: {stats['total_messages']}")
    print(f"User messages: {stats['user_messages']}")
    print(f"Assistant messages: {stats['assistant_messages']}")
    print(f"\nConversation Statistics:")
    print(f"  Average length: {stats['avg_conversation_length']:.1f} messages")
    print(f"  Max length: {stats['max_conversation_length']} messages")
    print(f"  Min length: {stats['min_conversation_length']} messages")
    print(f"\nMessage Statistics:")
    print(f"  Average length: {stats['avg_message_length']:.0f} characters")
    
    if stats['message_lengths']:
        print(f"  Max message length: {max(stats['message_lengths'])} characters")
        print(f"  Min message length: {min(stats['message_lengths'])} characters")
    
    if stats["validation_errors"]:
        print(f"\n⚠️  Validation Errors ({len(stats['validation_errors'])}):")
        for error in stats["validation_errors"]:
            print(f"  - {error}")
    else:
        print("\n✅ All conversations passed validation!")

def combine_datasets(input_files: List[str], output_file: str):
    """Combine multiple JSONL files into one."""
    all_conversations = []
    
    for file_path in input_files:
        conversations = load_jsonl(file_path)
        all_conversations.extend(conversations)
        print(f"Loaded {len(conversations)} conversations from {file_path}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for conversation in all_conversations:
            f.write(json.dumps(conversation, ensure_ascii=False) + '\n')
    
    print(f"\nCombined {len(all_conversations)} conversations into {output_file}")

def main():
    """Main function to run dataset analysis."""
    # Look for dataset files in the data directory
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
    raw_dir = os.path.join(data_dir, "raw")
    processed_dir = os.path.join(data_dir, "processed")

    dataset_files = [
        os.path.join(raw_dir, "single_turn_conversations.jsonl"),
        os.path.join(raw_dir, "multi_turn_conversations.jsonl")
    ]

    print("Conversational Dataset Analysis Tool")
    print("=" * 40)

    for file_path in dataset_files:
        if os.path.exists(file_path):
            print_dataset_report(file_path)
        else:
            print(f"\nFile not found: {file_path}")

    # Combine datasets
    existing_files = [f for f in dataset_files if os.path.exists(f)]
    if len(existing_files) > 1:
        print(f"\n{'='*40}")
        combined_path = os.path.join(processed_dir, "combined_dataset.jsonl")
        combine_datasets(existing_files, combined_path)
        print_dataset_report(combined_path)

if __name__ == "__main__":
    main()
