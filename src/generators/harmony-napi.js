/**
 * 鸿蒙NAPI代码生成器
 * 生成HarmonyOS NAPI C++代码和对应的TypeScript/ArkTS包装类
 */
export class HarmonyNapiGenerator {
  constructor(config = {}) {
    this.moduleName = config.module_name || 'CppBridge';
    this.namespace = config.namespace || 'cppbridge';
  }

  /**
   * 生成鸿蒙NAPI代码
   * @param {Object} parsedInterface - 解析后的C++接口
   * @param {Object} fileManager - 文件管理器
   * @returns {Array} 生成的文件列表
   */
  async generate(parsedInterface, fileManager) {
    const files = [];

    // 生成NAPI C++代码
    const napiCppCode = this.generateNapiCpp(parsedInterface);
    const napiCppFile = `harmony/src/main/cpp/napi/${parsedInterface.functionName}_napi.cpp`;
    await fileManager.writeFile(napiCppFile, napiCppCode);
    files.push(napiCppFile);

    // 生成NAPI头文件
    const napiHeaderCode = this.generateNapiHeader(parsedInterface);
    const napiHeaderFile = `harmony/src/main/cpp/napi/${parsedInterface.functionName}_napi.h`;
    await fileManager.writeFile(napiHeaderFile, napiHeaderCode);
    files.push(napiHeaderFile);

    // 生成NAPI模块注册文件
    const moduleCode = this.generateNapiModule(parsedInterface);
    const moduleFile = `harmony/src/main/cpp/napi/napi_init.cpp`;
    await fileManager.writeFile(moduleFile, moduleCode);
    files.push(moduleFile);

    // 生成TypeScript声明文件
    const tsDeclarationCode = this.generateTypeScriptDeclaration(parsedInterface);
    const tsDeclarationFile = `harmony/src/main/ets/types/${this.moduleName}.d.ts`;
    await fileManager.writeFile(tsDeclarationFile, tsDeclarationCode);
    files.push(tsDeclarationFile);

    // 生成ArkTS包装类
    const arktsCode = this.generateArkTSWrapper(parsedInterface);
    const arktsFile = `harmony/src/main/ets/${this.moduleName}.ets`;
    await fileManager.writeFile(arktsFile, arktsCode);
    files.push(arktsFile);

    // 生成CMakeLists.txt
    const cmakeCode = this.generateCMakeLists(parsedInterface);
    const cmakeFile = `harmony/src/main/cpp/CMakeLists.txt`;
    await fileManager.writeFile(cmakeFile, cmakeCode);
    files.push(cmakeFile);

    // 生成oh-package.json5
    const packageCode = this.generateOhPackage(parsedInterface);
    const packageFile = `harmony/oh-package.json5`;
    await fileManager.writeFile(packageFile, packageCode);
    files.push(packageFile);

    // 生成build-profile.json5
    const buildProfileCode = this.generateBuildProfile();
    const buildProfileFile = `harmony/build-profile.json5`;
    await fileManager.writeFile(buildProfileFile, buildProfileCode);
    files.push(buildProfileFile);

    return files;
  }

  /**
   * 生成NAPI C++实现代码
   */
  generateNapiCpp(parsedInterface) {
    const { functionName, returnType, parameters, namespace } = parsedInterface;
    const napiFunctionName = `NAPI_${functionName}`;
    
    const paramConversions = this.generateNapiParamConversions(parameters);
    const paramNames = parameters.map(param => param.name).join(', ');
    const returnConversion = this.generateNapiReturnConversion(returnType);

    return `#include "${parsedInterface.functionName}_napi.h"
#include <hilog/log.h>
${namespace ? `#include "${namespace}.h"` : '// Include your C++ header file here'}

using namespace std;

static constexpr unsigned int LOG_PRINT_DOMAIN = 0xFF00;
static constexpr char LOG_TAG[] = "${this.moduleName}";

napi_value ${napiFunctionName}(napi_env env, napi_callback_info info) {
    OH_LOG_Print(LOG_APP, LOG_INFO, LOG_PRINT_DOMAIN, LOG_TAG, "NAPI ${functionName} called");
    
    size_t argc = ${parameters.length};
    napi_value args[${Math.max(parameters.length, 1)}];
    napi_value thisVar = nullptr;
    
    napi_status status = napi_get_cb_info(env, info, &argc, args, &thisVar, nullptr);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to parse arguments");
        return nullptr;
    }
    
    if (argc != ${parameters.length}) {
        napi_throw_error(env, nullptr, "Wrong number of arguments");
        return nullptr;
    }
    
    try {
        ${paramConversions}
        
        ${returnType === 'void' ? '' : 'auto result = '}${namespace ? namespace + '::' : ''}${functionName}(${paramNames});
        
        ${returnConversion}
    } catch (const std::exception& e) {
        OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_PRINT_DOMAIN, LOG_TAG, "Error in ${functionName}: %{public}s", e.what());
        napi_throw_error(env, nullptr, e.what());
        ${returnType === 'void' ? 'return nullptr;' : 'return nullptr;'}
    }
}`;
  }

  /**
   * 生成NAPI头文件
   */
  generateNapiHeader(parsedInterface) {
    const { functionName } = parsedInterface;
    const napiFunctionName = `NAPI_${functionName}`;
    const headerGuard = `${functionName.toUpperCase()}_NAPI_H`;

    return `#ifndef ${headerGuard}
