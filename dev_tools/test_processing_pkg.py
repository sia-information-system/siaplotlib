# Standard
import unittest
# Own
from siaplotlib.processing.parallelism import AsyncRunner


class TestAsyncRunner(unittest.TestCase):
  def __init__(self, methodName: str = "runTest") -> None:
    super().__init__(methodName)
    self.async_process_ok: bool = False


  def sync_fn(self, text: str):
    text_splited = text.split(' ')
    l = len(text_splited)
    return text_splited, l


  def sync_fn_success_callback(self, text_splited, length):
    print(f'\nText splited: {text_splited}. Length: {length}')
    self.async_process_ok = True
  

  def sync_fn_failure_callback(self, err):
    self.async_process_ok = False
    print(err)


  def test_async_runner(self):
    self.async_process_ok = False
    async_runner = AsyncRunner(
      sync_fn=self.sync_fn,
      sync_fn_kwargs={'text': 'hello, world!'},
      success_callback=self.sync_fn_success_callback,
      failure_callback=self.sync_fn_failure_callback)
    async_runner.run()
    async_runner.wait()
    self.assertTrue(self.async_process_ok)
  

  def sync_fn_1_return_val(self, text: str):
    text_splited = text.split(' ')
    return text_splited


  def sync_fn_1_return_val_success_callback(self, text_splited):
    print(f'\nText splited: {text_splited}.')
    self.async_process_ok = True


  def test_async_runner_1_return_val(self):
    self.async_process_ok = False
    async_runner = AsyncRunner(
      sync_fn=self.sync_fn_1_return_val,
      sync_fn_kwargs={'text': 'hello, world!'},
      success_callback=self.sync_fn_1_return_val_success_callback,
      failure_callback=self.sync_fn_failure_callback)
    async_runner.run()
    async_runner.wait()
    self.assertTrue(self.async_process_ok)
  

  def sync_fn_return_int(self, text: str):
    text_splited = text.split(' ')
    return len(text_splited)


  def sync_fn_return_int_success_callback(self, text_splited):
    print(f'\nText splited length: {text_splited}.')
    self.async_process_ok = True


  def test_async_runner_return_int(self):
    self.async_process_ok = False
    async_runner = AsyncRunner(
      sync_fn=self.sync_fn_return_int,
      sync_fn_kwargs={'text': 'hello, world!'},
      success_callback=self.sync_fn_return_int_success_callback,
      failure_callback=self.sync_fn_failure_callback)
    async_runner.run()
    async_runner.wait()
    self.assertTrue(self.async_process_ok)
  

  def sync_fn_catch_tuple(self, *tp):
    print(f'\nTuple: {tp}')
    self.async_process_ok = True

  
  def test_async_runner_catch_tupples(self):
    self.async_process_ok = False
    async_runner = AsyncRunner(
      sync_fn=self.sync_fn,
      sync_fn_kwargs={'text': 'hello, world!'},
      success_callback=self.sync_fn_catch_tuple,
      failure_callback=self.sync_fn_failure_callback)
    async_runner.run()
    async_runner.wait()
    self.assertTrue(self.async_process_ok)


if __name__ == '__main__':
  unittest.main()
