# 🏭 Warehouse AI

> **AI-Powered Warehouse Management System with Natural Language Queries**

Transform your warehouse database into an intelligent assistant. Ask questions in plain English, get instant answers with voice responses. Built with OpenAI GPT-4, Gradio, and Python.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991.svg)
![Gradio](https://img.shields.io/badge/Gradio-4.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📖 About This Project

This project bridges **traditional database engineering** with **modern AI technology**. Inspired by real work experience at Metro Inc. Etobicoke Distribution Center, it demonstrates how AI can make enterprise systems accessible without sacrificing robustness.

### What It Does

Instead of writing SQL queries like this:
```sql
SELECT p.Name, COUNT(o.Order_ID), SUM(o.Total_Items)
FROM Order_Picker p
JOIN Orders o ON p.Picker_ID = o.Picker_ID
WHERE o.Status = 'Completed'
GROUP BY p.Name
ORDER BY SUM(o.Total_Items) DESC;
```

Just ask:
> **"Who picked the most items this week?"**

And get an instant answer with voice response! 🔊

---

## ✨ Features

- 🤖 **Natural Language Interface** - Ask questions in plain English
- 🔊 **Voice Responses** - Text-to-speech for hands-free operation
- 🧠 **Agentic AI** - Multi-step reasoning and tool calling
- 🗄️ **11-Table Database** - Normalized schema based on real warehouse operations
- ⚡ **Real-time Queries** - Instant database access
- 🎨 **Beautiful UI** - Built with Gradio
- 🔒 **Business Logic** - Triggers and constraints enforce data integrity

---

## 🎥 Demo

### Traditional Database Layer
```bash
python demos/1_trigger_demo.py
```
Shows how database triggers prevent invalid operations:
- ❌ Cannot assign multiple orders to same picker
- ✅ Data integrity maintained automatically

### AI-Powered Interface
```bash
python demos/2_warehouse_ai.py
```
Chat with your database using natural language:
- 💬 "How many workers are available today?"
- 💬 "Does any shift need overtime?"
- 💬 "Who are the top performers?"
- 💬 "What orders are still pending?"

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/warehouse-ai.git
cd warehouse-ai
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
```
Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-api-key-here
```

4. **Initialize the database**
```bash
python setup.py
```

You should see:
```
✅ SETUP COMPLETE!
Database Statistics:
  • Warehouses: 2
  • Stores: 3
  • Order Pickers: 5
  • Products: 5
  • Orders: 6
```

5. **Run the demos!**

**Traditional Database Demo:**
```bash
python demos/1_trigger_demo.py
```

**AI-Powered Interface:**
```bash
python demos/2_warehouse_ai.py
```

The Gradio interface will open automatically in your browser at `http://localhost:7860`

---

## 📁 Project Structure

```
warehouse-ai/
│
├── database/
│   ├── schema.sql              # Database schema (11 tables)
│   ├── data.sql                # Sample warehouse data
│   └── triggers.sql            # Business rule triggers
│
├── demos/
│   ├── 1_trigger_demo.py       # Traditional DB demo (2 min)
│   └── 2_warehouse_ai.py       # AI interface demo (5 min)
│
├── tools/
│   └── warehouse_tools.py      # Database query functions
│
├── setup.py                    # Database initialization
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
├── README.md                   # This file
└── DEMO_SCRIPT.md             # 9-minute presentation guide
```

---

## 🗄️ Database Schema

11 normalized tables modeling warehouse operations:

```
Warehouse
├── Order_Picker (Workers)
├── Product
├── Location (Aisle locations)
└── Equipment (Pallet jacks, forklifts)

Store
└── Orders
    ├── Order_Line_Item
    └── Damaged_Product

Workforce_Plan (Shift planning)
```

**Key Features:**
- 3rd Normal Form (3NF)
- Foreign key relationships
- Check constraints
- Business rule triggers
- Sample data from real warehouse

---

## 💬 Example Queries

Once the AI interface is running, try these:

### Workforce Management
```
"How many workers are available today?"
"Who is working the night shift?"
"Which shift needs more workers?"
```

### Orders & Operations
```
"What is the total load for today?"
"Which orders are still pending?"
"Show me active orders"
```

### Performance Analytics
```
"Who picked the most items?"
"Show me top 5 pickers"
"What's the damage report?"
```

### Inventory & Planning
```
"Are there any low stock items?"
"What equipment is available?"
"Does any shift need overtime?"
```

### Complex Queries (Agentic Workflow)
```
"Are we properly staffed for today's workload?"
```
*The AI will automatically call multiple tools to analyze workforce + workload + planning data!*

---

## 🏗️ Architecture

### How It Works

```
User Question (Natural Language)
        ↓
OpenAI GPT-4 (Understanding + Tool Selection)
        ↓
Python Tool Functions (Database Queries)
        ↓
SQLite Database (11 Tables)
        ↓
Formatted Response + Audio (TTS)
        ↓
User Gets Answer (Text + Voice)
```

### Technology Stack

**Backend:**
- Python 3.8+
- SQLite (easily switchable to MySQL/PostgreSQL)
- OpenAI API (GPT-4 for NLP, TTS for audio)

**Frontend:**
- Gradio 4.0+ (Web interface)
- Real-time chat with history
- Audio playback

**AI Features:**
- Tool calling (function calling)
- Agentic workflows (multi-step reasoning)
- Prompt engineering
- Text-to-speech

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file:
```bash
# OpenAI API Key (Required)
OPENAI_API_KEY=sk-your-api-key-here
```

### Customization

**Change TTS Voice:**

Edit `demos/2_warehouse_ai.py`:
```python
voice="onyx"  # Options: alloy, echo, fable, onyx, nova, shimmer
```

**Use MySQL Instead of SQLite:**

Edit `tools/warehouse_tools.py`:
```python
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='your_username',
    password='your_password',
    database='warehouse'
)
```

**Add Custom Tools:**

Add new functions to `tools/warehouse_tools.py` and update the `TOOLS` list in `demos/2_warehouse_ai.py`

---

## 📊 Database Tables

### Core Tables

| Table | Description | Rows |
|-------|-------------|------|
| **Warehouse** | Distribution centers (General/Frozen) | 2 |
| **Store** | Metro retail locations | 3 |
| **Order_Picker** | Warehouse workers | 5 |
| **Product** | Inventory items | 5 |
| **Location** | Aisle locations for products | 5 |
| **Orders** | Customer orders | 6 |
| **Order_Line_Item** | Items within orders | 5 |
| **Damaged_Product** | Damage tracking | 3 |
| **Equipment** | Pallet jacks, forklifts | 5 |
| **Workforce_Plan** | Shift planning & overtime | 2 |

---

## 🎯 Use Cases

### For Warehouse Managers
- Check worker availability instantly
- Monitor pending orders
- Track top performers
- Manage overtime decisions
- Get spoken answers while walking the floor

### For Developers
- Learn OpenAI tool calling
- Understand agentic AI workflows
- Practice database design
- Build conversational interfaces
- Study prompt engineering

### For Students
- Real-world database project
- AI/ML integration example
- Clean code architecture
- Portfolio-ready project
- Job interview talking points

---

## 🎓 Learning Outcomes

This project demonstrates:

✅ **Database Design** - Normalization, relationships, constraints  
✅ **SQL Programming** - Triggers, complex queries, JOINs  
✅ **Python Development** - Clean architecture, error handling  
✅ **AI Integration** - OpenAI API, tool calling, agentic workflows  
✅ **Web Development** - Gradio interfaces, user experience  
✅ **Real-world Application** - Business logic, operational requirements  

---

## 📈 Roadmap

### Current Version (v1.0)
- ✅ SQLite database with 11 tables
- ✅ OpenAI GPT-4 integration
- ✅ Gradio chat interface
- ✅ Text-to-speech responses
- ✅ 9 specialized warehouse tools
- ✅ Agentic workflows

### Planned Features (v2.0)
- [ ] MySQL/PostgreSQL support
- [ ] User authentication
- [ ] Multi-warehouse support
- [ ] Real-time order tracking
- [ ] Predictive analytics
- [ ] Voice input (speech-to-text)
- [ ] Mobile app
- [ ] Multi-language support
- [ ] Export reports (PDF/Excel)
- [ ] Dashboard with charts

### Future Ideas
- Integration with actual warehouse systems
- Computer vision for inventory tracking
- Automated restocking suggestions
- Route optimization for pickers
- Performance benchmarking

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Areas for Contribution
- Add new warehouse tools/queries
- Improve prompt engineering
- Add support for other databases (PostgreSQL, Oracle)
- Create additional demo scenarios
- Improve error handling
- Add tests
- Enhance documentation
- Create video tutorials

---

## 🐛 Troubleshooting

### Common Issues

**"No module named 'openai'"**
```bash
pip install -r requirements.txt
```

**"OPENAI_API_KEY not found"**
- Make sure `.env` file exists
- Check API key is correct
- Restart your terminal/IDE

**"Database file not found"**
```bash
python setup.py
```

**Audio not playing**
- Check system volume
- Try different browser
- Audio is optional - text still works

**Gradio interface not opening**
- Check console for URL (usually http://localhost:7860)
- Try opening manually in browser
- Set `share=True` in `demo.launch()` for public URL

---

## 💰 Cost Estimate

**OpenAI API Usage:**
- GPT-4 queries: ~$0.01-0.02 per question
- Text-to-speech: ~$0.015 per 1000 characters
- **Typical demo (10 questions):** $0.20 - $0.30

**Recommendation:** Add $5-10 to OpenAI account for development/testing

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

**Inspired by:**
- Real work experience at Metro Inc. Etobicoke Distribution Center, Canada
- AI Engineering Bootcamp (Week 2 - OpenAI Tool Calling patterns)

**Built with:**
- [OpenAI](https://openai.com/) - GPT-4 API and TTS
- [Gradio](https://gradio.app/) - Web interface framework
- [Python](https://python.org/) - Programming language
- [SQLite](https://sqlite.org/) - Database engine

**Special Thanks:**
- Metro Inc. for warehouse insights
- OpenAI for excellent API documentation
- Gradio team for the amazing UI framework
- The open-source community

---

## 📧 Contact

**Sahil Bhusal**
- GitHub: [@YOUR_GITHUB_USERNAME](https://github.com/YOUR_GITHUB_USERNAME)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/your-profile)
- Email: your.email@example.com

---

## 🌟 Show Your Support

If this project helped you, please ⭐ star the repository!

---

## 📸 Screenshots

### Trigger Demo
![Trigger Demo](docs/screenshots/trigger-demo.png)
*Demonstrating business rule enforcement*

### AI Interface
![AI Chat Interface](docs/screenshots/ai-interface.png)
*Natural language queries with voice responses*

### Database Schema
![Database Schema](docs/screenshots/schema-diagram.png)
*11-table normalized database design*

---

## 📚 Documentation

- [Demo Script](DEMO_SCRIPT.md) - 9-minute presentation guide
- [Database Schema](database/schema.sql) - Full SQL schema
- [Tool Functions](tools/warehouse_tools.py) - All query functions
- [API Documentation](docs/API.md) - Tool calling reference *(coming soon)*

---



*Bridging Traditional Database Engineering with Modern AI Technology*

---

echo "" >> README.md
echo "Last updated: $(date +%Y-%m-%d)" >> README.md