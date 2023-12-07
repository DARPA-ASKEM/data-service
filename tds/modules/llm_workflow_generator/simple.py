# -*- coding: utf-8 -*-
import warnings
import json
warnings.filterwarnings("ignore")
from langchain import OpenAI
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor,StructuredChatAgent


from langchain.memory import ConversationBufferMemory,ConversationBufferWindowMemory,ChatMessageHistory
from langchain import LLMChain
from workflow_tools import workflow_screen_tools,home_screen_tools,clear_workflow,get_workflow,WORKFLOW_ID
    
def main():
    #prompt
    
    prompt = {}
    prompt['prefix']="""You are a helpful assistant whose goal it is to assist the user in constructing a workflow in the Terarium scientific modeling application.
    
    Terarium is a comprehensive modeling and simulation ecosystem designed to support decision making in diverse missions and scientific domains built for researchers. Within the application users can create models which model different systems, datasets to calibrate models and simulations to use models to make predictions given certain configurations of model parameters.
    
    You will be given information about the current state of the workflow as well as tools with which to perform actions for the user in the Terarium application.
    The current workflow information will be formatted as a dictionary as follows:
    {{'id':str id of the workflow,'timestamp':str when the workflow was created,'name':str name of the workflow,'description':str description of the workflow,'nodes':list of dictionaries with information about objects(models, datasets,simulations, calibrations) in the current workflow,'edges':list of dictionaries with information on edges representing connections between objects,'transform':dict with x,y,k}}
    
    If the user asks you to perform an action but does not give all the inputs needed for using the tools required to perform those actions, ask the user clarifying questions using the Ask User tool to get the rest of the inputs, then perform those actions using the appropriate tools.
    
    The tools you have access to in order to interact with Terarium are:"""
    prompt['format_instructions']="""\
        Use the following format:
    
        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question
        
        If you think you can answer the question without using any tools skip the action, action input and observation and just skip to Final Answer:
    """
    prompt['format_instructions']="""\
    Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).

    Valid "action" values: "Final Answer" or {tool_names}
    
    Provide only ONE action per $JSON_BLOB, as shown:
    
    ```
    {{{{
      "action": $TOOL_NAME,
      "action_input": $INPUT
    }}}}
    ```
    
    Follow this format:
    
    Question: input question to answer
    Thought: consider previous and subsequent steps
    Action:
    ```
    $JSON_BLOB
    ```
    Observation: action result
    ... (repeat Thought/Action/Observation N times)
    Thought: I know what to respond
    Action:
    ```
    {{{{
      "action": "Final Answer",
      "action_input": "Final response to human"
    }}}}
    ```"""
    prompt['suffix']="""Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation:.
    
    {chat_history}
    User Request: {input}
    
    Here is information on the workflow currently. This may be updated by tool use: \n{workflow}
    
    {agent_scratchpad}"""
    
    tools = workflow_screen_tools #home_screen_tools
    prompt = StructuredChatAgent.create_prompt(
    tools,
    prefix=prompt['prefix'],
    suffix=prompt['suffix'],
    format_instructions=prompt['format_instructions'],
    input_variables=["input", "chat_history", "agent_scratchpad","workflow"],
    )
    
    #memory
    memory = ConversationBufferWindowMemory(memory_key="chat_history",input_key="input",output_key="output",k=10,chat_memory=ChatMessageHistory())
    
    #make agent
    llm=OpenAI(model_name='gpt-4-1106-preview',temperature=0)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    agent = StructuredChatAgent(llm_chain=llm_chain, tools=tools, verbose=True)
    agent_chain = AgentExecutor.from_agent_and_tools(
        agent=agent, tools=tools, verbose=True,
        memory=memory,return_intermediate_steps=True,
        handle_parsing_errors=True, max_iterations=25
    )
    

    ################ CLI ###################
    agent_chain.memory.clear()
    input_text="""\n\nWelcome to the Terarium Workflow CLI where you can interact with the Terarium Workflow using free form text.\n
    You can do things like search for models by typing a request like 'Can you find a model for COVID-19?' or add different objects like models, simulations or datasets to your workflow by making a request like 'Can you add a dataset on covid-19 cases in Boston?'\n
    You (type 'exit' to quit, type 'clear' to clear conversation history, type 'reset' to reset the workflow to a blank workflow, type 'history' to see the conversation history, type 'help' to get a full list of options):\n"""
    #add help option in which LLM looks at state and determines possible options for what to do next
    in_help_menu=False
    while True:
        user_response = input(input_text)
        
        input_text="You (type 'exit' to quit, type 'clear' to clear conversation history, type 'reset' to reset the workflow to a blank workflow, type 'history' to see the conversation history, type 'help' to get a full list of options):\n"
            
        if user_response.lower() == "help":
            main_help_print="""\n\nWelcome to the Terarium Workflow CLI where you can interact with the Terarium Workflow using free form text.
            Terarium is a comprehensive modeling and simulation ecosystem designed to support decision making in diverse missions and scientific domains built for researchers.
            In the workflow screen you can create workflows in which different Terarium assets (such as models, datasets, model configurations, calibrations, simulations) interact. For more information on Terarium and Terarium objects visit www.terarium-docs.com.
            
            Here are some types of requests you can do in the Terarium Workflow CLI:
            Search for models - Example Request: Can you find a model for COVID-19?'
            Add models - Example Request: Can you add a model for COVID-19 to my workflow?
            Delete models - Example Request: Can you remove the model we just added?
            Add Datasets - Example Request: Can you add the dataset with id insert_dataset_id to my workflow?
            Delete Datasets - Example Request: Can you delete the first dataset?
            Add Simulation - Example Request: Can you simulate the covid-19 model with the default simulation settings?
            Modify Simulation - Example Request: Can you modify the simulation we just made with the same settings we just had but until time insert_time_here?
            Delete Simulation - Example Request: Can you delete the simulation we just did?
            Request Workflow Information - Example Request: How many models are in my current workflow?
            
            Additionally you can issue more complex requests and the terarium cli will fill in the missing pieces where appropriate and ask you where appropriate.
            
            For example, you may ask "I'd like to use the SIR model to perform a simulation for a location 
            with a total population of 1M where 99% start out susceptible, 
            1% are infected and there are no recovered people to begin with. 
            Gamma should be 0.1 and the other parameters can be left as default."
            
            In this case the cli would find an SIR model and it may ask you to pick from a list of models it found. After that it will add the model to the workflow.
            Then it will create a new model configuration with the new settings and then create a simulation node with the model connected.
            
            For more information go to www.terarium-docs.com/workflow-cli
            
            """
            print(main_help_print)
            continue
        if user_response.lower() == "exit":
            print("Exiting...")
            break
        if user_response.lower() == "clear":
            print("Clearing Conversation History...")
            agent_chain.memory.clear()
            print("History Cleared... ")
            continue
        if user_response.lower() == "reset":
            print("\nResetting workflow to blank state")
            clear_workflow()
            print("\nWorkflow has been reset\n")
            continue
        if user_response.lower() == "history":
            history_string='\n\n'.join([mes.content for mes in agent_chain.memory.chat_memory.messages])
            print(f"Here is the history of our conversation:\n\n{history_string}\n")
            continue
        if user_response.lower() == "workflow":
            workflow_string='\n\n'+ json.dumps(get_workflow(WORKFLOW_ID))
            print(f"\nHere is the current workflow dict: {workflow_string}\n")
            continue
        
        ai_response=agent_chain.invoke({"input":user_response,"workflow":get_workflow(WORKFLOW_ID)})
        print(ai_response['output'])
        print('\n')
        
            
if __name__=="__main__":
    main()    

