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

// mdriver 구동을 위한 team정보 struct 설정
team_t team = {
    /* Team name */
    "jungle",
    /* First member's full name */
    "Saihim Cho",
    /* First member's email address */
    "SaihimCho@kaist.ac.kr",
    /* Second member's full name (leave blank if none) */
    "",
    /* Second member's email address (leave blank if none) */
    ""};

// *** Variables *** //
#define WSIZE 4 // word and header footer 사이즈를 byte로.
#define DSIZE 8 // double word size를 byte로
#define CHUNKSIZE (1 << 12)

static char *heap_listp = 0;
static char *free_listp = 0;
static char *start_nextfit = 0;

//****** MACROS ******* //
#define MAX(x, y) ((x) > (y) ? (x) : (y))

// size를 pack하고 개별 word 안의 bit를 할당 (size와 alloc을 비트연산)
#define PACK(size, alloc) ((size) | (alloc))

/* address p위치에 words를 read와 write를 한다. */
#define GET(p) (*(unsigned int *)(p))
#define PUT(p, val) (*(unsigned int *)(p) = (val))

// address p위치로부터 size를 읽고 field를 할당
#define GET_SIZE(p) (GET(p) & ~0x7)
#define GET_ALLOC(p) (GET(p) & 0x1)

/* given block ptr bp, 그것의 header와 footer의 주소를 계산*/
#define HDRP(bp) ((char *)(bp)-WSIZE)
#define FTRP(bp) ((char *)(bp) + GET_SIZE(HDRP(bp)) - DSIZE)

/* GIVEN block ptr bp, 이전 블록과 다음 블록의 주소를 계산*/
#define NEXT_BLKP(bp) ((char *)(bp) + GET_SIZE(((char *)(bp)-WSIZE)))
#define PREV_BLKP(bp) ((char *)(bp)-GET_SIZE(((char *)(bp)-DSIZE)))

//EXPLICIT ADDRESS ARRAY
#define GET_PREV_PTR(bp) (*(char **)(bp))
#define GET_NEXT_PTR(bp) (*(char **)(bp + WSIZE))

#define PUT_PREV_PTR(bp, qp) (GET_PREV_PTR(bp) = qp)
#define PUT_NEXT_PTR(bp, qp) (GET_NEXT_PTR(bp) = qp)

//****** Function headers ******* //
int mm_init(void);
void mm_free(void *bp);

void *mm_malloc(size_t size);
void *mm_realloc(void *ptr, size_t size);

static void place(void *bp, size_t asize);
static void *extend_heap(size_t words);
static void *coalesce(void *bp);
static void *find_fit(size_t asize);

static void insert_in_freelist(void *bp);
static void remove_from_freelist(void *bp);

/* 
 * mm_init - initialize the malloc package.
 */
int mm_init(void)
{
    printf("*** mm_init **** \n");

    /* create 초기 빈 heap*/
    if ((heap_listp = mem_sbrk(4 * WSIZE)) == (void *)-1)
    {
        return -1;
    }
    PUT(heap_listp, 0);
    PUT(heap_listp + (1 * WSIZE), PACK(DSIZE, 1));
    PUT(heap_listp + (2 * WSIZE), PACK(DSIZE, 1));
    PUT(heap_listp + (3 * WSIZE), PACK(0, 1));
    
    free_listp = heap_listp + 2*WSIZE;
    heap_listp += (2 * WSIZE);

    start_nextfit = heap_listp;

    printf("free_listp: %p\n", (free_listp));
    printf("heap_listp: %p\n", (heap_listp));



    if (extend_heap(CHUNKSIZE / WSIZE) == NULL)
        return -1;

    printf("successed extend_heap: \n");
    printf("pre, next: %p, %p\n", GET_PREV_PTR(free_listp),GET_NEXT_PTR(free_listp));
    

    return 0;
}

static void *extend_heap(size_t words)
{ // 새 가용 블록으로 힙 확장
    
    printf("*** extend_heap **** \n");

    char *bp;
    size_t size;
    /* alignment 유지를 위해 짝수 개수의 words를 Allocate */
    size = (words % 2) ? (words + 1) * WSIZE : words * WSIZE;
    if ((long)(bp = mem_sbrk(size)) == -1)
    {
        return NULL;
    }

    PUT(HDRP(bp), PACK(size, 0));         // free block header
    PUT(FTRP(bp), PACK(size, 0));         // free block footer
    PUT(HDRP(NEXT_BLKP(bp)), PACK(0, 1)); // new epilogue header 추가

    /* 만약 prev block이 free였다면, coalesce해라.*/
    return coalesce(bp);
}

