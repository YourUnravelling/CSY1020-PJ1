import ast, pathlib
root = pathlib.Path('.')
for p in root.rglob('*.py'):
    try:
        tree = ast.parse(p.read_text(encoding='utf8'))
    except Exception as e:
        print(p, 'PARSE_ERROR', e); continue
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                print(p, 'import', n.name)
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ''
            print(p, 'from', '.'*node.level + mod, 'import', ','.join(n.name for n in node.names))