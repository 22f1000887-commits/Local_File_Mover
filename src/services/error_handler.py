def format_error_message(exception: Exception) -> str:
    message = str(exception)
    if "No such file or directory" in message:
        return "Source or destination path not found"
    if "Permission denied" in message:
        return "Permission denied when accessing a file or folder"
    if "existing file" in message or "destination" in message:
        return "Failed due to an existing file at destination"
    return message
