from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolCall, ToolMessage
import uuid

def maintain_state():
    messages = []
    
    prompt = "Who is the Prime Minister of India"
    msg = HumanMessage(content=prompt, name="Saketh")
    messages.append(msg)

    sys_prompt = "You are an expert in political knowledge"
    msg = SystemMessage(content=sys_prompt, name="SYSTEM")
    messages.append(msg)
    
    answer = "Narendra Modi"
    msg = AIMessage(content=answer, name="LLM")
    messages.append(msg)
    
    sys_prompt = " You are an Mathematical expert."
    msg = SystemMessage(content=sys_prompt, name="SYSTEM")
    messages.append(msg)                        
    
    user_prompt = "Is 5 even or Odd?"
    msg = HumanMessage(content=user_prompt, name="Moksha")
    messages.append(msg)
    
    Tool_call = ToolCall(tool_name="EvenOddChecker", tool_input={"number":5}, tool_call_id=str(uuid.uuid4()))
    ai_with_tool = AIMessage(content=prompt, tool_calls=[Tool_call], name="LLM")
    messages.append(ai_with_tool)    
    
    answer = "even"
    tool_response = ToolMessage(content=answer, tool_name="EvenOddChecker", tool_call_id=Tool_call.tool_call_id, name="EvenOddChecker")
    messages.append(tool_response)
    
    response = "5 Is Even"
    tool_response = AIMessage(content=response, name="LLM")
    messages.append(tool_response)
    
    retval = add_messages([], messages) 
    print(f"retval type :{type(retval)}")    
    for m in retval:
        m.pretty_print()
        
def main():
    maintain_state()

if __name__ == "__main__":
    main()
    