import json
content = '{"filename":"dd574932672a49c3a78aaccb9e476f7c.jpg","save_path":"D:\\Django\\GDYL-Blog\\source\\img\\dd574932672a49c3a78aaccb9e476f7c.jpg","url":"http://127.0.0.1:8000/img/dd574932672a49c3a78aaccb9e476f7c.jpg","id":10,"upload_time":"2025-05-11T13:57:22.708589"}'
try:
    data = json.loads(content)
    save_path = data.get('save_path')
    # 打印或处理路径
    print(save_path)
except json.JSONDecodeError as e:
    print(f"解析 JSON 出错: {e}")