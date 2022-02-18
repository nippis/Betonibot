from telegram.ext import MessageFilter, Filters

class FilterHashtag(MessageFilter):
    def filter(self, message):
        return message.text.startswith("#protip")

class FilterCalculation(MessageFilter):
    def filter(self, message):
        plus = r'=\s*[0-9]+\s*\+\s*[0-9]+'
        minus = r'=\s*[0-9]+\s*-\s*[0-9]+'
        mult = r'=\s*[0-9]+\s*\*\s*[0-9]+'
        div = r'=\s*[0-9]+\s*/\s*[0-9]+'
        return Filters.regex(plus) | Filters.regex(minus) | Filters.regex(mult) | Filters.regex(div)