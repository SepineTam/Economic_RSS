import difflib

def compare_content(old_content, new_content):
    # 使用 difflib 比较内容差异
    diff = difflib.unified_diff(old_content.splitlines(), new_content.splitlines())
    return list(diff)