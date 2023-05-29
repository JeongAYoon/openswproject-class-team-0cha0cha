import os
import googlemaps
import requests

########################################-----------수정 사항---------#########################################################
# result_list에 사진 값도 추가하긴 했는데 값이 길어서 이건 어떻게 할 건지 정하기(url로 대체함 안되면 content로 변경)
# ㄴ되는 거 확인되서 그대로 유지
# 폐업상태 제외하기
# ㄴ 최종 결과 리스트(result_list)에 '-1' 뜨는 건 아무리 걸러도 폐업한 것만 있을때 넣어논 거임
# ㄴ완료
# result_list=[0 or 1,'검색한 장소=검색한 결과의 장소','평점','리뷰 수','사진링크', '좌표(lat)', '좌표(lng)']
#############################################################################################################################

def search(input_search_locations=[]):
    api_key = 'YOUR_API_KEY'
    map_clinet = googlemaps.Client(api_key)

    result_list = [] #최종 결과물 리스트
    result_ex=[] #최종 결과물 리스트 전 단계

    # chat-gpt 로 받아올 데이터
    search_locations=input_search_locations

    min_rating = 0  # 최소 평점
    min_reviews = 0  # 최소 리뷰 수


    # 지도에 데이터 보낼 때 좌표로 보내는 걸로 코드 바꾸기(원한다면)
    for locations in search_locations:
        response = map_clinet.places(query=locations) # 데이터를 api로 보냄
        destination = [] 
        
        if(response['status'] !='ZERO_RESULTS'): #검색데이터 결과가 빈 리스트로 오는 경우(=검색결과가 없을때)를 걸러줌
            if('rating' in response['results'][0]): # 인덱스 번호에 따라 영업점 나오는 듯. 기준으로만 일단 만듬
                if('business_status' in response['results'][0]): #'business_status'가 없는 경우 분류
                    if(response['results'][0]['business_status']=='OPERATIONAL'): #폐업인 경우 제외
                        # '0'->지역 외의 장소, 평점이 있는 것
                        
                        if('photos' in response['results'][0]): # 'photos'가 아예없는 경우 제외
                            #사진 요청
                            photo_reference=response['results'][0]['photos'][0]['photo_reference'] #'photos'중 첫번째꺼
                            photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                            response_photo = requests.get(photo_url)
                            res_photo=response_photo.url
                            
                            destination.append(0)
                            destination.append(response['results'][0]['name'])
                            destination.append(response['results'][0]['rating'])
                            destination.append(response['results'][0]['user_ratings_total'])
                            destination.append(res_photo)
                            
                            # 좌표
                            search_location_lat=(response['results'][0]['geometry']['location']['lat'])
                            search_location_lng=(response['results'][0]['geometry']['location']['lng'])
                            destination.append(search_location_lat)
                            destination.append(search_location_lng)                                 
                        else:
                            destination.append(0)
                            destination.append(response['results'][0]['name'])
                            destination.append(response['results'][0]['rating'])
                            destination.append(response['results'][0]['user_ratings_total'])
                            destination.append('No Image')
                            # 좌표
                            search_location_lat=(response['results'][0]['geometry']['location']['lat'])
                            search_location_lng=(response['results'][0]['geometry']['location']['lng'])
                            destination.append(search_location_lat)
                            destination.append(search_location_lng)
    
                    else: # 폐업한 경우 '-1'
                        destination.append(-1)
                else:
                    if('photos' in response['results'][0]): # 'photos'가 아예없는 경우 제외
                        #사진 요청
                        photo_reference=response['results'][0]['photos'][0]['photo_reference'] #'photos'중 첫번째꺼
                        photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                        response_photo = requests.get(photo_url)
                        res_photo=response_photo.url
                        
                        destination.append(0)
                        destination.append(response['results'][0]['name'])
                        destination.append(response['results'][0]['rating'])
                        destination.append(response['results'][0]['user_ratings_total'])
                        destination.append(res_photo)
                        # 좌표
                        search_location_lat=(response['results'][0]['geometry']['location']['lat'])
                        search_location_lng=(response['results'][0]['geometry']['location']['lng'])
                        destination.append(search_location_lat)
                        destination.append(search_location_lng)                                      
                    else:
                        destination.append(0)
                        destination.append(response['results'][0]['name'])
                        destination.append(response['results'][0]['rating'])
                        destination.append(response['results'][0]['user_ratings_total'])
                        destination.append('No Image')
                        # 좌표
                        search_location_lat=(response['results'][0]['geometry']['location']['lat'])
                        search_location_lng=(response['results'][0]['geometry']['location']['lng'])
                        destination.extend(search_location_lat)
                        destination.extend(search_location_lng)
                    
                    
                        
            else:
                # '1'->지역이름, 여기서 지역이름에 관광명소를 평점높고 리뷰수 많은거 1개 가져오면 됨. 단, 없는건 건너뛰고

                # 장소 '1'에 해당되는 장소의 좌표값
                location_lat=response['results'][0]['geometry']['location']['lat']
                location_lng=response['results'][0]['geometry']['location']['lng']
                    
                radius=2000 # 반경 2,000m
                    
                # 장소 세부요청 (전달받은 위치의 반경 2000m에 있는 관광명소 탐색)
                payload={}
                headers = {}
                attractions = []
                    
                #장소 세부요청
                url=f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location_lat},{location_lng}&radius={radius}&type=tourist+attractions&key={api_key}"
                data=requests.request("GET", url, headers=headers, data=payload)
                res_lo=data.json()
                    
                # 받아온 데이터 상태가 없음일 경우를 제외
                if(res_lo['status']!='ZERO_RESULTS'):
                    max_reviewer = -1
                    max_index = -1
                    for i in range(len(res_lo)):
                        # 리뷰 수가 높은 순으로 정렬 필요
                        #print(i)
                        if 'rating' in res_lo['results'][i]:
                            if('business_status' in res_lo['results'][i]): #'business_status'가 없는 경우 분류
                                if(res_lo['results'][i]['business_status']=='OPERATIONAL'): #폐업인 경우 제외
                                    name = res_lo['results'][i]['name']
                                    rating = res_lo['results'][i]['rating']
                                    reviews = res_lo['results'][i]['user_ratings_total']
                                    if reviews >= max_reviewer:
                                        max_reviewer = reviews
                                        max_index = i
                            else:
                                name = res_lo['results'][i]['name']
                                rating = res_lo['results'][i]['rating']
                                reviews = res_lo['results'][i]['user_ratings_total']
                                if reviews >= max_reviewer:
                                    max_reviewer = reviews
                                    max_index = i
                                
                    name = res_lo['results'][max_index]['name']
                    rating = res_lo['results'][max_index]['rating']
                    reviews = res_lo['results'][max_index]['user_ratings_total']
                    
                    # 관광명소, 평점, 리뷰가 있는 것만 추가
                    if name is not None and rating is not None and reviews is not None:
                        if rating >= min_rating and reviews >= min_reviews:
                            if attractions!=(name,rating,reviews): #리스트 내에 있는 관광명소와 중복방지
                                attractions.append((name,rating,reviews))
                    
                    # 좌표
                    search_location_lat=(res_lo['results'][max_index]['geometry']['location']['lat'])
                    search_location_lng=(res_lo['results'][max_index]['geometry']['location']['lng'])
                    destination.append(search_location_lat)
                    destination.append(search_location_lng)

                    if('photos' in res_lo['results'][max_index]):  # 'photos'가 아예없는 경우 제외
                        #사진 요청
                        photo_reference=res_lo['results'][max_index]['photos'][0]['photo_reference'] #'photos'중 첫번째꺼
                        photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                        response_photo = requests.get(photo_url)
                        res_photo=response_photo.url
                        attractions.append(res_photo)
                        
                        destination.append(1)      
                        destination.append(locations) # 검색한 지역이름
                        destination.extend(attractions)
                    else:
                        destination.append(1)      
                        destination.append(locations) # 검색한 지역이름
                        destination.extend(attractions)
                        destination.extend('No Image')
                    
                    
                #검색데이터 결과가 빈 리스트로 오는 경우(=검색결과가 없을때) 텍스트 검색으로 다시 찾기
                else: 
                    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={locations}&key={api_key}"
                    response = requests.get(url)
                    data = response.json()
                    
                    attractions = []
                    
                    max_reviewer = -1
                    max_index = -1
                    for i in range(len(res_lo)):
                        # 리뷰 수가 높은 순으로 정렬 필요
                        #print(i)
                        if('business_status' in res_lo['results'][i]): #'business_status'가 없는 경우 분류
                            if(res_lo['results'][i]['business_status']=='OPERATIONAL'): #폐업인 경우 제외
                                if 'rating' in data['results'][i]:
                                    name = data['results'][i]['name']
                                    rating = data['results'][i]['rating']
                                    reviews = data['results'][i]['user_ratings_total']
                                    if reviews >= max_reviewer:
                                        max_reviewer = reviews
                                        max_index = i
                        else:
                            if 'rating' in data['results'][i]:
                                name = data['results'][i]['name']
                                rating = data['results'][i]['rating']
                                reviews = data['results'][i]['user_ratings_total']
                                if reviews >= max_reviewer:
                                    max_reviewer = reviews
                                    max_index = i
                                
                    name = data['results'][max_index]['name']
                    rating = data['results'][max_index]['rating']
                    reviews = data['results'][max_index]['user_ratings_total']

                        # 이름, 평점, 리뷰가 있는 것만 추가
                    if name is not None and rating is not None and reviews is not None:
                        if rating >= min_rating:
                            attractions.append((name, rating, reviews))

                    if('photos' in res_lo['results'][max_index]):  # 'photos'가 아예없는 경우 제외
                        photo_reference=res_lo['results'][max_index]['photos'][0]['photo_reference'] #'photos'중 첫번째꺼
                        photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                        response_photo = requests.get(photo_url)
                        res_photo=response_photo.url
                        attractions.append(res_photo)
                    else:
                        attractions.append('No Image')

                    
                    # 받아온 데이터가 공백리스트가 아닌 경우만 destination 리스트에 추가
                    if(attractions!=[]):
                        destination.append(1)
                        destination.append(locations) # 검색한 지역이름
                        destination.extend(attractions)
                        
                    # 좌표
                    search_location_lat=(res_lo['results'][max_index]['geometry']['location']['lat'])
                    search_location_lng=(res_lo['results'][max_index]['geometry']['location']['lng'])
                    destination.append(search_location_lat)
                    destination.append(search_location_lng)
                    
        else: #검색데이터 결과가 빈 리스트로 오는 경우(=검색결과가 없을때) 텍스트 검색으로 다시 찾기
            url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={locations}&key={api_key}"
            response = requests.get(url)
            data = response.json()

            attractions = []
            if(data['status'] !='ZERO_RESULTS'): # 이것도 공백 리스트 경우를 제외
                max_reviewer = -1
                max_index = -1
                for i in range(len(res_lo)):
                    # 리뷰 수가 높은 순으로 정렬 필요
                    #print(i)
                    if('business_status' in data['results'][i]): #'business_status'가 없는 경우 분류
                        if(data['results'][i]['business_status']=='OPERATIONAL'): #폐업인 경우 제외
                            if 'rating' in data['results'][i]:
                                name = data['results'][i]['name']
                                rating = data['results'][i]['rating']
                                reviews = data['results'][i]['user_ratings_total']
                                if reviews >= max_reviewer:
                                    max_reviewer = reviews
                                    max_index = i
                    else:
                        if 'rating' in data['results'][i]:
                            name = data['results'][i]['name']
                            rating = data['results'][i]['rating']
                            reviews = data['results'][i]['user_ratings_total']
                            if reviews >= max_reviewer:
                                max_reviewer = reviews
                                max_index = i
                                
                name = data['results'][max_index]['name']
                rating = data['results'][max_index]['rating']
                reviews = data['results'][max_index]['user_ratings_total']
                    
                    # 이름, 평점, 리뷰가 있는 것만 추가
                if name is not None and rating is not None and reviews is not None:
                    if rating >= min_rating:
                        attractions.append((name, rating, reviews))

                if('photos' in data['results'][max_index]):  # 'photos'가 아예없는 경우 제외
                    #사진 요청
                    photo_reference=data['results'][max_index]['photos'][0]['photo_reference'] #'photos'중 첫번째꺼
                    photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                    response_photo = requests.get(photo_url)
                    res_photo=response_photo.url
                    attractions.append(res_photo)
                    
                    destination.append(1)
                    destination.append(locations) # 검색한 지역이름
                    destination.extend(attractions)
                else:
                    destination.append(1)
                    destination.append(locations) # 검색한 지역이름
                    destination.extend(attractions)
                    destination.extend('No Image')
                    
                # 좌표
                search_location_lat=(data['results'][max_index]['geometry']['location']['lat'])
                search_location_lng=(data['results'][max_index]['geometry']['location']['lng'])
                destination.append(search_location_lat)
                destination.append(search_location_lng)
                    
            else: # 그래도 공백 리스트인 경우
                locations_blank_text=locations.split("(")
                
                response_blank = map_clinet.places(query=locations_blank_text[0]) # 데이터를 api로 보냄
                
            
                if(response_blank['status'] !='ZERO_RESULTS'): #검색데이터 결과가 빈 리스트로 오는 경우(=검색결과가 없을때)를 걸러줌
                    if('rating' in response_blank['results'][0]): # 인덱스 번호에 따라 영업점 나오는 듯. 기준으로만 일단 만듬
                        if('business_status' in response_blank['results'][0]): #'business_status'가 없는 경우 분류
                            if(response_blank['results'][0]['business_status']=='OPERATIONAL'): #폐업인 경우 제외
                                # '0'->지역 외의 장소, 평점이 있는 것

                                destination.append(0)
                                if('photos' in response_blank['results'][0]):  # 'photos'가 아예없는 경우 제외
                                    #사진 요청
                                    photo_reference=response_blank['results'][0]['photos'][0]['photo_reference'] #'photos'중 첫번째꺼
                                    photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                                    response_photo = requests.get(photo_url)
                                    res_photo=response_photo.url
                                    
                            
                                    destination.append(response_blank['results'][0]['name'])
                                    destination.append(response_blank['results'][0]['rating'])
                                    destination.append(response_blank['results'][0]['user_ratings_total'])
                                    destination.append(res_photo)
                                else:
                                    destination.append(response_blank['results'][0]['name'])
                                    destination.append(response_blank['results'][0]['rating'])
                                    destination.append(response_blank['results'][0]['user_ratings_total'])
                                    destination.append('No Image')
                                # 좌표
                                search_location_lat=(response_blank['results'][0]['geometry']['location']['lat'])
                                search_location_lng=(response_blank['results'][0]['geometry']['location']['lng'])
                                destination.append(search_location_lat)
                                destination.append(search_location_lng)
                                
                            else: # 폐업인 경우 '-1'
                                destination.append(-1)
                        else:
                            destination.append(0)
                            if('photos' in response_blank['results'][0]):  # 'photos'가 아예없는 경우 제외
                                #사진 요청
                                photo_reference=response_blank['results'][0]['photos'][0]['photo_reference'] #'photos'중 첫번째꺼
                                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                                response_photo = requests.get(photo_url)
                                res_photo=response_photo.url
                                
                        
                                destination.append(response_blank['results'][0]['name'])
                                destination.append(response_blank['results'][0]['rating'])
                                destination.append(response_blank['results'][0]['user_ratings_total'])
                                destination.append(res_photo)
                            else:
                                destination.append(response_blank['results'][0]['name'])
                                destination.append(response_blank['results'][0]['rating'])
                                destination.append(response_blank['results'][0]['user_ratings_total'])
                                destination.append('No Image')
                            # 좌표
                            search_location_lat=(response_blank['results'][0]['geometry']['location']['lat'])
                            search_location_lng=(response_blank['results'][0]['geometry']['location']['lng'])
                            destination.append(search_location_lat)
                            destination.append(search_location_lng)     
                    else:
                        # '1'->지역이름, 여기서 지역이름에 관광명소를 평점높고 리뷰수 많은거 1개 가져오면 됨. 단, 없는건 건너뛰고

                        # 장소 '1'에 해당되는 장소의 좌표값
                        location_lat=response_blank['results'][0]['geometry']['location']['lat']
                        location_lng=response_blank['results'][0]['geometry']['location']['lng']
                            
                        radius=2000 # 반경 2,000m
                            
                        # 장소 세부요청 (전달받은 위치의 반경 2000m에 있는 관광명소 탐색)
                        payload={}
                        headers = {}
                        attractions = []
                            
                        #장소 세부요청
                        url=f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location_lat},{location_lng}&radius={radius}&type=tourist+attractions&key={api_key}"
                        data=requests.request("GET", url, headers=headers, data=payload)
                        res_lo=data.json()
                            
                        # 받아온 데이터 상태가 없음일 경우를 제외
                        if(res_lo['status']!='ZERO_RESULTS'):
                            max_reviewer = -1
                            max_index = -1
                            for i in range(len(res_lo)):
                                # 리뷰 수가 높은 순으로 정렬 필요
                                #print(i)
                                if('business_status' in res_lo['results'][i]): #'business_status'가 없는 경우 분류
                                    if(res_lo['results'][i]['business_status']=='OPERATIONAL'): #폐업인 경우 제외
                                        if 'rating' in res_lo['results'][i]:
                                            name = res_lo['results'][i]['name']
                                            rating = res_lo['results'][i]['rating']
                                            reviews = res_lo['results'][i]['user_ratings_total']
                                            if reviews >= max_reviewer:
                                                max_reviewer = reviews
                                                max_index = i
                                else:
                                    if 'rating' in res_lo['results'][i]:
                                        name = res_lo['results'][i]['name']
                                        rating = res_lo['results'][i]['rating']
                                        reviews = res_lo['results'][i]['user_ratings_total']
                                        if reviews >= max_reviewer:
                                            max_reviewer = reviews
                                            max_index = i
                                
                            name = res_lo['results'][max_index]['name']
                            rating = res_lo['results'][max_index]['rating']
                            reviews = res_lo['results'][max_index]['user_ratings_total']
                            

                            # 관광명소, 평점, 리뷰가 있는 것만 추가
                            if name is not None and rating is not None and reviews is not None:
                                if rating >= min_rating and reviews >= min_reviews:
                                    if attractions!=(name,rating,reviews): #리스트 내에 있는 관광명소와 중복방지
                                        attractions.append((name,rating,reviews))
                                                
                            if('photos' in res_lo['results'][max_index]):  # 'photos'가 아예없는 경우 제외
                                #사진 요청
                                photo_reference=res_lo['results'][max_index]['photos'][0]['photo_reference'] #'photos'중 첫번째꺼
                                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                                response_photo = requests.get(photo_url)
                                res_photo=response_photo.url
                                
                                destination.append(1)
                                destination.append(locations) # 검색한 지역이름
                                destination.extend(attractions)
                                destination.append(res_photo)
                            else:
                                destination.append(1)
                                destination.append(locations) # 검색한 지역이름
                                destination.extend(attractions)
                                destination.extend('No Image')
                            # 좌표
                            search_location_lat=(res_lo['results'][max_index]['geometry']['location']['lat'])
                            search_location_lng=(res_lo['results'][max_index]['geometry']['location']['lng'])
                            destination.append(search_location_lat)
                            destination.append(search_location_lng)
                        #검색데이터 결과가 빈 리스트로 오는 경우(=검색결과가 없을때) 텍스트 검색으로 다시 찾기
                        else: 
                            url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={locations_blank_text[0]}&key={api_key}"
                            response = requests.get(url)
                            data = response.json()
                            
                            attractions = []
                            max_reviewer = -1
                            max_index = -1
                            for i in range(len(res_lo)):
                                # 리뷰 수가 높은 순으로 정렬 필요
                                #print(i)
                                if('business_status' in data['results'][i]): #'business_status'가 없는 경우 분류
                                    if(data['results'][i]['business_status']=='OPERATIONAL'): #폐업인 경우 제외
                                        if 'rating' in data['results'][i]:
                                            name = data['results'][i]['name']
                                            rating = data['results'][i]['rating']
                                            reviews = data['results'][i]['user_ratings_total']
                                            if reviews >= max_reviewer:
                                                max_reviewer = reviews
                                                max_index = i
                                else:
                                    if 'rating' in data['results'][i]:
                                        name = data['results'][i]['name']
                                        rating = data['results'][i]['rating']
                                        reviews = data['results'][i]['user_ratings_total']
                                        if reviews >= max_reviewer:
                                            max_reviewer = reviews
                                            max_index = i
                                
                            name = data['results'][max_index]['name']
                            rating = data['results'][max_index]['rating']
                            reviews = data['results'][max_index]['user_ratings_total']

                            # 이름, 평점, 리뷰가 있는 것만 추가
                            if name is not None and rating is not None and reviews is not None:
                                if rating >= min_rating:
                                    attractions.append((name, rating, reviews))

                            if('photos' in data['results'][max_index]): # 'photos'가 아예없는 경우 제외
                                #사진 요청
                                photo_reference=data['results'][max_index]['photos'][0]['photo_reference'] #'photos'중 첫번째꺼
                                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                                response_photo = requests.get(photo_url)
                                res_photo=response_photo.url
                                attractions.append(res_photo)
                            else:
                                attractions.append('No Image')
                            
                            # 받아온 데이터가 공백리스트가 아닌 경우만 destination 리스트에 추가
                            if(attractions!=[]):
                                destination.append(1)
                                destination.append(locations) # 검색한 지역이름
                                destination.extend(attractions)
                                
                            # 좌표
                            search_location_lat=(data['results'][max_index]['geometry']['location']['lat'])
                            search_location_lng=(data['results'][max_index]['geometry']['location']['lng'])
                            destination.append(search_location_lat)
                            destination.append(search_location_lng)
            
        if(destination!=[]): # destination 안에 비어있는 경우 제외
            result_ex.append(destination)

    result_list.extend(result_ex)
    
    # [0 ,'검색한 장소=검색한 결과의 장소','평점','리뷰 수','사진링크','lat','lng']
    # [1 ,'검색한 장소','검색한 결과의 장소','평점','리뷰 수','사진링크','lat','lng']
    return result_list #최종 리턴값

