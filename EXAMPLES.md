# 使用示例

本文档提供了跨平台代码生成器 MCP 工具的详细使用示例。

## 基础示例

### 示例 1: 简单数学函数

#### C++ 接口
```cpp
namespace MathUtils {
    int add(int a, int b);
    double multiply(double x, double y);
    bool isEven(int number);
}
```

#### 生成所有平台代码
```javascript
{
  "cpp_interface": "namespace MathUtils { int add(int a, int b); double multiply(double x, double y); bool isEven(int number); }",
  "output_directory": "./generated",
  "platforms": ["android", "ios", "harmony"],
  "android_config": {
    "package_name": "com.example.mathutils",
    "class_name": "MathUtils",
    "language": "kotlin"
  },
  "ios_config": {
    "class_prefix": "MU",
    "framework_name": "MathUtils"
  },
  "harmony_config": {
    "module_name": "MathUtils",
    "namespace": "mathutils"
  }
}
```

#### 生成的 Android Kotlin 代码
```kotlin
package com.example.mathutils

class MathUtils {
    companion object {
        init {
            System.loadLibrary("mathutils")
        }
    }
    
    private external fun addNative(a: Int, b: Int): Int
    private external fun multiplyNative(x: Double, y: Double): Double
    private external fun isEvenNative(number: Int): Boolean
    
    fun add(a: Int, b: Int): Int {
        return addNative(a, b)
    }
    
    fun multiply(x: Double, y: Double): Double {
        return multiplyNative(x, y)
    }
    
    fun isEven(number: Int): Boolean {
        return isEvenNative(number)
    }
}
```

### 示例 2: 字符串处理函数

#### C++ 接口
```cpp
namespace StringUtils {
    std::string toUpperCase(const std::string& input);
    int getLength(const std::string& text);
    std::string concatenate(const std::string& first, const std::string& second);
}
```

#### 仅生成 iOS 代码
```javascript
{
  "cpp_interface": "namespace StringUtils { std::string toUpperCase(const std::string& input); int getLength(const std::string& text); std::string concatenate(const std::string& first, const std::string& second); }",
  "output_directory": "./ios-output",
  "platforms": ["ios"],
  "ios_config": {
    "class_prefix": "SU",
    "framework_name": "StringUtils"
  }
}
```

#### 生成的 iOS Objective-C 头文件
```objc
//  SUStringUtils.h
//  StringUtils

#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

@interface SUStringUtils : NSObject

- (NSString*)toUpperCase:(NSString*)input;
- (int)getLength:(NSString*)text;
- (NSString*)concatenate:(NSString*)first second:(NSString*)second;

+ (NSString*)toUpperCase:(NSString*)input;
+ (int)getLength:(NSString*)text;
+ (NSString*)concatenate:(NSString*)first second:(NSString*)second;

@end

NS_ASSUME_NONNULL_END
```

## 高级示例

### 示例 3: 复杂数据处理

#### C++ 接口
```cpp
namespace DataProcessor {
    struct Point {
        double x;
        double y;
    };
    
    double calculateDistance(const Point& p1, const Point& p2);
    bool isValidCoordinate(double latitude, double longitude);
    std::string formatCoordinate(double value, int precision);
}
```

#### 仅解析接口信息
```javascript
{
  "cpp_interface": "namespace DataProcessor { struct Point { double x; double y; }; double calculateDistance(const Point& p1, const Point& p2); bool isValidCoordinate(double latitude, double longitude); std::string formatCoordinate(double value, int precision); }"
}
```

#### 解析结果
```
Parsed C++ interface:

Functions found:
1. calculateDistance
   - Return Type: double
   - Parameters:
     - const Point& p1
     - const Point& p2

2. isValidCoordinate
   - Return Type: bool
   - Parameters:
     - double latitude
     - double longitude

3. formatCoordinate
   - Return Type: std::string
   - Parameters:
     - double value
     - int precision

Namespace: DataProcessor
```

### 示例 4: 图像处理库

#### C++ 接口
```cpp
namespace ImageProcessor {
    enum class FilterType {
        BLUR,
        SHARPEN,
        GRAYSCALE
    };
    
    bool processImage(const std::string& inputPath, 
                     const std::string& outputPath,
                     FilterType filter);
    
    int getImageWidth(const std::string& imagePath);
    int getImageHeight(const std::string& imagePath);
    
    std::string getSupportedFormats();
}
```

