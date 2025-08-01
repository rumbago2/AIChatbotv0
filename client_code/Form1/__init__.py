from ._anvil_designer import Form1Template
from anvil import *
import anvil.server 

class Form1(Form1Template):
  def __init__(self, **properties):
    self.init_components(**properties)

  def submitllm_click(self, **event_args):
    """Called when the button is clicked"""

    try:
      # Captura de inputs
      user_prompt = self.user_prompt.text.strip()
      llm_name = self.llm_name.selected_value.strip()
      pl = float(self.petal_length.text) if self.petal_length.text else 0.0
      pw = float(self.petal_width.text) if self.petal_width.text else 0.0

      if not user_prompt or not llm_name:
        raise ValueError("Prompt and LLM model must not be empty.")

      self.species_label.visible = True
      self.species_label.text = "Contacting LLM, please wait..."
      print(f"📤 Calling ask_llm({user_prompt}, {llm_name}, {pl}, {pw})")

      # Llama la función del backend
      result = anvil.server.call('ask_llm', user_prompt, llm_name, pl, pw)

      if "error" in result:
        self.species_label.text = f"❌ Error: {result['error']}"
      else:
        self.species_label.text = (
          f"🤖 LLM ({result['model']}) response:\n\n{result['response']}\n\n"
          f"🧮 Tokens used: {result['tokens_used']}"
        )
    except Exception as e:
      self.species_label.visible = True
      self.species_label.text = f"❌ Error: {e}"
      print(f"⚠️ Exception: {e}")
