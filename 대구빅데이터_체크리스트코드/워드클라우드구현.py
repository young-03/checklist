print("\n","워드클라우드 생성중...")

okt = Okt()

def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)  # 특수문자 제거
    tokens = okt.nouns(text)  # 형태소 분석
    stopwords = ['시','목적','수','내','구매','스','도','전','직접','중','또','나','참고','추천','부분','층','글','등','사장','때','밍','게이','위','선택','점','용','암','제공','율',
                 '개','너','원','가지','것','체크','리스트','판매','사용','때문','차량','곳','분','대해','고려','방법','꼭','통해','신뢰','더','요구','지급','계약','여부','보상','경우',
                 '배상','구입','발생','요구','대한','문의','후','비','피','청구','및','이','그','저','의','그리고','그러나','하지만','그래서','또는','즉','다시','더욱','따라서','또한',
                 '에','에서','으로','로','와','과','을','를','은','는','이다','있다','없다','했다','한다','한다면','라고','이에','이와','이래서','이에따라','이곳','이런','이렇게','저기',
                 '저런','저렇게','그','요','우리','그녀','그들','먼저','녀석','누구','룰루','거','좀','제','이사','걸','고민','감','안','마음','무엇','어디','번','다른','기본','정도','이상','가장',
                 '손','약','하나','브이','확인','장','댓글','블로그','블로그','공감','살','로그','제품','저희','바로','가성','이동','여러분','생각','무','작성','다이소','지지','함','데',
                 '당신','어떻게','답변','가정','여러','기','장점','다음','터','큘','아래','위','활용','샘','중고','사항','단점','보고','사람','매장','동물','무용','미니','삭제','총','후기','언제',
                 '너무','아주','많이','적게','일부','모든','하고','정말','이용','감','짐','해','포스팅','옷','쇼핑','구매','준비']
    tokens = [word for word in tokens if word not in stopwords]  # 불용어 제거
    return tokens

df['tokens'] = df['내용'].apply(clean_text)

# 8. 키워드 추출 (빈도 분석)
all_tokens = sum(df['tokens'], [])  # 모든 토큰을 하나의 리스트로 결합
counter = Counter(all_tokens)
common_words = dict(counter.most_common(31))  # 상위 30개 단어 추출
print(common_words)


# 폰트 파일 경로 설정
font_path = 'C:\\Windows\\Fonts\\malgun.ttf'  # 폰트 파일 경로 설정
font_name = fm.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

words = list(common_words.keys())
frequencies = list(common_words.values())

top_15 = list(common_words.keys())[2:16]
print('\n','상위 15개의 단어','\n',top_15)

# 9. 워드클라우드 생성
x, y = np.ogrid[:300, :300]
mask = (x - 150) ** 2 + (y - 150) ** 2 > 140 ** 2
mask = 255 * mask.astype(int)

wordcloud = WordCloud(mask = mask, font_path='C:\\Windows\\Fonts\\malgunbd.ttf', width=800, height=400, background_color='white',colormap='viridis').generate_from_frequencies(common_words)
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

# 막대그래프 그리기
plt.figure(figsize=(10, 8))
plt.bar(words, frequencies, color='tab:purple')
plt.xlabel('키워드')
plt.xticks(rotation=45, ha='right')
plt.ylabel('빈도수')
plt.title('검색어 관련 단어 빈도수')
plt.show()

# 결과 출력
print("\n<제목과 출처 모음 10개>")
for i in range(0, min(10, len(titles))):
    print('\n',titles[i])
    print(links[i])
