/**
 * C++接口解析器
 * 用于解析C++函数声明并提取函数信息
 */
export class CppInterfaceParser {
  constructor() {
    // C++基本类型映射
    this.typeMapping = {
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
    };
  }

  /**
   * 解析C++接口函数
   * @param {string} cppCode - C++函数代码
   * @returns {Object} 解析结果
   */
  parse(cppCode) {
    try {
      // 清理代码，移除注释和多余空白
      const cleanCode = this.cleanCode(cppCode);
      
      // 提取命名空间
      const namespace = this.extractNamespace(cleanCode);
      
      // 提取函数信息
      const functionInfo = this.extractFunctionInfo(cleanCode);
      
      return {
        namespace,
        functionName: functionInfo.name,
        returnType: functionInfo.returnType,
        parameters: functionInfo.parameters,
        isStatic: functionInfo.isStatic,
        isVirtual: functionInfo.isVirtual,
        isConst: functionInfo.isConst,
        originalCode: cppCode.trim()
      };
    } catch (error) {
      throw new Error(`Failed to parse C++ interface: ${error.message}`);
    }
  }

  /**
   * 清理代码
   */
  cleanCode(code) {
    // 移除单行注释
    code = code.replace(/\/\/.*$/gm, '');
    // 移除多行注释
    code = code.replace(/\/\*[\s\S]*?\*\//g, '');
    // 移除多余空白
    code = code.replace(/\s+/g, ' ').trim();
    return code;
  }

  /**
   * 提取命名空间
   */
  extractNamespace(code) {
    const namespaceMatch = code.match(/namespace\s+([a-zA-Z_][a-zA-Z0-9_]*)/);
    return namespaceMatch ? namespaceMatch[1] : null;
  }

  /**
   * 提取函数信息
   */
  extractFunctionInfo(code) {
    // 匹配函数声明的正则表达式
    const functionRegex = /(?:(static|virtual|inline)\s+)?(?:(static|virtual|inline)\s+)?([a-zA-Z_][a-zA-Z0-9_:*&<>\s]*)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\)\s*(?:(const)\s*)?(?:;|{)/;
    
    const match = code.match(functionRegex);
    if (!match) {
      throw new Error('Could not parse function declaration');
    }

    const [, modifier1, modifier2, returnType, functionName, paramStr, constModifier] = match;
    
    // 解析修饰符
    const modifiers = [modifier1, modifier2].filter(Boolean);
    const isStatic = modifiers.includes('static');
    const isVirtual = modifiers.includes('virtual');
    const isConst = !!constModifier;

    // 解析参数
    const parameters = this.parseParameters(paramStr);

    return {
      name: functionName,
      returnType: this.normalizeType(returnType.trim()),
      parameters,
      isStatic,
      isVirtual,
      isConst
    };
  }

  /**
   * 解析函数参数
   */
  parseParameters(paramStr) {
    if (!paramStr || paramStr.trim() === '') {
      return [];
    }

    const parameters = [];
    const params = this.splitParameters(paramStr);

    for (const param of params) {
      const paramInfo = this.parseParameter(param.trim());
      if (paramInfo) {
        parameters.push(paramInfo);
      }
    }

    return parameters;
  }

  /**
   * 分割参数字符串（处理模板和嵌套情况）
   */
  splitParameters(paramStr) {
    const params = [];
    let current = '';
    let depth = 0;
    let inString = false;
    let stringChar = '';

    for (let i = 0; i < paramStr.length; i++) {
      const char = paramStr[i];
      
      if (!inString) {
        if (char === '"' || char === "'") {
          inString = true;
          stringChar = char;
        } else if (char === '<' || char === '(') {
          depth++;
        } else if (char === '>' || char === ')') {
          depth--;
        } else if (char === ',' && depth === 0) {
          params.push(current.trim());
          current = '';
          continue;
        }
      } else if (char === stringChar) {
        inString = false;
      }

      current += char;
    }

    if (current.trim()) {
      params.push(current.trim());
    }

    return params;
  }

  /**
   * 解析单个参数
   */
  parseParameter(param) {
    if (!param) return null;

    // 匹配参数声明：[const] type [&|*] name [= default_value]
    const paramRegex = /(?:(const)\s+)?([a-zA-Z_][a-zA-Z0-9_:*&<>\s]*?)([*&]?)\s*([a-zA-Z_][a-zA-Z0-9_]*)?(?:\s*=\s*(.+))?$/;
    
    const match = param.match(paramRegex);
    if (!match) {
      // 尝试简单的类型匹配
      const simpleMatch = param.match(/([a-zA-Z_][a-zA-Z0-9_:*&<>\s]*)/);
      if (simpleMatch) {
        return {
          type: this.normalizeType(simpleMatch[1].trim()),
          name: `param${Math.random().toString(36).substr(2, 8)}`, // 生成随机参数名
          isConst: false,
          isPointer: false,
          isReference: false,
          defaultValue: null
        };
      }
      return null;
    }

    const [, constModifier, baseType, ptrRef, name, defaultValue] = match;

    return {
      type: this.normalizeType((baseType + (ptrRef || '')).trim()),
      name: name || `param${Math.random().toString(36).substr(2, 8)}`,
      isConst: !!constModifier,
      isPointer: ptrRef === '*',
      isReference: ptrRef === '&',
      defaultValue: defaultValue ? defaultValue.trim() : null
    };
  }

  /**
   * 标准化类型名称
   */
  normalizeType(type) {
    // 移除多余空白
    type = type.replace(/\s+/g, ' ').trim();
    
    // 处理常见的C++类型
    if (this.typeMapping[type]) {
      return this.typeMapping[type];
    }

    // 处理指针类型
    if (type.endsWith('*')) {
      const baseType = type.slice(0, -1).trim();
      if (this.typeMapping[baseType]) {
        return this.typeMapping[baseType];
      }
    }

    // 处理const类型
    if (type.startsWith('const ')) {
      const baseType = type.slice(6).trim();
      return this.normalizeType(baseType);
    }

    // 处理std::命名空间
    if (type.startsWith('std::')) {
      const baseType = type.slice(5);
      if (this.typeMapping[baseType]) {
        return this.typeMapping[baseType];
      }
    }

    return type;
  }

  /**
   * 获取Java类型映射
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
   * 获取Kotlin类型映射
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
   * 获取Objective-C类型映射
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
   * 获取TypeScript类型映射（用于鸿蒙NAPI）
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
}
