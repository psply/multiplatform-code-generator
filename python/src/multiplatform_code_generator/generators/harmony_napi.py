"""
HarmonyOS NAPI Code Generator

Generates HarmonyOS NAPI C++ code and corresponding TypeScript/ArkTS wrapper classes.
"""

from typing import Dict, List, Any
from ..parsers.cpp_parser import ParsedFunction, Parameter
from ..utils.file_manager import FileManager


class HarmonyNapiGenerator:
    """HarmonyOS NAPI code generator."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the generator.
        
        Args:
            config: HarmonyOS-specific configuration
        """
        self.module_name = config.get("module_name", "CppBridge")
        self.namespace = config.get("namespace", "cppbridge")

    async def generate(self, parsed_interface: ParsedFunction, file_manager: FileManager) -> List[str]:
        """
        Generate HarmonyOS NAPI code.
        
        Args:
            parsed_interface: Parsed C++ interface
            file_manager: File manager instance
            
        Returns:
            List of generated file paths
        """
        files = []

        # Generate NAPI C++ code
        napi_cpp_code = self._generate_napi_cpp(parsed_interface)
        napi_cpp_file = f"harmony/src/main/cpp/napi/{parsed_interface.function_name}_napi.cpp"
        await file_manager.write_file(napi_cpp_file, napi_cpp_code)
        files.append(napi_cpp_file)

        # Generate NAPI header file
        napi_header_code = self._generate_napi_header(parsed_interface)
        napi_header_file = f"harmony/src/main/cpp/napi/{parsed_interface.function_name}_napi.h"
        await file_manager.write_file(napi_header_file, napi_header_code)
        files.append(napi_header_file)

        # Generate NAPI module registration file
        module_code = self._generate_napi_module(parsed_interface)
        module_file = "harmony/src/main/cpp/napi/napi_init.cpp"
        await file_manager.write_file(module_file, module_code)
        files.append(module_file)

        # Generate TypeScript declaration file
        ts_declaration_code = self._generate_typescript_declaration(parsed_interface)
        ts_declaration_file = f"harmony/src/main/ets/types/{self.module_name}.d.ts"
        await file_manager.write_file(ts_declaration_file, ts_declaration_code)
        files.append(ts_declaration_file)

        # Generate ArkTS wrapper class
        arkts_code = self._generate_arkts_wrapper(parsed_interface)
        arkts_file = f"harmony/src/main/ets/{self.module_name}.ets"
        await file_manager.write_file(arkts_file, arkts_code)
        files.append(arkts_file)

        # Generate CMakeLists.txt
        cmake_code = self._generate_cmake_lists(parsed_interface)
        cmake_file = "harmony/src/main/cpp/CMakeLists.txt"
        await file_manager.write_file(cmake_file, cmake_code)
        files.append(cmake_file)

        # Generate oh-package.json5
        package_code = self._generate_oh_package(parsed_interface)
        package_file = "harmony/oh-package.json5"
        await file_manager.write_file(package_file, package_code)
        files.append(package_file)

        # Generate build-profile.json5
        build_profile_code = self._generate_build_profile()
        build_profile_file = "harmony/build-profile.json5"
        await file_manager.write_file(build_profile_file, build_profile_code)
        files.append(build_profile_file)

        return files

    def _generate_napi_cpp(self, parsed_interface: ParsedFunction) -> str:
        """Generate NAPI C++ implementation code."""
        function_name = parsed_interface.function_name
        return_type = parsed_interface.return_type
        parameters = parsed_interface.parameters
        namespace = parsed_interface.namespace

        napi_function_name = f"NAPI_{function_name}"
        
        param_conversions = "\n        ".join(
            self._generate_napi_param_conversion(param, i) 
            for i, param in enumerate(parameters)
        )
        param_names = ", ".join(param.name for param in parameters)
        return_conversion = self._generate_napi_return_conversion(return_type)

        return f"""#include "{parsed_interface.function_name}_napi.h"
#include <hilog/log.h>
{f'#include "{namespace}.h"' if namespace else '// Include your C++ header file here'}

using namespace std;

static constexpr unsigned int LOG_PRINT_DOMAIN = 0xFF00;
static constexpr char LOG_TAG[] = "{self.module_name}";

napi_value {napi_function_name}(napi_env env, napi_callback_info info) {{
    OH_LOG_Print(LOG_APP, LOG_INFO, LOG_PRINT_DOMAIN, LOG_TAG, "NAPI {function_name} called");
    
    size_t argc = {len(parameters)};
    napi_value args[{max(len(parameters), 1)}];
    napi_value thisVar = nullptr;
    
    napi_status status = napi_get_cb_info(env, info, &argc, args, &thisVar, nullptr);
    if (status != napi_ok) {{
        napi_throw_error(env, nullptr, "Failed to parse arguments");
        return nullptr;
    }}
    
    if (argc != {len(parameters)}) {{
        napi_throw_error(env, nullptr, "Wrong number of arguments");
        return nullptr;
    }}
    
    try {{
        {param_conversions}
        
        {'' if return_type == 'void' else 'auto result = '}{namespace + '::' if namespace else ''}{function_name}({param_names});
        
        {return_conversion}
    }} catch (const std::exception& e) {{
        OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_PRINT_DOMAIN, LOG_TAG, "Error in {function_name}: %{{public}}s", e.what());
        napi_throw_error(env, nullptr, e.what());
        return nullptr;
    }}
}}"""

    def _generate_napi_header(self, parsed_interface: ParsedFunction) -> str:
        """Generate NAPI header file."""
        function_name = parsed_interface.function_name
        napi_function_name = f"NAPI_{function_name}"
        header_guard = f"{function_name.upper()}_NAPI_H"

        return f"""#ifndef {header_guard}
#define {header_guard}

#include <node_api.h>

/**
 * NAPI wrapper for {function_name}
 */
napi_value {napi_function_name}(napi_env env, napi_callback_info info);

#endif // {header_guard}"""

    def _generate_napi_module(self, parsed_interface: ParsedFunction) -> str:
        """Generate NAPI module registration file."""
        function_name = parsed_interface.function_name
        napi_function_name = f"NAPI_{function_name}"

        return f"""#include "napi/native_api.h"
#include "{parsed_interface.function_name}_napi.h"

static napi_value Init(napi_env env, napi_value exports) {{
    napi_property_descriptor desc[] = {{
        {{ "{function_name}", nullptr, {napi_function_name}, nullptr, nullptr, nullptr, napi_default, nullptr }}
    }};
    
    napi_status status = napi_define_properties(env, exports, sizeof(desc) / sizeof(desc[0]), desc);
    if (status != napi_ok) {{
        return nullptr;
    }}
    
    return exports;
}}

static napi_module demoModule = {{
    .nm_version = 1,
    .nm_flags = 0,
    .nm_filename = nullptr,
    .nm_register_func = Init,
    .nm_modname = "{self.module_name}",
    .nm_priv = ((void*)0),
    .reserved = {{ 0 }},
}};

extern "C" __attribute__((constructor)) void RegisterModule(void) {{
    napi_module_register(&demoModule);
}}"""

    def _generate_typescript_declaration(self, parsed_interface: ParsedFunction) -> str:
        """Generate TypeScript declaration file."""
        function_name = parsed_interface.function_name
        return_type = parsed_interface.return_type
        parameters = parsed_interface.parameters

        ts_return_type = self._get_typescript_type(return_type)
        
        param_declarations = ", ".join(
            f"{param.name}: {self._get_typescript_type(param.type)}" 
            for param in parameters
        )

        return f"""/**
 * TypeScript declaration for {self.module_name}
 * Generated automatically - do not modify
 */

declare namespace {self.namespace} {{
  /**
   * {function_name} function
   */
  function {function_name}({param_declarations}): {ts_return_type};
}}

export = {self.namespace};"""

    def _generate_arkts_wrapper(self, parsed_interface: ParsedFunction) -> str:
        """Generate ArkTS wrapper class."""
        function_name = parsed_interface.function_name
        return_type = parsed_interface.return_type
        parameters = parsed_interface.parameters

        ts_return_type = self._get_typescript_type(return_type)
        
        param_declarations = ", ".join(
            f"{param.name}: {self._get_typescript_type(param.type)}" 
            for param in parameters
        )

        param_names = ", ".join(param.name for param in parameters)

        return f"""/**
 * ArkTS wrapper for {function_name}
 * Generated automatically - do not modify
 */

import {self.module_name} from 'lib{self.module_name.lower()}.so';

export class {self._capitalize_first_letter(function_name)}Bridge {{
  
  /**
   * Call the native {function_name} function
   */
  static {function_name}({param_declarations}): {ts_return_type} {{
    try {{
      {'' if return_type == 'void' else 'return '}{self.module_name}.{function_name}({param_names});
    }} catch (error) {{
      console.error(`Error calling {function_name}: ${{error}}`);
      {'' if return_type == 'void' else 'throw error;'}
    }}
  }}
  
  /**
   * Async version of {function_name}
   */
  static async {function_name}Async({param_declarations}): Promise<{ts_return_type}> {{
    return new Promise((resolve, reject) => {{
      try {{
        const result = this.{function_name}({param_names});
        resolve(result);
      }} catch (error) {{
        reject(error);
      }}
    }});
  }}
}}

/**
 * Default export for convenience
 */
export default {self._capitalize_first_letter(function_name)}Bridge;

/**
 * Namespace export
 */
export namespace {self._capitalize_first_letter(function_name)} {{
  export const bridge = {self._capitalize_first_letter(function_name)}Bridge;
  
  export function {function_name}({param_declarations}): {ts_return_type} {{
    return bridge.{function_name}({param_names});
  }}
  
  export function {function_name}Async({param_declarations}): Promise<{ts_return_type}> {{
    return bridge.{function_name}Async({param_names});
  }}
}}"""

    def _generate_cmake_lists(self, parsed_interface: ParsedFunction) -> str:
        """Generate CMakeLists.txt."""
        function_name = parsed_interface.function_name
        library_name = self.module_name.lower()

        return f"""cmake_minimum_required(VERSION 3.16)
project({self.module_name})

set(NATIVERENDER_ROOT_PATH ${{CMAKE_CURRENT_SOURCE_DIR}})

if(DEFINED PACKAGE_FIND_FILE)
    include(${{PACKAGE_FIND_FILE}})
endif()

include_directories(${{NATIVERENDER_ROOT_PATH}}
                    ${{NATIVERENDER_ROOT_PATH}}/include)

add_library({library_name} SHARED
    napi/napi_init.cpp
    napi/{function_name}_napi.cpp
    # Add your C++ source files here
)

target_link_libraries({library_name} PUBLIC libace_napi.z.so libhilog_ndk.z.so)"""

    def _generate_oh_package(self, parsed_interface: ParsedFunction) -> str:
        """Generate oh-package.json5."""
        return f"""{{
  "name": "{self.module_name.lower()}",
  "version": "1.0.0",
  "description": "Native {parsed_interface.function_name} bridge for HarmonyOS",
  "main": "index.ets",
  "author": "Generated Code",
  "license": "MIT",
  "dependencies": {{}}
}}"""

    def _generate_build_profile(self) -> str:
        """Generate build-profile.json5."""
        return """{
  "apiType": 'stageMode',
  "targets": [
    {
      "name": "default",
      "runtimeOS": "HarmonyOS"
    }
  ]
}"""

    def _generate_napi_param_conversion(self, param: Parameter, index: int) -> str:
        """Generate NAPI parameter conversion code."""
        param_type = param.type
        param_name = param.name
        
        if param_type == 'boolean':
            return f"""// Convert boolean parameter
        bool {param_name};
        napi_get_value_bool(env, args[{index}], &{param_name});"""
        
        elif param_type == 'int':
            return f"""// Convert int parameter
        int32_t {param_name};
        napi_get_value_int32(env, args[{index}], &{param_name});"""
        
        elif param_type == 'long':
            return f"""// Convert long parameter
        int64_t {param_name};
        napi_get_value_int64(env, args[{index}], &{param_name});"""
        
        elif param_type == 'float':
            return f"""// Convert float parameter
        double {param_name}_double;
        napi_get_value_double(env, args[{index}], &{param_name}_double);
        float {param_name} = static_cast<float>({param_name}_double);"""
        
        elif param_type == 'double':
            return f"""// Convert double parameter
        double {param_name};
        napi_get_value_double(env, args[{index}], &{param_name});"""
        
        elif param_type == 'string':
            return f"""// Convert string parameter
        size_t {param_name}_len = 0;
        napi_get_value_string_utf8(env, args[{index}], nullptr, 0, &{param_name}_len);
        char* {param_name}_buffer = new char[{param_name}_len + 1];
        napi_get_value_string_utf8(env, args[{index}], {param_name}_buffer, {param_name}_len + 1, &{param_name}_len);
        std::string {param_name}({param_name}_buffer);
        delete[] {param_name}_buffer;"""
        
        else:
            return f"// TODO: Handle {param_type} parameter conversion for {param_name}"

    def _generate_napi_return_conversion(self, return_type: str) -> str:
        """Generate NAPI return value conversion code."""
        if return_type == 'void':
            return '        return nullptr;'
        
        elif return_type == 'boolean':
            return """        napi_value napiResult;
        napi_get_boolean(env, result, &napiResult);
        return napiResult;"""
        
        elif return_type == 'int':
            return """        napi_value napiResult;
        napi_create_int32(env, result, &napiResult);
        return napiResult;"""
        
        elif return_type == 'long':
            return """        napi_value napiResult;
        napi_create_int64(env, result, &napiResult);
        return napiResult;"""
        
        elif return_type in ['float', 'double']:
            return """        napi_value napiResult;
        napi_create_double(env, result, &napiResult);
        return napiResult;"""
        
        elif return_type == 'string':
            return """        napi_value napiResult;
        napi_create_string_utf8(env, result.c_str(), NAPI_AUTO_LENGTH, &napiResult);
        return napiResult;"""
        
        else:
            return '        // TODO: Handle return type conversion\n        return nullptr;'

    def _get_typescript_type(self, cpp_type: str) -> str:
        """Get TypeScript type."""
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

    def _capitalize_first_letter(self, string: str) -> str:
        """Capitalize first letter."""
        return string[0].upper() + string[1:] if string else ""
