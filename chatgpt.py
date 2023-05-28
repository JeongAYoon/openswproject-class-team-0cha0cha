from apikey import OPENAI_API_KEY, RapidAPI_KEY  # 보안을 위해, 따로 저장한 apikey
import json


def gpt(topic, n = 10, except_list=[], retry = 0, add = 0):
    if retry >= 3:
        return [] # 다차례 오류 발생시 공백리스트 리턴
    import openai

    openai.api_key = OPENAI_API_KEY

    model = "gpt-3.5-turbo"

    train_topic = "'''tokyo shopping travel'''"

    prev2 = """
    {
    "destinations": [
        {
            "name": "Shibuya Crossing",
            "region": "Shibuya, Tokyo, Japan",
            "description": "One of the most famous and busiest intersections in Tokyo, Shibuya Crossing is a must-visit destination for any shopper. Featuring a vast array of department stores, boutiques, and specialty shops, it's the perfect place to find the latest fashion trends and unique souvenirs."
        },
        {
            "name": "Ginza",
            "region": "Chuo City, Tokyo, Japan",
            "description": "Known as one of the most luxurious shopping districts in the world, Ginza is home to high-end stores like Chanel, Gucci, and Dior. Apart from luxury boutiques, the area is also home to department stores, art galleries, and traditional Japanese craft shops."
        },
        {
            "name": "Shinjuku",
            "region": "Shinjuku City, Tokyo, Japan",
            "description": "A shopping mecca, Shinjuku offers an incredible variety of stores, restaurants, and entertainment venues. Its bustling streets and towering skyscrapers house a seemingly endless range of shopping options, from major department stores like Isetan and Takashimaya to unique local boutiques."
        },
        {
            "name": "Harajuku",
            "region": "Shibuya City, Tokyo, Japan",
            "description": "Famous for its vibrant street fashion, Harajuku is a haven for shoppers seeking the latest trends. Takeshita-dori street is the place to go for kawaii accessories, while Omotesando Avenue offers high-end designer shops and sleek modern architecture."
        },
        {
            "name": "Ameyoko Market",
            "region": "Taito City, Tokyo, Japan",
            "description": "Located beneath the railway tracks near Ueno Station, Ameyoko Market is a bustling location famous for its vibrant street market atmosphere. With over 400 shops selling everything from clothing to seafood, this is the perfect place to discover a unique shopping experience."
        },
        {
            "name": "Nakamise Shopping Street",
            "region": "Asakusa, Tokyo, Japan",
            "description": "One of Tokyo's oldest shopping districts, Nakamise Shopping Street is a pedestrian street lined with traditional stores selling sweets, souvenirs, and other Japanese trinkets. Located directly in front of the ancient Senso-ji Temple, this is a destination not to be missed."
        },
        {
            "name": "Odaiba",
            "region": "Minato City, Tokyo, Japan",
            "description": "A popular shopping and entertainment district, Odaiba offers something for everyone. From high-end boutiques and gourmet restaurants to family-friendly attractions like Legoland Discovery Center and Sega Joypolis, this futuristic island in Tokyo Bay is a must-visit."
        },
        {
            "name": "Musashi-Kosugi",
            "region": "Kawasaki, Kanagawa Prefecture, Japan",
            "description": "Located just outside of Tokyo in the city of Kawasaki, Musashi-Kosugi is a popular destination for shopping and dining. With a large selection of department stores, restaurants, and specialty shops, this bustling area is frequented by both locals and tourists alike."
        },
        {
            "name": "Ikebukuro",
            "region": "Toshima City, Tokyo, Japan",
            "description": "One of Tokyo's three major hubs, Ikebukuro is a lively district with abundant shopping and dining options. Featuring several large department stores, specialty shops like the Pokemon Center, and the Sunshine City complex, there's no shortage of things to explore here."
        },
        {
            "name": "Kappabashi-dori",
            "region": "Taito City, Tokyo, Japan",
            "description": "Known as the 'Kitchen Town' of Tokyo, Kappabashi-dori is home to over 170 shops selling cooking supplies and equipment. From exquisite Japanese knives to elaborate plastic food replicas, this unique shopping district is a must-visit for any food lover."
        }
    ],
    "topic_introduction": [
        "Tokyo is known for its unique shopping culture, offering everything from luxury brands to quirky accessories and traditional crafts. Whether you're looking for stylish boutiques or bustling street markets, Tokyo has something for every shopping enthusiast. Don't miss out on the chance to discover the latest trends and bring home one-of-a-kind souvenirs from this vibrant city."
        ]
    }
    """
    # If you're given a country theme, rather than a specific region, suggest destinations that give an overview of the region, rather than just attractions (places).
    # In case of a specific region is given,
    systemsay = f"""
    You are in the middle of a preliminary study to answer the following questions:
    Find me Exactly ten of travel destinations related to the topic.
    In the following user query, topic will be provided wrapped in triple backticks.
    Topic can be provided in a variety of languages. Translate the topic to English for you.
    Provide the results in the following order :
    Step 0. Imagine yourself as an expert travel guide AI speaking English. Do not say any other languages..
    Step 1. Follow the following conditions wrapped in angle brackets and find {n} of travel destinations related to topic in English :
    < You must only write places that can be cited and verified on Google Maps.
    You should include places that are heavily visited and has high ratings by tourists.
    destinations must be close each other. So, The distances between all of each travel destinations must be less than 10km.
    You must write close destinations(destinations in same or close administrative region, district or area) back-to-back.
    You must arrange the destinations order so that all destinations are visited in an optimal path. >
    Step 2. Be sure to follow the precautions in Step 1 to ensure that condition is complete at all of each destination and if any of the conditions are not met, fix what you find.
    Step 3. Follow the following conditions wrapped in angle brackets and find region name where the travel destinations belongs to.
    < If the region is multiple, write the only one region that is most representative. >
    Step 4. write 3 sentences introductions and to each destination.
    Step 5. lastly, write 2 sentences introductions about topic.
    Step 6. provide the output taht is {n} of travel destinations related to topic in English and only json format. The order of the output must satisfy the conditions in Step 1.
    Your output should be in json format with two list and have the following fields in first list :
     'name', 'region', 'description'. first list key is "destinations".
    In second list, You should write only introduction about topic. Second list key is "topic_introduction".
    """

    # 아래 오류목록 참고해서, 확인 후 고쳐보고.


    # 2. 먼거리 추천 에러 step1 요구사항 3,4,5번 라인



    # 3. 특정 지역 제외 후 재검색 기능 비작동 ( 영국 시계탑 중복 추천 등 일부 chatgpt가 실수하는 경우 있음. 드문 빈도. 다만, 관찰 필요. 무시해도 가능할 정도로 보임.) 주요문제는 x

    # 재검색시 지역전체소개는 빼도록 하면 속도개선 가능. (0으로 대충 답변하게 추가는 했지만, 잘 x), 주요기능은 x

    #### 현 기준 해결 사항

    # 개선사항 1. step1와 step2에서 여행지찾는 알고리즘 개선
    # 너무 광범위한 주제를 받았을 때 여행지간 거리 문제와, 최적 경로 순서로 추천하는 부분은 개선이 안 된다.
    # 최적 경로는 gpt에게 요구하기보다, 구글 맵 api를 활용하는 편이 적절할 수 있음.
    # 나라와, 특정 지역을 받았을때를 나눠보려했는데, 조금 더 고려해보고 해야겠다.
    # 다른 부분은 거의 해결
    # chatgpt상에서는 불가능한것으로 보임.
    # 1. 개수 부족하면 추가로 돌도록 코딩하기 (이제 거의 발생 x. 다만 개수 부족이 아니라, 과잉으로 제공하는 경우도 있다.(재시도 상황 포함, 에러 대비책 필요.)
    # 특히 재시도상황에서의 해당 문제는 치환시 치명적 문제 일으킬 수 있음. 중요!
    # 맨위에서 언급했듯, gpt는 예상할 수 없기 때문에, 항상 try except를 활용하게 해야겠다.
    # 6. 갑자기 json 로드가 안되는 치명적 오류 발생! 해결해야함(갑자기 안남! 계속 관찰 필요) 원인확인원료. json 앞뒤로 ```이 붙는 이상한 오류 발생. 발생 이제 거의 x ok
    # 3. 지역명 왔다갔다(상당히 명확해짐. 이정도면 그냥 뽑아도 될듯.) ok
    # 4. 갑자기 한국어로 응답 (이제 거의 일어나지 않는 버그긴 한데, 관찰 필요.) ok

    query = f"```{topic} in English```"

    messages = [
        {"role": "system", "content": systemsay},
        {"role": "user", "content": train_topic},
        {"role": "assistant", "content": prev2},
        {"role": "user", "content": query}
    ]
    #         The rest of the instructions are the same as before.
    if except_list != []:
        except_destination = ", ".join(except_list)
        systemsay2 = f"""
        in next answer, You must find {n} of travel destinations related to topic in English, And You should follow the following conditions wrapped in angle brackets too.
        < First, You must exclude the destinations wrapped in following double backticks. So, you must find the destinations that is not provided in following double backticks.
        ``{except_destination}``. this is Top priority requirement.
        Second, You don't need to write 2 sentences introductions about topic. Instead, Just write '0'. > 
        The rest of the instructions are the same as preliminary study.
        """
        messages = [
            {"role": "system", "content": systemsay},
            {"role": "user", "content": train_topic},
            {"role": "assistant", "content": prev2},
            {"role": "user", "content": systemsay2},
            {"role": "user", "content": query}
        ]

    response = openai.ChatCompletion.create(model=model, messages=messages)

    answer = response['choices'][0]['message']['content']  # 응답 부분
    # ## answer 테스트 부분
    # print(response['choices'][0]['message']['content'])
    # print("json 변환 전 \n\n")
    result = {}
    if answer[0] == '`' or answer[len(answer)-1] == '`': # 아주 적은 빈도로, ```가 양쪽에 붙는 문제 해결
        answer.strip('`')

    try:
        result = json.loads(response['choices'][0]['message']['content'])
    except:
        print("re-try\n\n")
        print(response['choices'][0]['message']['content'])
        retry += 1
        return gpt(topic,n,except_list, retry)
    # print(result)
    # answer = []
    # for i in result["destinations"]:
    #     name_with_region = i['name'] + '(' + i['region'] + ')'
    #     answer.append(name_with_region)
    #     print(name_with_region, i["description"], sep=' :: ', end="\n\n")
    # print(result['topic_introduction'])
    # print(answer, len(answer), sep='\n')
    # return answer

    ### 개수 점검기
    # 초과하는 케이스 우선
    if len(result['destinations']) > n:
        for i in range(len(result['destinations']) - n):
            result['destinations'].pop()  # result에 len개만큼만 남기도록 하고 뒤로 넘김
    elif len(result['destinations']) < n: # 미만인 케이스
        new_except_list = except_list[:]
        for i in result["destinations"]:
            name_with_region = i['name'] + '(' + i['region'] + ')'
            new_except_list.append(name_with_region)
        new_n = n-len(result['destinations'])
        result['destinations'].extend(gpt(topic,new_n,new_except_list,0,1))
        # new_except_list에 현재 검색한 양만큼 추가 후, new_n 은 n-len으로 맞춘 후, gpt를 새로 호출해서 받아온 뒤, 진행중이던 곳에 추가하기.
        # 디폴트 인자로 해당케이스 속성값을 줘서, 얘에 추가하는 전용으로 영문값만 받아오는 케이스를 만들어야겠다.

    ### 추가용 gpt버전으로 들어왔는지 점검기

    if add == 1:
        return result['destinations']
        # 번역 없이, 영어값 그대로 정리해서 리턴

    # return [answer, result]

    ### 영문 여행지명 리스트 생성기


    try:
        eng_name = []
        for dest in result['destinations']:
            eng_name.append(dest['name'] + '(' + dest['region'] + ')')

        # print(eng_name) # !테스트 부분

        # 번역을 위한 데이터 처리 부분 1-

        text = ""

        for dest in result['destinations']:
            text = text + dest['name'] + ' :: ' + dest['region'] + ' :: ' + dest['description'] + '\n'

        text += result['topic_introduction'][0]

        # print(text) # 테스트용


        ### deepl api
        import requests

        url = "https://deepl-translator.p.rapidapi.com/translate"

        payload = {
            "text": text,
            "source": "EN",
            "target": "KO"
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": RapidAPI_KEY,
            "X-RapidAPI-Host": "deepl-translator.p.rapidapi.com"
        }

        response = requests.post(url, json=payload, headers=headers)

        # print(response.json()['text']) # 번역 완료 내용 테스트

        translated_text = response.json()['text']
        # print(translated_text) #테스트 !!!


        #### 아래는 리턴을 위한 데이터 처리 부분 2-

        textlist = translated_text.split('\n')
        # print(textlist) # !!!테스트
        # print(textdata) # !!!테스트
        name = []
        introduce = []
        PS = textlist.pop()
        for texts in textlist:
            temp_name, temp_region, temp_introduce = texts.split("::")
            name.append(temp_name.strip().strip(":") + '(' + temp_region.strip().strip(":") + ')')
            introduce.append(temp_introduce.strip().strip(":"))

        return [eng_name, name, introduce, PS]
    except:
        retry += 1
        return gpt(topic, n, except_list, retry)



