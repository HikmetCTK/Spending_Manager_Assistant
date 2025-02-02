import gradio as gr
import pymysql
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import json
from pathlib import Path
import os
load_dotenv()
import sys
from tabulate import tabulate
import matplotlib.pyplot as plt

def connect():

        try:
            connection=pymysql.connect(host='localhost',
                                user='root',
                                password="sql5858",
                                database='rcpt_mng1')
            return connection
        except pymysql.MySQLError as e:
            return str(e)   
class Agent:
    def __init__(self,system_prompt:str):
        self.api_key=os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)
        self.system_prompt=system_prompt
        self.generation_config={
    "temperature":0.1,
    "max_output_tokens":2048,
    "response_mime_type": "application/json"
 
}
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config=self.generation_config,
            system_instruction=self.system_prompt
)
        self.model_chatbot=genai.GenerativeModel(model_name="gemini-1.5-flash",
                                                generation_config={
                                                    "temperature":0.7 ,  # Balance between creativity and consistency
                                                    "top_p":0.96,
                                                    "top_k":15,
                                                    "max_output_tokens":8192},
                                                system_instruction=self.system_prompt)
        self.chat_hist=self.model_chatbot.start_chat(history=[])
        


    def process_img(self,img):
        # Load the image from the given path and get answer
        
        try:
            response=self.model.generate_content(["",img])
            return response.text
        except Exception as e:
            return str(e)

    def chat_with_receipt(self, question: str):
        try:
           
            response = self.chat_hist.send_message(question)
            return response.text
        except Exception as e:
            return str(e)
        
 # database functions(inserting data to database)

def last_receipt_id(person_id):
    connection=connect()
    with connection.cursor() as cursor:
        try:
            query="select max(r_id) from receipt_items where c_id=%s"  #!!!!!!! c_id is not in receipt_items table
            cursor.execute(query,(person_id,))
            result=cursor.fetchone()
            
            if result[0] is None:
                
                return 1
            else:
                
                return result[0]
        except Exception as e:
            return str(e)
        finally:
            
            connection.close()

def receipt_item(r_id,r_item_name,r_quantity,r_price,c_id):
    connection=connect()
    try:
        with connection.cursor() as cursor:
            
            query="""INSERT INTO receipt_items (r_id, r_item_name, r_quantity, r_price, c_id) VALUES (%s,%s,%s,%s,%s)"""
            cursor.execute(query,(r_id,r_item_name,r_quantity,r_price,c_id))
            connection.commit()
            

    except Exception as e:
        return str(e)
    finally:
        
        connection.close()           

def p_total_price(r_id,total_amount):
    connection=connect()
    try:
        with connection.cursor() as cursor:
            query="""INSERT INTO p_total_price (r_id, p_date, p_total) VALUES (%s,NOW(),%s)"""
            cursor.execute(query,(r_id,total_amount))
            connection.commit()
    except Exception as e:
        return str(e)
    finally:
        cursor.close()
        connection.close()
def receipt_header(c_id):
    
    connection=connect()
    
    try:
        with connection.cursor() as cursor:
            query="INSERT INTO receipt_header (c_id) VALUES (%s)" #customer id
            cursor.execute(query,(c_id))
            connection.commit()
    except Exception as e:
        return e
    finally:
        cursor.close()
        connection.close()   


# Function to process the receipt data
def process_multi_receipts(receipt_data,cid,image_id):
    # Check if the data is a list (multiple receipts) or a dictionary (single receipt)
    if isinstance(receipt_data, list):
        # Process each receipt when it's a list
        for receipt in receipt_data:
            process_single_receipt(receipt,cid,image_id)
    else:
        # Process single receipt if it's not a list
        process_single_receipt(receipt_data,cid,image_id)
        

