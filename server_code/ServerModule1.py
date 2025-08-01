from ._anvil_designer import Form1Template
from anvil import *
import anvil.server

class Form1(Form1Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    print("Client: Form initialized.")

  def categorise_button_click(self, **event_args):
    """Called when the button is clicked."""
    # Read and validate input values
    try:
      sl = float(self.sepal_length.text)
      sw = float(self.sepal_width.text)
      pl = float(self.petal_length.text)
      pw = float(self.petal_width.text)
      print(f"Client: Input values received -> SL:{sl}, SW:{sw}, PL:{pl}, PW:{pw}")
    except ValueError:
      self.species_label.visible = True
      self.species_label.text = "Please enter valid numeric values."
      print("Client: Invalid input values, aborting prediction.")
      return

      # Show processing message
    self.species_label.visible = True
    self.species_label.text = "Predicting species, please wait..."
    print("Client: Calling 'predict_iris' server function.")

    try:
      # Call backend function exposed via Anvil Uplink (in Colab)
      iris_category = anvil.server.call('predict_iris', sl, sw, pl, pw)
      print(f"Client: Received prediction result: {iris_category}")

      if iris_category:
        self.species_label.text = f"The species is {iris_category.capitalize()}"
      else:
        self.species_label.text = "No result returned from model."
        print("Client: Warning - No result returned.")
    except Exception as e:
      self.species_label.text = f"Error during prediction: {e}"
      print(f"Client: Exception when calling backend: {e}")