#### 生成鸿蒙代码
```javascript
{
  "cpp_interface": "namespace ImageProcessor { enum class FilterType { BLUR, SHARPEN, GRAYSCALE }; bool processImage(const std::string& inputPath, const std::string& outputPath, FilterType filter); int getImageWidth(const std::string& imagePath); int getImageHeight(const std::string& imagePath); std::string getSupportedFormats(); }",
  "output_directory": "./harmony-output",
  "platforms": ["harmony"],
  "harmony_config": {
    "module_name": "ImageProcessor",
    "namespace": "imageprocessor"
  }
}
```

#### 生成的鸿蒙 ArkTS 代码
```typescript
/**
 * ArkTS wrapper for ImageProcessor
 */

import ImageProcessor from 'libimageprocessor.so';

export class ImageProcessorBridge {
  
  static processImage(inputPath: string, outputPath: string, filter: number): boolean {
    try {
      return ImageProcessor.processImage(inputPath, outputPath, filter);
    } catch (error) {
      console.error(`Error calling processImage: ${error}`);
      throw error;
    }
  }
  
  static getImageWidth(imagePath: string): number {
    try {
      return ImageProcessor.getImageWidth(imagePath);
    } catch (error) {
      console.error(`Error calling getImageWidth: ${error}`);
      throw error;
    }
  }
  
  static getImageHeight(imagePath: string): number {
    try {
      return ImageProcessor.getImageHeight(imagePath);
    } catch (error) {
      console.error(`Error calling getImageHeight: ${error}`);
      throw error;
    }
  }
  
  static getSupportedFormats(): string {
    try {
      return ImageProcessor.getSupportedFormats();
    } catch (error) {
      console.error(`Error calling getSupportedFormats: ${error}`);
      throw error;
    }
  }
}

export default ImageProcessorBridge;

export namespace ImageProcessor {
  export const bridge = ImageProcessorBridge;
  
  export enum FilterType {
    BLUR = 0,
    SHARPEN = 1,
    GRAYSCALE = 2
  }
  
  export function processImage(inputPath: string, outputPath: string, filter: FilterType): boolean {
    return bridge.processImage(inputPath, outputPath, filter);
  }
  
  export function getImageWidth(imagePath: string): number {
    return bridge.getImageWidth(imagePath);
  }
  
  export function getImageHeight(imagePath: string): number {
    return bridge.getImageHeight(imagePath);
  }
  
  export function getSupportedFormats(): string {
    return bridge.getSupportedFormats();
  }
}
```

## 平台特定示例

### Android Java 示例

#### 生成 Java 而非 Kotlin
```javascript
{
  "cpp_interface": "int factorial(int n);",
  "output_directory": "./android-java",
  "platforms": ["android"],
  "android_config": {
    "package_name": "com.example.math",
    "class_name": "Factorial",
    "language": "java"
  }
}
```

#### 生成的 Java 代码
```java
package com.example.math;

public class Factorial {
    
    static {
        System.loadLibrary("factorial");
    }
    
    private native int factorialNative(int n);
    
    public int factorial(int n) {
        return factorialNative(n);
    }
}
```

### iOS Swift 集成示例

#### 使用生成的 Objective-C 代码
```swift
import Foundation

class CalculatorViewController: UIViewController {
    
    let calculator = CPPCalculator()
    
    @IBAction func addButtonTapped(_ sender: UIButton) {
        let result = calculator.add(5, b: 3)
        print("5 + 3 = \(result)")
    }
    
    @IBAction func multiplyButtonTapped(_ sender: UIButton) {
        let result = CPPCalculator.multiply(4.5, y: 2.0)
        print("4.5 * 2.0 = \(result)")
    }
}
```

### 鸿蒙 ArkTS 集成示例

