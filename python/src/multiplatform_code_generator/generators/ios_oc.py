"""
iOS Objective-C Code Generator

Generates Objective-C wrapper classes to call C++ code.
"""

from typing import Dict, List, Any
from ..parsers.cpp_parser import ParsedFunction, Parameter
from ..utils.file_manager import FileManager


class IosOcGenerator:
    """iOS Objective-C code generator."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the generator.
        
        Args:
            config: iOS-specific configuration
        """
        self.class_prefix = config.get("class_prefix", "CPP")
        self.framework_name = config.get("framework_name", "CppBridge")

    async def generate(self, parsed_interface: ParsedFunction, file_manager: FileManager) -> List[str]:
        """
        Generate iOS Objective-C code.
        
        Args:
            parsed_interface: Parsed C++ interface
            file_manager: File manager instance
            
        Returns:
            List of generated file paths
        """
        files = []
        class_name = f"{self.class_prefix}{self._capitalize_first_letter(parsed_interface.function_name)}"

        # Generate Objective-C header file
        header_code = self._generate_objc_header(parsed_interface, class_name)
        header_file = f"ios/{class_name}.h"
        await file_manager.write_file(header_file, header_code)
        files.append(header_file)

        # Generate Objective-C implementation file
        implementation_code = self._generate_objc_implementation(parsed_interface, class_name)
        implementation_file = f"ios/{class_name}.m"
        await file_manager.write_file(implementation_file, implementation_code)
        files.append(implementation_file)

        # Generate C++ bridge header file
        bridge_header_code = self._generate_cpp_bridge_header(parsed_interface, class_name)
        bridge_header_file = f"ios/{class_name}Bridge.hpp"
        await file_manager.write_file(bridge_header_file, bridge_header_code)
        files.append(bridge_header_file)

        # Generate C++ bridge implementation file
        bridge_implementation_code = self._generate_cpp_bridge_implementation(parsed_interface, class_name)
        bridge_implementation_file = f"ios/{class_name}Bridge.cpp"
        await file_manager.write_file(bridge_implementation_file, bridge_implementation_code)
        files.append(bridge_implementation_file)

        # Generate Swift wrapper class (optional)
        swift_code = self._generate_swift_wrapper(parsed_interface, class_name)
        swift_file = f"ios/{class_name}Swift.swift"
        await file_manager.write_file(swift_file, swift_code)
        files.append(swift_file)

        # Generate Podspec file
        podspec_code = self._generate_podspec(parsed_interface)
        podspec_file = f"ios/{self.framework_name}.podspec"
        await file_manager.write_file(podspec_file, podspec_code)
        files.append(podspec_file)

        # Generate Xcode configuration
        xconfig_code = self._generate_xcode_config()
        xconfig_file = "ios/Config.xcconfig"
        await file_manager.write_file(xconfig_file, xconfig_code)
        files.append(xconfig_file)

        return files

    def _generate_objc_header(self, parsed_interface: ParsedFunction, class_name: str) -> str:
        """Generate Objective-C header file."""
        function_name = parsed_interface.function_name
        return_type = parsed_interface.return_type
        parameters = parsed_interface.parameters

        objc_return_type = self._get_objc_type(return_type)
        
        method_signature = self._generate_objc_method_signature(function_name, parameters, objc_return_type)
        property_declarations = self._generate_property_declarations(parameters)

        return f"""//
//  {class_name}.h
//  {self.framework_name}
//
//  Generated automatically - do not modify
//

#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

/**
 * Objective-C wrapper for {function_name}
 */
@interface {class_name} : NSObject

{property_declarations}

/**
 * Initialize with default values
 */
- (instancetype)init;

/**
 * Call the native {function_name} function
 */
{method_signature};

/**
 * Static convenience method
 */
+ ({objc_return_type}){function_name}{self._generate_static_method_params(parameters)};

@end

NS_ASSUME_NONNULL_END"""

    def _generate_objc_implementation(self, parsed_interface: ParsedFunction, class_name: str) -> str:
        """Generate Objective-C implementation file."""
        function_name = parsed_interface.function_name
        return_type = parsed_interface.return_type
        parameters = parsed_interface.parameters

        objc_return_type = self._get_objc_type(return_type)
        
        method_signature = self._generate_objc_method_signature(function_name, parameters, objc_return_type)
        method_implementation = self._generate_objc_method_implementation(parsed_interface)
        static_method_implementation = self._generate_static_method_implementation(parsed_interface)
        property_implementations = self._generate_property_implementations(parameters)

        return f"""//
//  {class_name}.m
//  {self.framework_name}
//
//  Generated automatically - do not modify
//

#import "{class_name}.h"
#import "{class_name}Bridge.hpp"

@implementation {class_name}

- (instancetype)init {{
    self = [super init];
    if (self) {{
        // Initialize default values
        {self._generate_default_initialization(parameters)}
    }}
    return self;
}}

{property_implementations}

{method_signature} {{
    {method_implementation}
}}

+ ({objc_return_type}){function_name}{self._generate_static_method_params(parameters)} {{
    {static_method_implementation}
}}

@end"""

    def _generate_cpp_bridge_header(self, parsed_interface: ParsedFunction, class_name: str) -> str:
        """Generate C++ bridge header file."""
        function_name = parsed_interface.function_name
        return_type = parsed_interface.return_type
        parameters = parsed_interface.parameters
        namespace = parsed_interface.namespace

        cpp_return_type = return_type
        
        param_declarations = ", ".join(
            f"{self._get_cpp_type(param.type)} {param.name}" 
            for param in parameters
        )

        return f"""//
//  {class_name}Bridge.hpp
//  {self.framework_name}
//
//  Generated automatically - do not modify
//

#ifndef {class_name}Bridge_hpp
#define {class_name}Bridge_hpp

#include <string>
{f'#include "{namespace}.h"' if namespace else '// Include your C++ header file here'}

namespace {self.framework_name.lower()}Bridge {{

/**
 * C++ bridge function for {function_name}
 */
{cpp_return_type} {function_name}Bridge({param_declarations});

/**
 * Utility functions for type conversion
 */
std::string NSStringToStdString(void* nsstring);
void* StdStringToNSString(const std::string& str);

}} // namespace {self.framework_name.lower()}Bridge

#endif /* {class_name}Bridge_hpp */"""

    def _generate_cpp_bridge_implementation(self, parsed_interface: ParsedFunction, class_name: str) -> str:
        """Generate C++ bridge implementation file."""
        function_name = parsed_interface.function_name
        return_type = parsed_interface.return_type
        parameters = parsed_interface.parameters
        namespace = parsed_interface.namespace

        param_names = ", ".join(param.name for param in parameters)
        param_conversions = self._generate_cpp_param_conversions(parameters)
        return_conversion = self._generate_cpp_return_conversion(return_type)

        return f"""//
//  {class_name}Bridge.cpp
//  {self.framework_name}
//
//  Generated automatically - do not modify
//

#include "{class_name}Bridge.hpp"
#import <Foundation/Foundation.h>

namespace {self.framework_name.lower()}Bridge {{

{return_type} {function_name}Bridge({", ".join(f"{self._get_cpp_type(param.type)} {param.name}" for param in parameters)}) {{
    try {{
        {param_conversions}
        
        {'' if return_type == 'void' else 'auto result = '}{namespace + '::' if namespace else ''}{function_name}({param_names});
        
        {return_conversion}
    }} catch (const std::exception& e) {{
        // Log error or throw Objective-C exception
        NSLog(@"Error in {function_name}: %s", e.what());
        {('return;' if return_type == 'void' else f'return {self._get_cpp_default_value(return_type)};')}
    }}
}}

std::string NSStringToStdString(void* nsstring) {{
    NSString* str = (__bridge NSString*)nsstring;
    return std::string([str UTF8String]);
}}

void* StdStringToNSString(const std::string& str) {{
    NSString* nsstr = [NSString stringWithUTF8String:str.c_str()];
    return (__bridge_retained void*)nsstr;
}}

}} // namespace {self.framework_name.lower()}Bridge"""

    def _generate_swift_wrapper(self, parsed_interface: ParsedFunction, class_name: str) -> str:
        """Generate Swift wrapper class."""
        function_name = parsed_interface.function_name
        return_type = parsed_interface.return_type
        parameters = parsed_interface.parameters

        swift_return_type = self._get_swift_type(return_type)
        
        param_declarations = ", ".join(
            f"{param.name}: {self._get_swift_type(param.type)}" 
            for param in parameters
        )

        param_names = ", ".join(param.name for param in parameters)

        return f"""//
//  {class_name}Swift.swift
//  {self.framework_name}
//
//  Generated automatically - do not modify
//

import Foundation

/**
 * Swift wrapper for {function_name}
 */
public class {class_name}Swift {{
    
    private let objcWrapper: {class_name}
    
    public init() {{
        self.objcWrapper = {class_name}()
    }}
    
    /**
     * Call the native {function_name} function
     */
    public func {function_name}({param_declarations}){' -> ' + swift_return_type if return_type != 'void' else ''} {{
        {'' if return_type == 'void' else 'return '}objcWrapper.{function_name}({param_names})
    }}
    
    /**
     * Static convenience method
     */
    public static func {function_name}({param_declarations}){' -> ' + swift_return_type if return_type != 'void' else ''} {{
        {'' if return_type == 'void' else 'return '}{class_name}.{function_name}({param_names})
    }}
}}"""

    def _generate_podspec(self, parsed_interface: ParsedFunction) -> str:
        """Generate Podspec file."""
        return f"""Pod::Spec.new do |spec|
  spec.name          = "{self.framework_name}"
  spec.version       = "1.0.0"
  spec.summary       = "C++ bridge framework for {parsed_interface.function_name}"
  spec.description   = "Generated iOS framework for calling C++ functions from Objective-C and Swift"
  
  spec.homepage      = "https://github.com/yourorg/{self.framework_name.lower()}"
  spec.license       = {{ :type => "MIT", :file => "LICENSE" }}
  spec.author        = {{ "Your Name" => "your.email@example.com" }}
  
  spec.ios.deployment_target = "11.0"
  spec.osx.deployment_target = "10.13"
  
  spec.source        = {{ :git => "https://github.com/yourorg/{self.framework_name.lower()}.git", :tag => "#{{spec.version}}" }}
  
  spec.source_files  = "ios/*.{{h,m,hpp,cpp}}"
  spec.public_header_files = "ios/*.h"
  
  spec.requires_arc = true
  spec.libraries = "c++"
  spec.pod_target_xcconfig = {{
    'CLANG_CXX_LANGUAGE_STANDARD' => 'c++17',
    'CLANG_CXX_LIBRARY' => 'libc++'
  }}
end"""

    def _generate_xcode_config(self) -> str:
        """Generate Xcode configuration file."""
        return """// Xcode configuration for C++ bridge
CLANG_CXX_LANGUAGE_STANDARD = c++17
CLANG_CXX_LIBRARY = libc++
GCC_C_LANGUAGE_STANDARD = c11
ENABLE_BITCODE = NO

// Header search paths
HEADER_SEARCH_PATHS = $(inherited) ./ios

// Library search paths
LIBRARY_SEARCH_PATHS = $(inherited)

// Other C++ flags
OTHER_CPLUSPLUSFLAGS = -std=c++17 -stdlib=libc++

// Preprocessor macros
GCC_PREPROCESSOR_DEFINITIONS = $(inherited)"""

    def _generate_objc_method_signature(self, function_name: str, parameters: List[Parameter], return_type: str) -> str:
        """Generate Objective-C method signature."""
        if not parameters:
            return f"- ({return_type}){function_name}"

        first_param = parameters[0]
        signature = f"- ({return_type}){function_name}:({self._get_objc_type(first_param.type)}){first_param.name}"

        for param in parameters[1:]:
            signature += f" {param.name}:({self._get_objc_type(param.type)}){param.name}"

        return signature

    def _generate_static_method_params(self, parameters: List[Parameter]) -> str:
        """Generate static method parameters."""
        if not parameters:
            return ""

        first_param = parameters[0]
        signature = f":({self._get_objc_type(first_param.type)}){first_param.name}"

        for param in parameters[1:]:
            signature += f" {param.name}:({self._get_objc_type(param.type)}){param.name}"

        return signature

    def _generate_property_declarations(self, parameters: List[Parameter]) -> str:
        """Generate property declarations."""
        if not parameters:
            return ""
        
        properties = []
        for param in parameters:
            prop_attr = self._get_property_attribute(param.type)
            objc_type = self._get_objc_type(param.type)
            properties.append(f"@property (nonatomic, {prop_attr}) {objc_type} {param.name};")
        
        return "\n".join(properties)

    def _generate_property_implementations(self, parameters: List[Parameter]) -> str:
        """Generate property implementations."""
        if not parameters:
            return ""
        
        return "\n".join(f"@synthesize {param.name} = _{param.name};" for param in parameters)

    def _generate_default_initialization(self, parameters: List[Parameter]) -> str:
        """Generate default initialization code."""
        if not parameters:
            return ""
        
        initializations = []
        for param in parameters:
            default_value = self._get_objc_default_value(param.type)
            initializations.append(f"        _{param.name} = {default_value};")
        
        return "\n".join(initializations)

    def _generate_objc_method_implementation(self, parsed_interface: ParsedFunction) -> str:
        """Generate Objective-C method implementation."""
        return_type = parsed_interface.return_type
        param_names = ", ".join(param.name for param in parsed_interface.parameters)
        bridge_call = f"{self.framework_name.lower()}Bridge::{parsed_interface.function_name}Bridge({param_names})"

        if return_type == 'void':
            return f"    {bridge_call};"
        else:
            return f"    return {bridge_call};"

    def _generate_static_method_implementation(self, parsed_interface: ParsedFunction) -> str:
        """Generate static method implementation."""
        function_name = parsed_interface.function_name
        return_type = parsed_interface.return_type
        param_names = ", ".join(param.name for param in parsed_interface.parameters)
        
        if return_type == 'void':
            return f"    {self.framework_name.lower()}Bridge::{function_name}Bridge({param_names});"
        else:
            return f"    return {self.framework_name.lower()}Bridge::{function_name}Bridge({param_names});"

    def _generate_cpp_param_conversions(self, parameters: List[Parameter]) -> str:
        """Generate C++ parameter conversions."""
        if not parameters:
            return ""
        
        conversions = []
        for param in parameters:
            if param.type == 'string':
                conversions.append(f"        std::string {param.name}_cpp = NSStringToStdString((void*){param.name});")
            else:
                conversions.append(f"        // {param.name} can be used directly")
        
        return "\n".join(conversions)

    def _generate_cpp_return_conversion(self, return_type: str) -> str:
        """Generate C++ return value conversion."""
        if return_type == 'void':
            return ""
        elif return_type == 'string':
            return "        return (NSString*)StdStringToNSString(result);"
        else:
            return "        return result;"

    def _get_objc_type(self, cpp_type: str) -> str:
        """Get Objective-C type."""
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

    def _get_swift_type(self, cpp_type: str) -> str:
        """Get Swift type."""
        swift_type_mapping = {
            'void': 'Void',
            'boolean': 'Bool',
            'byte': 'Int8',
            'short': 'Int16',
            'int': 'Int32',
            'long': 'Int64',
            'float': 'Float',
            'double': 'Double',
            'string': 'String'
        }
        return swift_type_mapping.get(cpp_type, 'Any')

    def _get_cpp_type(self, cpp_type: str) -> str:
        """Get C++ type."""
        cpp_type_mapping = {
            'string': 'std::string',
            'boolean': 'bool'
        }
        return cpp_type_mapping.get(cpp_type, cpp_type)

    def _get_property_attribute(self, type_name: str) -> str:
        """Get property attribute."""
        if type_name == 'string':
            return 'strong'
        return 'assign'

    def _get_objc_default_value(self, type_name: str) -> str:
        """Get Objective-C default value."""
        default_values = {
            'boolean': 'NO',
            'byte': '0',
            'short': '0',
            'int': '0',
            'long': '0',
            'float': '0.0f',
            'double': '0.0',
            'string': 'nil'
        }
        return default_values.get(type_name, 'nil')

    def _get_cpp_default_value(self, type_name: str) -> str:
        """Get C++ default value."""
        default_values = {
            'boolean': 'false',
            'byte': '0',
            'short': '0',
            'int': '0',
            'long': '0',
            'float': '0.0f',
            'double': '0.0',
            'string': 'std::string()'
        }
        return default_values.get(type_name, '{}')

    def _capitalize_first_letter(self, string: str) -> str:
        """Capitalize first letter."""
        return string[0].upper() + string[1:] if string else ""
