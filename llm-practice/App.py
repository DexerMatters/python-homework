import gradio as gr
from Utils import Utils

utils = Utils()

def get_llm_info(llm_dropdown):
    llm_name = llm_dropdown
    agent = utils.findAgent(llm_name)
    return agent["name"], agent["agent_description"]

def chat_with_llm(llm_dropdown, user_prompt):
    llm_name = llm_dropdown
    agent = utils.findAgent(llm_name)
    response = utils.get_response(user_prompt, agent)
    return response

def create_llm(name_input, description_input, system_prompt_input, persona_input, temperature_input):
    utils.addAgent(name_input, description_input, system_prompt_input, persona_input, temperature_input)
    utils.save_data()
    return f"LLM {name_input} created successfully!"

with gr.Blocks() as demo:
     
    with gr.Tab("对话"):
        gr.Markdown("## LLM对话")
        llm_dropdown = gr.Dropdown(label="选择LLM", choices=[], interactive=True)
        llm_name_display = gr.Textbox(label="LLM名称", interactive=False)
        llm_description_display = gr.Textbox(label="LLM描述", interactive=False)
        user_prompt = gr.Textbox(label="你的输入")
        chat_button = gr.Button("发送")
        chat_output = gr.Textbox(label="对话结果")

        llm_dropdown.change(get_llm_info, inputs=llm_dropdown, outputs=[llm_name_display, llm_description_display])
        chat_button.click(chat_with_llm, inputs=[llm_dropdown, user_prompt], outputs=chat_output)


    with gr.Tab("创建LLM"):
        gr.Markdown("## 创建一个自定义的LLM")
        input_name = gr.Textbox(label="名称")
        input_agent_description = gr.Textbox(label="对LLM的描述")
        input_client_description = gr.Textbox(label="对我的描述")
        input_persona = gr.Textbox(label="LLM的个性")
        input_temperature = gr.Slider(minimum=0, maximum=1, step=0.1, default=0.5, label="温度")
        create_button = gr.Button("创建")
        create_output = gr.Textbox(label="创建结果")

        create_button.click(
            create_llm, 
            inputs=[input_name, input_agent_description, input_client_description, input_persona, input_temperature], 
            outputs=[create_output, llm_dropdown])

demo.launch(share=False) # share=True to make the app accessible to others 
