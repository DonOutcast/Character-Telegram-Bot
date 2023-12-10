def get_user_response_from_data(data: dict) -> str:
    try:
        result = data.get("choices")[0].get("message").get("content")
    except:
        result = ""
    return result