# Function to process a single receipt
def process_single_receipt(json_receipt,cid,image_id):

    SUM_amount= json_receipt['total_amount']
    
    p_total_price(r_id=image_id,total_amount=SUM_amount)
    receipt_header(cid)
    
    # Loop through each item in the receipt
    for item in json_receipt['objects']:
        item_name = item['item_name']
        quantity = item['quantity']
        price = item['price']
        #confidence = item['confidence']
        #it can be added confidence condition here
        receipt_item(image_id,item_name,quantity,price,cid)


def login(email: str, password: str):
    connection = connect()

    try:
        with connection.cursor() as cursor:
            query = "select * from customer where c_name=%s and c_password=%s"
            cursor.execute(query, (email, int(password)))
            record = cursor.fetchone()
            if record:
                return "True", (record[0])  # Return status and customer ID
            else:
                return "False", ""  # Return status and empty string for failed login
    except Exception as e:
        return str(e), ""  # Return error message and empty string
    finally:
        connection.close()

#Agent prompts        
def process_image(image):
    """This function processes the uploaded image and returns the extracted information in JSON format."""
    if image is None:
        return "Please upload an image"
    
    try:
        # Initialize the processor
        system_prompt1="""Analyze this receipt image and extract the following information in JSON format:
    - item name
    -Quantity
    - All items purchased with their prices
    - Date and time of purchase
    -Total amount
**Response format:**
{
    "image_id": {"type": "STRING"},
    "date_time": {"type": "STRING"},
    "total_amount": {"type": "NUMBER"},
    "objects": {
        "type": "ARRAY",
        "items": {
            "type": "OBJECT",
            "properties": {
                "item_name": {"type": "STRING"},
                "quantity": {"type": "INTEGER"},
                "price": {"type": "NUMBER"},
                "confidence": {"type": "NUMBER"}
            },
            "required": ["item_name", "quantity", "price", "confidence"]
        }
    },
    "required": ["image_id", "date_time", "total_amount", "objects"]
}


"""
        receipt_to_json = Agent(system_prompt=system_prompt1)
        
        # Process the image directly
        result = receipt_to_json.process_img(image)
        return result
    
    except Exception as e:
        return f"Error: {str(e)}"
    
def receipt_analyzer_prompt(cid):
    """This function gets the data of customer from database."""
    connection = connect()
    prompt="""You are a helpful receipts assistant that can help people manage their receipts. You have access to all receipt data of the customer, including the items purchased, their categories, prices, and purchase dates. Based on user queries, you will:  
* Retrieve and analyze receipt data to answer questions accurately.  
* Provide insights, such as total spending, category-based expenses, or frequently purchased items.  
* Suggest budgeting tips, cost-saving strategies, or recommendations to improve spending habits based on the customer's query and receipt history.  
* Format your responses clearly and concisely for easy understanding.  

Always ensure your responses are polite, actionable, and relevant to the user's request. If the user asks for suggestions, provide practical advice tailored to their spending patterns.
*Sample Receipt information format*:
(item_name, item_quantity,price, receipt_date)

**Customer receipt informations**:
{all_data}
"""
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT   ri.r_item_name, ri.r_quantity, ri.r_price, rh.r_date 
            FROM     receipt_items ri         
            JOIN     receipt_header rh ON rh.all_receipt_id = ri.c_id 
            WHERE    ri.c_id = %s
            AND rh.r_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            ORDER BY rh.r_date DESC;
            """
            cursor.execute(query, (cid))
            records = cursor.fetchall()
            formatted_records = []
            for record in records:
                formatted_records.append(str(record))
            # Join records and format the prompt
            records_str = "\n".join(formatted_records)
            final_prompt = prompt.format(all_data=records_str)
            #print(records)
            return final_prompt
    except Exception as e:
        return str(e)
    finally:
        
        connection.close()


def get_customer_receipts(cid):
    """This function fetches the receipt history of the customer from the database."""
    connection = connect()
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    ri.r_item_name, 
                    ri.r_quantity, 
                    ri.r_price, 
                    rh.r_date 
                FROM 
                    receipt_items ri
                JOIN 
                    receipt_header rh 
                ON 
                    rh.all_receipt_id = ri.r_id  
                WHERE 
                    rh.c_id = %s 
                ORDER BY 
                    rh.r_date DESC
            """
            cursor.execute(query, (cid,))
            records = cursor.fetchall()
            headers = ["Item Name", "Quantity", "Price (₺)", "Date"]
            return tabulate(records, headers=headers, tablefmt="grid"),records
    except Exception as e:
        return f"Error fetching receipts: {e}"
    finally:
        connection.close()
            
            
