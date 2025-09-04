/**
 * Android JNI代码生成器
 * 生成JNI C++代码和对应的Java/Kotlin包装类
 */
export class AndroidJniGenerator {
  constructor(config) {
    this.packageName = config.package_name;
    this.className = config.class_name;
    this.language = config.language || 'java';
  }

  /**
   * 生成Android JNI代码
   * @param {Object} parsedInterface - 解析后的C++接口
   * @param {Object} fileManager - 文件管理器
   * @returns {Array} 生成的文件列表
   */
  async generate(parsedInterface, fileManager) {
    const files = [];

    // 生成JNI C++代码
    const jniCppCode = this.generateJniCpp(parsedInterface);
    const jniCppFile = `android/jni/${parsedInterface.functionName}_jni.cpp`;
    await fileManager.writeFile(jniCppFile, jniCppCode);
    files.push(jniCppFile);

    // 生成JNI头文件
    const jniHeaderCode = this.generateJniHeader(parsedInterface);
    const jniHeaderFile = `android/jni/${parsedInterface.functionName}_jni.h`;
    await fileManager.writeFile(jniHeaderFile, jniHeaderCode);
    files.push(jniHeaderFile);

    // 生成Java/Kotlin包装类
    if (this.language === 'kotlin') {
      const kotlinCode = this.generateKotlinWrapper(parsedInterface);
      const kotlinFile = `android/src/main/kotlin/${this.packageName.replace(/\./g, '/')}/${this.className}.kt`;
      await fileManager.writeFile(kotlinFile, kotlinCode);
      files.push(kotlinFile);
    } else {
      const javaCode = this.generateJavaWrapper(parsedInterface);
      const javaFile = `android/src/main/java/${this.packageName.replace(/\./g, '/')}/${this.className}.java`;
      await fileManager.writeFile(javaFile, javaCode);
      files.push(javaFile);
    }

    // 生成CMakeLists.txt
    const cmakeCode = this.generateCMakeLists(parsedInterface);
    const cmakeFile = `android/jni/CMakeLists.txt`;
    await fileManager.writeFile(cmakeFile, cmakeCode);
    files.push(cmakeFile);

    // 生成build.gradle配置
    const gradleCode = this.generateGradleConfig();
    const gradleFile = `android/build.gradle.jni`;
    await fileManager.writeFile(gradleFile, gradleCode);
    files.push(gradleFile);

    return files;
  }

  /**
   * 生成JNI C++实现代码
   */
  generateJniCpp(parsedInterface) {
    const { functionName, returnType, parameters, namespace } = parsedInterface;
    const jniFunctionName = this.getJniFunctionName(functionName);
    const jniReturnType = this.getJniType(returnType);
    
    const paramDeclarations = parameters.map(param => 
      `${this.getJniType(param.type)} ${param.name}`
    ).join(', ');

    const paramConversions = parameters.map(param => 
      this.generateParamConversion(param)
    ).join('\n    ');

    const paramNames = parameters.map(param => param.name).join(', ');
    const returnConversion = this.generateReturnConversion(returnType);

    return `#include <jni.h>
#include "${parsedInterface.functionName}_jni.h"
${namespace ? `#include "${namespace}.h"` : '// Include your C++ header file here'}

extern "C" {

JNIEXPORT ${jniReturnType} JNICALL
${jniFunctionName}(JNIEnv *env, jobject thiz${paramDeclarations ? ', ' + paramDeclarations : ''}) {
    ${paramConversions}
    
    try {
        ${returnType === 'void' ? '' : `auto result = `}${namespace ? namespace + '::' : ''}${functionName}(${paramNames});
        ${returnConversion}
    } catch (const std::exception& e) {
        // 抛出Java异常
        jclass exceptionClass = env->FindClass("java/lang/RuntimeException");
        env->ThrowNew(exceptionClass, e.what());
        ${returnType === 'void' ? 'return;' : 'return ' + this.getDefaultValue(returnType) + ';'}
    }
}

} // extern "C"`;
  }

  /**
   * 生成JNI头文件
   */
  generateJniHeader(parsedInterface) {
    const { functionName, returnType, parameters } = parsedInterface;
    const jniFunctionName = this.getJniFunctionName(functionName);
    const jniReturnType = this.getJniType(returnType);
    
    const paramDeclarations = parameters.map(param => 
      `${this.getJniType(param.type)} ${param.name}`
    ).join(', ');

    const headerGuard = `${functionName.toUpperCase()}_JNI_H`;

    return `#ifndef ${headerGuard}
#define ${headerGuard}

#include <jni.h>

extern "C" {

/**
 * JNI wrapper for ${functionName}
 */
JNIEXPORT ${jniReturnType} JNICALL
${jniFunctionName}(JNIEnv *env, jobject thiz${paramDeclarations ? ', ' + paramDeclarations : ''});

} // extern "C"

#endif // ${headerGuard}`;
  }

