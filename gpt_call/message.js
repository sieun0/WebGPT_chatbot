const keywordmessages = [ //검색어 입력 키워드 추출해내는 메시지
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
                        {'role':'user', 'content':'유통기한이 2023년 이내인 몰티져스 초콜릿을 찾아줘.'},
                        {'role':'assistant', 'content':'몰티져스 초콜릿'},
                        {'role':'user', 'content':'캐리비안 베이 티켓은 얼마야? 그것도 여기 파나?'},
                        {'role':'assistant', 'content':'캐리비안 베이 티켓'},
                        {'role': 'user', 'content': inputText}
                        //{'role':'assistant', 'content': {'prompt':'5L 이상인 에어 프라이어를 보여줘.', 'completion':'에어 프라이어'}}
                        ]
 