# ! 테스팅
topic = input()
# ans, res = gpt(topic)
eng_name, name, introduce, PS = gpt(topic)
print(eng_name)
print(name)
print(introduce)
print(PS)

print("제외후 재 테스트\n")
a, b, c, d = gpt(topic, 1, eng_name)
print(a, b, c, d, sep="\n")
# print(gpt(topic, 1, ans))


# 번역 이전의 검색및 활용 데이터리스트 1개, 번역이 완료된 출력용 데이터리스트 2개를 만들 예정.
# 데이터리스트 1개는 여행지 제목만을 제공할 것
# 나머지 데이터리스트 1개는 여행지 정보를 제공할 것
#
# 검색용 데이터리스트는 여행지 제목 영어 원문 데이터를 가질 예정.
#

## 검색할 데이터는 받아온다고 가정 ! 테스팅
# topic = "도쿄 역사 여행"

#
# def gpt(topic):
#     #### chatgpt api
#     import openai
#
#     openai.api_key = OPENAI_API_KEY
#
#     model = "gpt-3.5-turbo"
#
#     n = 10  # 여행지 수 표현
#     query = f"'{topic}' is topic. Follow the prompts to respond."
#
#     prev = """Akihabara::Akihabara, also known as "Electric Town," is a mecca for anime and manga enthusiasts. This bustling neighborhood is filled with shops, arcades, and maid cafes, offering a wide range of anime merchandise and experiences.
#
# 	Studio Ghibli Museum::Visit the Studio Ghibli Museum in Mitaka to immerse yourself in the enchanting world of Hayao Miyazaki's iconic animated films. Explore the exhibits, watch exclusive short films, and marvel at the beautiful artwork and craftsmanship.
#
# 	Nakano Broadway::Nakano Broadway is a multi-story complex in Tokyo that houses numerous anime and manga shops. Here, you can find rare collectibles, vintage merchandise, and a vast selection of manga from various genres.
#
# 	Ikebukuro::Ikebukuro is another anime hotspot, featuring large-scale stores dedicated to anime, manga, and character goods. It's home to the famous Sunshine City complex, which includes an anime-themed shopping mall, an observation deck, and even an indoor theme park.
#
# 	Odaiba::Odaiba is not only known for its futuristic architecture and stunning views of Tokyo Bay but also for its anime-related attractions. You can visit the Gundam Base Tokyo, where you'll find a life-sized Gundam statue, or explore the Tokyo Joypolis amusement park, which features anime-themed rides and games.
#
# 	Pokemon Center Mega Tokyo::Pokemon fans shouldn't miss the Pokemon Center Mega Tokyo in Ikebukuro. This store offers an extensive range of Pokemon merchandise, including plush toys, trading cards, apparel, and exclusive items that you won't find elsewhere.
#
# 	Tokyo Character Street::Located in the basement of Tokyo Station, Tokyo Character Street is a shopping arcade lined with shops dedicated to popular anime, manga, and game characters. From Hello Kitty to Dragon Ball, you'll find a wide variety of character goods here.
#
# 	Mandarake Complex::The Mandarake Complex in Nakano is a treasure trove for anime and manga enthusiasts. This multi-story building houses numerous Mandarake stores, each specializing in different aspects of otaku culture, such as vintage toys, cosplay, and rare collectibles.
#
# 	Comiket::If you're lucky enough to visit Tokyo during the Comic Market (Comiket), it's a must-visit event for anime and manga fans. Held twice a year, Comiket is the largest self-published comic book fair in Japan, featuring thousands of doujinshi (fan-made comics) and cosplay.
#
# 	Shinjuku::Shinjuku is a vibrant district that offers a mix of modern entertainment and anime-related attractions. Explore the various department stores like Takashimaya and Kinokuniya, which have dedicated anime and manga sections, or visit the Animate store for a wide selection of anime merchandise.
#
# 	Embark on a Tokyo Anime Trip and immerse yourself in the colorful world of Japanese animation. From bustling neighborhoods like Akihabara and Ikebukuro to dedicated stores, museums, and events, Tokyo offers a paradise for anime enthusiasts. Get ready to indulge in your favorite characters, collectibles, and experiences while exploring the dynamic cityscape."""
#
#     prev2 = """Gyeongbokgung Palace::Gyeongbokgung Palace, located in Seoul, is a majestic symbol of the Joseon Dynasty. Explore its grand architecture, intricate details, and beautiful gardens as you step back in time and learn about Korean history.
#
# 	Changdeokgung Palace::Changdeokgung Palace is a UNESCO World Heritage site known for its harmonious blend of architecture and natural surroundings. Discover the secret garden, stroll through the palace halls, and delve into the historical significance of this royal residence.
#
# 	Bulguksa Temple::Located in Gyeongju, Bulguksa Temple is one of Korea's most significant Buddhist temples. Marvel at its stunning design, including the intricate stone carvings and serene atmosphere, while appreciating its historical and cultural importance.
#
# 	Hwaseong Fortress::Hwaseong Fortress in Suwon is a well-preserved fortress from the Joseon Dynasty. Walk along its walls, visit the gates, and explore the various pavilions, offering insights into Korea's military architecture and defense strategies.
#
# 	National Museum of Korea::The National Museum of Korea in Seoul is a treasure trove of artifacts showcasing Korea's rich history. Discover ancient relics, royal treasures, and archaeological findings that span thousands of years, providing a comprehensive overview of Korean heritage.
#
# 	Seokguram Grotto::Located on Mount Toham, the Seokguram Grotto houses a remarkable granite Buddha statue. Appreciate the artistry and religious significance of this masterpiece, which is considered one of Korea's most important Buddhist sites.
#
# 	Gyeongju Historic Areas::Gyeongju, known as the "museum without walls," is a city filled with historic sites and cultural heritage. Explore the ancient tombs, temple ruins, and UNESCO-listed sites, immersing yourself in the glory of Korea's ancient capital.
#
# 	Jeonju Hanok Village::Jeonju Hanok Village offers a glimpse into traditional Korean architecture and culture. Wander through its narrow alleyways lined with traditional hanok houses, visit museums and craft workshops, and indulge in the city's famous bibimbap cuisine.
#
# 	Andong Hahoe Folk Village::Step into the past at the Andong Hahoe Folk Village, a well-preserved village that showcases traditional Korean rural life. Admire the thatched-roof houses, participate in cultural activities, and witness traditional performances like mask dances.
#
# 	War Memorial of Korea::The War Memorial of Korea in Seoul commemorates the history and sacrifices of the Korean War and other significant conflicts. Explore its exhibits, including military equipment, photographs, and multimedia presentations, to gain a deeper understanding of Korea's tumultuous past.
#
# 	Embark on a Korean history tour and uncover the rich cultural heritage of this fascinating country. From magnificent palaces and temples to historic fortresses and museums, each destination offers a unique glimpse into Korea's past. Immerse yourself in the stories, traditions, and architectural marvels that have shaped Korea's history over centuries."""
#
#     # 현재 가장 큰 이슈는 종종 앞에 숫자를 붙여주거나, 위에 쓸데없는 잡설을 다는 경우. 해당 이슈가 가장 많이 등장함.
#     # 마지막에 한줄소개를 까먹는 예
#     # 오사카 맛집여행을 찾아달라니까 뜬금없이 관련없는 일본 여행지를 추천해주는 예
#     # 뜬금없이 한줄만 답변해주는 예도 일어남.
#     # 이런식. Jeju Island Volcanic Landscape Tour//Embark on a journey to Jeju Island, known for its unique volcanic terrain shaped by millions of years of volcanic activity. Explore the stunning natural wonders formed by the volcanic landscape, from majestic mountains to fascinating caves, craters, and beaches. Discover the geological history of the island and get ready for an adventure of a lifetime on this one-of-a-kind volcanic landscape tour.
#     # '제주도 화산 지형 여행'으로 하자 저렇게 나옴
#     # '프랑스 문화 여행' 에도 위와 같이 응답
#
#     # '제주도 화산지형 여행'으로 검색하자 7가지만 추천해줌. 번호도 붙었고. 개수가 부족했나..?
#     # 종종 10가지 안쓰고 덜 쓰는 경우가 일어나네?
#
#     # 예외가 자주 잃어나지만 않는다면, try except로 잡아버린는것도 괜찮음.
#
#     # 질문을 조금 바꾸자, 주제에 대해서 갑자기 소개를 쏼라쏼라 하기도 함.
#     # 한번 더 바꾸니, 정상 작동.
#     # 하는듯 싶었지만, 8개만 추천해주고 비정상 작동.
#
#     # 제주도, 도쿄 등 검색시 그 자체에 대해서 여행지로 소개해주는 문제.
#
#     # 오류 빈도가 적은데, try except들로 걸러주는거 괜찮을듯? 몇번 재실행 하도록 하고, 안된다면, 특정 카운트수가 넘어간다면 탈출하도록.
#
#     # 다른 오류는 많이 줄었지만, 개수가 부족한 경우가 종종 일어난다.
#     # 1. 개수 부족(주제에 대해서만 소개하거나, 부족하게 소개)
#     # 2. 위에 잡설 출력 3. 앞에 숫자 붙임 4. 거리가 먼 부적절한 여행지 추천 5. 순서 부적절
#
#     # messages = [
#     #         {"role": "system", "content": "You are currently being pre-trained to answer the following query. Imagine you are an expert tour guide AI that provides correct answers in a structured grammatical format. You must need to list 10 travel destinations for questioner to use this informations for travel based on the topic being asked. Write a three-line introduction to your destination, tailored to the question. At last line, Write a 1-line story to introduce your topic. Your responses should be based on the question and focus on destinations that many people like. You should answer with a list of destinations that are close to each other so that the traveler can travel in a shorter period of time. To put it another way, you must never involve in list about distant from each other destinations.  the most important thing is all destinations are close each others. <<for example, The Henry Ford Museum of American Innovation is not close to Route 66. There is a significant distance between the two locations, with Route 66 primarily traversing the western states while The Henry Ford Museum is situated in the Midwest. So, you must never involve these destinations that is far from each other in your destinations list>> the order in which the destinations are displayed should allow the traveler to visit them all in the shortest amount of time without having to retrace their steps. Every element in the entire list (travel destinations) must fully satisfy the conditions for every other element. ----- Also, Your response grammatical format should be absolutely consistent. The response grammatical format is as follows: 1. Write the name of the destination and a description of the destination, nothing else. 2. Write the name of the destination immediately, followed by a '::' to separate it from the description. Immediately follow this with a description of the destination, i.e., 'Destination Name::Description of Destination', line by line. Do not write anything other than a Destination name, Description of Destination and lastly 1-line story to introduce topic . Use the format of your previous response as a writing guide for current your answer. In the previous answer, you answered the question 'Tokyo Anime Trip' and 'Korean history tour'. You should write current answer to Match the grammatical format of your previous answers without any grammatical diffrences. Do you understand? You will now be given a topic. using pre-trained things, please answer about topic."},
#     #         {"role": "assistant", "content": prev},
#     #         {"role": "assistant", "content": prev2},
#     #         {"role": "user", "content": query}
#     # ]
