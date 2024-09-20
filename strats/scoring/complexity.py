import ast
import re

def score(src: str) -> int:
    return score_ast(ast.parse(src))

def score_ast(node: ast.AST):

    def recurse(iterable):
        return sum(map(score_ast, iterable))

    match node:
        case None:
            return 0
        case ast.Module():
            return 1 + recurse(node.body)
        case ast.Expression():
            return 1 + score_ast(node.body)
        case ast.Constant():
            if isinstance(node.value, str):
                return len(re.findall(r"\b\S+?\b", node.value))
            return 1
        case ast.FormattedValue():
            return 1 + score_ast(node.value)
        case ast.JoinedStr():
            return 1 + recurse(node.values)
        case ast.List() | ast.Tuple() | ast.Set():
            return 1 + recurse(node.elts)
        case ast.Dict():
            return 1 + recurse(node.keys + node.values)
        case ast.Name() | ast.Starred():
            return 1
        case ast.Expr():
            return 1 + score_ast(node.value)
        case ast.UnaryOp():
            return 1 + score_ast(node.operand)
        case ast.BinOp():
            return 1 + score_ast(node.left) + score_ast(node.right)
        case ast.BoolOp():
            return 1 + recurse(node.values)
        case ast.Compare():
            return 1 + score_ast(node.left) + recurse(node.comparators)
        case ast.Call():
            return 1 + score_ast(node.func) + recurse(node.args + node.keywords) 
        case ast.keyword():
            return 1 + score_ast(node.value)
        case ast.IfExp():
            return 1 + recurse([node.test, node.body, node.orelse])
        case ast.Attribute():
            return 1 + score_ast(node.value)
        case ast.NamedExpr():
            return 1 + score_ast(node.target) + score_ast(node.value)
        case ast.Subscript():
            return 1 + score_ast(node.value) + score_ast(node.slice)
        case ast.Slice():
            return 1 + recurse([node.lower, node.upper, node.step])
        case ast.ListComp() | ast.SetComp() | ast.GeneratorExp():
            return 1 + score_ast(node.elt) + recurse(node.generators)
        case ast.DictComp():
            return 1 + score_ast(node.key) + score_ast(node.value) + recurse(node.generators)
        case ast.comprehension():
            return 1 + score_ast(node.target) + score_ast(node.iter) + recurse(node.ifs)
        case ast.Assign():
            return 1 + recurse(node.targets) + score_ast(node.value)
        case ast.AnnAssign():
            return 1 + score_ast(node.target) + score_ast(node.value)
        case ast.AugAssign():
            return 1 + score_ast(node.target) + score_ast(node.value)
        case ast.Raise():
            return 1 + score_ast(node.exc) + score_ast(node.cause)
        case ast.Assert():
            # asserts should be free, but not if they modify state
            if any(isinstance(child, ast.Call) for child in ast.walk(node.test)):
                return score_ast(node.test)
            return 0
        case ast.Delete():
            return 1 + recurse(node.targets)
        case ast.Pass():
            return 1
        case ast.Import() | ast.ImportFrom():
            return 1 + recurse(node.names)
        case ast.alias():
            return 1
        case ast.If():
            return 1 + score_ast(node.test) + recurse(node.body + node.orelse)
        case ast.For() | ast.AsyncFor():
            return 1 + score_ast(node.target) + score_ast(node.iter) + recurse(node.body + node.orelse)
        case ast.While():
            return 1 + score_ast(node.test) + recurse(node.body + node.orelse)
        case ast.Break() | ast.Continue():
            return 1
        case ast.Try() | ast.TryStar():
            return 1 + recurse(node.body + node.handlers + node.orelse + node.finalbody)
        case ast.ExceptHandler():
            return 1 + score_ast(node.type) + recurse(node.body)
        case ast.With() | ast.AsyncWith():
            return 1 + recurse(node.items + node.body)
        case ast.withitem():
            return 1 + score_ast(node.context_expr)
        case ast.Match():
            return 1 + score_ast(node.subject) + recurse(node.cases)
        case ast.match_case():
            return 1 + score_ast(node.pattern) + score_ast(node.guard) + recurse(node.body)
        case ast.MatchValue() | ast.MatchSingleton():
            return 1 + score_ast(node.value)
        case ast.MatchSequence():
            return 1 + recurse(node.patterns)
        case ast.MatchStar():
            return 1
        case ast.MatchMapping():
            return 1 + recurse(node.keys + node.patterns)
        case ast.MatchClass():
            return 1 + score_ast(node.cls) + recurse(node.kwd_attrs + node.kwd_patterns)
        case ast.MatchAs():
            return 1
        case ast.MatchOr():
            return 1 + recurse(node.patterns)
        case ast.FunctionDef() | ast.AsyncFunctionDef():
            return 1 + score_ast(node.args) + recurse(node.body)
        case ast.Lambda():
            return 1 + score_ast(node.args) + score_ast(node.body)
        case ast.arguments():
            return 1 + recurse(node.posonlyargs + node.args + node.kwonlyargs)
        case ast.arg():
            return 1
        case ast.Return() | ast.Yield() | ast.YieldFrom() | ast.Await():
            return 1 + score_ast(node.value)
        case ast.Global() | ast.Nonlocal():
            return 0
        case ast.ClassDef():
            return recurse(node.body)
        case _:
            try:
                return recurse(node)
            except:
                print(f"WARNING: Unrecognised node type {type(node).__qualname__}!")
                return 1