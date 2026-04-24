class Solution:
    def entityParser(self, text: str) -> str:
        entityMap = {
            "&quot;": '"',
            "&apos;": "'",
            "&amp;": "&",
            "&gt;": ">",
            "&lt;": "<",
            "&frasl;": "/"
        }

        for entity, char in entityMap.items():
            text = text.replace(entity, char)

        return text