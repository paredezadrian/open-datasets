# Open Datasets

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

**A curated collection of high-quality datasets for machine learning and AI research**

Created and maintained by Adrian Paredez

## Mission

To provide researchers, developers, and AI enthusiasts with professionally curated, well-documented, and ready-to-use datasets for training and evaluating machine learning models.

## Available Datasets

### [Conversational AI Dataset](conversational-ai-dataset/)
High-quality conversational examples for training transformer-based AI models (GPT-style).

- **Type**: Conversational AI / NLP
- **Size**: 60 conversations, 156 messages
- **Formats**: Alpaca, ChatML, Simple prompt-completion
- **Use Cases**: Chatbot training, instruction following, conversational AI
- **Quality**: Professionally curated and validated

**Quick Stats:**
- 15+ topic categories (technical, practical, creative)
- Average message length: 654 characters
- Ready-to-use train/validation/test splits
- Comprehensive tooling and documentation

[View Documentation](conversational-ai-dataset/README.md) | [Quick Start](conversational-ai-dataset/PROJECT_INFO.md)

---

## Getting Started

### Clone the Repository
```bash
git clone https://github.com/paredezadrian/open-datasets.git
cd open-datasets
```

### Explore a Dataset
```bash
# Navigate to any dataset
cd conversational-ai-dataset

# Follow the dataset-specific README for usage instructions
cat README.md
```

## Repository Structure

```
open-datasets/
├── README.md                          # This file
├── LICENSE                           # MIT License
├── conversational-ai-dataset/        # Conversational AI training data
│   ├── data/                        # Dataset files
│   ├── src/                         # Analysis tools
│   ├── docs/                        # Documentation
│   ├── examples/                    # Usage examples
│   ├── tests/                       # Unit tests
│   └── README.md                    # Dataset documentation
└── [future-datasets]/               # Additional datasets coming soon
```

## Dataset Categories

### Natural Language Processing
- **Conversational AI Dataset** - Training data for chatbots and conversational models

### Coming Soon
- **Text Classification Dataset** - Multi-label text classification examples
- **Question Answering Dataset** - Q&A pairs for reading comprehension
- **Sentiment Analysis Dataset** - Labeled sentiment data across domains

## Quality Standards

All datasets in this collection adhere to strict quality standards:

- **Professional Curation**: Manually reviewed and validated
- **Comprehensive Documentation**: Clear usage guides and examples
- **Ready-to-Use Tools**: Analysis and preprocessing utilities included
- **Tested**: Unit tests ensure data integrity
- **Multiple Formats**: Support for popular ML frameworks
- **Proper Licensing**: Clear usage rights and attribution

## Contributing

Interested in contributing a dataset or improving existing ones?

1. **Fork** the repository
2. **Create** a new branch for your dataset
3. **Follow** the established structure and quality standards
4. **Submit** a pull request with comprehensive documentation

### Dataset Contribution Guidelines

- Ensure data is properly licensed for open use
- Include comprehensive documentation and examples
- Provide analysis and preprocessing tools
- Add unit tests for data validation
- Follow the established directory structure

## 📄 License

This repository and all datasets are released under the [MIT License](LICENSE).

### Usage Rights
- Commercial use
- Modification
- Distribution
- Private use

### Requirements
- Include copyright notice
- Include license text

## Citation

If you use any datasets from this collection in your research or projects, please cite:

```bibtex
@misc{paredez2025opendatasets,
  author = {Adrian Paredez},
  title = {Open Datasets: A Curated Collection for Machine Learning and AI Research},
  year = {2025},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/paredezadrian/open-datasets}}
}
```

For individual datasets, please also refer to their specific documentation for additional citation information.

## Contact

**Adrian Paredez**
- Email: contact@paredez.dev
- GitHub: [@paredezadrian](https://github.com/paredezadrian)

## Statistics

- **Total Datasets**: 1 (growing!)
- **Total Data Points**: 156 messages, 60 conversations
- **Languages Supported**: English (more coming)
- **ML Frameworks**: PyTorch, Transformers, Custom

---

**Star this repository** if you find these datasets useful for your research or projects.

**Watch** for updates as new datasets are added regularly.

**Share** with the ML/AI community to help others discover quality training data.

---

*Last Updated: 2025-07-30*
