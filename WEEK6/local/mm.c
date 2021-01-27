/*
 * mm-naive.c - The fastest, least memory-efficient malloc package.
 * 
 * In this naive approach, a block is allocated by simply incrementing
 * the brk pointer.  A block is pure payload. There are no headers or
 * footers.  Blocks are never coalesced or reused. Realloc is
 * implemented directly using mm_malloc and mm_free.
 *
 * NOTE TO STUDENTS: Replace this header comment with your own header
 * comment that gives a high level description of your solution.
 */
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <unistd.h>
#include <string.h>

#include "mm.h"
#include "memlib.h"

/*********************************************************
 * NOTE TO STUDENTS: Before you do anything else, please
 * provide your team information in the following struct.
 ********************************************************/
team_t team = {
    /* Team name */
    "ateam",
    /* First member's full name */
    "Harry Bovik",
    /* First member's email address */
    "bovik@cs.cmu.edu",
    /* Second member's full name (leave blank if none) */
    "",
    /* Second member's email address (leave blank if none) */
    ""};

/* single word (4) or double word (8) alignment */
#define ALIGNMENT 8
/* rounds up to the nearest multiple of ALIGNMENT */
#define ALIGN(size) (((size) + (ALIGNMENT - 1)) & ~0x7)
// ALIGNMNET의 배수만큼 블록을 할당해야 할 때, 내가 할당 받고자 하는 워드 수에서 반올림해서 가장 가까운 8의 배수
#define SIZE_T_SIZE (ALIGN(sizeof(size_t)))

//******MACROs*************//
/* Basic constants and macros */
#define WSIZE 4 /* Word and header/footer size (bytes) */
#define DSIZE 8 /* Double word size (bytes) */

#define CHUNKSIZE (1 << 12) /* Extend heap by this amount (bytes) */ //Heap size; 2^12 = 4KB; 2^10=KB, 2^20=MB, 2^30=GB           \
                                                                     //?? page의 maximum size: 가상 메모리를 나눠둔 것 \
                                                                     //Heap을 연장할 때 사용할 기본 사이즈
#define MAX(x, y) ((x) > (y) ? (x) : (y))

/* Pack a size and allocated bit into a word */
#define PACK(size, alloc) ((size) | (alloc)) //그림 9.37같은 것들에서 (16/1) 이 부분을 나타냄 \
                                             //해당 블럭의 사이즈와, allocation을 저장           \
                                             //0x00000018 | 0x1 이 설명 있는 것이랑 비슷! 앞쪽이 사이즈, 뒷쪽이 allocation 비트

/* Read and write a word at address p */
#define GET(p) (*(unsigned int *)(p))
#define PUT(p, val) (*(unsigned int *)(p) = (val))

/* Read the size and allocated fields from address p */
#define GET_SIZE(p) (GET(p) & ~0x7) // ~은 not이라는 뜻. 2 진수로 7은 000...000111 인데 ~00...00111은 11...11000이다. \
                                    // & 연산을 사용해서 비트연산을 하면 뒤에서부터 세번째 비트 이상의 수들중에서 1인 비트만 뽑아낼 수 있다!
#define GET_ALLOC(p) (GET(p) & 0x1) // 젤 마지막 비트만 확인하면 되니깐, 0000...00001이랑 &연산을 하면       \
                                    //앞의 자리는 다 0이 되고 마지막 비트만 0이나 1 둘 중 하나를 갖는다. \
                                    //가장 마지막 자리수는 1의 자리수니깐 1이면 연산결과가 1, 0이면 연산결과도 0

/* Given block ptr bp, compute address of its header and footer */
#define HDRP(bp) ((char *)(bp)-WSIZE)                        //bp(payload의 첫번째 주소) 보다 한칸 앞에 가리키는 칸 HEADER pointer찾기
#define FTRP(bp) ((char *)(bp) + GET_SIZE(HDRP(bp)) - DSIZE) //footer pointer찾기.                                                            \
                                                             //bp에서부터 header에서 찾은 block의 사이즈만큼 뒤로 간 다음에 \
                                                             //한 칸 앞으로

/* Given block ptr bp, compute address of next and previous blocks */
#define NEXT_BLKP(bp) ((char *)(bp) + GET_SIZE(((char *)(bp)-WSIZE))) //헤더에서 getsize해서 블록 사이즈 만큼 뒤로 간다!
#define PREV_BLKP(bp) ((char *)(bp)-GET_SIZE(((char *)(bp)-DSIZE)))   // 앞의 블록의 footer에서 앞의 블록의 사이즈를 얻고 그 만큼 앞으로 가면 됨

/* 
 * mm_init - initialize the malloc package.
 */
