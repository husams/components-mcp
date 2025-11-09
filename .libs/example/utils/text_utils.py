"""Text utility functions."""


def format_text(text: str, format: str = "upper") -> str:
    """
    Format text with various options.
    
    Args:
        text: The text to format
        format: Format option - 'upper', 'lower', 'title', or 'capitalize'
    
    Returns:
        Formatted text string
    
    Examples:
        >>> format_text("hello world", "upper")
        'HELLO WORLD'
        >>> format_text("HELLO WORLD", "title")
        'Hello World'
    """
    if format == "upper":
        return text.upper()
    elif format == "lower":
        return text.lower()
    elif format == "title":
        return text.title()
    elif format == "capitalize":
        return text.capitalize()
    else:
        return text
