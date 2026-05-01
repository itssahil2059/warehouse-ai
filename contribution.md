# Contributing to Warehouse AI

Thank you for your interest in contributing to this project!

## How to Contribute

### Reporting Issues
- Use GitHub Issues to report bugs
- Include steps to reproduce
- Specify your environment (OS, Python version)

### Suggesting Features
- Open an issue with the "enhancement" label
- Describe the use case
- Explain expected behavior

### Code Contributions
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Development Setup

```bash
# Clone the repo
git clone https://github.com/sahilbhusal/warehouse-ai.git
cd warehouse-ai

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Add your OpenAI API key to .env

# Initialize database
python3 setup.py

# Run demos
python3 demos/1_trigger_demo.py
python3 demos/2_warehouse_ai.py
```

## Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and small

## Testing
- Test all database queries
- Verify tool calling works
- Check both demos run successfully

## Questions?
Feel free to open an issue for any questions!

---

Built with ❤️ by Sahil Bhusal