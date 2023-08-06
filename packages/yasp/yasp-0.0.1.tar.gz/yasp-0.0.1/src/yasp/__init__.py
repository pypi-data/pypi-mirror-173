'''
yasp: Yet-another Apertium stream parser
'''
import re
from typing import Any
from parsec import generate, string, regex, many, joint


@generate
def stream_format() -> Any:
    '''
    Stream format parser
    '''
    val = yield string("[") >> regex(r"(\\\]|\\\[|[^\[^\]])+") << string("]")
    return ("FORMAT", re.sub(r"\\([\[\]])", r"\1", val))


@generate
def ling_form_chars() -> Any:
    '''
    Form characters parser
    '''
    val = yield regex(
        r"([^^^$^@^*^/^<^>^{^}^\\^[^\]^#^+]|\\\^|\\\$" +
        r"|\\@|\\\*|\\/|\\<|\\>|\\{|\\}|\\\\|\\\[|\\\]|\\\#|\\\+)+"
    )
    return re.sub(
        r"\\([\\\^|\\\$|\\@|\\\*|\\/|\\<|\\>" +
        r"|\\{|\\}|\\\\|\\\[|\\\]|\\#|\\\+])",
        r"\1",
        val,
    )


@generate
def tag() -> Any:
    '''
    Tag parser
    '''
    val = yield string("<") >> regex(r"[^<^>]+") << string(">")
    return ("TAG", val)


@generate
def flag() -> Any:
    '''
    Flag parser
    '''
    val = yield regex(r"(\*|\#|@)?")
    return ("FLAG", val)


@generate
def ling_form() -> Any:
    '''
    Linguistic form parser
    '''
    val = yield ling_form_chars
    return ("LING-FORM", val)


sub_invariable_part = string("#") >> ling_form_chars


@generate
def invariable_part() -> Any:
    '''
    Invariable part parser
    '''
    val = yield many(sub_invariable_part)
    return ("INVARIABLE-PART", val)


@generate
def tags() -> Any:
    '''
    Tags parser
    '''
    val = yield many(tag)
    return ("TAGS", [i[1] for i in val])


sub_lu = joint(flag, ling_form, invariable_part, tags, invariable_part)


@generate
def sub_lus() -> Any:
    '''
    Sub-lexical units parser
    '''
    val = yield joint(sub_lu, many(string("/") >> sub_lu))
    sub_lu0 = val[0]
    buf = []
    buf.append(sub_lu0)
    if len(val) > 1:
        for another_sub_lu in val[1]:
            buf.append(another_sub_lu)
    return buf


@generate
def basic_lu() -> Any:
    '''
    Basic lexical unit parser
    '''
    val = yield string("^") >> sub_lus << string("$")
    return ("LEXICAL-UNIT", val)


@generate
def joined_sub_lus() -> Any:
    '''
    Joined sub lexical units parser
    '''
    val = yield sub_lus + many(string("+") >> sub_lus)
    buf = []
    buf.append(val[0])
    if len(val) > 1:
        for another_sub_lu in val[1]:
            buf.append(another_sub_lu)
    return buf


@generate
def joined_lu() -> Any:
    '''
    Joined lexica unit parser
    '''
    val = yield string("^") >> joined_sub_lus << string("$")
    return ("JOINED-LEXICAL-UNIT", val)


@generate
def unparsed() -> Any:
    '''
    Unparsed unit parser
    '''
    val = yield regex(r"[^[^\]^^^$^{^}]+")
    return ("UNPARSED", val)


@generate
def chunk_children() -> Any:
    '''
    Chunk children parser
    '''
    val = (
        yield string("{")
        >> many((stream_format | basic_lu | joined_lu | unparsed))
        << string("}")
    )
    return val


@generate
def chunk() -> Any:
    '''
    Chunk parser
    '''
    head, children = yield sub_lu + chunk_children
    return ("CHUNK", dict(HEAD=head, CHILDREN=children))


stream_unit = unparsed ^ stream_format ^ basic_lu ^ joined_lu ^ chunk
stream = many(stream_unit)
