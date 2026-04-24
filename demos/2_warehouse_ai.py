"""
Warehouse AI - DEBUG VERSION
"""

import os
import sys
import json
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.warehouse_tools import execute_tool

load_dotenv()
openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
MODEL = "gpt-4o-mini"

SYSTEM_MESSAGE = "You are a helpful warehouse assistant. Be clear and concise."

TOOLS = [
    {"type": "function", "function": {"name": "get_worker_availability", "description": "Check workers", "parameters": {"type": "object", "properties": {"shift": {"type": "string", "enum": ["Day", "Night", "All"]}}, "required": ["shift"]}}},
    {"type": "function", "function": {"name": "get_pending_orders", "description": "Pending orders", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "get_top_pickers", "description": "Top performers", "parameters": {"type": "object", "properties": {}}}}
]


def handle_tool_calls(message):
    responses = []
    for tool_call in message.tool_calls:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        print(f"🔧 Calling: {name} with {args}")
        result = execute_tool(name, args)
        print(f"✓ Result: {result[:100]}")
        responses.append({"role": "tool", "content": result, "tool_call_id": tool_call.id})
    return responses


def chat(message, history):
    print("\n" + "="*60)
    print(f"📨 New message: {message}")
    print(f"📚 History type: {type(history)}")
    print(f"📚 History length: {len(history) if history else 0}")
    
    if history:
        print(f"📚 History items:")
        for i, h in enumerate(history):
            print(f"   [{i}] Type: {type(h)}, Content: {h}")
    
    # Build messages
    messages = [{"role": "system", "content": SYSTEM_MESSAGE}]
    
    # Process history
    if history:
        for h in history:
            print(f"Processing history item: {h}")
            try:
                user_msg = h[0] if len(h) > 0 else None
                bot_msg = h[1] if len(h) > 1 else None
                
                if user_msg:
                    messages.append({"role": "user", "content": user_msg})
                    print(f"  ✓ Added user: {user_msg[:50]}")
                if bot_msg:
                    messages.append({"role": "assistant", "content": bot_msg})
                    print(f"  ✓ Added bot: {bot_msg[:50]}")
            except Exception as e:
                print(f"  ❌ Error processing history item: {e}")
    
    # Add current message
    messages.append({"role": "user", "content": message})
    print(f"\n📤 Sending {len(messages)} messages to OpenAI")
    
    try:
        response = openai.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS)
        print(f"✓ Got response, finish_reason: {response.choices[0].finish_reason}")
        
        # Tool loop
        while response.choices[0].finish_reason == "tool_calls":
            print("🔧 Processing tool calls...")
            msg = response.choices[0].message
            tool_resp = handle_tool_calls(msg)
            messages.append(msg)
            messages.extend(tool_resp)
            response = openai.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS)
            print(f"✓ Got response after tools, finish_reason: {response.choices[0].finish_reason}")
        
        reply = response.choices[0].message.content
        print(f"✅ Final reply: {reply[:100]}")
        return reply
        
    except Exception as e:
        print(f"❌ EXCEPTION: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return f"Error: {str(e)}"


if __name__ == "__main__":
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ No API key!")
        exit(1)
    
    if not os.path.exists("warehouse.db"):
        print("❌ No database!")
        exit(1)
    
    print("\n🏭 Warehouse AI - DEBUG MODE")
    print("✓ Ready\n")
    
    gr.ChatInterface(fn=chat).launch(server_port=7860, inbrowser=True)