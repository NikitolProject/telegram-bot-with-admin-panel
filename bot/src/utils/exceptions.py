from __future__ import annotations

__all__ = (
    'ChatNotFoundException', 
    'MatfilterDisabledException', 
    'AntispamFilterDisabledException',
    'CaptchaModuleDisabledException'
)


class ChatNotFoundException(Exception):

    def __init__(self: ChatNotFoundException, title: str) -> None:
        super().__init__(f"The chat \"{title}\" was not found in the database")


class MatfilterDisabledException(Exception):

    def __init__(self: MatfilterDisabledException, title: str) -> None:
        super().__init__(f"The checkmate filter is turned off in the \"{title}\" chat")


class AntispamFilterDisabledException(Exception):

    def __init__(self: AntispamFilterDisabledException, title: str) -> None:
        super().__init__(f"The anti-spam filter is turned off in the \"{title}\" chat")


class CaptchaModuleDisabledException(Exception):

    def __init__(self: CaptchaModuleDisabledException, title: str) -> None:
        super().__init__(f"The captha module is turned off in the \"{title}\" chat")
