# Conversational AI Dataset

> **High-quality conversational examples for training transformer AI models**

## Overview

This dataset contains 29 professionally curated conversations designed for training GPT-style AI models. Each conversation demonstrates natural, helpful, and engaging interactions across diverse topics.

## Quick Stats

| Metric | Value |
|--------|-------|
| **Conversations** | 29 |
| **Messages** | 66 (33 user, 33 assistant) |
| **Avg Message Length** | 654 characters |
| **Topics** | 15+ categories |
| **Formats** | Alpaca, ChatML, Simple |

## Content Categories

- 🔬 **Technical**: Programming, AI/ML, science explanations
- 🛠️ **Practical**: Health, career, finance, troubleshooting  
- 🎨 **Creative**: Storytelling, hobbies, personal advice
- ⚡ **Reference**: Quick facts, calculations, definitions

## Features

✅ **Professional Quality**: All conversations pass validation  
🔄 **Multiple Formats**: Ready for Alpaca, ChatML, or simple training  
📊 **Pre-split**: Train/validation/test splits included  
🛠️ **Tools Included**: Analysis and preprocessing utilities  
📚 **Well Documented**: Comprehensive guides and examples  
🧪 **Tested**: Full unit test coverage  

## Quick Start

```bash
# Navigate to the dataset
cd conversational-ai-dataset

# Analyze the dataset
python -m src.tools.dataset_analyzer

# Prepare training data
python -m src.tools.data_preprocessor
```

## File Structure

```
conversational-ai-dataset/
├── data/
│   ├── raw/           # Original conversations
│   ├── processed/     # Combined dataset
│   └── splits/        # Training splits
├── src/tools/         # Analysis & preprocessing
├── examples/          # Usage examples
├── tests/             # Unit tests
└── README.md         # Full documentation
```

## Training Ready

The dataset includes pre-formatted files for popular training frameworks:

- `data/splits/train_alpaca.jsonl` - Alpaca instruction format
- `data/splits/train_chatml.jsonl` - ChatML conversation format  
- `data/splits/train_simple.jsonl` - Simple prompt-completion format

## Author

**Adrian Paredez**
📧 contact@paredez.dev | 🐙 [@paredezadrian](https://github.com/paredezadrian)

## License

MIT License - Free for research and commercial use

---

📖 **[View Full Documentation](README.md)** | 🔧 **[See Examples](examples/)** | 🧪 **[Run Tests](tests/)**
