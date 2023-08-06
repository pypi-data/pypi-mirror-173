import tokenize

from pylint.checkers import BaseTokenChecker

from .. import settings

ODOO_MSGS = {
    # C->convention R->refactor W->warning E->error F->fatal
    "W%d02"
    % settings.BASE_FORMAT_ID: ("Use of vim comment", "use-vim-comment", settings.DESC_DFLT),
}


class FormatChecker(BaseTokenChecker):

    name = settings.CFG_SECTION
    msgs = ODOO_MSGS

    def is_vim_comment(self, comment):
        return comment.strip("# ").lower().startswith("vim:")

    def process_tokens(self, tokens):
        for tok_type, token_content, start_line_col, _end_line_col, _line_content in tokens:
            if tokenize.COMMENT == tok_type:
                line_num = start_line_col[0]
                if self.is_vim_comment(token_content):
                    self.add_message("use-vim-comment", line=line_num)
