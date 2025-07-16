<<<<<<< HEAD
def double_list_items(data: list[float]) -> list[float]:
    """
    接收一个包含数字的列表，将每个元素都乘以2后返回新的列表。
    参数:
        data (list[float]): 输入的数字列表。
    返回:
        list[float]: 每个元素都乘以2的新列表。
    """
    return [item * 2 for item in data]
=======
# simple_utils.py - A tiny utility library

def reverse_string(text):
    """
    Return a new string with the characters of the input string in reverse order.
    
    Parameters:
        text (str): The string to be reversed.
    
    Returns:
        str: The reversed string.
    """
    return text[::-1]

def count_words(sentence):
    """
    Count the number of words in a sentence by splitting on whitespace.
    
    Parameters:
    	sentence (str): The sentence to analyze.
    
    Returns:
    	int: The number of words in the sentence.
    """
    return len(sentence.split())

def celsius_to_fahrenheit(celsius):
    """
    Convert a temperature from Celsius to Fahrenheit.
    
    Parameters:
        celsius (float): Temperature value in degrees Celsius.
    
    Returns:
        float: Equivalent temperature in degrees Fahrenheit.
    """
    return (celsius * 9/5) + 32
>>>>>>> 0cea6f35f20b4f9e4848f55682216c4caec4869b
