from __future__ import annotations

import argparse
import contextlib
import re
import textwrap
from typing import Generator
from typing import Match
from typing import NamedTuple
from typing import Sequence

import black

MD_RE = re.compile(
    r'(?P<before>^(?P<indent> *)```(\{code-cell\})?\s*python\n)'
    r'(?P<code>.*?)'
    r'(?P<after>^(?P=indent)```\s*$)',
    re.DOTALL | re.MULTILINE,
)

TAG_RE = re.compile(
    r'(?P<tag>(:tags:[\s]*[\[\"\-\]\w\d\s,_]*\n))'
    r'(?P<code>.*?)$',
    re.DOTALL | re.MULTILINE,
)

PERCENT_PERCENT_RE = re.compile(
    r'(?P<cmd>(%%[\s]*[\[\"\-\]\w\d\s,_]*\n))'
    r'(?P<code>.*?)$',
    re.DOTALL | re.MULTILINE,
)


class TagParserError(RuntimeError):
    pass


class CmdParserError(RuntimeError):
    pass


class CodeBlockError(NamedTuple):
    offset: int
    exc: Exception


def format_str(
    src: str,
    black_mode: black.FileMode,
) -> tuple[str, Sequence[CodeBlockError]]:
    errors: list[CodeBlockError] = []

    @contextlib.contextmanager
    def _collect_error(match: Match[str]) -> Generator[None, None, None]:
        try:
            yield
        except Exception as e:
            errors.append(CodeBlockError(match.start(), e))

    def _md_match(match: Match[str]) -> str:
        code = textwrap.dedent(match['code'])
        is_code_cell = '{code-cell}' in match['before']
        tags = ''
        pps = ''
        has_tag = code.startswith(':tags:')
        has_pp = code.startswith('%%')

        with _collect_error(match):
            if has_tag:
                tag_match = TAG_RE.match(code)
                if tag_match is not None:
                    tags = tag_match['tag']
                    code = tag_match['code']
                else:
                    raise TagParserError(code)

            if has_pp:
                pp_match = PERCENT_PERCENT_RE.match(code)
                if pp_match is not None:
                    pps = pp_match['cmd']
                    code = pp_match['code']
                else:
                    raise CmdParserError(code)

            if is_code_cell:
                code = black.format_cell(code, fast=True, mode=black_mode)
                code += '\n'  # Add extra newline
            else:
                code = black.format_str(code, mode=black_mode)

        code = textwrap.indent(code, match['indent'])
        return f'{match["before"]}{tags}{pps}{code}{match["after"]}'

    src = MD_RE.sub(_md_match, src)
    return src, errors


def format_file(
    filename: str,
    black_mode: black.FileMode,
    skip_errors: bool,
) -> int:
    with open(filename, encoding='UTF-8') as f:
        contents = f.read()
    new_contents, errors = format_str(contents, black_mode)
    for error in errors:
        lineno = contents[: error.offset].count('\n') + 1
        print(f'{filename}:{lineno}: code block parse error {error.exc}')
    if errors and not skip_errors:
        return 1
    if contents != new_contents:
        print(f'{filename}: Rewriting...')
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write(new_contents)
        return 1
    else:
        return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-l',
        '--line-length',
        type=int,
        default=black.DEFAULT_LINE_LENGTH,
    )
    parser.add_argument(
        '-t',
        '--target-version',
        action='append',
        type=lambda v: black.TargetVersion[v.upper()],
        default=[],
        help=f'choices: {[v.name.lower() for v in black.TargetVersion]}',
        dest='target_versions',
    )
    parser.add_argument(
        '-S',
        '--skip-string-normalization',
        action='store_true',
    )
    parser.add_argument('-E', '--skip-errors', action='store_true')
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    black_mode = black.FileMode(
        target_versions=set(args.target_versions),
        line_length=args.line_length,
        string_normalization=not args.skip_string_normalization,
        # is_ipynb=True,
        # python_cell_magics={'timeit'},
    )

    retv = 0
    for filename in args.filenames:
        retv |= format_file(filename, black_mode, skip_errors=args.skip_errors)
    return retv


if __name__ == '__main__':
    raise SystemExit(main())