  /**
   * 生成Java包装类
   */
  generateJavaWrapper(parsedInterface) {
    const { functionName, returnType, parameters } = parsedInterface;
    const javaReturnType = this.getJavaType(returnType);
    
    const paramDeclarations = parameters.map(param => 
      `${this.getJavaType(param.type)} ${param.name}`
    ).join(', ');

    const paramNames = parameters.map(param => param.name).join(', ');

    return `package ${this.packageName};

/**
 * JNI wrapper class for ${functionName}
 * Generated automatically - do not modify
 */
public class ${this.className} {
    
    static {
        System.loadLibrary("${this.className.toLowerCase()}");
    }
    
    /**
     * Native method declaration
     */
    private native ${javaReturnType} ${functionName}Native(${paramDeclarations});
    
    /**
     * Public wrapper method
     */
    public ${javaReturnType} ${functionName}(${paramDeclarations}) {
        ${returnType === 'void' ? '' : 'return '}${functionName}Native(${paramNames});
    }
}`;
  }

  /**
   * 生成Kotlin包装类
   */
  generateKotlinWrapper(parsedInterface) {
    const { functionName, returnType, parameters } = parsedInterface;
    const kotlinReturnType = this.getKotlinType(returnType);
    
    const paramDeclarations = parameters.map(param => 
      `${param.name}: ${this.getKotlinType(param.type)}`
    ).join(', ');

    const paramNames = parameters.map(param => param.name).join(', ');

    return `package ${this.packageName}

/**
 * JNI wrapper class for ${functionName}
 * Generated automatically - do not modify
 */
class ${this.className} {
    
    companion object {
        init {
            System.loadLibrary("${this.className.toLowerCase()}")
        }
    }
    
    /**
     * Native method declaration
     */
    private external fun ${functionName}Native(${paramDeclarations}): ${kotlinReturnType}
    
    /**
     * Public wrapper method
     */
    fun ${functionName}(${paramDeclarations}): ${kotlinReturnType} {
        ${returnType === 'void' ? '' : 'return '}${functionName}Native(${paramNames})
    }
}`;
  }

  /**
   * 生成CMakeLists.txt
   */
  generateCMakeLists(parsedInterface) {
    const { functionName } = parsedInterface;
    const libraryName = this.className.toLowerCase();

    return `cmake_minimum_required(VERSION 3.10.2)

project("${libraryName}")

# 设置C++标准
set(CMAKE_CXX_STANDARD 17)

# 添加库
add_library(${libraryName} SHARED
    ${functionName}_jni.cpp
    # 在这里添加您的C++源文件
)

# 查找所需的包
find_library(log-lib log)

# 链接库
target_link_libraries(${libraryName}
    \${log-lib}
    # 在这里添加您需要链接的其他库
)

# 包含目录
target_include_directories(${libraryName} PRIVATE
    .
    # 在这里添加您的头文件目录
)`;
  }

  /**
   * 生成Gradle配置
   */
  generateGradleConfig() {
    return `// 添加到您的 app/build.gradle 文件中

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
    // 添加您需要的依赖
}`;
  }

  /**
   * 获取JNI函数名
   */
  getJniFunctionName(functionName) {
    const packagePath = this.packageName.replace(/\./g, '_');
    return `Java_${packagePath}_${this.className}_${functionName}Native`;
  }

  /**
   * 获取JNI类型
   */
  getJniType(cppType) {
    const jniTypeMapping = {
      'void': 'void',
      'boolean': 'jboolean',
      'byte': 'jbyte',
      'short': 'jshort',
      'int': 'jint',
      'long': 'jlong',
      'float': 'jfloat',
      'double': 'jdouble',
      'string': 'jstring'
    };

    return jniTypeMapping[cppType] || 'jobject';
  }

  /**
   * 获取Java类型
   */
  getJavaType(cppType) {
    const javaTypeMapping = {
      'void': 'void',
      'boolean': 'boolean',
      'byte': 'byte',
      'short': 'short',
      'int': 'int',
      'long': 'long',
      'float': 'float',
      'double': 'double',
      'string': 'String'
    };

    return javaTypeMapping[cppType] || 'Object';
  }

  /**
   * 获取Kotlin类型
   */
  getKotlinType(cppType) {
    const kotlinTypeMapping = {
      'void': 'Unit',
      'boolean': 'Boolean',
      'byte': 'Byte',
      'short': 'Short',
      'int': 'Int',
      'long': 'Long',
      'float': 'Float',
      'double': 'Double',
      'string': 'String'
    };

    return kotlinTypeMapping[cppType] || 'Any';
  }

  /**
   * 生成参数转换代码
   */
  generateParamConversion(param) {
    const { type, name } = param;
    
    switch (type) {
      case 'string':
        return `    // Convert jstring to std::string
    const char* ${name}_chars = env->GetStringUTFChars(${name}, nullptr);
    std::string ${name}_cpp(${name}_chars);
    env->ReleaseStringUTFChars(${name}, ${name}_chars);`;
      
      default:
        return `    // ${name} can be used directly as ${type}`;
    }
  }

  /**
   * 生成返回值转换代码
   */
  generateReturnConversion(returnType) {
    switch (returnType) {
      case 'void':
        return '';
      
      case 'string':
        return '        return env->NewStringUTF(result.c_str());';
      
      default:
        return '        return result;';
    }
  }

  /**
   * 获取默认值
   */
  getDefaultValue(type) {
    const defaultValues = {
      'boolean': 'false',
      'byte': '0',
      'short': '0',
      'int': '0',
      'long': '0L',
      'float': '0.0f',
      'double': '0.0',
      'string': 'nullptr'
    };

    return defaultValues[type] || 'nullptr';
  }
}
