import re

async def remove_markdown(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'`(.*?)`', r'\1', text)
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1', text)
    text = re.sub(r'!\[(.*?)\]\((.*?)\)', r'\1', text)
    text = re.sub(r'#{1,6}\s+(.*?)\n', r'\1\n', text)
    text = re.sub(r'---', '', text)
    text = re.sub(r'-\s+(.*?)\n', r'\1\n', text)
    text = re.sub(r'\d+\.\s+(.*?)\n', r'\1\n', text)
    return text