def plot_receipt_summary(data):
    """This function generates a bar plot of the total prices of items in the receipt."""
    item_names = [item[0] for item in data ]       # Extract item names
    #quantities = [item[1] for item in data]       # Extract quantities
    total_prices = [item[2] for item in data]

    
    # Create the plot
    plt.figure(figsize=(10, 15))
    plt.barh(item_names, total_prices, color="skyblue")
    plt.xlabel("Total Price (₺)")
    plt.ylabel("Item Name")
    plt.title("Receipt Summary")
    plt.tight_layout()
    return plt.gcf()

def talk_with_receipt(question, cid, chat_hist):
    """This function allows the user to chat with the receipt assistant."""
    try:
        # Generate the prompt with user-specific receipt data
        prompt_with_data= receipt_analyzer_prompt(cid)
        
        # Create the Agent with the generated prompt
        receipt_analyzer = Agent(system_prompt=prompt_with_data)
        
        # Chat with the receipt
        response = receipt_analyzer.chat_with_receipt(question)
        
        # Update chat history
        chat_hist.append({"role": "user", "content": question})
        chat_hist.append({"role": "assistant", "content": response})
        
        return "", chat_hist
    except Exception as e:
        return f"Sorry, I couldn't access your receipt history: {e}", chat_hist


#Interface functions
def exit_gradio():
    sys.exit
    return "Exiting Gradio app..."
    

def login_switch(login_status):
    if login_status == "True":
        return gr.update(visible=True), gr.update(visible=False)
    else:
        return gr.update(visible=False), gr.update(visible=True)

def switch_to_process():
    return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)

def switch_to_view():
    return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)

def switch_to_chat():
    return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)

def update_database(updated_text, cid):
    try:
        data = json.loads(updated_text)
        receipt_id = last_receipt_id(cid)
        receipt_id += 1
        
        process_multi_receipts(data, cid, str(receipt_id))
        return "Receipt information successfully added to database🎉🎉"
    except Exception as e:
        
        return f"You have corrupted the text format, please try again. Error: {e}----[{cid}]---{receipt_id}----|\n\n----{updated_text}"



def handle_login(username, password):
    status, cid = login(username, password)
    return status, cid

