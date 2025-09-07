#!/bin/bash

echo "🚗 Customer FAQ System Setup Script"
echo "=================================="

# Check Python version
python_version=$(python3 --version 2>&1)
if [[ $? -eq 0 ]]; then
    echo "✓ Found $python_version"
else
    echo "❌ Python 3 is required but not found"
    exit 1
fi

# Create virtual environment (optional)
read -p "Do you want to create a virtual environment? (y/n): " create_venv
if [[ $create_venv =~ ^[Yy]$ ]]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ Virtual environment activated"
fi

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

if [[ $? -eq 0 ]]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create environment variables file
if [[ ! -f .env ]]; then
    echo "⚙️ Setting up environment variables..."
    cp .env.example .env
    echo "📝 Please edit .env file and add your OpenAI API key"
    echo "   OPENAI_API_KEY=your_api_key_here"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your OpenAI API key"
echo "2. Run the server: python run.py"
echo "3. Visit http://localhost:8000/docs for API documentation"
echo ""
echo "Happy coding! 🚀"