static void *coalesce(void *bp)
{
    printf("*** coalesce **** \n");
    size_t prev_alloc = GET_ALLOC(FTRP(PREV_BLKP(bp))) || PREV_BLKP(bp) == bp;
    size_t next_alloc = GET_ALLOC(HDRP(NEXT_BLKP(bp)));
    size_t size = GET_SIZE(HDRP(bp));

    if (prev_alloc && next_alloc)
    { // case 1 - 이전과 다음 블록이 모두 할당 되어있는 경우, 현재 블록의 상태는 할당에서 가용으로 변경
        return bp;
    }
    else if (prev_alloc && !next_alloc)
    {      
        printf(">>> case 2 \n");                                    // case2 - 이전 블록은 할당 상태, 다음 블록은 가용상태. 현재 블록은 다음 블록과 통합 됨.
        size += GET_SIZE(HDRP(NEXT_BLKP(bp))); // 다음 블록의 헤더만큼 사이즈 추가?
        remove_from_freelist((NEXT_BLKP(bp)));
        PUT(HDRP(bp), PACK(size, 0)); // 헤더 갱신
        PUT(FTRP(bp), PACK(size, 0)); // 푸터 갱신
    }
    else if (!prev_alloc && next_alloc)
    { // case 3 - 이전 블록은 가용상태, 다음 블록은 할당 상태. 이전 블록은 현재 블록과 통합.
        printf(">>> case 3 \n"); 
        size += GET_SIZE(HDRP(PREV_BLKP(bp)));
        remove_from_freelist((PREV_BLKP(bp)));
        PUT(FTRP(bp), PACK(size, 0));
        PUT(HDRP(PREV_BLKP(bp)), PACK(size, 0)); // 헤더를 이전 블록의 BLKP만큼 통합?
        bp = PREV_BLKP(bp);
    }
    else
    {      
        printf(">>> case 4 \n");                                                                     // case 4- 이전 블록과 다음 블록 모두 가용상태. 이전,현재,다음 3개의 블록 모두 하나의 가용 블록으로 통합.
        size += GET_SIZE(HDRP(PREV_BLKP(bp))) + GET_SIZE(FTRP(NEXT_BLKP(bp))); // 이전 블록 헤더, 다음 블록 푸터 까지로 사이즈 늘리기

        remove_from_freelist(PREV_BLKP(bp));
        remove_from_freelist(NEXT_BLKP(bp));

        PUT(HDRP(PREV_BLKP(bp)), PACK(size, 0));
        PUT(FTRP(NEXT_BLKP(bp)), PACK(size, 0));

        bp = PREV_BLKP(bp);
    }

    insert_in_freelist(bp);
    start_nextfit = bp;
    return bp;
}

void *mm_malloc(size_t size)
{
    size_t asize;      // 블록 사이즈 조정
    size_t extendsize; // heap에 맞는 fit이 없으면 확장하기 위한 사이즈
    char *bp;

    printf("*** MALLOC **** \n");

    /* 거짓된 요청 무시*/
    if (size == 0)
        return NULL;

    /* overhead, alignment 요청 포함해서 블록 사이즈 조정*/
    if (size <= DSIZE)
    {
        asize = 2 * DSIZE;
    }
    else
    {
        asize = DSIZE * ((size + (DSIZE) + (DSIZE - 1)) / DSIZE);
    }
    /* fit에 맞는 free 리스트를 찾는다.*/
    if ((bp = find_fit(asize)) != NULL)
    {        
        printf(">>> well found \n");
        place(bp, asize);
        return bp;
    }
    
    printf(">>> no fit \n");
    /* fit 맞는게 없다. 메모리를 더 가져와 block을 위치시킨다.*/
    extendsize = MAX(asize, CHUNKSIZE);
    if ((bp = extend_heap(extendsize / WSIZE)) == NULL)
    {
        return NULL;
    }
    printf(">>> well extended  \n");
    place(bp, asize);
    return bp;
}

static void *find_fit(size_t asize)
{
    printf("*** find_fit **** \n");
    void *bp;

    for (bp = free_listp; GET_ALLOC(HDRP(bp)) == 0; bp = GET_NEXT_PTR(bp))
    {
        if (!GET_ALLOC(HDRP(bp)) && (asize <= GET_SIZE(HDRP(bp))))
        {
            return bp;
        }
    }

    return NULL;
}

