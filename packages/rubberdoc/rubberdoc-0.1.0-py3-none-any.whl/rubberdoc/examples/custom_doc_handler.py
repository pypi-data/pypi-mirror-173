from rubberdoc.doc_handler import BaseDocHandler
from rubberdoc.config_provider import RubberDocConfig
import ast

class CustomDocHandler(BaseDocHandler):
    def __init__(self, file_path: str, config: RubberDocConfig):
        super().__init__(file_path=file_path, config=config)
    
    def __init__(self, file_path: str, config: RubberDocConfig):
        super().__init__(file_path=file_path, config=config)
    
    def process_node(self, level: int, node: ast.ClassDef | ast.FunctionDef, parent=None):
        if parent:
            self.doc.append(self.wrap_func_cls_lbl(parent.name))
        
        # function or class name
        self.doc.append(self.wrap_func_cls_name(level, node))
        
        # here we are adding another step to add the function parameters
        if isinstance(node, ast.FunctionDef):
            self.doc.append(self.wrap_function_params(node))
        
        docstring = self.get_docstring(node)
        source_code = self.get_node_code(node)
        
        self.doc.append(self.wrap_docstring(docstring))
        if self.config.output['include_source_code']:
            self.doc.append(self.wrap_codeblock(source_code))
        self.doc.append('\n---  \n')
    
    def wrap_function_params(self, node: ast.FunctionDef) -> str:
        params = self.get_function_params(node) or ''
        if params:
            params = f"**Params:** `{', '.join(params)}`  \n"
        return params
    
    def wrap_func_cls_lbl(self, parent_name: str):
        """Overriding the default wrapper for a function's class label"""
        return f"<label class='class-label'>{parent_name}</label>  \n"
    
    def wrap_docstring(self, docstring: str) -> str:
        """Overriding the docstring to include tabs (1)"""
        d = '=== "Documentation"\n'
        d += '\n'.join(f"    {d}" for d in docstring.splitlines())
        d += "  \n\n"
        return d
    
    def wrap_codeblock(self, code: str) -> str:
        """Overriding the codeblock to include tabs (2)"""
        c = '=== "Code"\n'
        c += '    ```py\n'
        c += '\n'.join(f"    {l}" for l in code.splitlines())
        c += '\n    ```  \n'
        c += "  \n\n"
        return c
