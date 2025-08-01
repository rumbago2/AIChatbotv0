from ._anvil_designer import Form1Template
from anvil import *
import anvil.server

class Form1(Form1Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.chat_history = []
    #self.llm_name.items = ["gemini-1.5-flash", "gemini-pro"]
    #self.llm_name.selected_value = "gemini-1.5-flash"
    self.status_label.text = ""
    self.chat_display.content = ""

  def submitllm_click(self, **event_args):
    """Send user prompt to LLM with history."""
    try:
      user_prompt = self.user_prompt.text.strip()
      llm_name = self.llm_name.selected_value

      if not user_prompt or not llm_name:
        alert("The prompt and model name must not be empty.")
        return

      pl = float(self.petal_length.text) if self.petal_length.text else 0.0
      pw = float(self.petal_width.text) if self.petal_width.text else 0.0

    except ValueError:
      alert("Petal Length and Petal Width must be numbers.")
      return

    self.status_label.text = "⏳ Asking LLM..."
    self.submitllm.enabled = False

    try:
      result = anvil.server.call('ask_llm', user_prompt, llm_name, pl, pw, self.chat_history)

      if "error" in result:
        self.status_label.text = f"❌ Error from backend: {result['error']}"
      else:
        self.chat_history = result["updated_chat_history"]
        self._update_chat_display()
        self.status_label.text = f"✅ Tokens used: {result['tokens_used']}"
        self.user_prompt.text = ""

    except Exception as e:
      self.status_label.text = f"❌ Unexpected error: {e}"
      print(e)

    finally:
      self.submitllm.enabled = True
      self.user_prompt.focus()

  def _update_chat_display(self):
    """Render chat history into RichText area with Markdown format."""
    formatted_chat = ""
    for turn in self.chat_history:
      role = turn["role"].capitalize()
      parts = "\n".join(turn["parts"])
      if role == "User":
        formatted_chat += f"**You:**\n{parts}\n\n"
      else:
        formatted_chat += f"**🤖 Model:**\n{parts}\n\n"

    self.chat_display.content = formatted_chat
    self.call_js("scrollRichTextToBottom", self.chat_display)

  def clear_button_click(self, **event_args):
    """Clear the conversation and reset UI."""
    self.chat_history = []
    self.chat_display.content = ""
    self.status_label.text = "Chat cleared."
    self.user_prompt.text = ""
