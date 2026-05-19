from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, AnyMessage

def messagae_types():
    msg = "Who is the president of India?"
    hmsg = HumanMessage(content=msg,name="Moksha")
    
    msg = "You are an expert in Indian politics."
    smsg = SystemMessage(content=msg,name ="System")
    
    msg = "The president of India is Droupadi Murmu."
    aimsg = AIMessage(content=msg,name="LLM")
    
    print(hmsg)
    print(smsg)
    print(aimsg)
    
    print(f"Message type of hmsg: {type(hmsg)}")    
    print(f"Message type of smsg: {type(smsg)}")
    print(f"Message type of aimsg: {type(aimsg)}")
    
def main():
    messagae_types()
if __name__ == "__main__":    
    main()