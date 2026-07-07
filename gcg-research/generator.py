#!/usr/bin/env python3
"""GenCG .gcg 생성기 (역설계 기반, 2026-07-07)
사용: python3 generator.py template.gcg out.gcg 가사.txt
  가사.txt: 빈 줄 = 페이지 구분, 줄 = 그대로 줄
구조: [공통헤더 C][페이지블록×N][트레일러 140B]
  - C 길이는 템플릿마다 계산: 같은 기기의 (1페이지, 1글자) 파일과 (2페이지) 파일 diff로 도출
    → 이 기기(교회 컴퓨터): C=59953
  - 0x9f (u8) = 전체 줄 수 + 2  (빈 페이지=1줄)
  - 텍스트 오브젝트(1페이지 파일 절대 오프셋):
    x@0x15b86 y@0x15b8a w@0x15b96 h@0x15b9a fontsize@~0x15bbf
    count@0x15bc3 = 글자수+1
    첫 글자 레코드@0x15bc7, 2번째부터 연속 배열@0x15c36
    레코드 = <HII>(UTF-16 코드, 0, 1) — 공백(0x20)·줄바꿈(0x0D)도 레코드
  - 글자색 #E5E5E5 / 테두리 #252525 (RGBA, 오브젝트 안)
  - 글자수 변경 시 갱신: count, width(비례 스케일), height(줄수 비례)
  - 썸네일(160px RGB565, 블록 중간)은 안 고쳐도 열림(미리보기만 낡음)
"""
import struct, sys

C_LEN, TRAILER, PAGECNT = 59953, 140, 0x9f
O_W,O_H,O_CNT,O_FIRST,O_ARRAY = 0x15b96,0x15b9a,0x15bc3,0x15bc7,0x15c36
U0 = 10.5  # 템플릿 최장줄 폭 단위 (한글1/공백0.5)

def units(l): return sum(0.5 if c==' ' else 1 for c in l)

def make(template: bytes, pages):
    T=template
    BS=len(T)-C_LEN-TRAILER; X=len(T)-TRAILER
    block0=T[X-BS:X]
    rel=lambda a:a-(X-BS)
    R_W,R_H,R_CNT,R_FIRST,R_ARR=map(rel,[O_W,O_H,O_CNT,O_FIRST,O_ARRAY])
    N0=struct.unpack_from('<I',block0,R_CNT)[0]-1
    W0=struct.unpack_from('<I',block0,R_W)[0]
    H0=struct.unpack_from('<I',block0,R_H)[0]
    out=bytearray(T[:X-BS]); total=0
    for lines in pages:
        chars='\r'.join(lines); N=len(chars)
        b=bytearray(block0)
        struct.pack_into('<I',b,R_CNT,N+1)
        struct.pack_into('<I',b,R_W,max(1,round(W0*max(map(units,lines))/U0)))
        struct.pack_into('<I',b,R_H,round(H0*len(lines)/2))
        struct.pack_into('<H',b,R_FIRST,ord(chars[0]))
        arr=b''.join(struct.pack('<HII',ord(c),0,1) for c in chars[1:])
        out+=bytes(b[:R_ARR])+arr+bytes(b[R_ARR+10*(N0-1):])
        total+=len(lines)
    out[PAGECNT]=2+total
    out+=T[X:]
    return bytes(out)

if __name__=='__main__':
    tpl=open(sys.argv[1],'rb').read()
    txt=open(sys.argv[3],encoding='utf-8').read().replace('\r','')
    pages=[[l for l in blk.split('\n') if l.strip()] for blk in txt.split('\n\n') if blk.strip()]
    open(sys.argv[2],'wb').write(make(tpl,pages))
    print(f"{sys.argv[2]}: {len(pages)}페이지 생성")
