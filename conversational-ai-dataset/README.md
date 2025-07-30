# Conversational AI Training Dataset

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Part of the [Open Datasets](https://github.com/paredezadrian/open-datasets) collection by Adrian Paredez**

A professionally organized, high-quality dataset of conversational examples designed for training transformer-based AI models (GPT-style). This dataset contains natural, helpful, and engaging conversations across diverse topics and conversation styles.

## 🚀 Quick Start

### Installation

```bash
# Clone the open-datasets repository
git clone https://github.com/paredezadrian/open-datasets.git
cd open-datasets/conversational-ai-dataset

# Install the package
pip install -e .

# Or install with optional dependencies
pip install -e ".[dev,analysis]"
```

> **Note**: This dataset is part of the [open-datasets](https://github.com/paredezadrian/open-datasets) repository, which contains multiple datasets for machine learning and AI research.

### Basic Usage

```bash
# Analyze the dataset
python -m src.tools.dataset_analyzer

# Prepare training data
python -m src.tools.data_preprocessor
```

## 📁 Project Structure

```
conversational-ai-dataset/
├── data/
│   ├── raw/                    # Original dataset files
│   │   ├── single_turn_conversations.jsonl
│   │   └── multi_turn_conversations.jsonl
│   ├── processed/              # Combined and cleaned data
│   │   └── combined_dataset.jsonl
│   └── splits/                 # Training/validation/test splits
│       ├── train_*.jsonl
│       ├── val_*.jsonl
│       └── test_*.jsonl
├── src/
│   ├── tools/                  # Main utilities
│   │   ├── dataset_analyzer.py
│   │   └── data_preprocessor.py
│   └── utils/                  # Helper functions
├── docs/                       # Documentation
├── examples/                   # Usage examples
├── tests/                      # Unit tests
├── configs/                    # Configuration files
└── README.md
```

## 📊 Dataset Overview

| Metric | Value |
|--------|-------|
| **Total Conversations** | 29 |
| **Total Messages** | 66 (33 user, 33 assistant) |
| **Average Conversation Length** | 2.3 messages |
| **Average Message Length** | 654 characters |
| **Topics Covered** | 15+ categories |
| **Quality Validation** | ✅ All conversations pass validation |

## Content Categories

### Technical & Educational
- Programming (Python, web development)
- Science explanations (quantum computing, water cycle)
- Technology concepts (AI/ML, cryptocurrency)

### Practical Life Skills
- Health and wellness advice
- Career development (interviews, workplace)
- Financial guidance and decision-making
- Home maintenance and troubleshooting

### Creative & Personal
- Creative writing and storytelling
- Hobby guidance (guitar, photography)
- Personal relationship advice
- Emotional support and guidance

### Quick Reference
- Simple calculations and facts
- Brief explanations and definitions

## Tools & Features

### Dataset Analyzer (`src/tools/dataset_analyzer.py`)
- Validate dataset format and structure
- Generate comprehensive statistics
- Combine multiple dataset files
- Check for formatting errors and inconsistencies

### Data Preprocessor (`src/tools/data_preprocessor.py`)
- Convert conversations to training examples
- Support for multiple formats (Alpaca, ChatML, Simple)
- Automatic train/validation/test splitting
- Context-aware example generation

## 📋 Supported Training Formats

### Alpaca Format
```json
{
  "instruction": "You are a helpful AI assistant...",
  "input": "User question",
  "output": "Assistant response"
}
```

### ChatML Format
```json
{
  "messages": [
    {"role": "system", "content": "You are a helpful AI assistant."},
    {"role": "user", "content": "User question"},
    {"role": "assistant", "content": "Assistant response"}
  ]
}
```

### Simple Format
```json
{
  "prompt": "Human: User question\nAssistant:",
  "completion": "Assistant response"
}
```

## 🔧 Usage Examples

### Analyze Dataset
```python
from src.tools.dataset_analyzer import analyze_dataset, print_dataset_report

# Analyze a specific dataset file
print_dataset_report("data/raw/single_turn_conversations.jsonl")
```

### Prepare Training Data
```python
from src.tools.data_preprocessor import load_conversations, prepare_training_data

# Load and prepare data
conversations = load_conversations("data/processed/combined_dataset.jsonl")
examples = prepare_training_data(conversations, include_context=True)
```

### Custom Training Pipeline
```python
from src.tools.data_preprocessor import split_dataset, save_formatted_dataset

# Split data
splits = split_dataset(examples, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1)

# Save in your preferred format
save_formatted_dataset(splits["train"], "my_train_data.jsonl", "alpaca")
```

## Quality Standards

### Response Characteristics
- **Helpful & Accurate:** Factually correct, practical advice
- **Well-Structured:** Logical organization with clear formatting
- **Engaging & Natural:** Conversational tone with empathy
- **Safe & Responsible:** No harmful content, balanced perspectives

### Content Guidelines
- Comprehensive responses with actionable advice
- Appropriate use of formatting (bullets, headers, code blocks)
- Follow-up questions to encourage interaction
- Professional disclaimers for sensitive topics

## Training Recommendations

### Hyperparameters
- **Batch size:** Start with 4-8 for fine-tuning
- **Learning rate:** Conservative rates (1e-5 to 5e-5)
- **Validation split:** 10-15% recommended
- **Context length:** Consider your model's token limits

### Best Practices
- Monitor validation loss to prevent overfitting
- Use gradient accumulation for larger effective batch sizes
- Consider data augmentation for domain-specific use cases
- Evaluate with both automated metrics and human review

## Validation & Testing

All conversations pass comprehensive validation:
- Proper JSON structure
- Required fields present
- Valid role assignments
- Non-empty content
- Reasonable message lengths

Run tests:
```bash
pytest tests/
```

## Extending the Dataset

### Adding New Conversations
1. Follow the existing JSON format in `data/raw/`
2. Maintain quality standards
3. Include diverse topics and perspectives
4. Run validation: `python -m src.tools.dataset_analyzer`

### Suggested Expansions
- Domain-specific conversations (medical, legal, technical)
- Multiple languages
- Different personality styles
- Error handling and clarification examples

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this dataset in your research or projects, please cite:

```bibtex
@misc{paredez2025conversational,
  author = {Adrian Paredez},
  title = {Conversational AI Dataset: High-Quality Examples for Training Transformer Models},
  year = {2025},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/paredezadrian/open-datasets/tree/main/conversational-ai-dataset}}
}
```

## Contributing

Contributions are welcome! Please:
- Maintain the established format and quality standards
- Include diverse perspectives and topics
- Test with the provided validation tools
- Follow the code style guidelines (black, flake8)
- Add tests for new functionality

## Documentation

- [Technical Documentation](docs/technical_documentation.md)
- [Configuration Guide](configs/dataset_config.yaml)
- [Examples](examples/)

## Links

- **Repository:** [GitHub](https://github.com/paredezadrian/open-datasets)
- **Issues:** [Bug Tracker](https://github.com/paredezadrian/open-datasets/issues)
- **Documentation:** [Docs](docs/)
- **Author:** Adrian Paredez

---

**Created:** 2025-07-30
**Author:** Adrian Paredez
**Version:** 1.0.0
**Total Examples:** 33 training examples from 29 conversations
