/**
 * iOS Objective-C代码生成器
 * 生成Objective-C包装类来调用C++代码
 */
export class IosOcGenerator {
  constructor(config = {}) {
    this.classPrefix = config.class_prefix || 'CPP';
    this.frameworkName = config.framework_name || 'CppBridge';
  }

  /**
   * 生成iOS Objective-C代码
   * @param {Object} parsedInterface - 解析后的C++接口
   * @param {Object} fileManager - 文件管理器
   * @returns {Array} 生成的文件列表
   */
  async generate(parsedInterface, fileManager) {
    const files = [];
    const className = `${this.classPrefix}${this.capitalizeFirstLetter(parsedInterface.functionName)}`;

    // 生成Objective-C头文件
    const headerCode = this.generateObjCHeader(parsedInterface, className);
    const headerFile = `ios/${className}.h`;
    await fileManager.writeFile(headerFile, headerCode);
    files.push(headerFile);

    // 生成Objective-C实现文件
    const implementationCode = this.generateObjCImplementation(parsedInterface, className);
    const implementationFile = `ios/${className}.m`;
    await fileManager.writeFile(implementationFile, implementationCode);
    files.push(implementationFile);

    // 生成C++桥接文件
    const bridgeHeaderCode = this.generateCppBridgeHeader(parsedInterface, className);
    const bridgeHeaderFile = `ios/${className}Bridge.hpp`;
    await fileManager.writeFile(bridgeHeaderFile, bridgeHeaderCode);
    files.push(bridgeHeaderFile);

    const bridgeImplementationCode = this.generateCppBridgeImplementation(parsedInterface, className);
    const bridgeImplementationFile = `ios/${className}Bridge.cpp`;
    await fileManager.writeFile(bridgeImplementationFile, bridgeImplementationCode);
    files.push(bridgeImplementationFile);

    // 生成Swift包装类（可选）
    const swiftCode = this.generateSwiftWrapper(parsedInterface, className);
    const swiftFile = `ios/${className}Swift.swift`;
    await fileManager.writeFile(swiftFile, swiftCode);
    files.push(swiftFile);

    // 生成Podspec文件
    const podspecCode = this.generatePodspec(parsedInterface);
    const podspecFile = `ios/${this.frameworkName}.podspec`;
    await fileManager.writeFile(podspecFile, podspecCode);
    files.push(podspecFile);

    // 生成Xcode项目配置
    const xconfigCode = this.generateXcodeConfig();
    const xconfigFile = `ios/Config.xcconfig`;
    await fileManager.writeFile(xconfigFile, xconfigCode);
    files.push(xconfigFile);

    return files;
  }

  /**
   * 生成Objective-C头文件
   */
  generateObjCHeader(parsedInterface, className) {
    const { functionName, returnType, parameters } = parsedInterface;
    const objcReturnType = this.getObjCType(returnType);
    
    const methodSignature = this.generateObjCMethodSignature(functionName, parameters, objcReturnType);
    const propertyDeclarations = this.generatePropertyDeclarations(parameters);

    return `//
//  ${className}.h
//  ${this.frameworkName}
//
//  Generated automatically - do not modify
//

#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

/**
 * Objective-C wrapper for ${functionName}
 */
@interface ${className} : NSObject

${propertyDeclarations}

/**
 * Initialize with default values
 */
- (instancetype)init;

/**
 * Call the native ${functionName} function
 */
${methodSignature};

/**
 * Static convenience method
 */
+ (${objcReturnType})${functionName}${this.generateStaticMethodParams(parameters)};

@end

NS_ASSUME_NONNULL_END`;
  }

