const { Configuration, OpenAIApi } = require('https://cdn.skypack.dev/openai');

function keywordGPTCall(input) {
    return new Promise((resolve, reject) => {
        const configuration = new Configuration({
            apiKey: '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'
        });
        const openai = new OpenAIApi(configuration);
        const messages = [ //검색어 입력 키워드 추출해내는 메시지
                    {'role':'system', 'content':'You are an AI that only extracts keyword words from sentences to search on the website. You are extract only words that are not in sentence form. For example, in the sentence "1Kg 이하의 삼성 이온 노트북의 가격을 비교해줘", the keyword word is "삼성 이온 노트북".'},
                    {'role':'user', 'content':'2만원 이하의 장수 사과를 찾아줘.'},
                    {'role':'assistant', 'content':'장수 사과'},
                    {'role':'user', 'content':'보라카이의 리조트를 가고 싶어'},
                    {'role':'assistant', 'content':'보라카이 리조트'},
                    {'role':'user', 'content':'여성여름바지사고싶어. 가격추천해줘.'},
                    {'role':'assistant', 'content':'여성여름바지'},
                    {'role':'user', 'content':'다이슨 청소기를 사고싶어. 가격을 알려줄래?'},
                    {'role':'assistant', 'content':'다이슨 청소기'},
                    {'role':'user', 'content':'여성여름 바지 가격 비교'},
                    {'role':'assistant', 'content':'여성여름 바지'},
                    {'role':'user', 'content':'제일 당류가 적은 커피는 ???'},
                    {'role':'assistant', 'content':'커피'},
                    {'role':'user', 'content':'나이키 브랜드의 슬리퍼를 구매하고 싶어. 제일 저렴한 게 뭐야?'},
                    {'role':'assistant', 'content':'나이키 슬리퍼'},
                    {'role': 'user', 'content': input}
                    //{'role':'assistant', 'content': {'prompt':'5L 이상인 에어 프라이어를 보여줘.', 'completion':'에어 프라이어'}}
                    ]


        openai.createChatCompletion({
            model: "gpt-3.5-turbo",
            //prompt: document.querySelector('#input').value,
            messages: messages,
            /*temperature: 0.7,
            max_tokens: 500,
            top_p: 1,
            frequency_penalty: 0,
            presence_penalty: 0,*/
            }).then((result)=>{
                //console.log(result.data.choices[0].message.content);
                //var output = `<div class="line">
                    //   <span class="chat-box">${ result.data.choices[0].message.content }</span>
                //</div>`
                const outputText = result.data.choices[0].message.content;
                resolve(outputText);
            })
            .catch((error) => {
                reject(error);
            });
                //document.querySelector('.chat-content').insertAdjacentHTML('beforeend', outputbox);
                
                /*const assistantMessages = messages.concat({'role':'assistant', 'content':result.data.choices[0].text});
                assistantMessages.forEach((message) => {
                assistant.appendMessage(message.role, message.content);
                    )*/
                            
        });
}
        