#define ${headerGuard}

#include <node_api.h>

/**
 * NAPI wrapper for ${functionName}
 */
napi_value ${napiFunctionName}(napi_env env, napi_callback_info info);

#endif // ${headerGuard}`;
  }

  /**
   * 生成NAPI模块注册文件
   */
  generateNapiModule(parsedInterface) {
    const { functionName } = parsedInterface;
    const napiFunctionName = `NAPI_${functionName}`;

    return `#include "napi/native_api.h"
#include "${parsedInterface.functionName}_napi.h"

static napi_value Init(napi_env env, napi_value exports) {
    napi_property_descriptor desc[] = {
        { "${functionName}", nullptr, ${napiFunctionName}, nullptr, nullptr, nullptr, napi_default, nullptr }
    };
    
    napi_status status = napi_define_properties(env, exports, sizeof(desc) / sizeof(desc[0]), desc);
    if (status != napi_ok) {
        return nullptr;
    }
    
    return exports;
}

static napi_module demoModule = {
    .nm_version = 1,
    .nm_flags = 0,
    .nm_filename = nullptr,
    .nm_register_func = Init,
    .nm_modname = "${this.moduleName}",
    .nm_priv = ((void*)0),
    .reserved = { 0 },
};

extern "C" __attribute__((constructor)) void RegisterModule(void) {
    napi_module_register(&demoModule);
}`;
  }

  /**
   * 生成TypeScript声明文件
   */
  generateTypeScriptDeclaration(parsedInterface) {
    const { functionName, returnType, parameters } = parsedInterface;
    const tsReturnType = this.getTypeScriptType(returnType);
    
    const paramDeclarations = parameters.map(param => 
      `${param.name}: ${this.getTypeScriptType(param.type)}`
    ).join(', ');

    return `/**
 * TypeScript declaration for ${this.moduleName}
 * Generated automatically - do not modify
 */

declare namespace ${this.namespace} {
  /**
   * ${functionName} function
   */
  function ${functionName}(${paramDeclarations}): ${tsReturnType};
}

export = ${this.namespace};`;
  }

  /**
   * 生成ArkTS包装类
   */
  generateArkTSWrapper(parsedInterface) {
    const { functionName, returnType, parameters } = parsedInterface;
    const tsReturnType = this.getTypeScriptType(returnType);
    
    const paramDeclarations = parameters.map(param => 
      `${param.name}: ${this.getTypeScriptType(param.type)}`
    ).join(', ');

    const paramNames = parameters.map(param => param.name).join(', ');

    return `/**
 * ArkTS wrapper for ${functionName}
 * Generated automatically - do not modify
 */

import ${this.moduleName} from 'lib${this.moduleName.toLowerCase()}.so';

export class ${this.capitalizeFirstLetter(functionName)}Bridge {
  
  /**
   * Call the native ${functionName} function
   */
  static ${functionName}(${paramDeclarations}): ${tsReturnType} {
    try {
      ${returnType === 'void' ? '' : 'return '}${this.moduleName}.${functionName}(${paramNames});
    } catch (error) {
      console.error(\`Error calling ${functionName}: \${error}\`);
      ${returnType === 'void' ? '' : 'throw error;'}
    }
  }
  
  /**
   * Async version of ${functionName}
   */
  static async ${functionName}Async(${paramDeclarations}): Promise<${tsReturnType}> {
    return new Promise((resolve, reject) => {
      try {
        const result = this.${functionName}(${paramNames});
        resolve(result);
      } catch (error) {
        reject(error);
      }
    });
  }
}

/**
 * Default export for convenience
 */
export default ${this.capitalizeFirstLetter(functionName)}Bridge;

/**
 * Namespace export
 */
export namespace ${this.capitalizeFirstLetter(functionName)} {
  export const bridge = ${this.capitalizeFirstLetter(functionName)}Bridge;
  
  export function ${functionName}(${paramDeclarations}): ${tsReturnType} {
    return bridge.${functionName}(${paramNames});
  }
  
  export function ${functionName}Async(${paramDeclarations}): Promise<${tsReturnType}> {
    return bridge.${functionName}Async(${paramNames});
  }
}`;
  }

  /**
   * 生成CMakeLists.txt
   */
  generateCMakeLists(parsedInterface) {
    const { functionName } = parsedInterface;
    const libraryName = this.moduleName.toLowerCase();

    return `cmake_minimum_required(VERSION 3.16)
project(${this.moduleName})

set(NATIVERENDER_ROOT_PATH \${CMAKE_CURRENT_SOURCE_DIR})

if(DEFINED PACKAGE_FIND_FILE)
    include(\${PACKAGE_FIND_FILE})
endif()

include_directories(\${NATIVERENDER_ROOT_PATH}
                    \${NATIVERENDER_ROOT_PATH}/include)

add_library(${libraryName} SHARED
    napi/napi_init.cpp
    napi/${functionName}_napi.cpp
    # Add your C++ source files here
)

target_link_libraries(${libraryName} PUBLIC libace_napi.z.so libhilog_ndk.z.so)`;
  }

  /**
   * 生成oh-package.json5
   */
  generateOhPackage(parsedInterface) {
    return `{
  "name": "${this.moduleName.toLowerCase()}",
  "version": "1.0.0",
  "description": "Native ${parsedInterface.functionName} bridge for HarmonyOS",
  "main": "index.ets",
  "author": "Generated Code",
  "license": "MIT",
  "dependencies": {}
}`;
  }

  /**
   * 生成build-profile.json5
   */
  generateBuildProfile() {
    return `{
  "apiType": 'stageMode',
  "targets": [
    {
      "name": "default",
      "runtimeOS": "HarmonyOS"
    }
  ]
}`;
  }

  /**
   * 生成NAPI参数转换代码
   */
  generateNapiParamConversions(parameters) {
    return parameters.map((param, index) => {
      const { type, name } = param;
      
      switch (type) {
        case 'boolean':
          return `        // Convert boolean parameter
        bool ${name};
        napi_get_value_bool(env, args[${index}], &${name});`;
        
        case 'int':
          return `        // Convert int parameter
        int32_t ${name};
        napi_get_value_int32(env, args[${index}], &${name});`;
        
        case 'long':
          return `        // Convert long parameter
        int64_t ${name};
        napi_get_value_int64(env, args[${index}], &${name});`;
        
        case 'float':
          return `        // Convert float parameter
        double ${name}_double;
        napi_get_value_double(env, args[${index}], &${name}_double);
        float ${name} = static_cast<float>(${name}_double);`;
        
        case 'double':
          return `        // Convert double parameter
        double ${name};
        napi_get_value_double(env, args[${index}], &${name});`;
        
        case 'string':
          return `        // Convert string parameter
        size_t ${name}_len = 0;
        napi_get_value_string_utf8(env, args[${index}], nullptr, 0, &${name}_len);
        char* ${name}_buffer = new char[${name}_len + 1];
        napi_get_value_string_utf8(env, args[${index}], ${name}_buffer, ${name}_len + 1, &${name}_len);
        std::string ${name}(${name}_buffer);
        delete[] ${name}_buffer;`;
        
        default:
          return `        // TODO: Handle ${type} parameter conversion for ${name}`;
      }
    }).join('\n');
  }

  /**
   * 生成NAPI返回值转换代码
   */
  generateNapiReturnConversion(returnType) {
    switch (returnType) {
      case 'void':
        return '        return nullptr;';
      
      case 'boolean':
        return `        napi_value napiResult;
        napi_get_boolean(env, result, &napiResult);
        return napiResult;`;
      
      case 'int':
        return `        napi_value napiResult;
        napi_create_int32(env, result, &napiResult);
        return napiResult;`;
      
      case 'long':
        return `        napi_value napiResult;
        napi_create_int64(env, result, &napiResult);
        return napiResult;`;
      
      case 'float':
      case 'double':
        return `        napi_value napiResult;
        napi_create_double(env, result, &napiResult);
        return napiResult;`;
      
      case 'string':
        return `        napi_value napiResult;
        napi_create_string_utf8(env, result.c_str(), NAPI_AUTO_LENGTH, &napiResult);
        return napiResult;`;
      
      default:
        return '        // TODO: Handle return type conversion\n        return nullptr;';
    }
  }

  /**
   * 获取TypeScript类型
   */
  getTypeScriptType(cppType) {
    const tsTypeMapping = {
      'void': 'void',
      'boolean': 'boolean',
      'byte': 'number',
      'short': 'number',
      'int': 'number',
      'long': 'number',
      'float': 'number',
      'double': 'number',
      'string': 'string'
    };

    return tsTypeMapping[cppType] || 'any';
  }

  /**
   * 首字母大写
   */
  capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  }
}
