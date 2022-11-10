# 텍스트 분석 간단 예제
이 레포지토리에서는 한국어 텍스트 분석을 위한 기초적인 예제 코드를 제공합니다. 예제 코드를 돌리기 위해서는 다음과 같은 요구 사항이 설치되어 있어야 합니다.

* Python3.6 이상
* kiwipiepy
* numpy

## KoreanSNS에서 분석용 텍스트 추출하기
https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=114 에서 데이터 전체를 다운 받을 수 있습니다.
압축 해제 후 다음 코드를 실행하여 텍스트 파일만 추출할 수 있습니다.

```console
# results 라는 폴더에 텍스트 파일을 저장할 예정
$ mkdir results 

# 압축 해제 후 파일들은 data 폴더 내에 있다고 가정
$ python3 extract_text_by_class.py results data/*.json 

# gender와 age 항목에 따라 텍스트를 나눠 저장하고 싶은 경우 --split_by 옵션을 사용할 수 있음
$ python3 extract_text_by_class.py results data/*.json --split_by gender age
```

## 형태소 분석 수행하기
```console
# 20대 여성 말뭉치를 형태소 분석할 경우
$ python3 tokenize_corpus.py results/여성.20대.txt > results/여성.20대.tokenized.txt
```

## NPMI를 이용한 2-gram 추출
```console
# 20대 여성 말뭉치 분석 결과에서 2-gram을 추출할 경우

$ python3 bigram_npmi.py results/여성.20대.tokenized.txt \
    --min_cnt 100
# 최소 100회 이상 등장한 2-gram만 사용
```

## 말뭉치 간 토큰 출현 비교하기
```console
# 20대 여성 vs 남성 간의 토큰 출현 차이를 비교할 경우

$ python3 frequent_tokens.py results/여성.20대.tokenized.txt \
    results/남성.20대.tokenized.txt \
    --mode pmi \
    --min_cnt 100 \
    --topn 20 \
    > 20대.성별간비교.pmi.txt 
# pmi를 사용하여 비교함
# 최소 100회 이상 등장한 토큰만 사용
# 상위 20개 토큰만 출력한다
# 비교 결과는 `20대.성별간비교.pmi.txt`에 저장됨
```
