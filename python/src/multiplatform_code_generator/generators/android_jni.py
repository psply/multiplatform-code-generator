"""
Android JNI Code Generator

Generates JNI C++ code and corresponding Java/Kotlin wrapper classes.
"""

from typing import Dict, List, Any
from ..parsers.cpp_parser import ParsedFunction, Parameter
from ..utils.file_manager import FileManager


class AndroidJniGenerator:
    """Android JNI code generator."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the generator.
        
        Args:
            config: Android-specific configuration
        """
        self.package_name = config["package_name"]
        self.class_name = config["class_name"]
        self.language = config.get("language", "java")

    async def generate(self, parsed_interface: ParsedFunction, file_manager: FileManager) -> List[str]:
        """
        Generate Android JNI code.
        
        Args:
            parsed_interface: Parsed C++ interface
            file_manager: File manager instance
            
        Returns:
            List of generated file paths
        """
        files = []

        # Generate JNI C++ code
        jni_cpp_code = self._generate_jni_cpp(parsed_interface)
        jni_cpp_file = f"android/jni/{parsed_interface.function_name}_jni.cpp"
        await file_manager.write_file(jni_cpp_file, jni_cpp_code)
        files.append(jni_cpp_file)

        # Generate JNI header file
        jni_header_code = self._generate_jni_header(parsed_interface)
        jni_header_file = f"android/jni/{parsed_interface.function_name}_jni.h"
        await file_manager.write_file(jni_header_file, jni_header_code)
        files.append(jni_header_file)

        # Generate Java/Kotlin wrapper class
        if self.language == "kotlin":
            kotlin_code = self._generate_kotlin_wrapper(parsed_interface)
            kotlin_file = f"android/src/main/kotlin/{self.package_name.replace('.', '/')}/{self.class_name}.kt"
            await file_manager.write_file(kotlin_file, kotlin_code)
            files.append(kotlin_file)
        else:
            java_code = self._generate_java_wrapper(parsed_interface)
            java_file = f"android/src/main/java/{self.package_name.replace('.', '/')}/{self.class_name}.java"
            await file_manager.write_file(java_file, java_code)
            files.append(java_file)

        # Generate CMakeLists.txt
        cmake_code = self._generate_cmake_lists(parsed_interface)
        cmake_file = "android/jni/CMakeLists.txt"
        await file_manager.write_file(cmake_file, cmake_code)
        files.append(cmake_file)

        # Generate build.gradle configuration
        gradle_code = self._generate_gradle_config()
        gradle_file = "android/build.gradle.jni"
        await file_manager.write_file(gradle_file, gradle_code)
        files.append(gradle_file)

        return files

    def _generate_jni_cpp(self, parsed_interface: ParsedFunction) -> str:
        """Generate JNI C++ implementation code."""
        function_name = parsed_interface.function_name
        return_type = parsed_interface.return_type
        parameters = parsed_interface.parameters
        namespace = parsed_interface.namespace

        jni_function_name = self._get_jni_function_name(function_name)
        jni_return_type = self._get_jni_type(return_type)
        
        param_declarations = ", ".join(
            f"{self._get_jni_type(param.type)} {param.name}" 
            for param in parameters
        )

        param_conversions = "\n    ".join(
            self._generate_param_conversion(param) 
            for param in parameters
        )

        param_names = ", ".join(param.name for param in parameters)
        return_conversion = self._generate_return_conversion(return_type)

        return f"""#include <jni.h>
#include "{parsed_interface.function_name}_jni.h"
{f'#include "{namespace}.h"' if namespace else '// Include your C++ header file here'}

extern "C" {{

JNIEXPORT {jni_return_type} JNICALL
{jni_function_name}(JNIEnv *env, jobject thiz{', ' + param_declarations if param_declarations else ''}) {{
    {param_conversions}
    
    try {{
        {'' if return_type == 'void' else 'auto result = '}{namespace + '::' if namespace else ''}{function_name}({param_names});
        {return_conversion}
    }} catch (const std::exception& e) {{
        // Throw Java exception
        jclass exceptionClass = env->FindClass("java/lang/RuntimeException");
        env->ThrowNew(exceptionClass, e.what());
        {('return;' if return_type == 'void' else f'return {self._get_default_value(return_type)};')}
    }}
}}

}} // extern "C" """

    def _generate_jni_header(self, parsed_interface: ParsedFunction) -> str:
        """Generate JNI header file."""
        function_name = parsed_interface.function_name
        return_type = parsed_interface.return_type
        parameters = parsed_interface.parameters

        jni_function_name = self._get_jni_function_name(function_name)
        jni_return_type = self._get_jni_type(return_type)
        
        param_declarations = ", ".join(
            f"{self._get_jni_type(param.type)} {param.name}" 
            for param in parameters
        )

        header_guard = f"{function_name.upper()}_JNI_H"

        return f"""#ifndef {header_guard}
#define {header_guard}

#include <jni.h>

extern "C" {{

/**
 * JNI wrapper for {function_name}
 */
JNIEXPORT {jni_return_type} JNICALL
{jni_function_name}(JNIEnv *env, jobject thiz{', ' + param_declarations if param_declarations else ''});

}} // extern "C"

#endif // {header_guard}"""

    def _generate_java_wrapper(self, parsed_interface: ParsedFunction) -> str:
        """Generate Java wrapper class."""
        function_name = parsed_interface.function_name
        return_type = parsed_interface.return_type
        parameters = parsed_interface.parameters

        java_return_type = self._get_java_type(return_type)
        
        param_declarations = ", ".join(
            f"{self._get_java_type(param.type)} {param.name}" 
            for param in parameters
        )

        param_names = ", ".join(param.name for param in parameters)

        return f"""package {self.package_name};

/**
 * JNI wrapper class for {function_name}
 * Generated automatically - do not modify
 */
public class {self.class_name} {{
    
    static {{
        System.loadLibrary("{self.class_name.lower()}");
    }}
    
    /**
     * Native method declaration
     */
    private native {java_return_type} {function_name}Native({param_declarations});
    
    /**
     * Public wrapper method
     */
    public {java_return_type} {function_name}({param_declarations}) {{
        {'' if return_type == 'void' else 'return '}{function_name}Native({param_names});
    }}
}}"""

    def _generate_kotlin_wrapper(self, parsed_interface: ParsedFunction) -> str:
        """Generate Kotlin wrapper class."""
        function_name = parsed_interface.function_name
        return_type = parsed_interface.return_type
        parameters = parsed_interface.parameters

        kotlin_return_type = self._get_kotlin_type(return_type)
        
        param_declarations = ", ".join(
            f"{param.name}: {self._get_kotlin_type(param.type)}" 
            for param in parameters
        )

        param_names = ", ".join(param.name for param in parameters)

        return f"""package {self.package_name}

/**
 * JNI wrapper class for {function_name}
 * Generated automatically - do not modify
 */
class {self.class_name} {{
    
    companion object {{
        init {{
            System.loadLibrary("{self.class_name.lower()}")
        }}
    }}
    
    /**
     * Native method declaration
     */
    private external fun {function_name}Native({param_declarations}): {kotlin_return_type}
    
    /**
     * Public wrapper method
     */
    fun {function_name}({param_declarations}): {kotlin_return_type} {{
        {'' if return_type == 'void' else 'return '}{function_name}Native({param_names})
    }}
}}"""

    def _generate_cmake_lists(self, parsed_interface: ParsedFunction) -> str:
        """Generate CMakeLists.txt."""
        function_name = parsed_interface.function_name
        library_name = self.class_name.lower()

        return f"""cmake_minimum_required(VERSION 3.10.2)

project("{library_name}")

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)

# Add library
add_library({library_name} SHARED
    {function_name}_jni.cpp
    # Add your C++ source files here
)

# Find required packages
find_library(log-lib log)

# Link libraries
target_link_libraries({library_name}
    ${{log-lib}}
    # Add other libraries you need to link here
)

# Include directories
target_include_directories({library_name} PRIVATE
    .
    # Add your header file directories here
)"""

    def _generate_gradle_config(self) -> str:
        """Generate Gradle configuration."""
        return """// Add to your app/build.gradle file

android {
    compileSdk 33

    defaultConfig {
        minSdk 21
        targetSdk 33

        ndk {
            abiFilters 'arm64-v8a', 'armeabi-v7a', 'x86', 'x86_64'
        }
    }

    externalNativeBuild {
        cmake {
            path "src/main/cpp/CMakeLists.txt"
            version "3.10.2"
        }
    }
}

dependencies {
    // Add your dependencies here
}"""

    def _get_jni_function_name(self, function_name: str) -> str:
        """Get JNI function name."""
        package_path = self.package_name.replace('.', '_')
        return f"Java_{package_path}_{self.class_name}_{function_name}Native"

    def _get_jni_type(self, cpp_type: str) -> str:
        """Get JNI type."""
        jni_type_mapping = {
            'void': 'void',
            'boolean': 'jboolean',
            'byte': 'jbyte',
            'short': 'jshort',
            'int': 'jint',
            'long': 'jlong',
            'float': 'jfloat',
            'double': 'jdouble',
            'string': 'jstring'
        }
        return jni_type_mapping.get(cpp_type, 'jobject')

    def _get_java_type(self, cpp_type: str) -> str:
        """Get Java type."""
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

    def _get_kotlin_type(self, cpp_type: str) -> str:
        """Get Kotlin type."""
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

    def _generate_param_conversion(self, param: Parameter) -> str:
        """Generate parameter conversion code."""
        if param.type == 'string':
            return f"""// Convert jstring to std::string
    const char* {param.name}_chars = env->GetStringUTFChars({param.name}, nullptr);
    std::string {param.name}_cpp({param.name}_chars);
    env->ReleaseStringUTFChars({param.name}, {param.name}_chars);"""
        else:
            return f"// {param.name} can be used directly as {param.type}"

    def _generate_return_conversion(self, return_type: str) -> str:
        """Generate return value conversion code."""
        if return_type == 'void':
            return ''
        elif return_type == 'string':
            return '        return env->NewStringUTF(result.c_str());'
        else:
            return '        return result;'

    def _get_default_value(self, type_name: str) -> str:
        """Get default value for type."""
        default_values = {
            'boolean': 'false',
            'byte': '0',
            'short': '0',
            'int': '0',
            'long': '0L',
            'float': '0.0f',
            'double': '0.0',
            'string': 'nullptr'
        }
        return default_values.get(type_name, 'nullptr')