int mm_init(void)
{
    //heap_listp 선언부: 그림 9.42/ prologue block의 중간을 가리킨다.
    /* Create the initial empty heap */
    if ((heap_listp = mem_sbrk(4 * WSIZE)) == (void *)-1) //meme_sbrk: 4 * WSIZE 만큼      //heap에서 공간을 할당 받아오는 것을 실패했을 때
        return -1;
    //그림 9.37 참고
    PUT(heap_listp, 0); /* Alignment padding */                          //젤 처음에 할당하는 미사용 패딩 워드
    PUT(heap_listp + (1 * WSIZE), PACK(DSIZE, 1)); /* Prologue header */ //힙의 처음을 나타내는 프롤로그 헤더
    PUT(heap_listp + (2 * WSIZE), PACK(DSIZE, 1)); /* Prologue footer */ //힙의 처음 나타내는 프롤로그 풋터
    PUT(heap_listp + (3 * WSIZE), PACK(0, 1)); /* Epilogue header */     //에필로그 설정

    heap_listp += (2 * WSIZE); //프롤로그 블록들 사이로 포인터를 옮겨준다.
                               //현재 포인터는 힙의 가장 아랫쪽을 가리키고 있음.
                               //alignment padding, prologue footer 뒤로 포인터를 위치시켜야 하니깐 두 칸 뒤로!

    /* Extend the empty heap with a free block of CHUNKSIZE bytes */
    if (extend_heap(CHUNKSIZE / WSIZE) == NULL) //아직 힙에 메모리를 배정하지 않았기 때문에 현재까지는 4워드.어라인패딩,프롤로그 헤더,풋터,에필로그 이렇게 4개
        return -1;                              //CHUNCKSIZE만큼 힙을 늘려준다.
    return 0;
}

static void *extend_heap(size_t words)
{
    char *bp;
    size_t size;

    /* Allocate an even number of words to maintain alignment */
    size = (words % 2) ? (words + 1) * WSIZE : words * WSIZE; //할당하고자 하는 워드의 수가,홀수이면 짝수로 만들어준다. 더블워드정렬 때문에!
    if ((long)(bp = mem_sbrk(size)) == -1)                    //mem_sbrk로 heap을 늘려준다. 실패하면 -1을 return
        return NULL;

    /* Initialize free block header/footer and the epilogue header */
    PUT(HDRP(bp), PACK(size, 0)); /* Free block header */           //현재 헤드를 0으로 프리시켜줌
    PUT(FTRP(bp), PACK(size, 0)); /* Free block footer */           //현재 풋터를 0으로 프리시켜줌
    PUT(HDRP(NEXT_BLKP(bp)), PACK(0, 1)); /* New epilogue header */ //다음 블럭의 마지막을 에필로그 블록으로 만들어줌

    /* Coalesce if the previous block was free */
    return coalesce(bp); //일단 extend_heap을 했으니깐 heap size는 늘려놨고
                         // 현재 bp의 앞뒤를 살펴봐서 끊겨있는 부분이 있으면 연결한다.(coalesce가 원래 하는 일)
}

/* 
 * mm_malloc - Allocate a block by incrementing the brk pointer.
 *     Always allocate a block whose size is a multiple of the alignment.
 */
void *mm_malloc(size_t size)
{
    //여기는 JUNGLE에서 제공해준 함수
    // int newsize = ALIGN(size + SIZE_T_SIZE);
    // void *p = mem_sbrk(newsize);
    // if (p == (void *)-1)
    //     return NULL;
    // else
    // {
    //     *(size_t *)p = size;
    //     return (void *)((char *)p + SIZE_T_SIZE);
    // }

    size_t asize; /* Adjusted block size */                  //헤더랑 푸터까지 붙인 블록 사이즈. 그래서 adjust라고 함.
    size_t extendsize; /* Amount to extend heap if no fit */ //extend 해야하면 얼마나 더 extend 해야하는가?를 결정해주는 것
    char *bp;

    /* Ignore spurious requests */
    if (size == 0)
        return NULL;

    /* Adjust block size to include overhead and alignment reqs. */
    if (size <= DSIZE)
        asize = 2 * DSIZE; // 2* double word size
                           //header 랑 footer가 들어가면 이미 8 byte는 써버렸지만
                           //중간에 데이터를 쓰려면 적어도 8보다는 크고 8의 배수 여야 하니깐 적어도 16 (더블 워드의 두 배)
    else
        asize = DSIZE * ((size + (DSIZE) + (DSIZE - 1)) / DSIZE); //header랑 footer 더한게 (DSIZE) 더해준거고,
                                                                  //(DSIZE) 더해서 /(DSIZE)로 나눠준건, 8의 배수로 round up 한 거

    /* Search the free list for a fit */
    if ((bp = find_fit(asize)) != NULL) //find_fit은 first fit으로 구현되어있다!!! 답지에 있음!
    {
        place(bp, asize);       //블록을 할당한다.(쪼개서 할당할 건지 전부다 할당한건지 검사후 할당)
        return bp;
    }

    //위에서 find_fit으로 할당할 곳을 찾았다면 return으로 함수가 끝나고 여기까지 오지 않았을텐데,
    //할당할 곳을 찾지 못해 여기까지 왔으니깐, heap을 extend 한다.
    /* No fit found. Get more memory and place the block */
    extendsize = MAX(asize, CHUNKSIZE); //그냥은 chunksize만큼 늘리는데, 요청한 사이즈가 더 크면 요청한 사이즈만큼 늘린다.
    if ((bp = extend_heap(extendsize / WSIZE)) == NULL) //위에서 결정된 만큼 늘린다.
        return NULL;
    place(bp, asize);   //다시 할당받는다!!
    return bp;
}

