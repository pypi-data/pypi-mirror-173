"""
yasp: Yet-another Apertium stream parser
"""
import re
from typing import Any, Generator, Tuple, TypedDict, Union
from parsec import generate, string, regex, many, joint


@generate
def stream_format() -> Generator[Any, str, Tuple[str, str]]:
    """
    Stream format parser
    """
    val = yield string("[") >> regex(r"(\\\]|\\\[|[^\[^\]])+") << string("]")
    return ("FORMAT", re.sub(r"\\([\[\]])", r"\1", val))


@generate
def ling_form_chars() -> Generator[Any, str, str]:
    """
    Form characters parser
    """
    val = yield regex(
        r"([^^^$^@^*^/^<^>^{^}^\\^[^\]^#^+]|\\\^|\\\$"
        + r"|\\@|\\\*|\\/|\\<|\\>|\\{|\\}|\\\\|\\\[|\\\]|\\\#|\\\+)+"
    )
    return re.sub(
        r"\\([\\\^|\\\$|\\@|\\\*|\\/|\\<|\\>" +
        r"|\\{|\\}|\\\\|\\\[|\\\]|\\#|\\\+])",
        r"\1",
        val,
    )


@generate
def tag() -> Generator[Any, str, str]:
    """
    Tag parser
    """
    val = yield string("<") >> regex(r"[^<^>]+") << string(">")
    return val


@generate
def flag() -> Generator[Any, str, str]:
    """
    Flag parser
    """
    val = yield regex(r"(\*|\#|@)?")
    return val


@generate
def ling_form() -> Generator[Any, str, str]:
    """
    Linguistic form parser
    """
    val = yield ling_form_chars
    return val


@generate
def sub_invariable_part() -> Generator[Any, str, str]:
    """
    Sub invariable part parser
    """
    val = yield string("#") >> ling_form_chars
    return val


@generate
def invariable_part() -> Generator[Any, list[str], list[str]]:
    """
    Invariable part parser
    """
    val = yield many(sub_invariable_part)
    return val


@generate
def tags() -> Generator[Any, list[str], list[str]]:
    """
    Tags parser
    """
    val = yield many(tag)
    return val


SubLu = TypedDict(
    "SubLu",
    {
        "FLAG": str,
        "LING-FORM": str,
        "INVARIABLE-PART0": list[str],
        "TAGS": list[str],
        "INVARIABLE-PART1": list[str],
    },
)


@generate
def sub_lu() -> Generator[
    Any, Tuple[str, str, list[str], list[str], list[str]], SubLu
]:
    """
    Sub lexical unit parser
    """
    val = yield joint(flag, ling_form, invariable_part, tags, invariable_part)
    return {
        "FLAG": val[0],
        "LING-FORM": val[1],
        "INVARIABLE-PART0": val[2],
        "TAGS": val[3],
        "INVARIABLE-PART1": val[4],
    }


@generate
def sub_lus() -> Generator[Any, Tuple[SubLu, list[SubLu]], list[SubLu]]:
    """
    Sub-lexical units parser
    """
    val = yield joint(sub_lu, many(string("/") >> sub_lu))
    sub_lu0 = val[0]
    buf = []
    buf.append(sub_lu0)
    if len(val) > 1:
        for another_sub_lu in val[1]:
            buf.append(another_sub_lu)
    return buf


@generate
def basic_lu() -> Generator[Any, list[SubLu], Tuple[str, list[SubLu]]]:
    """
    Basic lexical unit parser
    """
    val = yield string("^") >> sub_lus << string("$")
    return ("LEXICAL-UNIT", val)


@generate
def joined_sub_lus() -> Generator[
        Any, Tuple[list[SubLu], list[list[SubLu]]], list[list[SubLu]]]:
    """
    Joined sub lexical units parser
    """
    val = yield sub_lus + many(string("+") >> sub_lus)
    buf = []
    buf.append(val[0])
    if len(val) > 1:
        for another_sub_lu in val[1]:
            buf.append(another_sub_lu)
    return buf


@generate
def joined_lu() -> Generator[
        Any, list[list[SubLu]], Tuple[str, list[list[SubLu]]]]:
    """
    Joined lexica unit parser
    """
    val = yield string("^") >> joined_sub_lus << string("$")
    return ("JOINED-LEXICAL-UNIT", val)


@generate
def unparsed() -> Generator[Any, str, Tuple[str, str]]:
    """
    Unparsed unit parser
    """
    val = yield regex(r"[^[^\]^^^$^{^}]+")
    return ("UNPARSED", val)


ChunkItem = Union[Tuple[str, str],
                  Tuple[str, list[SubLu]],
                  Tuple[str, list[list[SubLu]]]]


ChunkItems = list[ChunkItem]


@generate
def chunk_children() -> Generator[Any, ChunkItems, ChunkItems]:
    """
    Chunk children parser
    """
    val = (
        yield string("{")
        >> many((unparsed ^ stream_format ^ basic_lu ^ joined_lu))
        << string("}")
    )
    return val


Chunk = TypedDict("Chunk", {"HEAD": SubLu, "CHILDREN": ChunkItems})


@generate
def chunk() -> Generator[Any, Tuple[SubLu, ChunkItems], Tuple[str, Chunk]]:
    """
    Chunk parser
    """
    head, children = yield sub_lu + chunk_children
    return ("CHUNK", dict(HEAD=head, CHILDREN=children))


stream_unit = unparsed ^ stream_format ^ basic_lu ^ joined_lu ^ chunk
stream = many(stream_unit)