static void place(void *bp, size_t asize)
{ // 요청한 블록을 가용 블록의 시작 부분에 배치, 나머지 부분의 크기가 최소 블록크기와 같거나 큰 경우에만 분할하는 함수.

    printf("*** place **** \n");
    size_t csize = GET_SIZE(HDRP(bp));

    if ((csize - asize) >= (2 * DSIZE))
    {
        PUT(HDRP(bp), PACK(asize, 1));
        PUT(FTRP(bp), PACK(asize, 1));
        remove_from_freelist(bp);
        bp = NEXT_BLKP(bp);
        PUT(HDRP(bp), PACK(csize - asize, 0));
        PUT(FTRP(bp), PACK(csize - asize, 0));
        coalesce(bp);
    }
    else
    {
        PUT(HDRP(bp), PACK(csize, 1));
        PUT(FTRP(bp), PACK(csize, 1));
        remove_from_freelist(bp);
    }

    start_nextfit = bp;
}

/*
 * mm_free - Freeing a block does nothing.
 */
void mm_free(void *bp)
{
    printf("*** mm_free **** \n");
    if (bp == NULL)
        return;
    size_t size = GET_SIZE(HDRP(bp));
    PUT(HDRP(bp), PACK(size, 0)); // header, footer 들을 free 시킨다.
    PUT(FTRP(bp), PACK(size, 0));
    coalesce(bp);
}

/*
 * mm_realloc - Implemented simply in terms of mm_malloc and mm_free
 */
void *mm_realloc(void *bp, size_t size)
{
    // void *oldptr = ptr;
    // void *newptr;
    // size_t copySize;

    // newptr = mm_malloc(size);
    // if (newptr == NULL)
    //     return NULL;
    // copySize = GET_SIZE(HDRP(oldptr));
    // if (size < copySize)
    //     copySize = size;
    // memcpy(newptr, oldptr, copySize);
    // mm_free(oldptr);
    // return newptr;

    if ((int)size < 0)
        return NULL;
    else if ((int)size == 0)
    {
        mm_free(bp);
        return NULL;
    }
    else if (size > 0)
    {
        size_t oldsize = GET_SIZE(HDRP(bp));
        size_t newsize = size + 2 * WSIZE; // 2 words for header and footer
        /*if newsize is less than oldsize then we just return bp */
        if (newsize <= oldsize)
        {
            return bp;
        }
        /*if newsize is greater than oldsize */
        else
        {
            size_t next_alloc = GET_ALLOC(HDRP(NEXT_BLKP(bp)));
            size_t csize;
            /* next block is free and the size of the two blocks is greater than or equal the new size  */
            /* then we only need to combine both the blocks  */
            if (!next_alloc && ((csize = oldsize + GET_SIZE(HDRP(NEXT_BLKP(bp))))) >= newsize)
            {
                remove_from_freelist(NEXT_BLKP(bp));
                PUT(HDRP(bp), PACK(csize, 1));
                PUT(FTRP(bp), PACK(csize, 1));
                return bp;
            }
            else
            {
                void *new_ptr = mm_malloc(newsize);
                place(new_ptr, newsize);
                memcpy(new_ptr, bp, newsize);
                mm_free(bp);
                return new_ptr;
            }
        }
    }
    else
        return NULL;
}

static void insert_in_freelist(void *bp)
{
    printf("*** insert_in_freelist **** \n");
    PUT_NEXT_PTR(bp, free_listp);
    PUT_PREV_PTR(free_listp, bp);
    PUT_PREV_PTR(bp, NULL);
    free_listp = bp;
}

static void remove_from_freelist(void *bp)
{
    printf("*** remove_from_freelist **** \n");
    if (GET_PREV_PTR(bp))
    {
        printf(">>>> 1 \n");
        PUT_NEXT_PTR(GET_PREV_PTR(bp), GET_NEXT_PTR(bp));
    }
    else
    {
        printf(">>>> 2 \n");
        free_listp = GET_NEXT_PTR(bp);
    }
    
    printf(">>>> 3 \n");
    printf("%p, %p\n", GET_NEXT_PTR(bp), GET_PREV_PTR(bp));

    PUT_PREV_PTR(GET_NEXT_PTR(bp), GET_PREV_PTR(bp));
    printf("*** remove_from_freelist ***\n");
}