with gr.Blocks() as app:
    cid_state = gr.State()
    prompt=gr.State()
    tuple_perceipt_data=gr.State()
    # Login Page
    with gr.Row(visible=True) as login_page:
        with gr.Column():
            gr.Markdown("### Welcome to Login Page🤗")
            username_input = gr.Textbox(label="Username")
            password_input = gr.Textbox(label="Password (Integer)", type="password")
            login_button = gr.Button("Login")
            login_status = gr.Textbox(label="Login Status", interactive=False)
            
            
    # Main Application (hidden initially)
    with gr.Row(visible=False) as main_page:

        # Left Navigation Menu
        with gr.Column(scale=1):
            gr.Markdown("### Navigation Menu")
            with gr.Row():
                process_page_btn = gr.Button("Process Receipts 🧾")
            with gr.Row():
                view_page_btn = gr.Button("View Receipts 📋")
            with gr.Row():
                chat_page_btn = gr.Button("Chat About Receipts 💬")
            with gr.Row():
                exit_button = gr.Button("Exit ❌")

        # Content Area
        with gr.Column(scale=4):
            # Receipt Processing Page
            with gr.Row(visible=True) as process_page:
                with gr.Column():
                    gr.Markdown("### Receipt to Text 🧾-->🔠")
                    image_input = gr.Image(type="pil", label="Upload Image")
                    output_text = gr.Textbox(
                        value="",
                        label="Analysis Result📊 (You can set values. LLM may misunderstand some values!! ⚠️ Don't change punctuation)",
                        lines=20
                    )
                    process_button = gr.Button("Analyze Image🔎")
                    success_message = gr.Textbox(label="Message", interactive=False)
                    update_button = gr.Button("Update✏️")
                
                with gr.Column():
                    gr.Markdown("#### Example Images (Click to Process)📸")
                    gr.Examples(
                        examples=[
                            ["026cdf26bef821b606534bcf3d46543b.jpg"],
                            ["Screenshot 2024-12-22 142937.png"],
                            ["Screenshot 2024-12-23 005014.png"]
                        ],
                        fn=process_image,
                        inputs=[image_input],
                        outputs=[output_text]
                    )

            # Receipt Viewing Page
            with gr.Row(visible=False) as view_page:
                with gr.Column():
                    gr.Markdown("### View Receipt History 📋")
                    receipts_display = gr.Textbox(
                        label="Your Receipt history",
                        lines=35,
                        interactive=False
                    )
                    get_receipts_button = gr.Button("Get all Receipts 🔄")

                with gr.Column():
                    gr.Markdown("### View Receipt Summary 📊 ⚠️You should run first receipt history part")
                    receipt_plot = gr.Plot(
                    label="Receipt Summary Plot"
                     # Assign the plot function
                )
                     
                    
                    visualize_button = gr.Button("Get Summary 📊")
            # Chatbot Page
            with gr.Row(visible=False) as chat_page:

                
                with gr.Column():
                    gr.Markdown("### Spending Habit Manager. Chat with  Your Receipts 💬")
                    chatbot = gr.Chatbot(
                        value="",
                        label="Chat History",
                        height=700
                        ,type="messages"
                    )
                    msg = gr.Textbox(
                        label="Ask your question here...",
                        placeholder="Type your question here...",
                        lines=2)
                    btn = gr.Button("Submit")
                    #get_data_button = gr.Button("Get my spending data")
                    clear_button = gr.ClearButton(components=[msg, chatbot], value="Clear console")


    # Event handlers
    login_button.click(
        fn=login,
        inputs=[username_input, password_input],
        outputs=[login_status, cid_state]
    )

    #chat_history=receipt_analyzer.chat_hist
    login_status.change(
        fn=login_switch,
        inputs=[login_status],
        outputs=[main_page, login_page]
    )
    
    # Navigation handlers
    process_page_btn.click(
        fn=switch_to_process,
        outputs=[process_page, view_page, chat_page]
    )
    view_page_btn.click(
        fn=switch_to_view,
        outputs=[process_page, view_page, chat_page]
    )
    chat_page_btn.click(
        fn=switch_to_chat,
        outputs=[process_page, view_page, chat_page]
    )
    
    # Process page handlers
    process_button.click(
        fn=process_image,
        inputs=[image_input],
        outputs=[output_text]
    )
    update_button.click(
        fn=update_database,
        inputs=[output_text, cid_state],
        outputs=[success_message]
    )
    
    # View page handlers
    get_receipts_button.click(
        fn=get_customer_receipts,
        inputs=[cid_state],
        outputs=[receipts_display,tuple_perceipt_data],
        scroll_to_output=True
    )

    btn.click(
        fn=talk_with_receipt,
        inputs=[msg,cid_state,chatbot], 
        outputs=[msg,chatbot])
    
    msg.submit(
        fn=talk_with_receipt, 
        inputs=[msg,cid_state,chatbot], 
        outputs=[msg,chatbot])

    visualize_button.click(
        fn=plot_receipt_summary,
        inputs=[tuple_perceipt_data],
        outputs=[receipt_plot]
    )
    exit_button.click(exit_gradio)

if __name__=="__main__":
    app.launch()