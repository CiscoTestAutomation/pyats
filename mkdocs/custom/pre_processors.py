import re
from markdown import Extension
from markdown.preprocessors import Preprocessor

class DoubleBacktickPreprocessor(Preprocessor):
    def run(self, lines):
        new_lines = []
        for line in lines:
            # Replace double backticks with <code> HTML tags
            line = re.sub(r'``(.*?)``', r'<code class="double-backtick-highlight">\1</code>', line)
            new_lines.append(line)
        return new_lines
    
class IndentPreprocessor(Preprocessor):
    def run(self, lines):
        new_lines = []
        for line in lines:
            if line.startswith('  '):  # Check for two leading spaces
                line = f'<div class="double-space-indent">{line[2:]}</div>'  # Remove spaces and wrap in div
            new_lines.append(line)
        return new_lines

class CustomMarkdownExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(DoubleBacktickPreprocessor(), 'double_backtick', 175)
        # md.preprocessors.register(IndentPreprocessor(), 'indent', 176)

def makeExtension(**kwargs):
    return CustomMarkdownExtension(**kwargs)