  /**
   * 生成Objective-C实现文件
   */
  generateObjCImplementation(parsedInterface, className) {
    const { functionName, returnType, parameters, namespace } = parsedInterface;
    const objcReturnType = this.getObjCType(returnType);
    
    const methodSignature = this.generateObjCMethodSignature(functionName, parameters, objcReturnType);
    const methodImplementation = this.generateObjCMethodImplementation(parsedInterface);
    const staticMethodImplementation = this.generateStaticMethodImplementation(parsedInterface);
    const propertyImplementations = this.generatePropertyImplementations(parameters);

    return `//
//  ${className}.m
//  ${this.frameworkName}
//
//  Generated automatically - do not modify
//

#import "${className}.h"
#import "${className}Bridge.hpp"

@implementation ${className}

- (instancetype)init {
    self = [super init];
    if (self) {
        // Initialize default values
        ${this.generateDefaultInitialization(parameters)}
    }
    return self;
}

${propertyImplementations}

${methodSignature} {
    ${methodImplementation}
}

+ (${objcReturnType})${functionName}${this.generateStaticMethodParams(parameters)} {
    ${staticMethodImplementation}
}

@end`;
  }

  /**
   * 生成C++桥接头文件
   */
  generateCppBridgeHeader(parsedInterface, className) {
    const { functionName, returnType, parameters, namespace } = parsedInterface;
    const cppReturnType = returnType;
    
    const paramDeclarations = parameters.map(param => 
      `${this.getCppType(param.type)} ${param.name}`
    ).join(', ');

    return `//
//  ${className}Bridge.hpp
//  ${this.frameworkName}
//
//  Generated automatically - do not modify
//

#ifndef ${className}Bridge_hpp
#define ${className}Bridge_hpp

#include <string>
${namespace ? `#include "${namespace}.h"` : '// Include your C++ header file here'}

namespace ${this.frameworkName.toLowerCase()}Bridge {

/**
 * C++ bridge function for ${functionName}
 */
${cppReturnType} ${functionName}Bridge(${paramDeclarations});

/**
 * Utility functions for type conversion
 */
std::string NSStringToStdString(void* nsstring);
void* StdStringToNSString(const std::string& str);

} // namespace ${this.frameworkName.toLowerCase()}Bridge

#endif /* ${className}Bridge_hpp */`;
  }

  /**
   * 生成C++桥接实现文件
   */
  generateCppBridgeImplementation(parsedInterface, className) {
    const { functionName, returnType, parameters, namespace } = parsedInterface;
    const paramNames = parameters.map(param => param.name).join(', ');
    const paramConversions = this.generateCppParamConversions(parameters);
    const returnConversion = this.generateCppReturnConversion(returnType);

    return `//
//  ${className}Bridge.cpp
//  ${this.frameworkName}
//
//  Generated automatically - do not modify
//

#include "${className}Bridge.hpp"
#import <Foundation/Foundation.h>

namespace ${this.frameworkName.toLowerCase()}Bridge {

${returnType} ${functionName}Bridge(${parameters.map(param => 
  `${this.getCppType(param.type)} ${param.name}`
).join(', ')}) {
    try {
        ${paramConversions}
        
        ${returnType === 'void' ? '' : 'auto result = '}${namespace ? namespace + '::' : ''}${functionName}(${paramNames});
        
        ${returnConversion}
    } catch (const std::exception& e) {
        // Log error or throw Objective-C exception
        NSLog(@"Error in ${functionName}: %s", e.what());
        ${returnType === 'void' ? 'return;' : 'return ' + this.getCppDefaultValue(returnType) + ';'}
    }
}

std::string NSStringToStdString(void* nsstring) {
    NSString* str = (__bridge NSString*)nsstring;
    return std::string([str UTF8String]);
}

void* StdStringToNSString(const std::string& str) {
    NSString* nsstr = [NSString stringWithUTF8String:str.c_str()];
    return (__bridge_retained void*)nsstr;
}

} // namespace ${this.frameworkName.toLowerCase()}Bridge`;
  }

