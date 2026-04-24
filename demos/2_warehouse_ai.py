"""
Warehouse AI - Chat with your database using natural language
Powered by OpenAI GPT-4 and Gradio
"""

import os
import sys
import json
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

# Add tools folder to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.warehouse_tools import execute_tool

# Load API key
load_dotenv()

# Setup OpenAI
openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
MODEL = "gpt-4o-mini"

# System instructions for the AI
SYSTEM_MESSAGE = """
You are a helpful warehouse assistant.
You help managers query the warehouse database using natural language.

Be clear and concise. Use bullet points for lists.
Always be professional and helpful.
"""


# Define what tools the AI can use
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_worker_availability",
            "description": "Check how many workers are available by shift",
            "parameters": {
                "type": "object",
                "properties": {
                    "shift": {
                        "type": "string",
                        "enum": ["Day", "Night", "All"],
                        "description": "Which shift to check"
                    }
                },
                "required": ["shift"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_daily_load",
            "description": "Get today's total orders, items, and weight",
            "parameters": {
                "type": "object",
                "properties": {
                    "shift": {
                        "type": "string",
                        "enum": ["Day", "Night", "All"]
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_pending_orders",
            "description": "Show all pending orders",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_active_orders",
            "description": "Show orders currently being picked",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_overtime_needed",
            "description": "Check if any shift needs overtime",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_pickers",
            "description": "Show top performers by items picked",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "How many top pickers to show"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_equipment_status",
            "description": "Check equipment availability",
            "parameters": {
                "type": "object",
                "properties": {
                    "warehouse_id": {
                        "type": "integer"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_low_stock_items",
            "description": "Find products running low",
            "parameters": {
                "type": "object",
                "properties": {
                    "threshold": {
                        "type": "integer",
                        "description": "Stock level threshold"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_damage_report",
            "description": "Show damaged products report",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]


# Handle tool calls from OpenAI
def handle_tool_calls(message):
    """Execute tools and return results"""
    responses = []
    
    for tool_call in message.tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        
        # Show what tool is being called
        print(f"\n🔧 Calling: {function_name}")
        print(f"   Input: {json.dumps(function_args)}")
        
        # Execute the tool
        result = execute_tool(function_name, function_args)
        
        print(f"   Result: {result[:100]}...")
        
        # Add result for OpenAI
        responses.append({
            "role": "tool",
            "content": result,
            "tool_call_id": tool_call.id
        })
    
    return responses


# Generate audio from text
def make_audio(text):
    """Convert text to speech"""
    try:
        response = openai.audio.speech.create(
            model="tts-1",
            voice="onyx",
            input=text
        )
        return response.content
    except Exception as e:
        print(f"Audio error: {e}")
        return None


# Main chat function
def chat(message, history):
    """Handle chat messages with AI"""
    
    # Convert history to OpenAI format
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    
    # Build message list
    messages = [
        {"role": "system", "content": SYSTEM_MESSAGE}
    ] + history + [
        {"role": "user", "content": message}
    ]
    
    # Call OpenAI
    response = openai.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS
    )
    
    # Keep calling tools until we get final answer
    # This is the "agentic loop"
    while response.choices[0].finish_reason == "tool_calls":
        assistant_message = response.choices[0].message
        
        # Execute all tool calls
        tool_responses = handle_tool_calls(assistant_message)
        
        # Add to conversation
        messages.append(assistant_message)
        messages.extend(tool_responses)
        
        # Call OpenAI again with tool results
        response = openai.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS
        )
    
    # Get final text response
    final_text = response.choices[0].message.content
    
    # Generate audio
    audio = make_audio(final_text)
    
    return final_text, audio


# Create Gradio interface
def create_interface():
    """Build the web UI"""
    
    # Example questions
    examples = [
        "How many workers are available today?",
        "What is the total load for today?",
        "Which orders are pending?",
        "Does any shift need overtime?",
        "Who are the top pickers?",
        "What equipment is available?",
        "Any low stock items?",
        "Show me the damage report"
    ]
    
    with gr.Blocks(title="Warehouse AI") as demo:
        
        gr.Markdown("""
        # 🏭 Warehouse AI Assistant
        
        Ask questions about your warehouse in plain English!
        
        *Powered by OpenAI GPT-4 with voice responses*
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                chatbot = gr.Chatbot(
                    type="messages",
                    height=500,
                    label="Chat"
                )
            
            with gr.Column(scale=1):
                gr.Markdown("### 🔊 Audio Response")
                audio_output = gr.Audio(
                    label="Listen",
                    autoplay=True
                )
                
                gr.Markdown("### 💡 Try These")
                for ex in examples[:4]:
                    gr.Markdown(f"• {ex}")
        
        with gr.Row():
            msg = gr.Textbox(
                label="Ask a question...",
                placeholder="e.g., How many workers are available?",
                scale=4
            )
            submit = gr.Button("Send", scale=1, variant="primary")
        
        with gr.Row():
            gr.Examples(
                examples=examples,
                inputs=msg
            )
        
        # Handle sending messages
        def user_msg(message, history):
            """Add user message to chat"""
            return "", history + [{"role": "user", "content": message}]
        
        def bot_response(history):
            """Get AI response"""
            message = history[-1]["content"]
            response_text, audio = chat(message, history[:-1])
            history.append({"role": "assistant", "content": response_text})
            return history, audio
        
        # Connect events
        submit.click(
            user_msg,
            inputs=[msg, chatbot],
            outputs=[msg, chatbot]
        ).then(
            bot_response,
            inputs=[chatbot],
            outputs=[chatbot, audio_output]
        )
        
        msg.submit(
            user_msg,
            inputs=[msg, chatbot],
            outputs=[msg, chatbot]
        ).then(
            bot_response,
            inputs=[chatbot],
            outputs=[chatbot, audio_output]
        )
    
    return demo


# Main
if __name__ == "__main__":
    
    # Check API key
    if not os.getenv('OPENAI_API_KEY'):
        print("\n❌ Error: OPENAI_API_KEY not found!")
        print("Create a .env file with your API key\n")
        exit(1)
    
    # Check database
    if not os.path.exists("warehouse.db"):
        print("\n❌ Error: warehouse.db not found!")
        print("Run: python3 setup.py\n")
        exit(1)
    
    print("\n" + "="*60)
    print("     WAREHOUSE AI ASSISTANT")
    print("="*60)
    print("\n✓ API key loaded")
    print("✓ Database connected")
    print("\n🚀 Starting Gradio interface...")
    print("   Opening in browser...\n")
    
    # Launch
    demo = create_interface()
    demo.launch(
        server_port=7860,
        inbrowser=True
    )