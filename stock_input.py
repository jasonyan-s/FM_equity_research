import ipywidgets as widgets
from IPython.display import display

# Create a text input widget
stock_code_input = widgets.Text(
    value='',
    placeholder='Stock code',
    description='Stock code:',
    disabled=False
)

# Create a button widget
submit_button = widgets.Button(
    description='Submit',
    disabled=False,
    button_style='', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Click me',
    icon='check'
)

# Create an output widget
output = widgets.Output()

# Variable to store the stock code
stock_code_value = None

# Define the function to handle button click
def on_button_click(b):
    global stock_code_value
    with output:
        output.clear_output()
        stock_code_value = stock_code_input.value
        print(f"Stock code entered: {stock_code_value}")

def get_stock_code():
    return stock_code_value
# Attach the function to the button click event
submit_button.on_click(on_button_click)

# Display the widgets
display(stock_code_input, submit_button, output)