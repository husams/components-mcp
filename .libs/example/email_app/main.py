"""
Email application main entry point.

This is an example application component that demonstrates the 'app' type structure.
"""

from typing import Optional
from .helpers import sender, inbox, search


def main(action: str, **kwargs) -> dict:
    """
    Main entry point for the email application.

    This function provides a unified interface for all email operations.

    Args:
        action: The action to perform - 'send', 'list', or 'search'
        **kwargs: Action-specific parameters

    Returns:
        Dictionary with operation results

    Examples:
        >>> main('send', to='user@example.com', subject='Hello', body='Test')
        {'status': 'sent', 'message_id': '...'}

        >>> main('list', folder='inbox', limit=10)
        [{'id': '1', 'subject': 'Test', ...}]

        >>> main('search', query='important', from_addr='boss@example.com')
        [{'id': '1', 'subject': 'Important meeting', ...}]
    """
    if action == 'send':
        to = kwargs.get('to', '')
        subject = kwargs.get('subject', '')
        body = kwargs.get('body', '')
        from_addr = kwargs.get('from_addr', 'noreply@example.com')
        return sender.send_email(to, subject, body, from_addr)

    elif action == 'list':
        folder = kwargs.get('folder', 'inbox')
        limit = kwargs.get('limit', 10)
        return inbox.list_emails(folder, limit)

    elif action == 'search':
        query = kwargs.get('query', '')
        folder = kwargs.get('folder', 'inbox')
        from_addr = kwargs.get('from_addr')
        limit = kwargs.get('limit', 10)
        return search.search_emails(query, folder, from_addr, limit)

    else:
        return {
            'error': f"Unknown action: {action}",
            'available_actions': ['send', 'list', 'search']
        }
