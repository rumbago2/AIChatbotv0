from ._anvil_designer import Form1Template
from anvil import *
import anvil.server

class Form1(Form1Template):
  def __init__(self, **properties):
    self.init_components(**properties)

    # --- Inicializa el historial y valores por defecto ---
    self.chat_history = []
    #self.llm_name.items = ["gemini-1.5-flash", "gemini-pro"]
    #self.llm_name.selected_value = "gemini-1.5-flash"

    self.chat_display.content = ""
    self.status_label.text = ""
    self.status_label.visible = False

  def submitllm_click(self, **event_args):
    """Se ejecuta al hacer clic en Enviar."""
    try:
      user_prompt = self.user_prompt.text.strip()
      llm_name = self.llm_name.selected_value

      if not user_prompt or not llm_name:
        alert("The prompt and LLM model cannot be empty.", title="Input Error")
        return

      pl = float(self.petal_length.text) if self.petal_length.text else 0.0
      pw = float(self.petal_width.text) if self.petal_width.text else 0.0

    except ValueError:
      alert("Petal Length and Petal Width must be valid numbers.", title="Input Error")
      return

    # Feedback de UI
    self.status_label.visible = True
    self.status_label.text = "🤖 Generating response, please wait..."
    self.submitllm.enabled = False

    try:
      result = anvil.server.call('ask_llm', user_prompt, llm_name, pl, pw, self.chat_history)

      if "error" in result:
        self.status_label.text = f"❌ Error from backend: {result['error']}"
      else:
        self.chat_history = result['updated_chat_history']
        self._update_chat_display()
        self.status_label.text = f"✅ Response received. Tokens used: {result['tokens_used']}"
        self.user_prompt.text = ""

    except Exception as e:
      self.status_label.text = f"❌ Unexpected error: {e}"
      print(f"❌ Exception during server call: {e}")

    finally:
      self.submitllm.enabled = True
      self.user_prompt.focus()

  def _update_chat_display(self):
    """Renderiza el historial de conversación en el componente RichText."""
    formatted_chat = ""
    for turn in self.chat_history:
      role = turn['role'].capitalize()
      content = "\n".join(turn['parts'])
      if role == 'User':
        formatted_chat += f"**You:**\n{content}\n\n"
      else:
        formatted_chat += f"**🤖 Model:**\n{content}\n\n"

    self.chat_display.content = formatted_chat
    self.call_js('scrollRichTextToBottom', self.chat_display)
    
  def clear_button_click(self, **event_args):
    """Reinicia la conversación."""
    self.chat_history = []
    self.user_prompt.text = ""
    self.chat_display.content = ""
    self.status_label.text = "🗑️ Chat cleared."
    print("Chat history cleared.")