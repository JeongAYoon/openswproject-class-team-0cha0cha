import googlemaps
import folium
import webbrowser
import requests
from apikey import GoogleMap_API_KEY
from geopy.distance import geodesic

#lat,lon구하기
# def FindLatLon(site):
#     lat=[]
#     lon=[]
#
#     #지점 개수
#     n=len(site)
#
#
#     # Geocoding API 엔드포인트
#     geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json'
#
#     #site 별 좌표 찾기
#     for i in range(n):
#
#         wanted=site[i]
#
#         # 요청 파라미터
#         params = {
#             'address': wanted,
#             'key': GoogleMap_API_KEY,
#         }
#
#         # geocode API 요청 보내기
#         response = requests.get(geocode_url, params=params)
#
#         # 응답 처리, 좌표 구하기
#         if response.status_code == 200:
#             data = response.json()
#             if data['status'] == 'OK':
#                 # 첫 번째 결과의 좌표 얻기
#                 location = data['results'][0]['geometry']['location']
#                 lat.append(location['lat'])
#                 lon.append(location['lng'])
#             else:
#                 print('장소를 찾을 수 없습니다.')
#         else:
#             print('API 요청 실패')
#
#     return lat,lon,gmaps,n

# 지점 저장
# def ReturnPoint(lat,lon,n):
#     point = []
#     for i in range(n):
#         point.append([lat[i], lon[i]])
#     return point

#시작점, 도착점 설정 및 경유지 리스트 생성
def FindOriDes(point,n):
    loong=0
    temp=[]
    temp.extend(point)
    index_ori = 0
    index_dest = 0
    for i in range(n-1):
        j=i+1
        for j in range(j,n):
            distance = geodesic(temp[i], temp[j]).meters
            if(distance > loong):
                loong=distance
                origin=temp[i]
                index_ori = i
                destination=temp[j]
                index_dest = j
                a=i
                b=j
        if (i==n-2):
            del(temp[a])
            del(temp[b-1])
    return origin,destination,temp, index_ori, index_dest

#맵 생성
def CreateMap(origin):
    map = folium.Map(location=origin, zoom_start=11)
    return map

#마커찍기
def mark(map,point,names, n):
    for i in range(n):
        folium.Marker([point[i][0],point[i][1]],popup=names[i]).add_to(map) # popup= 으로 위에 글 띄우기 가능

#경로 그리기
def DrawDirec(origin,destination,locations,gmaps,map,opt,n):

    directions_response=gmaps.directions(origin,destination,mode='driving',waypoints=locations,optimize_waypoints = opt)

    if len(directions_response) > 0 and 'legs' in directions_response[0]:

        for i in range(n-1):
            route = directions_response[0]['legs'][i]

            points = []
            for step in route['steps']:
                start = (step['start_location']['lat'], step['start_location']['lng'])
                end = (step['end_location']['lat'], step['end_location']['lng'])
                points.extend([start, end])

            for i in range(len(points)-1):
                if (i==0):
                    locate.append(points[0])#0
                locate.append(((points[i][0]+points[i+1][0])/2,(points[i][1]+points[i+1][1])/2)) #2
                locate.append(points[i+1])#3
            
                
            if (len(locate) <= 100):
                snapped_points = gmaps.snap_to_roads(locate, interpolate=True)
                locate = [(point['location']['latitude'], point['location']['longitude']) for point in snapped_points]
            folium.PolyLine(locate, color='blue', weight=5).add_to(map)



        if opt == 1: ##### 디렉션 리스폰스에서, 정렬된 데이터 관련 응답. 단, 웨이포인트 오더로 인한 갯수 오류가 있을지 우려됨
            return directions_response[0]['waypoint_order']

    else:
        print("No directions found")


# HTML 파일로 저장
def ReturnHTML(map):
    map.save('route.html')

    return 'route.html'

# 생성된 HTML 파일 열기
def OpenMap(html):
    webbrowser.open(html)

# 총괄 함수
def MainFunc(point,names, opt=0,retry = 0):
    if retry >= 3:
        return "-99"
    try:
        n=len(point)
        gmaps = googlemaps.Client(key=GoogleMap_API_KEY)
        locations=[]
        # 시작점, 도착점
        if (opt==1):
            origin,destination,locations, index_ori, index_dest=FindOriDes(point,n)
        else:
            origin=point[0]
            destination=point[n-1]
            for i in range(1,n-1):
                locations.append(point[i])

        # 맵 시작지점과 비율 관련 조절 관련 생각######
        # zoom = int(geodesic(origin, destination).meters / 50000)
        # mid_x = (origin[0] + destination[0]) / 2 # mid 대신 다른걸 찾는 방법 생각해봐야함
        # mid_y = (origin[1] + destination[1]) / 2
        # mid = (mid_x,mid_y)
        map=CreateMap(origin)

        #마커 찍기 함수
        mark(map,point,names, n)

        if opt == 1: # 웨이포인트 오더 데이터 정리 부분
            real_waypoint_order = [0, 0, 0, 0, 0]
            waypoint_order = DrawDirec(origin,destination,locations,gmaps,map,opt,n)
            temp_p = point[:]
            real_waypoint_order[0] = index_ori

            real_waypoint_order[4] = index_dest

            temp_p[index_ori] = (-1,)
            temp_p[index_dest] = (-1,)
            for i in range(len(waypoint_order)):
                k = 0
                j = 0
                while 1:
                    if temp_p[j] == (-1,):
                        j += 1
                        continue
                    if waypoint_order[i] == k:
                        break
                    else:
                        j += 1
                        k += 1
                real_waypoint_order[1 + i] = j

            html = ReturnHTML(map)
            return [html, real_waypoint_order]
        else:
            DrawDirec(origin, destination, locations, gmaps, map, opt, n)
            html=ReturnHTML(map)
            # OpenMap(html)
            return html
    except:
        retry += 1
        print("google map error")
        return MainFunc(point,names, opt,retry)
