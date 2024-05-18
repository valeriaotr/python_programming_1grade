from homework08.vkapi import config  # type: ignore
from homework08.vkapi.session import Session  # type: ignore

session = Session(config.VK_CONFIG["domain"])
