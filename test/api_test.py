import requests
import json

def test_post_api():
    """
    测试 POST API 的完整示例
    """
    # 1. API 端点配置
    url = "http://0.0.0.0:9090/task/run" 
    
    # 2. 准备请求数据
    payload = {"name": "一个任务", "instruct":'计划','session_id':'557852b0-dfab-4787-8a9e-615d2271a372'}
    
    # 3. 设置请求头
    headers = {
        "Content-Type": "application/json",
    }
    
    try:
        # 4. 发送 POST 请求
        print("🚀 发送 POST 请求...")
        response = requests.post(
            url=url,
            data=json.dumps(payload),  # 将字典转换为 JSON 字符串
            headers=headers,
            timeout=10  # 设置超时时间
        )
        
        # 5. 检查响应状态码
        print(f"📊 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 请求成功！")
            
            # 6. 解析响应数据
            response_data = response.json()
            
            # 7. 验证响应内容
            print("\n📄 响应数据:")
            print(response_data)
            
            
        else:
            print(f"❌ 请求失败，状态码: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ 请求超时，请检查网络连接或增加超时时间")
    except requests.exceptions.ConnectionError:
        print("🔌 连接错误，请检查URL或网络连接")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ 请求异常: {e}")
    except json.JSONDecodeError:
        print("📝 响应不是有效的JSON格式")
    except Exception as e:
        print(f"💥 未知错误: {e}")
 

if __name__ == "__main__":
    # 运行测试
    test_post_api()
    
