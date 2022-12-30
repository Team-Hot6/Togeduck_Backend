![header](https://capsule-render.vercel.app/api?type=waving&color=auto&height=300&section=header&text=🐤Togeduck%&fontSize=90)
# 👋 We are Team-Hot6 👋
## 👨‍👩‍👧‍👦 팀원 소개
<table>
  <tr>
    <td align="center">
      <a href="https://github.com/94KJS">
        <sub><b>김준식</b></sub></a><br />
        <sub><b>Captin</b></sub></a><br />
        <a href="https://github.com/94KJS">🙍‍♂️</a>
    </td>
    <td align="center">
      <a href="https://github.com/9yuhyeon">
        <sub><b>김규현</b></sub></a><br />
        <sub><b>Member</b></sub></a><br />
        <a href="https://github.com/9yuhyeon">🙍‍♂️</a>
    </td>
    <td align="center">
      <a href="https://github.com/jihyun-cho-0">
        <sub><b>조지현</b></sub></a><br />
        <sub><b>Member</b></sub></a><br />
        <a href="https://github.com/jihyun-cho-0">🙍</a>
    </td>
    <td align="center">
      <a href="https://github.com/Carrotww">
        <sub><b>유형석</b></sub></a><br />
        <sub><b>Member</b></sub></a><br />
        <a href="https://github.com/Carrotww">🙍‍♂️</a>
    </td>
    <td align="center">
      <a href="https://github.com/sunmi-park">
        <sub><b>박선미</b></sub></a><br />
        <sub><b>Member</b></sub></a><br />
        <a href="https://github.com/sunmi-park">🙍</a>
    </td>
  </tr>
</table>

## 🏂 취미 공유 플랫폼
- 모임을 만들고 함께할 사람을 모집할 수 있는 workshop 기능 제공
- 사람들과 같은 관심사를 가지고 소통할 수 있는 community 기능 제공
- 편리한 모임 합류를 위한 채팅, 지도, 결제 기능 제공

## ⚒ 기술스택
- **개발언어** 
<div>
  <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=JavaScript&logoColor=white">
</div>

- **데이터베이스**
<div>
  <img src="https://img.shields.io/badge/SQLite3-003B57?style=for-the-badge&logo=SQLite&logoColor=white">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=PostgreSQL&logoColor=white">
</div>

- **개발환경**
<div>
  <img src="https://img.shields.io/badge/django rest framework-092E20?style=for-the-badge&logo=django&logoColor=white"> 
  <img src="https://img.shields.io/badge/django channels-83B81A?style=for-the-badge&logo=django&logoColor=white">
</div>

- **배포환경** 
<div>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white">
  <img src="https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=Ubuntu&logoColor=white">
  <img src="https://img.shields.io/badge/Daphne-092E20?style=for-the-badge&logo=Daphne&logoColor=white">
  <img src="https://img.shields.io/badge/NGINX-009639?style=for-the-badge&logo=NGINX&logoColor=white">
</div>
<div>
  <img src="https://img.shields.io/badge/EC2-FF9900?style=for-the-badge&logo=Amazon EC2&logoColor=white">
  <img src="https://img.shields.io/badge/aws s3-569A31?style=for-the-badge&logo=Amazon S3&logoColor=white">
  <img src="https://img.shields.io/badge/aws cloudfront-232F3E?style=for-the-badge&logo=Amazon AWS&logoColor=white">
</div>

## 🖼️ 와이어프레임
<img src="https://user-images.githubusercontent.com/113074921/207654055-4deed7a7-cf6e-452f-8746-f2442abe286c.png" width="700px" height="500px">

## 📋 ERD
https://www.erdcloud.com/d/aE5HXR2pEyvyvAHYr
<img src="https://user-images.githubusercontent.com/109906864/209798825-4eef219b-1da3-455c-b0df-a0e9c4ab274d.png" width="700px" height="500px">

## 📋 API 설계
https://www.notion.so/7b72107e734640e4b92d6305ec0db12b?v=c88e7821924c401ea4e8f2f9372e70f1
<img src="https://velog.velcdn.com/images/def3ff/post/566cf838-2456-4603-bc73-cbd211e409ba/image.jpg">


## ⭐ 커밋 컨벤션
 - create : 생성
 - update : 수정
 - delete : 삭제
 - temp : 임시

## 🌈 네이밍 컨벤션

### 👉 URL name 패턴 이름에는 언더바(_)를 사용
url(...
name='add_topping')

### 👉 클래스명은 CamelCase로 작성 (UserView)
class BlogWriter:
pass

### 👉 Variable, Function, Method의 이름은 underscore로 작성
def get_unique_voters():
pass

### 👉 Model Field 이름은 underscore로 
class Person(models.Model):
first_name = models.CharField(max_length=20)
last_name = models.CharField(max_length=40)

# 🕖 중간 점검 2022/12/02 ~ 2022/12/14
## 남은 기간 목표(달성한 목표는 체크박스에서 체크로 표시)
### 1. 기능 다듬기
- [x] Article app 과 Workshop app 에서 Category 별 최신순, 인기순 정렬 기능(CRUD 다듬기)

### 2. 목표 추가 기능
- [x] Kakao 지도 api를 이용한 워크샵 시행 위치를 사용자에게 직관적으로 제공
- [x] 소셜 로그인 도입으로 사용자 편의 증대
- [ ] 아임포트를 이용한 결제 모델 추가 or kakao 네이버 결제 api 도입 목표
- [ ] Chat app 읽은 채팅, 읽지 않은 채팅 식별과 채팅알림 기능 추가
- [x] django cron tab 을 이용한 실시간 인기 게시물 시간, 좋아요, 조회수의 점수를 조합하여 갱신

### 3. 수정될 디자인
- [x] 워크샵, 커뮤니티를 제외한 부분 전반적인 수정
- [x] 워크샵 커뮤니티 페이지 다듬기

### 4. 배포
- 실시간 채팅을 위해 미들웨어 ASGI를 사용하여 Gunicorn으로 배포 불가능
- [x] AWS 서버를 이용하여 Daphne를 이용한 배포 예정

# 🏹 Trouble Shooting
- docker의 volume이 지워지지 않아 migration 오류 발생 <br>
  해결 : docker system prune -a -volumes 명령어로 볼륨까지 모두 삭제 후 migration 진행<br>
- SSL 적용 후 채팅 기능 작동하지 않음 <br>
  해결 : 인증서는 Domain에 적용하였는데 Url은 IP 주소를 사용하여 발생한 문제로, IP 주소를 인증서가 적용된 Domain으로 변경하여 해결


# 💡 사용자 피드백 (개선 완료된 사항)
- 회원가입 시 카테고리를 선택했을 때 아무 효과가 없어서 카테고리가 선택되었는지 안되었는지 알 수가 없어요
- 회원가입 시 취미 카테고리를 더블 클릭하면 브라우저가 멈춰버려요
- 카카오 계정으로 로그인 시 네비바의 닉네임이 undefined로 표기되요
- 비로그인 사용자도 워크샵 생성 페이지 접근이 가능해요
- 회원탈퇴 기능이 있었으면 해요
- 워크샵 상세 페이지에서 문의하기(채팅) 클릭 시 채팅창이 상세 페이지 내 지도 뒤에서 보여져요
- 워크샵 생성 페이지의 지역 선택 항목에서 인천 지역이 없어요
- 워크샵 생성 시 각 항목에 어떤 것들을 입력해야할지 입력 창에 적혀있으면 좋을 것 같아요
- 워크샵 생성 시 참가비, 참가인원을 1000000000000000000000000000 으로 하면 생성이 안되고 모든 항목을 작성하라는 메시지만 나와요
- 메인 페이지에서 인기 워크샵의 제목이 양 옆으로 겹쳐 보이는 것들이 있어요
- 댓글의 작성 날짜/시간이 너무 길게 표기되요/ 2022-12-23(T01:15:14.558129)
- 커뮤니티의 게시글에 이미지가 엑박으로 보여져요
- 커뮤니티의 게시글 순서 초기값이 최신순으로 정렬되면 좋겠어요
- 비로그인 사용자가 댓글 작성 및 추천하기 클릭 시 401 alert 창이 떠요
- 워크샵의 지역이 도 단위로 구성되어 있는데 보다 상세하게 나누는게 좋을 것 같아요
- 워크샵에 댓글 작성 후 입력 창이 유지되는데 작성 및 수정 할 때만 입력 창이 보이면 좋을 것 같아요

# 시연영상 링크
https://vimeo.com/784742380