# search_locations=['Tower of London', 'Westminster Abbey', 
#                   'Buckingham Palace', 'Churchill War Rooms', 
#                   'The British Museum', 'Canterbury Cathedral', 
#                   'Stonehenge', 'Roman Baths', "St. Paul's Cathedral", 
#                   'Edinburgh Castle']

#도쿄 애니메이션 여행
#search_locations=['J-World Tokyo(Ikebukuro, Tokyo, Japan)', 'Tokyo Anime Center(Chiyoda City, Tokyo, Japan)', 'Otome Road(Ikebukuro, Tokyo, Japan)']

#도쿄 애니메이션 여행
# search_locations=['Ghibli Museum(Mitaka, Tokyo, Japan)', 'Akihabara(Chiyoda City, Tokyo, Japan)', 'Odaiba(Minato City, Tokyo, Japan)', 
#                 'Nakano Broadway(Nakano, Tokyo, Japan)', 'Pokemon Center Tokyo(Chuo City, Tokyo, Japan)', 'J-World Tokyo(Ikebukuro, Tokyo, Japan)', 
#                 'Animate Ikebukuro(Toshima City, Tokyo, Japan)', 'Tokyo Anime Center(Chiyoda City, Tokyo, Japan)', 'Otome Road(Ikebukuro, Tokyo, Japan)', 
#                 'Shinjuku Wald 9(Shinjuku City, Tokyo, Japan)']
#search_locations=['J-World Tokyo(Ikebukuro, Tokyo, Japan)']
#search_locations=['Tokyo Disneyland(Urayasu, Chiba Prefecture, Japan)', 'Osaka Castle(Osaka, Japan)', 
#                   'Fushimi Inari Shrine(Kyoto, Japan)', 'Hiroshima Peace Memorial Park(Hiroshima, Japan)', 
#                   'Kinkaku-ji Temple(Kyoto, Japan)', 'Nagoya Castle(Nagoya, Aichi Prefecture, Japan)', 
#                   'Mount Fuji(Yamanashi Prefecture, Japan)', 'Universal Studios Japan(Osaka, Japan)', 
#                   'Shinjuku Gyoen National Garden(Shinjuku City, Tokyo, Japan)', 'Gunkanjima Island(Nagasaki, Japan)']
