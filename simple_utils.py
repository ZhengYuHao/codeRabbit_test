
async def e(text: str, doc_type: str) -> Dict[str, Any]:
    if doc_type == '专利':
        prompt = f"""
        从以下专利文本中提取信息：
        {text[:5000]}

        请提取：
        1. 专利号
        2. 申请日期（YYYY-MM-DD）
        3. 授权日期（如无则写N/A）
        4. 发明人（逗号分隔）
        5. 受让人（公司/机构）

        返回 JSON 格式。
        """
    if doc_type == '论文':
        prompt = f"""
            请从以下论文文本中精确提取信息：
            {text[:5000]}

            要求返回严格JSON格式，包含以下字段：
            1. 标题（必须提取）
            2. 作者（分号分隔，如"张三; 李四; 王五"）
            3. 期刊/会议名称（完整名称）
            4. 发表年份（YYYY，必须从文本中提取）
            5. DOI（完整格式，如"10.1002/ajh.27272"，若无则写N/A）
            6. received_date（收稿日期，YYYY-MM-DD格式）
            7. accepted_date（接受日期，YYYY-MM-DD格式）
            8. published_date（出版日期，YYYY-MM-DD格式）

            特别注意：
            - 日期格式示例：Received:4December2023 → received_date: "2023-12-04"
            - 必须包含所有8个字段，没有的字段写N/A
            - 年份优先从出版日期提取，其次接受日期，最后收稿日期

            示例格式：
            {{
              "标题": "Report of IRF2BP1 as a novel partner of RARA in variant acute promyelocytic leukemia",
              "作者": "Jiang Bin; Zhang San; Li Si",
              "期刊": "American Journal of Hematology",
              "year": 2024,
              "DOI": "10.1002/ajh.27272",
              "received_date": "2023-12-04",
              "accepted_date": "2024-02-18",
              "published_date": "2024-03-01"
            }}
            """

    role = "你是一个信息提取专家"
    api_key = get_llm_key()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    data = {
        'model': "qwen-plus",
        'messages': [
            {"role": "system", "content": "你是一个文档分类专家"},
            {"role": "user", "content": prompt}
        ],
    }
    response = await send_async_request(url, headers, data)
    content = response['choices'][0]['message']['content']
    if content.startswith("```json"):
        content = content.strip("```json").strip("```")
    result = json.loads(content)
    # print("提取结果:", result)

    # 确保所有字段存在
    if doc_type == '论文':
        required_fields = [
            '标题', '作者', '期刊', 'year',
            'DOI', 'received_date', 'accepted_date', 'published_date'
        ]
        for field in required_fields:
            if field not in result:
                result[field] = "N/A"

    return result