#### 在页面中使用
```typescript
import { ImageProcessor } from '../ImageProcessor';

@Entry
@Component
struct ImageProcessorPage {
  @State imageWidth: number = 0;
  @State imageHeight: number = 0;
  
  aboutToAppear() {
    this.loadImageInfo();
  }
  
  async loadImageInfo() {
    try {
      const imagePath = "/data/storage/el2/base/haps/entry/files/test.jpg";
      this.imageWidth = await ImageProcessor.getImageWidth(imagePath);
      this.imageHeight = await ImageProcessor.getImageHeight(imagePath);
    } catch (error) {
      console.error('Failed to load image info:', error);
    }
  }
  
  async processImage() {
    try {
      const inputPath = "/data/storage/el2/base/haps/entry/files/input.jpg";
      const outputPath = "/data/storage/el2/base/haps/entry/files/output.jpg";
      
      const success = await ImageProcessor.processImage(
        inputPath, 
        outputPath, 
        ImageProcessor.FilterType.BLUR
      );
      
      if (success) {
        console.log('Image processed successfully');
      }
    } catch (error) {
      console.error('Image processing failed:', error);
    }
  }
  
  build() {
    Column() {
      Text(`Image Size: ${this.imageWidth}x${this.imageHeight}`)
        .fontSize(16)
        .margin(20)
      
      Button('Process Image')
        .onClick(() => this.processImage())
    }
    .width('100%')
    .height('100%')
  }
}
```

## 错误处理示例

### 处理不支持的类型

#### C++ 接口（包含复杂类型）
```cpp
namespace ComplexTypes {
    std::vector<int> processArray(const std::vector<int>& input);
    std::map<std::string, int> getStatistics();
}
```

#### 解析结果
```
Parsed C++ interface:

Function: processArray
Return Type: std::vector<int> (Warning: Complex type, may need manual conversion)
Parameters:
  - const std::vector<int>& input (Warning: Complex type, may need manual conversion)

Function: getStatistics  
Return Type: std::map<std::string, int> (Warning: Complex type, may need manual conversion)
Parameters: (none)

Namespace: ComplexTypes

Note: Complex types like std::vector and std::map require manual implementation 
of serialization/deserialization logic.
```

### 处理解析错误

#### 无效的 C++ 代码
```cpp
invalid syntax here {
    int broken function(
}
```

#### 错误响应
```
Error: Failed to parse C++ interface: Could not parse function declaration

Suggestions:
1. Check for missing semicolons
2. Verify proper bracket matching
3. Ensure valid C++ syntax
4. Remove unsupported language features
```

## 最佳实践示例

### 1. 组织良好的命名空间

```cpp
namespace MyLibrary {
    namespace Math {
        double sqrt(double x);
        double pow(double base, double exponent);
    }
    
    namespace String {
        std::string trim(const std::string& input);
        bool startsWith(const std::string& text, const std::string& prefix);
    }
}
```

### 2. 使用一致的参数命名

```cpp
namespace GoodNaming {
    // 好的参数命名
    double calculateArea(double width, double height);
    std::string formatCurrency(double amount, const std::string& currencyCode);
    
    // 避免这样的命名
    // double calc(double a, double b);
    // std::string fmt(double x, const std::string& y);
}
```

### 3. 适当的错误处理

```cpp
namespace SafeFunctions {
    // 返回错误码而不是抛出异常
    int divideNumbers(double dividend, double divisor, double& result);
    
    // 使用布尔返回值表示成功/失败
    bool validateEmail(const std::string& email);
    
    // 提供默认值的安全函数
    std::string getConfigValue(const std::string& key, const std::string& defaultValue);
}
```

## 调试示例

### 使用解析工具调试

```javascript
// 第一步：解析接口
{
  "tool": "parse_cpp_interface",
  "cpp_interface": "double calculate(int a, float b);"
}

// 查看解析结果
// 第二步：生成代码
{
  "tool": "generate_multiplatform_code",
  "cpp_interface": "double calculate(int a, float b);",
  "output_directory": "./debug-output",
  "platforms": ["android"]
  // ... 其他配置
}
```

### 逐步验证生成的代码

1. **检查 JNI 签名**:
```cpp
// 生成的 JNI 函数签名
JNIEXPORT jdouble JNICALL
Java_com_example_Calculator_calculateNative(JNIEnv *env, jobject thiz, jint a, jfloat b);
```

2. **验证类型转换**:
```cpp
// 参数转换
int a_cpp = static_cast<int>(a);
float b_cpp = static_cast<float>(b);

// 调用原始函数
double result = calculate(a_cpp, b_cpp);

// 返回值转换
return static_cast<jdouble>(result);
```

3. **测试生成的包装类**:
```java
// Android 测试代码
Calculator calc = new Calculator();
double result = calc.calculate(10, 3.14f);
Assert.assertEquals(expected, result, 0.001);
```

---

更多示例和用例，请参考 [API 文档](API.md) 或访问我们的 [GitHub 仓库](https://github.com/yourorg/multiplatform_code)。
