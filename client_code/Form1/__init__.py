from ._anvil_designer import Form1Template
from anvil import *
import anvil.server 

class Form1(Form1Template):
  def __init__(self, **properties):
    # The line above MUST be present and named correctly.
    self.init_components(**properties)

    # Your other code here...

  def categorise_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Call the google colab function and pass it the iris measurements
    iris_category = anvil.server.call(
      'predict_iris', 
      int(self.sepal_length.text),
      int(self.sepal_width.text),
      int(self.petal_length.text),
      int(self.petal_width.text)
    )

    # If a category is returned set our species 
    if iris_category:
      self.species_label.visible = True
      self.species_label.text = "The species is " + iris_category.capitalize()
