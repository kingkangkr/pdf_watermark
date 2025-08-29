import fitz  # PyMuPDF 라이브러리

# --- 설정 값 ---
INPUT_PDF = "sample.pdf"
OUTPUT_PDF = "watermarked_output.pdf"
LOGO_IMAGE = "logo.png"
# -------------

try:
    # 1. 원본 PDF와 로고 이미지 열기
    pdf_document = fitz.open(INPUT_PDF)
    logo = fitz.open(LOGO_IMAGE)

    # 2. 로고를 삽입할 위치와 크기(사각형) 정의하기
    #    각 페이지의 오른쪽 아래에 위치시킵니다.
    page_width = pdf_document[0].rect.width
    page_height = pdf_document[0].rect.height
    
    # 로고 크기 설정 (너비 100픽셀, 높이는 비율에 맞게 자동 조정)
    logo_width = 100
    logo_height = logo[0].rect.height * (logo_width / logo[0].rect.width)

    # 위치 계산: 오른쪽에서 20px, 아래에서 20px 떨어진 곳
    x_pos = page_width - logo_width - 20
    y_pos = page_height - logo_height - 20
    
    rect = fitz.Rect(x_pos, y_pos, x_pos + logo_width, y_pos + logo_height)

    # 3. 모든 페이지를 순회하며 로고 삽입하기
    for page in pdf_document:
        # insert_image() 함수를 사용해 로고를 삽입합니다.
        page.insert_image(rect, filename=LOGO_IMAGE)

    # 4. 워터마크가 추가된 새 PDF 파일로 저장하기
    pdf_document.save(OUTPUT_PDF)
    
    print(f"🎉 성공! '{INPUT_PDF}' 파일의 모든 페이지에 워터마크를 추가했습니다.")
    print(f"결과물은 '{OUTPUT_PDF}' 파일로 저장되었습니다.")

except FileNotFoundError as e:
    print(f"오류: 파일을 찾을 수 없습니다. '{e.filename}' 파일이 폴더에 있는지 확인해주세요.")
except Exception as e:
    print(f"알 수 없는 오류가 발생했습니다: {e}")
finally:
    # 파일 객체가 열려있으면 닫아줍니다.
    if 'pdf_document' in locals() and pdf_document.is_closed is False:
        pdf_document.close()
    if 'logo' in locals() and logo.is_closed is False:
        logo.close()