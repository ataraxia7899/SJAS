# 📄 프로젝트: SJAS (Sales Journal Automation System)

## 🖥️ 프로젝트 소개

이 프로젝트는 Kaggle의 "Online Retail II" 데이터셋을 활용하여 대용량 판매 기록 데이터를 효율적으로 처리하고 분석 가능한 형태로 정제하는 **데이터 전처리 자동화 시스템**입니다. `pandas` 라이브러리의 `chunksize` 옵션을 활용하여 메모리 사용량을 최적화하였고, 이를 통해 저사양 환경에서도 안정적으로 대용량 데이터를 처리할 수 있도록 설계되었습니다.

## 📢 구현한 기능

### 1\. 대용량 데이터 처리 최적화

  - `pandas`의 `chunksize` 옵션을 사용하여 전체 데이터셋을 메모리에 한 번에 로드하지 않고, 작은 조각(chunk) 단위로 나누어 처리합니다.
  - 이를 통해 파일 크기가 큰 경우 발생할 수 있는 메모리 부족 현상을 방지하고 자원 소비를 최소화했습니다.

### 2\. 데이터 정제 (Data Cleansing)

  - **결측치 처리**: 분석에 필수적인 `Customer ID`가 없는 행을 제거합니다.
  - **이상치 제거**: 수량(`Quantity`)과 단가(`Price`)가 0 이하인 비정상적인 거래 데이터를 필터링합니다.
  - **데이터 타입 변환**: `Customer ID`를 정수형으로, `InvoiceDate`를 날짜/시간(datetime) 형식으로 변환하여 데이터의 일관성을 확보합니다.

### 3\. 데이터 가공 및 생성 (Data Transformation & Feature Engineering)

  - **파생 변수 생성**:
      - `TotalPrice`: `Quantity`와 `Price`를 곱하여 각 거래의 총 판매 금액을 계산합니다.
      - `PaymentMethod`: `Customer ID`를 기반으로 '신용카드'와 '계좌이체' 결제 수단을 임의로 생성하여 데이터를 풍부하게 만듭니다.
  - **피벗 테이블용 데이터 준비**:
      - `InvoiceDate`에서 연, 월, 일, 요일 정보를 추출하여 시계열 분석 및 다양한 기준의 집계가 용이하도록 새로운 컬럼을 추가합니다.

## 🛠️ 기술 스택

  - **Python**: 데이터 처리 로직의 주요 구현 언어입니다.
  - **Pandas**: 데이터 조작, 정제 및 분석을 위한 핵심 라이브러리입니다.
  - **NumPy**: 효율적인 수치 계산 및 배열 처리를 위해 사용되었습니다.

## 📂 디렉토리 구조

```
📦 SJAS_Project/
├── 📄 dataset.py           # 데이터 전처리 및 가공 메인 스크립트
├── 📄 online_retail_II.csv # 원본 데이터셋 (Kaggle "Online Retail II")
├── 📄 requirements.txt     # 프로젝트 실행에 필요한 라이브러리 목록
├── 📄 .gitignore           # Git 버전 관리에서 제외할 파일 목록
```

### 📁 주요 파일 설명

  - `dataset.py`: `online_retail_II.csv` 파일을 청크 단위로 읽어들여 정제 및 가공을 수행하고, 최종 분석용 데이터를 준비하는 모든 로직을 포함합니다.
  - `online_retail_II.csv`: 2009년부터 2011년까지의 온라인 소매 거래 원본 데이터입니다.
  - `requirements.txt`: `pip`를 통해 프로젝트에 필요한 `pandas`, `numpy`, `openpyxl` 라이브러리를 설치하기 위한 파일입니다.
  - `자체평가.txt`: 메모리 최적화 등 이 프로젝트에서 중점적으로 해결한 문제에 대한 설명이 담겨 있습니다.

## 🏃‍♂️ 로컬 개발 및 실행 방법

### 1\. 필요 라이브러리 설치

프로젝트 폴더 내에서 다음 명령어를 실행하여 필요한 라이브러리를 설치합니다.

```bash
pip install -r requirements.txt
```

### 2\. 스크립트 실행

Python 환경에서 `dataset.py` 스크립트를 실행합니다. 스크립트 내 `refine_and_prepare_data` 함수의 인자에 원본 데이터 파일 경로와 저장할 파일 경로를 지정해야 합니다.

```python
# dataset.py 파일 예시
# ... (함수 정의) ...

# 스크립트 실행 부분
if __name__ == "__main__":
    input_csv_path = 'online_retail_II.csv'
    output_csv_path = 'refined_sales_data.csv' # 결과가 저장될 파일명
    refine_and_prepare_data(input_csv_path, output_csv_path)

```

위와 같이 스크립트를 수정한 후, 터미널에서 다음 명령어를 실행합니다.

```bash
python dataset.py
```