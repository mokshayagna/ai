from google import genai - this import genai from the module google
from google.genai import types - To import types

model_name = "xyz" - model name declared

client = genai.Client() - this connects to LLM

if tools are used
    tools_config = types.GenerateContentConfig(tools=[function_name]) 
    """ 
        this implicitly call tools
    """

    auto_call = types.AutomaticFunctionCallingConfig(disable=True)
    tools_config = types.GenerateContentConfig(tools=[tool_name], automatic_function_calling=auto_call)
    """
        this will not call tool directly, we should manually call the tool
    """

if chat is used
    Chat is used because when we start a converstaion the LLM will not remember the past conversations 
    if we use chats then we can make LLM remmeber all the past conversation
    FOR EXAMPLE:
        prompt1:if we ask who is the PM of INDIA?
        Response: Narendra Modi
        prompt2: when did he take the responsiblity?
        Response : "IT may be anything"
        it will not remember whom you ar refereing to.
    so we use chat 

    IN CHAT:
        we will send prompt1 
        LLM give answer
    NEXT:
        while sending prompt2
        we will send Prompt1 + response of Prompt1 + prompt2
    this is how chat continues

    """ FUNCTIONS USED IN CHAT """
    Initialization of chat
    chat = client.chats.create(model=MODEL_NAME)

    TO send message
    response = chat.send_message(Prompt)

To print response
    """
    if tools are used
    """
    response = client.models.generate_content(model=MODEL, contents=prompt, config=tools_config)
    print(response.text)

    """
    if tools are not used. we are storing the output in response and printing it's text
    """
    response = client.models.generate_content(model=model_name, contents=prompt)
    print(response.text)

    """
    if chat is used
    """
    response = chat.send_message(prompt)
    print(response.text)

    If we print only response 
        print(response)
         it will be json format.

    if we want to extract which tool and argument LLM sent then we should access one by one

    1st we need to convert to dict

    data = response.to_json_dict() converts to dict

    candidate = data["candidates"][0]

    part = candidate["content"]["part"][0]

    function_call = part["funcation_call"]
    function_name = function_call["name"]

    arg = function_call["arg"]


    for sending response manually
    function_response_content = {
        "role": "user",   # NOTE: must be 'user' in new SDK
        "parts": [
            {
                "function_response": {
                    "name": function_name,
                    "response": {"result": user_output},
                }
            }
        ],
    }

    user_message = {
        "role": "user",
        "parts": [{"text": prompt}]
    }
    
    final_message = [user_message, function_response_content]
    response = client.models.generate_content(
        model=model_name,
        contents=[user_message, function_response_content]
    )

    print(response.text)