/*
 * mm_free - Freeing a block does nothing.
 */
void mm_free(void *ptr)
{
    size_t size = GET_SIZE(HDRP(bp)); //이제 비울 블록의 사이즈를 알아낸다!
    PUT(HDRP(bp), PACK(size, 0));
    PUT(FTRP(bp), PACK(size, 0));
    coalesce(bp); //지금 비운 블록 앞뒤로 검사해서 비어있으면 합친다!
}

static void *coalesce(void *bp)
{
    size_t prev_alloc = GET_ALLOC(FTRP(PREV_BLKP(bp)));
    size_t next_alloc = GET_ALLOC(HDRP(NEXT_BLKP(bp)));
    size_t size = GET_SIZE(HDRP(bp));
    if (prev_alloc && next_alloc)
    { /* Case 1 */
        return bp;
    }
    else if (prev_alloc && !next_alloc)
    { /* Case 2 */
        size += GET_SIZE(HDRP(NEXT_BLKP(bp)));
        PUT(HDRP(bp), PACK(size, 0));
        PUT(FTRP(bp), PACK(size, 0));
    }
    else if (!prev_alloc && next_alloc)
    { /* Case 3 */
        size += GET_SIZE(HDRP(PREV_BLKP(bp)));
        PUT(FTRP(bp), PACK(size, 0));
        PUT(HDRP(PREV_BLKP(bp)), PACK(size, 0));
        bp = PREV_BLKP(bp);
    }
    else
    { /* Case 4 */
        size += GET_SIZE(HDRP(PREV_BLKP(bp))) +
                GET_SIZE(FTRP(NEXT_BLKP(bp)));
        PUT(HDRP(PREV_BLKP(bp)), PACK(size, 0));
        PUT(FTRP(NEXT_BLKP(bp)), PACK(size, 0));
        bp = PREV_BLKP(bp);
    }
    return bp;
}

/*
 * mm_realloc - Implemented simply in terms of mm_malloc and mm_free
 */
void *mm_realloc(void *ptr, size_t size) //범규님과 다름!
{
    void *oldptr = ptr;
    void *newptr;
    size_t copySize;

    newptr = mm_malloc(size);
    if (newptr == NULL)
        return NULL;
    copySize = *(size_t *)((char *)oldptr - SIZE_T_SIZE); //헤더랑 풋터 자른 현재 블록의 사이즈! 진짜 데이터만 들어가는 사이즈
    if (size < copySize)
        copySize = size;
    memcpy(newptr, oldptr, copySize); //old ptr에서 copysize만큼 newptr로 copy한다.
    mm_free(oldptr);                  //old ptr과
    return newptr;
}

static void *find_fit(size_t asize)
{
    /* First fit search */
    void *bp;
    for (bp = heap_listp; GET_SIZE(HDRP(bp)) > 0; bp = NEXT_BLKP(bp)) //heap_listp: 힙 시작점, 다음 헤더들을 차례로 돌면서 빈자리 체크
    {
        if (!GET_ALLOC(HDRP(bp)) && (asize <= GET_SIZE(HDRP(bp))))  //헤더들을 차례로 검사하면서
                                                                    //블록이 차 있지 않고
                                                                    //블록 사이즈가 asize보다 크거나 같으면 그 bp를 return
        {
            return bp;
        }
    }
    return NULL; /* No fit */
}


//현재 할당하려고 하는 블록의 사이즈와 할당 받고 싶어하는 사이즈을 비교해서
//할당을 하고도 남은 블록이 사용가능하면 할당 받고 싶어하는 만큼만 쪼개서 할당하고
//남은 부분이 별 필요없는 짜투리가 될 것 같으면 그냥 그 블록을 통채로 할당해준다.
static void place(void *bp, size_t asize)   
{
    size_t csize = GET_SIZE(HDRP(bp));      //할당당할 블록의 사이즈를 검사해본다.
    if ((csize - asize) >= (2 * DSIZE))     //할당 받고 싶은 사이즈(asize)와 현 블록의 사이즈를 비교해서 ..
                                            //2*더블 워드 이상 남으면 쪼개서 할당
    {
        PUT(HDRP(bp), PACK(asize, 1));      //현재 블록의 bp부터
        PUT(FTRP(bp), PACK(asize, 1));      //asize만큼 뒤로 가서 할당
        bp = NEXT_BLKP(bp);                 //다음 블록의 헤더로 bp를 이동시킨 다음에
        PUT(HDRP(bp), PACK(csize - asize, 0));  //그 블록은 빈칸으로 헤더 설정
        PUT(FTRP(bp), PACK(csize - asize, 0));  //빈칸으로 풋터 설정
    }
    else                                    //남은 공간이 그리 많지 않다면, 그냥 그 블록전체를 할당
    {
        PUT(HDRP(bp), PACK(csize, 1));
        PUT(FTRP(bp), PACK(csize, 1));
    }
}