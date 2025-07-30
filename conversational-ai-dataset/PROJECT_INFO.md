# Conversational AI Dataset

**Part of the [Open Datasets](https://github.com/paredezadrian/open-datasets) collection by Adrian Paredez**

## About This Dataset

This is a high-quality conversational dataset designed for training transformer-based AI models (GPT-style). It contains 60 natural, helpful, and engaging conversations across diverse topics and conversation styles.

## Quick Stats

- **Total Conversations**: 60
- **Total Messages**: 156 (78 user, 78 assistant)
- **Average Message Length**: 842 characters
- **Topics**: 25+ categories
- **Quality**: All conversations pass validation
- **Formats**: Alpaca, ChatML, Simple prompt-completion

## Content Categories

- **Technical & Educational**: Programming, AI/ML, science
- **Practical Life Skills**: Health, career, finance
- **Creative & Personal**: Storytelling, hobbies, relationships
- **Quick Reference**: Facts, calculations, definitions

## Repository Structure

This dataset is part of the larger [open-datasets](https://github.com/paredezadrian/open-datasets) repository. Within that repository, you'll find this dataset at:

```
open-datasets/
└── conversational-ai-dataset/
    ├── data/                   # Dataset files
    ├── src/                    # Analysis and preprocessing tools
    ├── docs/                   # Documentation
    ├── examples/               # Usage examples
    ├── tests/                  # Unit tests
    └── README.md              # Full documentation
```

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/paredezadrian/open-datasets.git
   cd open-datasets/conversational-ai-dataset
   ```

2. **Analyze the dataset**:
   ```bash
   python -m src.tools.dataset_analyzer
   ```

3. **Prepare training data**:
   ```bash
   python -m src.tools.data_preprocessor
   ```

## Usage

The dataset comes with professional tools for:
- Dataset validation and analysis
- Format conversion (Alpaca, ChatML, Simple)
- Automatic train/validation/test splitting
- Context-aware example generation

## Training Formats

Ready-to-use formats for popular training frameworks:
- **Alpaca**: Instruction-following format
- **ChatML**: Conversation format
- **Simple**: Prompt-completion format

## Quality Standards

- Natural, helpful, and engaging responses
- Comprehensive answers with actionable advice
- Proper formatting and structure
- Safe and responsible content
- Diverse topics and perspectives

## Author

**Adrian Paredez**
- GitHub: [@paredezadrian](https://github.com/paredezadrian)
- Email: contact@paredez.dev

## License

MIT License - See [LICENSE](LICENSE) for details.

## Part of Open Datasets Collection

This dataset is part of a larger collection of open datasets for machine learning and AI research. Visit the [main repository](https://github.com/paredezadrian/open-datasets) to explore other datasets.

---

For complete documentation, installation instructions, and advanced usage examples, see the [full README](README.md).
