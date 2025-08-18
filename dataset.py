import pandas as pd
import numpy as np

def refine_and_prepare_data(input_path, output_path):
    """
    Kaggle의 원본 데이터를 읽어와 정제하고, 피벗 테이블용 컬럼까지 추가하여
    하나의 최종 파일로 저장합니다.
    (chunksize 옵션을 사용하여 대용량 데이터 처리 최적화)
    """
    print(f"'{input_path}' 파일에서 데이터 처리를 시작합니다...")

    # --- 1. 데이터 정제 (refine_sales_data) ---
    try:
        chunk_iterator = pd.read_csv(input_path, encoding='ISO-8859-1', chunksize=10000)
    except FileNotFoundError:
        print(f"오류: '{input_path}' 파일을 찾을 수 없습니다.")
        return

    processed_chunks = []
    print("청크 단위로 데이터 정제 중...")
    for chunk in chunk_iterator:
        chunk.dropna(subset=['Customer ID'], inplace=True)
        chunk = chunk[chunk['Quantity'] > 0]
        chunk = chunk[chunk['Price'] > 0]
        chunk['Customer ID'] = chunk['Customer ID'].astype(int)
        chunk['InvoiceDate'] = pd.to_datetime(chunk['InvoiceDate'])
        chunk['TotalPrice'] = chunk['Quantity'] * chunk['Price']
        chunk['PaymentMethod'] = np.where(chunk['Customer ID'] % 2 == 0, '신용카드', '계좌이체')
        processed_chunks.append(chunk)
    
    print("모든 청크 정제가 완료되었습니다.")
    df = pd.concat(processed_chunks, ignore_index=True)
    
    print("\n--- 전체 데이터 정보 ---")
    df.info()

    df_refined = df[[
        'InvoiceDate', 'Invoice', 'Description', 'TotalPrice', 'PaymentMethod', 'Customer ID'
    ]].copy()
    df_refined.rename(columns={
        'InvoiceDate': '거래일자', 'Invoice': '주문번호', 'Description': '상품명',
        'TotalPrice': '판매금액', 'PaymentMethod': '결제수단', 'Customer ID': '고객ID'
    }, inplace=True)
    df_refined['판매금액'] = df_refined['판매금액'].astype(int)
    
    print("\n데이터 정제가 완료되었습니다.")

    # --- 2. 피벗 테이블용 데이터 가공 (prepare_data_for_pivot) ---
    print("\n피벗 테이블용 데이터 가공을 시작합니다...")
    
    # '거래일자'가 이미 datetime 형식이므로 추가 변환 필요 없음
    df_refined['연도'] = df_refined['거래일자'].dt.year
    df_refined['월'] = df_refined['거래일자'].dt.month
    df_refined['일'] = df_refined['거래일자'].dt.day
    weekday_map = {0: '월', 1: '화', 2: '수', 3: '목', 4: '금', 5: '토', 6: '일'}
    df_refined['요일'] = df_refined['거래일자'].dt.weekday.map(weekday_map)

    # --- 3. 최종 파일 저장 ---
    df_refined.to_excel(output_path, index=False)
    
    print(f"\n모든 데이터 처리가 완료되었습니다. '{output_path}' 파일을 확인하세요.")
    print("--- 최종 데이터 샘플 ---")
    print(df_refined.head())


# --- 스크립트 실행 ---
if __name__ == "__main__":
    refine_and_prepare_data('online_retail_II.csv', 'sales_data_for_pivot.xlsx')
