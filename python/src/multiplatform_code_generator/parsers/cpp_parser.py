"""
C++ Interface Parser

Parses C++ function declarations and extracts function information.
"""

import re
from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class Parameter:
    """Represents a function parameter."""
    type: str
    name: str
    is_const: bool = False
    is_pointer: bool = False
    is_reference: bool = False
    default_value: Optional[str] = None


@dataclass
class ParsedFunction:
    """Represents a parsed C++ function."""
    function_name: str
    return_type: str
    parameters: List[Parameter]
    namespace: Optional[str] = None
    is_static: bool = False
    is_virtual: bool = False
    is_const: bool = False
    original_code: str = ""


class CppInterfaceParser:
    """C++ interface parser for extracting function information."""

    def __init__(self):
        """Initialize the parser."""
        # C++ type mappings to common types
        self.type_mapping = {
            'void': 'void',
            'bool': 'boolean',
            'char': 'byte',
            'unsigned char': 'byte',
            'short': 'short',
            'unsigned short': 'short',
            'int': 'int',
            'unsigned int': 'int',
            'long': 'long',
            'unsigned long': 'long',
            'long long': 'long',
            'float': 'float',
            'double': 'double',
            'char*': 'string',
            'const char*': 'string',
            'std::string': 'string',
            'string': 'string'
        }

    def parse(self, cpp_code: str) -> ParsedFunction:
        """
        Parse C++ interface function.
        
        Args:
            cpp_code: C++ function code
            
        Returns:
            ParsedFunction: Parsed function information
            
        Raises:
            ValueError: If parsing fails
        """
        try:
            # Clean the code
            clean_code = self._clean_code(cpp_code)
            
            # Extract namespace
            namespace = self._extract_namespace(clean_code)
            
            # Extract function information
            function_info = self._extract_function_info(clean_code)
            
            return ParsedFunction(
                function_name=function_info["name"],
                return_type=function_info["return_type"],
                parameters=function_info["parameters"],
                namespace=namespace,
                is_static=function_info["is_static"],
                is_virtual=function_info["is_virtual"],
                is_const=function_info["is_const"],
                original_code=cpp_code.strip()
            )
        except Exception as e:
            raise ValueError(f"Failed to parse C++ interface: {e}")

    def _clean_code(self, code: str) -> str:
        """Clean the code by removing comments and extra whitespace."""
        # Remove single-line comments
        code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
        # Remove multi-line comments
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        # Remove extra whitespace
        code = re.sub(r'\s+', ' ', code).strip()
        return code

    def _extract_namespace(self, code: str) -> Optional[str]:
        """Extract namespace from code."""
        namespace_match = re.search(r'namespace\s+([a-zA-Z_][a-zA-Z0-9_]*)', code)
        return namespace_match.group(1) if namespace_match else None

    def _extract_function_info(self, code: str) -> Dict[str, Any]:
        """Extract function information from code."""
        # Match function declaration
        function_regex = (
            r'(?:(static|virtual|inline)\s+)?'
            r'(?:(static|virtual|inline)\s+)?'
            r'([a-zA-Z_][a-zA-Z0-9_:*&<>\s]*)\s+'
            r'([a-zA-Z_][a-zA-Z0-9_]*)\s*'
            r'\(([^)]*)\)\s*'
            r'(?:(const)\s*)?'
            r'(?:;|{)'
        )
        
        match = re.search(function_regex, code)
        if not match:
            raise ValueError('Could not parse function declaration')

        modifier1, modifier2, return_type, function_name, param_str, const_modifier = match.groups()
        
        # Parse modifiers
        modifiers = [m for m in [modifier1, modifier2] if m]
        is_static = 'static' in modifiers
        is_virtual = 'virtual' in modifiers
        is_const = bool(const_modifier)

        # Parse parameters
        parameters = self._parse_parameters(param_str) if param_str else []

        return {
            "name": function_name,
            "return_type": self._normalize_type(return_type.strip()),
            "parameters": parameters,
            "is_static": is_static,
            "is_virtual": is_virtual,
            "is_const": is_const
        }

    def _parse_parameters(self, param_str: str) -> List[Parameter]:
        """Parse function parameters."""
        if not param_str or param_str.strip() == '':
            return []

        parameters = []
        params = self._split_parameters(param_str)

        for param in params:
            param_info = self._parse_parameter(param.strip())
            if param_info:
                parameters.append(param_info)

        return parameters

    def _split_parameters(self, param_str: str) -> List[str]:
        """Split parameter string handling templates and nested structures."""
        params = []
        current = ''
        depth = 0
        in_string = False
        string_char = ''

        for char in param_str:
            if not in_string:
                if char in ['"', "'"]:
                    in_string = True
                    string_char = char
                elif char in ['<', '(']:
                    depth += 1
                elif char in ['>', ')']:
                    depth -= 1
                elif char == ',' and depth == 0:
                    params.append(current.strip())
                    current = ''
                    continue
            elif char == string_char:
                in_string = False

            current += char

        if current.strip():
            params.append(current.strip())

        return params

    def _parse_parameter(self, param: str) -> Optional[Parameter]:
        """Parse a single parameter."""
        if not param:
            return None

        # Match parameter declaration: [const] type [&|*] name [= default_value]
        param_regex = (
            r'(?:(const)\s+)?'
            r'([a-zA-Z_][a-zA-Z0-9_:*&<>\s]*?)'
            r'([*&]?)\s*'
            r'([a-zA-Z_][a-zA-Z0-9_]*)?'
            r'(?:\s*=\s*(.+))?$'
        )
        
        match = re.search(param_regex, param)
        if not match:
            # Try simple type matching
            simple_match = re.search(r'([a-zA-Z_][a-zA-Z0-9_:*&<>\s]*)', param)
            if simple_match:
                return Parameter(
                    type=self._normalize_type(simple_match.group(1).strip()),
                    name=f"param_{id(param) % 10000}",  # Generate random param name
                    is_const=False,
                    is_pointer=False,
                    is_reference=False,
                    default_value=None
                )
            return None

        const_modifier, base_type, ptr_ref, name, default_value = match.groups()

        return Parameter(
            type=self._normalize_type((base_type + (ptr_ref or '')).strip()),
            name=name or f"param_{id(param) % 10000}",
            is_const=bool(const_modifier),
            is_pointer=ptr_ref == '*',
            is_reference=ptr_ref == '&',
            default_value=default_value.strip() if default_value else None
        )

    def _normalize_type(self, type_name: str) -> str:
        """Normalize type name."""
        # Remove extra whitespace
        type_name = re.sub(r'\s+', ' ', type_name).strip()
        
        # Check direct mapping
        if type_name in self.type_mapping:
            return self.type_mapping[type_name]

        # Handle pointer types
        if type_name.endswith('*'):
            base_type = type_name[:-1].strip()
            if base_type in self.type_mapping:
                return self.type_mapping[base_type]

        # Handle const types
        if type_name.startswith('const '):
            base_type = type_name[6:].strip()
            return self._normalize_type(base_type)

        # Handle std:: namespace
        if type_name.startswith('std::'):
            base_type = type_name[5:]
            if base_type in self.type_mapping:
                return self.type_mapping[base_type]

        return type_name

    def get_java_type(self, cpp_type: str) -> str:
        """Get Java type mapping."""
        java_type_mapping = {
            'void': 'void',
            'boolean': 'boolean',
            'byte': 'byte',
            'short': 'short',
            'int': 'int',
            'long': 'long',
            'float': 'float',
            'double': 'double',
            'string': 'String'
        }
        return java_type_mapping.get(cpp_type, 'Object')

    def get_kotlin_type(self, cpp_type: str) -> str:
        """Get Kotlin type mapping."""
        kotlin_type_mapping = {
            'void': 'Unit',
            'boolean': 'Boolean',
            'byte': 'Byte',
            'short': 'Short',
            'int': 'Int',
            'long': 'Long',
            'float': 'Float',
            'double': 'Double',
            'string': 'String'
        }
        return kotlin_type_mapping.get(cpp_type, 'Any')

    def get_objc_type(self, cpp_type: str) -> str:
        """Get Objective-C type mapping."""
        objc_type_mapping = {
            'void': 'void',
            'boolean': 'BOOL',
            'byte': 'char',
            'short': 'short',
            'int': 'int',
            'long': 'long',
            'float': 'float',
            'double': 'double',
            'string': 'NSString*'
        }
        return objc_type_mapping.get(cpp_type, 'id')

    def get_typescript_type(self, cpp_type: str) -> str:
        """Get TypeScript type mapping (for HarmonyOS NAPI)."""
        ts_type_mapping = {
            'void': 'void',
            'boolean': 'boolean',
            'byte': 'number',
            'short': 'number',
            'int': 'number',
            'long': 'number',
            'float': 'number',
            'double': 'number',
            'string': 'string'
        }
        return ts_type_mapping.get(cpp_type, 'any')
