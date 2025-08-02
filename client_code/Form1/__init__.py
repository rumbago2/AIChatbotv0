from ._anvil_designer import Form1Template
from anvil import *
import anvil.server

class Form1(Form1Template):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Diccionario de historiales por modelo
    self.histories_by_model = {}
    self.active_model = self.llm_name.selected_value or ""
    self.chat_display.content = ""
    self.status_label.text = ""
    self.status_label.visible = False

  def submitllm_click(self, **event_args):
    self._handle_prompt_submission()

  def user_prompt_pressed_enter(self, **event_args):
    self._handle_prompt_submission()

  def llm_name_change(self, **event_args):
    """Cambia el modelo activo y actualiza visualización sin perder historiales previos."""
    self.active_model = self.llm_name.selected_value
    self.chat_history = self.histories_by_model.get(self.active_model, [])
    self._update_chat_display()
    self.status_label.text = f"🧠 Switched model to: {self.active_model}"
    print(f"🔄 Model changed to: {self.active_model}")

  def _handle_prompt_submission(self):
    """Envía el prompt al modelo seleccionado y actualiza el historial."""
    try:
      user_prompt = self.user_prompt.text.strip()
      llm_name = self.llm_name.selected_value

      if not user_prompt or not llm_name:
        alert("The prompt and LLM model cannot be empty.", title="Input Error")
        return

      petal_length = float(self.petal_length.text) if self.petal_length.text else 0.0
      petal_width = float(self.petal_width.text) if self.petal_width.text else 0.0

    except ValueError:
      alert("Petal Length and Petal Width must be valid numbers.", title="Input Error")
      return

    # Recuperar historial del modelo actual
    self.chat_history = self.histories_by_model.get(llm_name, [])

    self.status_label.visible = True
    self.status_label.text = "🤖 Generating response, please wait..."
    self.submitllm.enabled = False

    try:
      result = anvil.server.call(
        'ask_llm', user_prompt, llm_name, petal_length, petal_width, self.chat_history
      )

      if "error" in result:
        self.status_label.text = f"❌ Error from backend: {result['error']}"
      else:
        self.chat_history = result['updated_chat_history']
        self.histories_by_model[llm_name] = self.chat_history  # Guardar historial por modelo
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
    """Renderiza el historial actual en el componente RichText."""
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
    """Borra historial del modelo actual."""
    self.chat_history = []
    self.histories_by_model[self.active_model] = []
    self.user_prompt.text = ""
    self.chat_display.content = ""
    self.status_label.text = "🗑️ Chat cleared."
    print(f"🗑️ Cleared chat for model: {self.active_model}")