  /**
   * 生成Swift包装类
   */
  generateSwiftWrapper(parsedInterface, className) {
    const { functionName, returnType, parameters } = parsedInterface;
    const swiftReturnType = this.getSwiftType(returnType);
    
    const paramDeclarations = parameters.map(param => 
      `${param.name}: ${this.getSwiftType(param.type)}`
    ).join(', ');

    const paramNames = parameters.map(param => param.name).join(', ');

    return `//
//  ${className}Swift.swift
//  ${this.frameworkName}
//
//  Generated automatically - do not modify
//

import Foundation

/**
 * Swift wrapper for ${functionName}
 */
public class ${className}Swift {
    
    private let objcWrapper: ${className}
    
    public init() {
        self.objcWrapper = ${className}()
    }
    
    /**
     * Call the native ${functionName} function
     */
    public func ${functionName}(${paramDeclarations}) ${returnType === 'void' ? '' : '-> ' + swiftReturnType} {
        ${returnType === 'void' ? '' : 'return '}objcWrapper.${functionName}(${paramNames})
    }
    
    /**
     * Static convenience method
     */
    public static func ${functionName}(${paramDeclarations}) ${returnType === 'void' ? '' : '-> ' + swiftReturnType} {
        ${returnType === 'void' ? '' : 'return '}${className}.${functionName}(${paramNames})
    }
}`;
  }

  /**
   * 生成Podspec文件
   */
  generatePodspec(parsedInterface) {
    return `Pod::Spec.new do |spec|
  spec.name          = "${this.frameworkName}"
  spec.version       = "1.0.0"
  spec.summary       = "C++ bridge framework for ${parsedInterface.functionName}"
  spec.description   = "Generated iOS framework for calling C++ functions from Objective-C and Swift"
  
  spec.homepage      = "https://github.com/yourorg/${this.frameworkName.toLowerCase()}"
  spec.license       = { :type => "MIT", :file => "LICENSE" }
  spec.author        = { "Your Name" => "your.email@example.com" }
  
  spec.ios.deployment_target = "11.0"
  spec.osx.deployment_target = "10.13"
  
  spec.source        = { :git => "https://github.com/yourorg/${this.frameworkName.toLowerCase()}.git", :tag => "#{spec.version}" }
  
  spec.source_files  = "ios/*.{h,m,hpp,cpp}"
  spec.public_header_files = "ios/*.h"
  
  spec.requires_arc = true
  spec.libraries = "c++"
  spec.pod_target_xcconfig = {
    'CLANG_CXX_LANGUAGE_STANDARD' => 'c++17',
    'CLANG_CXX_LIBRARY' => 'libc++'
  }
end`;
  }

  /**
   * 生成Xcode配置文件
   */
  generateXcodeConfig() {
    return `// Xcode configuration for C++ bridge
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
GCC_PREPROCESSOR_DEFINITIONS = $(inherited)`;
  }

  /**
   * 生成Objective-C方法签名
   */
  generateObjCMethodSignature(functionName, parameters, returnType) {
    if (parameters.length === 0) {
      return `- (${returnType})${functionName}`;
    }

    const firstParam = parameters[0];
    let signature = `- (${returnType})${functionName}:(${this.getObjCType(firstParam.type)})${firstParam.name}`;

    for (let i = 1; i < parameters.length; i++) {
      const param = parameters[i];
      signature += ` ${param.name}:(${this.getObjCType(param.type)})${param.name}`;
    }

    return signature;
  }

  /**
   * 生成静态方法参数
   */
  generateStaticMethodParams(parameters) {
    if (parameters.length === 0) {
      return '';
    }

    const firstParam = parameters[0];
    let signature = `:(${this.getObjCType(firstParam.type)})${firstParam.name}`;

    for (let i = 1; i < parameters.length; i++) {
      const param = parameters[i];
      signature += ` ${param.name}:(${this.getObjCType(param.type)})${param.name}`;
    }

    return signature;
  }

  /**
   * 生成属性声明
   */
  generatePropertyDeclarations(parameters) {
    return parameters.map(param => 
      `@property (nonatomic, ${this.getPropertyAttribute(param.type)}) ${this.getObjCType(param.type)} ${param.name};`
    ).join('\n');
  }

  /**
   * 生成属性实现
   */
  generatePropertyImplementations(parameters) {
    return parameters.map(param => 
      `@synthesize ${param.name} = _${param.name};`
    ).join('\n');
  }

