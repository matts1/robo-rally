# extends with parameters
# modified version of this: http://djangosnippets.org/snippets/447/
# usage:
# {% xextends "some.html" %}
# {% xextends "some.html" with title="title1" %}
# {% xextends "some.html" with title="title2"|capfirst %}

from django import template
from django.template.loader_tags import do_extends
import tokenize
import StringIO

register = template.Library()

class XExtendsNode(template.Node):
    def __init__(self, node, kwargs):
        self.node = node
        self.kwargs = kwargs

    def render(self, context):
        context.update(self.kwargs)
        try:
            return self.node.render(context)
        finally:
            context.pop()

def do_xextends(parser, token):
    bits = token.contents.split()
    kwargs = {}
    if 'with' in bits:
        pos = bits.index('with')
        argslist = bits[pos+1:]
        i = 0
        while i < len(argslist):
            if argslist[i].count('"') % 2 or argslist[i].count("'") % 2:
                argslist[i] += " " + argslist[i + 1]
                argslist.pop(i + 1)
            else:
                i += 1
        bits = bits[:pos]

        for i in argslist:
            try:
                a, b = i.split('=', 1); a = a.strip(); b = b.strip()
                keys = list(tokenize.generate_tokens(StringIO.StringIO(a).readline))
                if keys[0][0] == tokenize.NAME:
                    kwargs[str(a)] = eval(b)
                else: raise ValueError
            except ValueError:
                raise template.TemplateSyntaxError, 'Argument syntax wrong: should be key=value'
            # before we are done, remove the argument part from the token contents,
        # or django's extends tag won't be able to handle it.
        token.contents = " ".join(bits)

    # let the orginal do_extends parse the tag, and wrap the ExtendsNode
    return XExtendsNode(do_extends(parser, token), kwargs)

register.tag('xextends', do_xextends)
