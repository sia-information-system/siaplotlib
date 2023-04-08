class SiaException(Exception):
  def __init__(self, messages: str | list[str] = None, tb = None):
    if type(messages) is str and messages != '':
      self.messages = [messages]
    elif type(messages) is list:
      self.messages = messages
    else:
      self.messages = []
    if tb is not None:
      self.with_traceback(tb)


  def __str__(self):
    message = ''
    if self.messages:
      message = '\nMessages:\n'
      for m in self.messages:
        message += f'-> {m}\n'
    return message
  

  def add_message(self, message: str):
    self.messages.append(message)


class AsyncRunnerBusyException(SiaException):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)


class DuplicatedAsyncRunnerException(SiaException):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)


class AsyncRunnerMissingException(SiaException):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