  /**
   * 生成默认初始化代码
   */
  generateDefaultInitialization(parameters) {
    return parameters.map(param => {
      const defaultValue = this.getObjCDefaultValue(param.type);
      return `        _${param.name} = ${defaultValue};`;
    }).join('\n');
  }

  /**
   * 生成Objective-C方法实现
   */
  generateObjCMethodImplementation(parsedInterface) {
    const { returnType, parameters } = parsedInterface;
    const paramNames = parameters.map(param => param.name).join(', ');
    const bridgeCall = `${this.frameworkName.toLowerCase()}Bridge::${parsedInterface.functionName}Bridge(${paramNames})`;

    if (returnType === 'void') {
      return `    ${bridgeCall};`;
    } else {
      return `    return ${bridgeCall};`;
    }
  }

  /**
   * 生成静态方法实现
   */
  generateStaticMethodImplementation(parsedInterface) {
    const { functionName, returnType, parameters } = parsedInterface;
    const paramNames = parameters.map(param => param.name).join(', ');
    
    if (returnType === 'void') {
      return `    ${this.frameworkName.toLowerCase()}Bridge::${functionName}Bridge(${paramNames});`;
    } else {
      return `    return ${this.frameworkName.toLowerCase()}Bridge::${functionName}Bridge(${paramNames});`;
    }
  }

  /**
   * 生成C++参数转换
   */
  generateCppParamConversions(parameters) {
    return parameters.map(param => {
      if (param.type === 'string') {
        return `        std::string ${param.name}_cpp = NSStringToStdString((void*)${param.name});`;
      }
      return `        // ${param.name} can be used directly`;
    }).join('\n');
  }

  /**
   * 生成C++返回值转换
   */
  generateCppReturnConversion(returnType) {
    if (returnType === 'void') {
      return '';
    } else if (returnType === 'string') {
      return '        return (NSString*)StdStringToNSString(result);';
    } else {
      return '        return result;';
    }
  }

  /**
   * 获取Objective-C类型
   */
  getObjCType(cppType) {
    const objcTypeMapping = {
      'void': 'void',
      'boolean': 'BOOL',
      'byte': 'char',
      'short': 'short',
      'int': 'int',
      'long': 'long',
      'float': 'float',
      'double': 'double',
      'string': 'NSString*'
    };

    return objcTypeMapping[cppType] || 'id';
  }

  /**
   * 获取Swift类型
   */
  getSwiftType(cppType) {
    const swiftTypeMapping = {
      'void': 'Void',
      'boolean': 'Bool',
      'byte': 'Int8',
      'short': 'Int16',
      'int': 'Int32',
      'long': 'Int64',
      'float': 'Float',
      'double': 'Double',
      'string': 'String'
    };

    return swiftTypeMapping[cppType] || 'Any';
  }

  /**
   * 获取C++类型
   */
  getCppType(cppType) {
    const cppTypeMapping = {
      'string': 'std::string',
      'boolean': 'bool'
    };

    return cppTypeMapping[cppType] || cppType;
  }

  /**
   * 获取属性特性
   */
  getPropertyAttribute(type) {
    if (type === 'string') {
      return 'strong';
    }
    return 'assign';
  }

  /**
   * 获取Objective-C默认值
   */
  getObjCDefaultValue(type) {
    const defaultValues = {
      'boolean': 'NO',
      'byte': '0',
      'short': '0',
      'int': '0',
      'long': '0',
      'float': '0.0f',
      'double': '0.0',
      'string': 'nil'
    };

    return defaultValues[type] || 'nil';
  }

  /**
   * 获取C++默认值
   */
  getCppDefaultValue(type) {
    const defaultValues = {
      'boolean': 'false',
      'byte': '0',
      'short': '0',
      'int': '0',
      'long': '0',
      'float': '0.0f',
      'double': '0.0',
      'string': 'std::string()'
    };

    return defaultValues[type] || '{}';
  }

  /**
   * 首字母大写
   */
  capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  }
}
