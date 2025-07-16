def double_list_items(data: list[float]) -> list[float]:
    """
    接收一个包含数字的列表，将每个元素都乘以2后返回新的列表。
    参数:
        data (list[float]): 输入的数字列表。
    返回:
        list[float]: 每个元素都乘以2的新列表。
    """
    return [item * 2 for item in data]