from openai import OpenAI

client = OpenAI(api_key='f658f3ff-b4b5-402d-9d20-221a8f78a010',base_url='https://ark.cn-beijing.volces.com/api/v3')

m = [{"role":"user","content":"你是怎推理的"}]

if __name__ == "__main__":
        response = client.chat.completions.create(
                model='deepseek-r1-250528',
                messages=m,
                #extra_body={"return_reasoning":True}
        )
        #aa = response.choices[0].message.model_extra['reasoning_content']
         
        print("-------------")
        print(response.choices[0].message.reasoning_content)