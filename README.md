# timed-input
Python timed input prompt that works for both windows and linux

# Syntax
```python
  input_with_timeout(prompt, timeout, default)
```
where:
variable | description
-------- | ----------------------------------------
prompt | the input prompt string
timeout | time to wait for response, in seconds
default | optional default return value
    
 If no default is specfied, and timeout occurs, None will be returned.

# Example:
```python
response = input_with_timeout("Continue (y|n): ", 10, "n")
if response in "Nn":
  print("Process aborted.")
  return
  
print("Let's condinue with the process...")
```   
